from flask import Flask, render_template, jsonify, request
from typing import Dict, Any, List
import sudoku_logic

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT: Dict[str, Any] = {
    'puzzle': None,
    'solution': None
}

@app.route('/')
def index() -> str:
    """Render the main sudoku game interface.
    
    Returns:
        The rendered HTML template for the sudoku game.
    """
    return render_template('index.html')

@app.route('/new')
def new_game() -> Dict[str, Any]:
    """Generate and return a new sudoku puzzle.
    
    Query Parameters:
        difficulty (str): Game difficulty level ('easy', 'medium', 'hard').
                         Defaults to 'medium' if not provided or invalid.
    
    Returns:
        JSON response with 'puzzle' key containing the 9x9 board, or
        JSON error with 'error' key if puzzle generation fails.
    """
    difficulty = request.args.get('difficulty', 'medium')
    
    # Validate difficulty level
    if difficulty not in sudoku_logic.DIFFICULTY_CLUES:
        difficulty = 'medium'
    
    clues = sudoku_logic.DIFFICULTY_CLUES[difficulty]
    try:
        puzzle, solution = sudoku_logic.generate_puzzle(
            clues=clues,
            validate_unique=True,
            max_attempts=50
        )
        CURRENT['puzzle'] = puzzle
        CURRENT['solution'] = solution
        return jsonify({'puzzle': puzzle})
    except Exception as e:
        # If puzzle generation fails, return an error
        return jsonify({'error': f'Failed to generate puzzle: {str(e)}'}), 500

@app.route('/check', methods=['POST'])
def check_solution() -> Dict[str, Any]:
    """Validate the player's submitted sudoku solution.
    
    Compares the submitted board against the stored solution and identifies
    all cells with incorrect values.
    
    Request JSON:
        board (list): A 9x9 sudoku board as a list of lists.
    
    Returns:
        JSON response with 'incorrect' key containing a list of [row, col]
        coordinates for cells with wrong values, or error if no game active.
    """
    try:
        data = request.json
        if not data or 'board' not in data:
            return jsonify({'error': 'Invalid request: missing board'}), 400
        
        board = data.get('board')
        
        # Validate board structure
        if not isinstance(board, list) or len(board) != sudoku_logic.SIZE:
            return jsonify({'error': 'Invalid board: must be 9x9'}), 400
        if not all(isinstance(row, list) and len(row) == sudoku_logic.SIZE for row in board):
            return jsonify({'error': 'Invalid board: all rows must have 9 cells'}), 400
        
        solution = CURRENT.get('solution')
        if solution is None:
            return jsonify({'error': 'No game in progress'}), 400
        
        # Find and record incorrect cells
        incorrect = []
        for i in range(sudoku_logic.SIZE):
            for j in range(sudoku_logic.SIZE):
                if board[i][j] != solution[i][j]:
                    incorrect.append([i, j])
        
        return jsonify({'incorrect': incorrect})
    except Exception as e:
        return jsonify({'error': f'Error checking solution: {str(e)}'}), 500

@app.route('/validate-cell', methods=['POST'])
def validate_cell() -> Dict[str, Any]:
    """Validate if a single cell entry is correct.
    
    Checks if the provided value matches the solution at the given position.
    
    Request JSON:
        row (int): The row index (0-8).
        col (int): The column index (0-8).
        value (int): The number to validate (1-9 or 0 for empty).
    
    Returns:
        JSON response with 'is_correct' boolean, or error if no game active.
    """
    try:
        data = request.json
        if not data or not all(k in data for k in ['row', 'col', 'value']):
            return jsonify({'error': 'Invalid request: missing row, col, or value'}), 400
        
        row = data.get('row')
        col = data.get('col')
        value = data.get('value')
        
        # Validate input ranges
        if not isinstance(row, int) or not (0 <= row < sudoku_logic.SIZE):
            return jsonify({'error': f'Invalid row: must be 0-{sudoku_logic.SIZE - 1}'}), 400
        if not isinstance(col, int) or not (0 <= col < sudoku_logic.SIZE):
            return jsonify({'error': f'Invalid column: must be 0-{sudoku_logic.SIZE - 1}'}), 400
        if not isinstance(value, int) or not (0 <= value <= 9):
            return jsonify({'error': 'Invalid value: must be 0-9'}), 400
        
        solution = CURRENT.get('solution')
        if solution is None:
            return jsonify({'error': 'No game in progress'}), 400
        
        # Check if the entered value matches the solution
        is_correct = (value == solution[row][col])
        
        return jsonify({'is_correct': is_correct})
    except Exception as e:
        return jsonify({'error': f'Error validating cell: {str(e)}'}), 500

@app.route('/hint', methods=['POST'])
def get_hint() -> Dict[str, Any]:
    """Return a hint for a cell in the current puzzle.
    
    Selects a random empty cell from the puzzle and returns its solution value.
    
    Request JSON:
        board (list): The current game board state (9x9).
    
    Returns:
        JSON response with 'row', 'col', and 'value' keys for the hint,
        or error if no empty cells or no game in progress.
    """
    try:
        data = request.json
        if not data or 'board' not in data:
            return jsonify({'error': 'Invalid request: missing board'}), 400
        
        board = data.get('board')
        
        # Validate board structure
        if not isinstance(board, list) or len(board) != sudoku_logic.SIZE:
            return jsonify({'error': 'Invalid board: must be 9x9'}), 400
        
        solution = CURRENT.get('solution')
        puzzle = CURRENT.get('puzzle')
        
        if solution is None or puzzle is None:
            return jsonify({'error': 'No game in progress'}), 400
        
        # Find empty cells in the current board that were originally empty
        empty_cells = []
        for i in range(sudoku_logic.SIZE):
            for j in range(sudoku_logic.SIZE):
                if board[i][j] == 0 and puzzle[i][j] == 0:
                    empty_cells.append((i, j))
        
        if not empty_cells:
            return jsonify({'error': 'No empty cells available for hints'}), 400
        
        # Pick a random empty cell and return the solution value
        import random
        row, col = random.choice(empty_cells)
        hint_value = solution[row][col]
        
        return jsonify({
            'row': row,
            'col': col,
            'value': hint_value
        })
    except Exception as e:
        return jsonify({'error': f'Error getting hint: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)