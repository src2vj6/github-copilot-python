import pytest
import sys
from pathlib import Path

# Add parent directory to path to import sudoku_logic
sys.path.insert(0, str(Path(__file__).parent.parent))
import sudoku_logic


class TestBoardCreation:
    """Test board creation and initialization."""
    
    def test_create_empty_board(self):
        """Test that empty board is created with correct dimensions."""
        board = sudoku_logic.create_empty_board()
        assert len(board) == 9
        assert all(len(row) == 9 for row in board)
        assert all(cell == 0 for row in board for cell in row)
    
    def test_empty_board_size_constant(self):
        """Test that SIZE constant is correct."""
        assert sudoku_logic.SIZE == 9
        assert sudoku_logic.EMPTY == 0


class TestBoardValidation:
    """Test sudoku validation logic."""
    
    def test_is_safe_empty_cell(self):
        """Test that numbers can be placed in empty cells."""
        board = sudoku_logic.create_empty_board()
        # Should be able to place any number 1-9 in empty board
        assert sudoku_logic.is_safe(board, 0, 0, 5)
        assert sudoku_logic.is_safe(board, 4, 4, 9)
    
    def test_is_safe_row_conflict(self):
        """Test that is_safe detects row conflicts."""
        board = sudoku_logic.create_empty_board()
        board[0][0] = 5
        # Can't place 5 in same row
        assert not sudoku_logic.is_safe(board, 0, 5, 5)
        # But can place other numbers
        assert sudoku_logic.is_safe(board, 0, 5, 3)
    
    def test_is_safe_column_conflict(self):
        """Test that is_safe detects column conflicts."""
        board = sudoku_logic.create_empty_board()
        board[0][0] = 5
        # Can't place 5 in same column
        assert not sudoku_logic.is_safe(board, 5, 0, 5)
        # But can place other numbers
        assert sudoku_logic.is_safe(board, 5, 0, 3)
    
    def test_is_safe_box_conflict(self):
        """Test that is_safe detects 3x3 box conflicts."""
        board = sudoku_logic.create_empty_board()
        board[0][0] = 5
        # Can't place 5 in same 3x3 box (top-left)
        assert not sudoku_logic.is_safe(board, 1, 1, 5)
        assert not sudoku_logic.is_safe(board, 2, 2, 5)
        # Can place 5 in different box
        assert sudoku_logic.is_safe(board, 3, 3, 5)
    
    def test_is_safe_all_constraints(self):
        """Test that is_safe checks row, column, and box simultaneously."""
        board = sudoku_logic.create_empty_board()
        # Set up a pattern
        board[0][0] = 1
        board[0][1] = 2
        board[1][0] = 3
        
        # Row conflict
        assert not sudoku_logic.is_safe(board, 0, 5, 1)
        assert not sudoku_logic.is_safe(board, 0, 5, 2)
        # Column conflict
        assert not sudoku_logic.is_safe(board, 5, 0, 1)
        assert not sudoku_logic.is_safe(board, 5, 0, 3)
        # Box conflict
        assert not sudoku_logic.is_safe(board, 1, 1, 1)
        # Valid placement
        assert sudoku_logic.is_safe(board, 2, 2, 5)


class TestPuzzleGeneration:
    """Test puzzle and solution generation."""
    
    def test_generate_puzzle_default(self):
        """Test that puzzle is generated with default clues."""
        puzzle, solution = sudoku_logic.generate_puzzle()
        
        # Both should be 9x9 boards
        assert len(puzzle) == 9
        assert len(solution) == 9
        assert all(len(row) == 9 for row in puzzle)
        assert all(len(row) == 9 for row in solution)
    
    def test_generate_puzzle_with_clues(self):
        """Test that puzzle is generated with specified number of clues."""
        clues = 40
        puzzle, solution = sudoku_logic.generate_puzzle(clues)
        
        # Count non-empty cells in puzzle
        num_clues = sum(1 for row in puzzle for cell in row if cell != 0)
        assert num_clues == clues
    
    def test_generate_puzzle_different_clues(self):
        """Test puzzle generation with different clue counts."""
        for clues in [20, 35, 50]:
            puzzle, solution = sudoku_logic.generate_puzzle(clues)
            num_clues = sum(1 for row in puzzle for cell in row if cell != 0)
            assert num_clues == clues
    
    def test_solution_is_complete(self):
        """Test that solution has no empty cells."""
        _, solution = sudoku_logic.generate_puzzle()
        
        # Solution should have all cells filled
        empty_count = sum(1 for row in solution for cell in row if cell == 0)
        assert empty_count == 0
    
    def test_solution_values_valid(self):
        """Test that solution contains only valid sudoku values."""
        _, solution = sudoku_logic.generate_puzzle()
        
        # All values should be 1-9
        for row in solution:
            for cell in row:
                assert 1 <= cell <= 9
    
    def test_puzzle_subset_of_solution(self):
        """Test that puzzle clues match solution values."""
        puzzle, solution = sudoku_logic.generate_puzzle()
        
        # Where puzzle has clues, they should match solution
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] != 0:
                    assert puzzle[i][j] == solution[i][j]
    
    def test_puzzle_fewer_clues_than_solution(self):
        """Test that puzzle has fewer filled cells than solution."""
        puzzle, solution = sudoku_logic.generate_puzzle()
        
        puzzle_clues = sum(1 for row in puzzle for cell in row if cell != 0)
        solution_clues = sum(1 for row in solution for cell in row if cell != 0)
        
        assert puzzle_clues < solution_clues
    
    def test_generate_puzzle_deterministic_clue_count(self):
        """Test that clue count is exactly as specified."""
        puzzle, _ = sudoku_logic.generate_puzzle(clues=45)
        clue_count = sum(1 for row in puzzle for cell in row if cell != 0)
        assert clue_count == 45


class TestDeepCopy:
    """Test deep copy functionality."""
    
    def test_deep_copy_creates_independent_copy(self):
        """Test that deep_copy creates an independent copy."""
        original = sudoku_logic.create_empty_board()
        original[0][0] = 5
        
        copied = sudoku_logic.deep_copy(original)
        copied[0][0] = 9
        
        # Original should not be affected
        assert original[0][0] == 5
        assert copied[0][0] == 9
    
    def test_deep_copy_preserves_values(self):
        """Test that deep_copy preserves all values."""
        original = sudoku_logic.create_empty_board()
        for i in range(9):
            original[i][i] = i + 1
        
        copied = sudoku_logic.deep_copy(original)
        assert original == copied
