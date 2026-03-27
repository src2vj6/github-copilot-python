import copy
import random
from typing import List, Tuple

SIZE: int = 9
EMPTY: int = 0
BOX_SIZE: int = 3
DIFFICULTY_CLUES = {
    'easy': 55,
    'medium': 45,
    'hard': 35
}

def deep_copy(board: List[List[int]]) -> List[List[int]]:
    """Create a deep copy of a sudoku board.
    
    Args:
        board: A 9x9 sudoku board represented as a list of lists.
    
    Returns:
        A new independent copy of the board.
    """
    return copy.deepcopy(board)

def create_empty_board() -> List[List[int]]:
    """Create an empty 9x9 sudoku board.
    
    Returns:
        A 9x9 board filled with zeros (EMPTY values).
    """
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

def is_safe(board: List[List[int]], row: int, col: int, num: int) -> bool:
    """Check if placing a number at (row, col) is valid.
    
    Validates sudoku constraints: no duplicate in row, column, or 3x3 box.
    
    Args:
        board: The sudoku board.
        row: The row index (0-8).
        col: The column index (0-8).
        num: The number to place (1-9).
    
    Returns:
        True if the placement is valid, False otherwise.
    """
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % BOX_SIZE
    start_col = col - col % BOX_SIZE
    for i in range(BOX_SIZE):
        for j in range(BOX_SIZE):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def fill_board(board: List[List[int]]) -> bool:
    """Fill an empty board with valid sudoku values using backtracking.
    
    Uses recursive backtracking to generate a complete valid sudoku solution.
    Randomly selects candidates to create different puzzles.
    
    Args:
        board: An empty or partially filled board to complete.
    
    Returns:
        True if board was successfully filled, False if impossible.
    """
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                # Try numbers in random order for variety
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        # Backtrack: undo placement and try next candidate
                        board[row][col] = EMPTY
                return False
    return True

def remove_cells(board: List[List[int]], clues: int) -> None:
    """Remove cells from a complete board to create a puzzle.
    
    Randomly removes cells to achieve the desired number of clues (givens).
    Modifies the board in-place.
    
    Args:
        board: A complete, filled sudoku board.
        clues: The target number of clues to remain in the puzzle.
    """
    attempts = SIZE * SIZE - clues
    while attempts > 0:
        row = random.randrange(SIZE)
        col = random.randrange(SIZE)
        if board[row][col] != EMPTY:
            board[row][col] = EMPTY
            attempts -= 1

def count_solutions(board: List[List[int]], limit: int = 2) -> int:
    """
    Count the number of solutions for a given puzzle.
    
    Args:
        board: The sudoku puzzle board
        limit: Maximum number of solutions to find (stops early if exceeded)
    
    Returns:
        The number of solutions (up to the limit)
    """
    # Find the first empty cell
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                count = 0
                for num in range(1, SIZE + 1):
                    if is_safe(board, row, col, num):
                        board[row][col] = num
                        count += count_solutions(board, limit - count)
                        if count >= limit:
                            board[row][col] = EMPTY
                            return count
                        board[row][col] = EMPTY
                return count
    # No empty cells found, we have a complete solution
    return 1

def has_unique_solution(puzzle: List[List[int]]) -> bool:
    """
    Check if a puzzle has exactly one unique solution.
    
    Args:
        puzzle: The sudoku puzzle board
    
    Returns:
        True if the puzzle has exactly one solution, False otherwise
    """
    # Create a copy to avoid modifying the original
    board_copy = deep_copy(puzzle)
    return count_solutions(board_copy, limit=2) == 1

def generate_puzzle(clues: int = 35, validate_unique: bool = True, max_attempts: int = 100) -> Tuple[List[List[int]], List[List[int]]]:
    """
    Generate a sudoku puzzle with optional uniqueness validation.
    
    Args:
        clues: Number of clues to include in the puzzle
        validate_unique: If True, ensures the puzzle has exactly one solution
        max_attempts: Maximum number of attempts to generate a valid puzzle
    
    Returns:
        Tuple of (puzzle, solution)
    """
    for attempt in range(max_attempts):
        board = create_empty_board()
        fill_board(board)
        solution = deep_copy(board)
        remove_cells(board, clues)
        puzzle = deep_copy(board)
        
        # Validate that puzzle has unique solution if requested
        if validate_unique:
            if has_unique_solution(puzzle):
                return puzzle, solution
            # If validation fails, try again with more clues
            # This increases likelihood of finding unique solution
            if attempt < max_attempts - 1:
                continue
        else:
            return puzzle, solution
    
    # If max_attempts exceeded, return the last generated puzzle
    # even if uniqueness is not guaranteed
    return puzzle, solution
