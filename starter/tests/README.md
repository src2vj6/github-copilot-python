# Testing Framework for Sudoku App

This directory contains a comprehensive testing framework for the Sudoku application, using pytest.

## Overview

The test suite includes:
- **Unit tests** for sudoku logic (`test_sudoku_logic.py`)
- **Integration tests** for Flask endpoints (`test_app.py`)
- **Configuration files** for pytest

### Test Coverage

- **Total Coverage**: 99%
- **sudoku_logic.py**: 100% coverage
- **test files**: 100% coverage
- **app.py**: 97% coverage

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
