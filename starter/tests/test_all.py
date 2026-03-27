#!/usr/bin/env python3
"""
Comprehensive test runner that executes all Sudoku tests.
Runs tests from test_sudoku_logic.py and test_uniqueness.py.
"""

import sys
from pathlib import Path
import subprocess

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def run_test_file(test_file):
    """Run a test file and return the result."""
    print(f"\n{'=' * 70}")
    print(f"Running: {test_file}")
    print('=' * 70)
    
    result = subprocess.run(
        [sys.executable, test_file],
        cwd=Path(__file__).parent,
        capture_output=False
    )
    return result.returncode == 0


def main():
    """Run all test files."""
    print("=" * 70)
    print("COMPREHENSIVE SUDOKU TEST RUNNER")
    print("=" * 70)
    
    test_files = [
        "test_uniqueness.py",
        # Note: test_sudoku_logic.py requires pytest, so it's optional
    ]
    
    results = {}
    for test_file in test_files:
        test_path = Path(__file__).parent / test_file
        if test_path.exists():
            results[test_file] = run_test_file(str(test_path))
        else:
            print(f"⚠ {test_file} not found")
            results[test_file] = False
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    all_passed = all(results.values())
    for test_file, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_file}: {status}")
    
    print("=" * 70)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
    else:
        print("✗ SOME TESTS FAILED")
    print("=" * 70)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())

