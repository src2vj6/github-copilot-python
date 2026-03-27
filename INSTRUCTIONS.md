# Copilot Instructions

This document provides clear guidance for GitHub Copilot when working with this repository.

## Code Style & Standards

### Python Guidelines
- Follow **PEP 8** style guide strictly
- Use type hints for all function parameters and return types
- Prefer descriptive variable and function names (≥3 characters)
- Keep functions focused and under 50 lines when possible
- Add docstrings to all functions and classes using Google-style format

### Code Quality
- Write defensive code with input validation
- Handle edge cases explicitly
- Use meaningful error messages in exceptions
- Avoid magic numbers; use named constants instead
- Keep cyclomatic complexity low (max 10 per function)

## Testing Approach

- Write unit tests using pytest framework
- Aim for minimum 80% code coverage
- Test both happy paths and edge cases
- Use descriptive test names that explain what is being tested
- Mock external dependencies; avoid integration test dependencies

## Project Structure

```
github-copilot-python/
├── starter/              # Main application code
│   ├── app.py           # Flask application
│   ├── sudoku_logic.py  # Core Sudoku logic
│   ├── static/          # CSS and JavaScript
│   ├── templates/       # HTML templates
│   └── tests/           # Test suite
├── requirements.txt     # Python dependencies
└── INSTRUCTIONS.md      # This file
```

## Specific Contexts

### Sudoku Application
- The application validates Sudoku board state
- Focus on logical correctness over performance
- Ensure all board operations are idempotent
- Maintain board immutability where practical
- Validate uniqueness constraints across rows, columns, and 3x3 boxes

### Testing Files
- `test_app.py` - Flask endpoint tests
- `test_sudoku_logic.py` - Core logic tests
- `test_uniqueness.py` - Constraint validation tests

## Documentation Requirements

- Add inline comments for complex logic (>3 lines)
- Document assumptions and preconditions
- Update docstrings when modifying functions
- Include example usage in class/function docstrings where helpful

## Version Control

- Write clear, descriptive commit messages
- Reference issue numbers when applicable
- Keep commits atomic and focused on single features/fixes

## Performance Considerations

- Prioritize code clarity over micro-optimizations
- Profile before optimizing
- Use appropriate data structures (sets for uniqueness checks, etc.)

## Security

- Validate all user input
- Avoid hardcoding sensitive values
- Use environment variables for configuration
- Escape output in templates to prevent XSS

## When to Ask for Clarification

- Ambiguous requirements
- Trade-offs between clarity and performance
- Architectural decisions affecting multiple components
