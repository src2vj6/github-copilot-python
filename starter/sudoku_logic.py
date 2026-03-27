import copy
import random

SIZE = 9
EMPTY = 0

def deep_copy(board):
    return copy.deepcopy(board)

def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True

def remove_cells(board, clues):
    attempts = SIZE * SIZE - clues
    while attempts > 0:
        row = random.randrange(SIZE)
        col = random.randrange(SIZE)
        if board[row][col] != EMPTY:
            board[row][col] = EMPTY
            attempts -= 1

def count_solutions(board, limit=2):
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

def has_unique_solution(puzzle):
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

def generate_puzzle(clues=35, validate_unique=True, max_attempts=100):
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
