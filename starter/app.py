from flask import Flask, render_template, jsonify, request
import sudoku_logic

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new_game():
    difficulty = request.args.get('difficulty', 'medium')
    
    # Map difficulty levels to number of clues
    # Adjusted to ensure puzzles can be generated with unique solutions in reasonable time
    difficulty_map = {
        'easy': 55,       # More clues = easier
        'medium': 45,     # Medium number of clues
        'hard': 35        # Fewer clues = harder, but still reasonable
    }
    
    clues = difficulty_map.get(difficulty, 45)
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
def check_solution():
    data = request.json
    board = data.get('board')
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    incorrect = []
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])
    return jsonify({'incorrect': incorrect})

@app.route('/hint', methods=['POST'])
def get_hint():
    data = request.json
    board = data.get('board')
    solution = CURRENT.get('solution')
    puzzle = CURRENT.get('puzzle')
    
    if solution is None or puzzle is None:
        return jsonify({'error': 'No game in progress'}), 400
    
    # Find empty cells in the current board
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

if __name__ == '__main__':
    app.run(debug=True)