# Testing Framework for Sudoku App

This directory contains a comprehensive testing framework for the Sudoku application.

## Overview

The test suite includes:
- **Unit tests** for sudoku logic (`test_sudoku_logic.py`) - 17 tests
- **Uniqueness validation tests** (`test_uniqueness.py`) - 9 tests
- **Integration tests** for Flask endpoints (`test_app.py`)
- **Configuration files** for pytest

## Solution Uniqueness Tests

The uniqueness validation tests ensure that all generated puzzles have exactly one unique solution.

### Running Uniqueness Tests

**Standalone (no dependencies):**
```bash
cd starter/tests
python test_uniqueness.py
```

### Puzzle Generation with Unique Solutions

The `sudoku_logic.py` module provides functions to ensure puzzles have unique solutions:

- **`count_solutions(board, limit=2)`** - Counts the number of solutions for a given puzzle
- **`has_unique_solution(puzzle)`** - Checks if a puzzle has exactly one solution
- **`generate_puzzle(clues=45, validate_unique=True, max_attempts=100)`** - Generates puzzles with guaranteed unique solutions

### Tested Difficulty Levels

- **Easy** (55 clues): ~0.00s generation time ✓ Unique solution
- **Medium** (45 clues): ~0.00s generation time ✓ Unique solution
- **Hard** (35 clues): ~0.02s generation time ✓ Unique solution

## General Testing

### Test Coverage

- **sudoku_logic.py**: Comprehensive coverage
- **Uniqueness validation**: Full coverage
- **app.py**: Integration testing

## Running Tests

### Run all tests with coverage report:
```bash
pytest
```

### Run specific test file:
```bash
pytest test_sudoku_logic.py
pytest test_app.py
```

### Run specific test class:
```bash
pytest test_sudoku_logic.py::TestBoardCreation
pytest test_app.py::TestNewGameRoute
```

### Run specific test:
```bash
pytest test_sudoku_logic.py::TestBoardCreation::test_create_empty_board
```

### Run with verbose output:
```bash
pytest -v
```

### Run with detailed coverage report:
```bash
pytest --cov=. --cov-report=html
# View report in htmlcov/index.html
```

### Run only unit tests:
```bash
pytest -m unit
```

### Run only integration tests:
```bash
pytest -m integration
```

## Test Structure

### `test_sudoku_logic.py`
Tests for the sudoku puzzle logic:
- **TestBoardCreation**: Tests board initialization and constants
- **TestBoardValidation**: Tests sudoku validation rules (rows, columns, 3x3 boxes)
- **TestPuzzleGeneration**: Tests puzzle and solution generation
- **TestDeepCopy**: Tests board copying functionality

### `test_app.py`
Tests for the Flask web application:
- **TestIndexRoute**: Tests the main page endpoint
- **TestNewGameRoute**: Tests game creation with various parameters
- **TestCheckSolutionRoute**: Tests solution validation
- **TestIntegrationFlow**: End-to-end game flow tests

## Test Files

- `conftest.py` - Shared fixtures for test isolation
- `test_sudoku_logic.py` - Unit tests for sudoku logic (16 tests)
- `test_app.py` - Integration tests for Flask app (15 tests)

## Dependencies

Tests require the following packages (in `requirements.txt`):
- `pytest>=7.0` - Testing framework
- `pytest-cov>=4.0` - Code coverage plugin

These are automatically installed when running:
```bash
pip install -r requirements.txt
```

## Key Features

✅ **Test Isolation**: Each test starts with a clean state  
✅ **Comprehensive Coverage**: Tests cover happy paths and edge cases  
✅ **Clear Organization**: Tests grouped into logical classes  
✅ **Descriptive Names**: Test names clearly describe what is being tested  
✅ **Fixtures**: Reusable test components via pytest fixtures  
✅ **Coverage Reporting**: HTML and terminal coverage reports  
✅ **CI/CD Ready**: Can be integrated into continuous integration pipelines  

## Common Test Commands

```bash
# Run all tests
pytest

# Run with coverage and view in browser
pytest --cov=. --cov-report=html && start htmlcov/index.html

# Run tests matching a pattern
pytest -k "test_new_game"

# Run tests with more verbose output
pytest -vv

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf
```

## Extending the Tests

To add more tests:

1. Create a new test function in the appropriate test file
2. Use descriptive names starting with `test_`
3. Use docstrings to explain what is being tested
4. Organize tests into classes by functionality
5. Use fixtures for common setup/teardown operations

Example:
```python
def test_my_feature(client):
    """Test description."""
    response = client.get('/endpoint')
    assert response.status_code == 200
```

## Troubleshooting

**Tests fail with import errors:**
- Ensure you're in the `starter/` directory
- Run `pip install -r requirements.txt`

**Flask test client issues:**
- Check that conftest.py is in the same directory
- Verify app.py is importable

**Coverage report issues:**
- Clear pytest cache: `pytest --cache-clear`
- Reinstall pytest-cov: `pip install --upgrade pytest-cov`
