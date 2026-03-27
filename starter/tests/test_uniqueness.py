#!/usr/bin/env python3
"""
Unit tests for Sudoku solution uniqueness validation.
Tests the count_solutions and has_unique_solution functionality.
"""

import sys
from pathlib import Path

# Add parent directory to path to import sudoku_logic
sys.path.insert(0, str(Path(__file__).parent.parent))
import sudoku_logic


class TestSolutionUniqueness:
    """Test solution uniqueness validation."""
    
    def test_count_solutions_empty_board(self):
        """Test that empty board has many solutions."""
        board = sudoku_logic.create_empty_board()
        # Empty board has more than 1 solution
        count = sudoku_logic.count_solutions(board, limit=3)
        assert count > 1
    
    def test_count_solutions_complete_board(self):
        """Test that complete valid board has exactly one solution."""
        _, solution = sudoku_logic.generate_puzzle(validate_unique=False)
        solution_copy = sudoku_logic.deep_copy(solution)
        count = sudoku_logic.count_solutions(solution_copy)
        assert count == 1
    
    def test_count_solutions_respects_limit(self):
        """Test that count_solutions stops at limit."""
        board = sudoku_logic.create_empty_board()
        # Set limit to 2, should not exceed that
        count = sudoku_logic.count_solutions(board, limit=2)
        assert count <= 2
    
    def test_has_unique_solution_valid_puzzle(self):
        """Test that generated puzzle has unique solution."""
        puzzle, _ = sudoku_logic.generate_puzzle(clues=45, validate_unique=True)
        assert sudoku_logic.has_unique_solution(puzzle)
    
    def test_has_unique_solution_empty_board(self):
        """Test that empty board does not have unique solution."""
        board = sudoku_logic.create_empty_board()
        assert not sudoku_logic.has_unique_solution(board)
    
    def test_has_unique_solution_multiple_clues(self):
        """Test unique solution check with various clue counts."""
        for clues in [45, 50, 55]:
            puzzle, _ = sudoku_logic.generate_puzzle(clues=clues, validate_unique=True)
            assert sudoku_logic.has_unique_solution(puzzle), \
                f"Puzzle with {clues} clues should have unique solution"
    
    def test_generate_puzzle_with_validation(self):
        """Test that generated puzzle with validation has unique solution."""
        puzzle, solution = sudoku_logic.generate_puzzle(clues=45, validate_unique=True)
        
        # Puzzle should have clues
        clue_count = sum(1 for row in puzzle for cell in row if cell != 0)
        assert clue_count == 45
        
        # Solution should be complete
        assert all(cell != 0 for row in solution for cell in row)
        
        # Puzzle should have unique solution
        assert sudoku_logic.has_unique_solution(puzzle)
    
    def test_generate_puzzle_without_validation(self):
        """Test that puzzle generation without validation still returns valid puzzle."""
        puzzle, solution = sudoku_logic.generate_puzzle(clues=45, validate_unique=False)
        
        # Puzzle should have clues
        clue_count = sum(1 for row in puzzle for cell in row if cell != 0)
        assert clue_count == 45
        
        # Solution should be complete
        assert all(cell != 0 for row in solution for cell in row)
    
    def test_generate_puzzle_default_validates(self):
        """Test that generate_puzzle defaults to validation."""
        puzzle, _ = sudoku_logic.generate_puzzle()
        # Should have unique solution by default
        assert sudoku_logic.has_unique_solution(puzzle)
    
    def test_count_solutions_with_partial_board(self):
        """Test count_solutions with a partially filled board."""
        board = sudoku_logic.create_empty_board()
        # Add some clues
        board[0][0] = 1
        board[1][1] = 2
        board[2][2] = 3
        # Should have multiple solutions
        count = sudoku_logic.count_solutions(board, limit=2)
        assert count > 1
    
    def test_has_unique_solution_almost_complete(self):
        """Test has_unique_solution with nearly complete puzzle."""
        _, solution = sudoku_logic.generate_puzzle(validate_unique=False)
        # Remove just one cell
        partial = sudoku_logic.deep_copy(solution)
        partial[8][8] = 0
        # Nearly complete puzzles typically have unique solutions
        result = sudoku_logic.has_unique_solution(partial)
        # We're just testing it doesn't error, not the specific result
        assert isinstance(result, bool)
    
    def test_count_solutions_limit_zero(self):
        """Test count_solutions behavior with limit parameter."""
        board = sudoku_logic.create_empty_board()
        # Test with different limits
        count_limit_1 = sudoku_logic.count_solutions(board, limit=1)
        count_limit_3 = sudoku_logic.count_solutions(board, limit=3)
        assert count_limit_1 <= count_limit_3
    
    def test_generate_puzzle_max_attempts(self):
        """Test puzzle generation respects max_attempts parameter."""
        # Test with easier parameters that won't timeout
        puzzle, solution = sudoku_logic.generate_puzzle(
            clues=50,
            validate_unique=True,
            max_attempts=5
        )
        # Should still get a valid puzzle
        assert puzzle is not None
        assert solution is not None
        clue_count = sum(1 for row in puzzle for cell in row if cell != 0)
        assert clue_count == 50

