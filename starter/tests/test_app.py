import pytest
import json
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))
from app import app, CURRENT
import sudoku_logic


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def app_context():
    """Create an app context for testing."""
    with app.app_context():
        yield


class TestIndexRoute:
    """Test the index route."""
    
    def test_index_returns_200(self, client):
        """Test that index route returns 200 status code."""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_index_returns_html(self, client):
        """Test that index route returns HTML content."""
        response = client.get('/')
        assert b'<!DOCTYPE html>' in response.data or b'<html>' in response.data


class TestNewGameRoute:
    """Test the new game route."""
    
    def test_new_game_default(self, client):
        """Test creating a new game with default settings."""
        response = client.get('/new')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'puzzle' in data
        assert len(data['puzzle']) == 9
        assert all(len(row) == 9 for row in data['puzzle'])
    
    def test_new_game_with_difficulty_parameter(self, client):
        """Test creating a new game with different difficulty levels."""
        difficulty_clue_map = {'easy': 55, 'medium': 45, 'hard': 35}
        for difficulty, expected_clues in difficulty_clue_map.items():
            response = client.get(f'/new?difficulty={difficulty}')
            assert response.status_code == 200
            
            data = json.loads(response.data)
            puzzle = data['puzzle']
            clue_count = sum(1 for row in puzzle for cell in row if cell != 0)
            assert clue_count == expected_clues
    
    def test_new_game_stores_puzzle_and_solution(self, client, app_context):
        """Test that new game stores puzzle and solution in CURRENT."""
        response = client.get('/new?difficulty=medium')
        assert response.status_code == 200
        
        assert CURRENT['puzzle'] is not None
        assert CURRENT['solution'] is not None
        assert len(CURRENT['puzzle']) == 9
        assert len(CURRENT['solution']) == 9
    
    def test_new_game_puzzle_matches_stored(self, client, app_context):
        """Test that returned puzzle matches stored puzzle."""
        response = client.get('/new?difficulty=medium')
        data = json.loads(response.data)
        
        assert data['puzzle'] == CURRENT['puzzle']
    
    def test_new_game_default_difficulty(self, client):
        """Test that new game defaults to medium difficulty."""
        response = client.get('/new')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        puzzle = data['puzzle']
        clue_count = sum(1 for row in puzzle for cell in row if cell != 0)
        assert clue_count == 45  # Medium difficulty


class TestCheckSolutionRoute:
    """Test the check solution route."""
    
    def test_check_solution_no_game_in_progress(self, client, app_context):
        """Test check solution when no game is in progress."""
        CURRENT['puzzle'] = None
        CURRENT['solution'] = None
        
        response = client.post('/check', 
                               json={'board': sudoku_logic.create_empty_board()},
                               content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_check_solution_correct_answer(self, client, app_context):
        """Test check solution with correct answer."""
        # Create a new game
        client.get('/new?clues=35')
        
        # The board submitted should be the solution
        response = client.post('/check',
                               json={'board': CURRENT['solution']},
                               content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'incorrect' in data
        assert len(data['incorrect']) == 0
    
    def test_check_solution_with_errors(self, client, app_context):
        """Test check solution with incorrect cells."""
        # Create a new game
        client.get('/new?clues=35')
        
        # Create a board with deliberate errors
        board = sudoku_logic.deep_copy(CURRENT['solution'])
        board[0][0] = 1 if board[0][0] != 1 else 2
        board[1][1] = 2 if board[1][1] != 2 else 3
        
        response = client.post('/check',
                               json={'board': board},
                               content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'incorrect' in data
        assert len(data['incorrect']) >= 2
    
    def test_check_solution_identifies_correct_cells(self, client, app_context):
        """Test that check solution correctly identifies error positions."""
        # Create a new game
        client.get('/new?clues=35')
        
        # Create a board with one specific error
        board = sudoku_logic.deep_copy(CURRENT['solution'])
        original_value = board[3][4]
        board[3][4] = 1 if original_value != 1 else 2
        
        response = client.post('/check',
                               json={'board': board},
                               content_type='application/json')
        
        data = json.loads(response.data)
        incorrect = data['incorrect']
        
        # Should contain [3, 4]
        assert [3, 4] in incorrect
    
    def test_check_solution_empty_board(self, client, app_context):
        """Test check solution with empty board against a solution."""
        # Create a new game
        client.get('/new?clues=35')
        
        # Submit empty board
        empty_board = sudoku_logic.create_empty_board()
        response = client.post('/check',
                               json={'board': empty_board},
                               content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        # All cells should be marked as incorrect
        incorrect_count = len(data['incorrect'])
        assert incorrect_count == 81  # 9x9 board, all empty


class TestIntegrationFlow:
    """Test complete game flow."""
    
    def test_complete_game_flow(self, client, app_context):
        """Test starting a game and submitting a solution."""
        # Start new game
        response = client.get('/new?clues=40')
        assert response.status_code == 200
        puzzle_data = json.loads(response.data)
        puzzle = puzzle_data['puzzle']
        
        # Verify puzzle is returned
        assert puzzle is not None
        assert len(puzzle) == 9
        
        # Submit the solution
        response = client.post('/check',
                               json={'board': CURRENT['solution']},
                               content_type='application/json')
        
        assert response.status_code == 200
        result = json.loads(response.data)
        assert len(result['incorrect']) == 0
    
    def test_multiple_games_sequence(self, client, app_context):
        """Test playing multiple games in sequence."""
        for _ in range(3):
            # Start new game
            response = client.get('/new?clues=35')
            assert response.status_code == 200
            
            # Verify it can be checked
            response = client.post('/check',
                                   json={'board': CURRENT['solution']},
                                   content_type='application/json')
            assert response.status_code == 200
