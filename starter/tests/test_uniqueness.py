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


def run_all_tests():
    """Run all uniqueness tests and display results."""
    print("=" * 70)
    print("SUDOKU SOLUTION UNIQUENESS TESTS")
    print("=" * 70)
    
    test_suite = TestSolutionUniqueness()
    tests = [
        ("Count solutions - empty board", test_suite.test_count_solutions_empty_board),
        ("Count solutions - complete board", test_suite.test_count_solutions_complete_board),
        ("Count solutions - respects limit", test_suite.test_count_solutions_respects_limit),
        ("Has unique solution - valid puzzle", test_suite.test_has_unique_solution_valid_puzzle),
        ("Has unique solution - empty board", test_suite.test_has_unique_solution_empty_board),
        ("Has unique solution - multiple clues", test_suite.test_has_unique_solution_multiple_clues),
        ("Generate puzzle - with validation", test_suite.test_generate_puzzle_with_validation),
        ("Generate puzzle - without validation", test_suite.test_generate_puzzle_without_validation),
        ("Generate puzzle - default validates", test_suite.test_generate_puzzle_default_validates),
    ]
    
    passed = 0
    failed = 0
    
    print("\n[Running Tests]")
    for test_name, test_func in tests:
        try:
            test_func()
            print(f"  ✓ {test_name}")
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {test_name}: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ {test_name}: ERROR - {e}")
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"Test Results: {passed} PASSED, {failed} FAILED")
    print("=" * 70)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit(run_all_tests())

