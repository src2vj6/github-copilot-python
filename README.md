# Refactor a Sudoku Game written in Python Flask

Use this simple Sudoku game as a starting point to practice your skills with GitHub Copilot. The goal is to refactor the code to use modern technologies, while also adding new features and improving the overall user experience.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Dependencies

```
- Modern web browser (Chrome, Firefox, Edge, etc.)
- Python 3
```

### Installation

1. Fork this repository to your GitHub account. (You can use the "Fork" button on the top right corner of the repository page.)

2. Clone your forked repository to your local machine.

3. Open a terminal window and navigate to the "github-copilot-python/starter" directory.

4. Create a Python virtual environment and activate it (optional but highly recommended).

```bash
python3 -m venv .venv
source .venv/bin/activate
```

5. Install required Python packages.

```bash
pip install -r requirements.txt
```

6. Run the Flask app.

```bash
python app.py
```

7. Open http://127.0.0.1:5000 in your browser.

## Project Instructions

Use GitHub Copilot to refactor the code for this game to add more advanced features. The goal is to create a more modern and maintainable codebase and add additional functionality to the final product. You can use any combination of code completion and chat features, like Ask, Edit, or Agent modes.

- Errors should be handled gracefully with appropriate messages to the user.
- ✓ **Implement a Sudoku board generator that creates a valid Sudoku puzzle with a unique solution.**
- ✓ **Add a timer to track how long it takes to solve the puzzle.**
- Implement a solution checker that verifies if the user's solution is correct using event delegation.
- ✓ **Add a difficulty selector to allow users to choose between easy, medium, and hard puzzles.**
- ✓ **Add a hint feature that provides clues for the user that are noted with unique colors.**
- Add a check puzzle button that checks the current state of the board against the solution.
- User should get immediate feedback on their input, such as highlighting invalid entries.
- Top 10 scores should be saved in local storage and displayed on the page with the user's name, time taken, hints used, and difficulty level.
- The game should be responsive and work well on both desktop and mobile devices.
- UI colors should be visually appealing and accessible.
- Completed and correct puzzles should display a congratulatory message with the time taken and hints used and ask for the user's name for Top 10 times.

## Features Completed

### Unique Solution Validation ✓

The puzzle generator now includes comprehensive validation to ensure each puzzle has exactly one unique solution. This is critical for a proper Sudoku game experience.

#### New Functions in `sudoku_logic.py`:

- **`count_solutions(board, limit=2)`**: Counts the number of solutions for a given puzzle, with a configurable limit to optimize performance.
- **`has_unique_solution(puzzle)`**: Checks if a puzzle has exactly one unique solution by analyzing the puzzle board.
- **Enhanced `generate_puzzle(clues=35, validate_unique=True, max_attempts=100)`**: Now includes optional uniqueness validation to ensure generated puzzles have exactly one solution.

#### Usage Example:

```python
# Generate a puzzle with guaranteed unique solution
puzzle, solution = sudoku_logic.generate_puzzle(
    clues=45,              # Number of clues (higher = easier)
    validate_unique=True,  # Ensure unique solution (default)
    max_attempts=100       # Max attempts before giving up
)

# Check if a puzzle has a unique solution
is_unique = sudoku_logic.has_unique_solution(puzzle)

# Count all solutions for a puzzle (up to a limit)
num_solutions = sudoku_logic.count_solutions(puzzle, limit=2)
```

For detailed testing instructions and documentation, see [tests/README.md](starter/tests/README.md).

All generated puzzles are guaranteed to have exactly one solution, providing a fair and enjoyable gaming experience.

### Timer Feature ✓

The game now includes a real-time timer that tracks how long it takes to solve each puzzle.

#### Features:

- **Timer Display**: Shows elapsed time in MM:SS format at the top of the game interface
- **Auto-start**: Timer automatically starts when a new game is created
- **Auto-stop**: Timer stops when the puzzle is solved correctly
- **Performance Tracking**: Elapsed time is displayed in the congratulations message when the puzzle is completed

#### How It Works:

The timer is implemented using JavaScript on the client-side:
- Starts on page load and when a new game is initiated
- Updates every second, displaying the time in MM:SS format
- Automatically pauses when the puzzle is successfully solved
- Provides immediate visual feedback of the player's progress

This encourages players to improve their solving times while maintaining the challenge of the puzzle.

### Hint Feature ✓

The game now includes an interactive hint system that helps users solve puzzles by revealing correct values for empty cells.

#### Features:

- **Get Hint Button**: Players can click "Get Hint" to receive help with solving the puzzle
- **Random Cell Selection**: Each hint reveals a random empty cell from the current puzzle state
- **Unique Visual Styling**: Hinted cells are highlighted with a distinctive yellow background (#fff9c4) and dark yellow text (#f57f17) for easy identification
- **Hint Counter**: Displays the total number of hints used during the current game
- **Performance Tracking**: The number of hints used is included in the congratulations message when the puzzle is completed

#### How It Works:

The hint system is implemented with both backend and frontend components:
- **Backend** (`/hint` endpoint in `app.py`): Finds empty cells that haven't been filled and returns a random cell with its solution value
- **Frontend** (JavaScript in `main.js`): Calls the hint endpoint, fills in the revealed value, applies the hinted styling, and updates the hint counter

#### Usage:

Players can click the "Get Hint" button at any time during gameplay. Each hint reveals one empty cell from the solution, making it easier to progress while still maintaining the challenge of solving most of the puzzle themselves.

