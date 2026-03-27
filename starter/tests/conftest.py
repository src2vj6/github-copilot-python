"""
Pytest configuration and shared fixtures.
"""
import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture(autouse=True)
def reset_current_state():
    """Reset CURRENT state before each test to ensure test isolation."""
    from app import CURRENT
    CURRENT['puzzle'] = None
    CURRENT['solution'] = None
    yield
    # Cleanup after test
    CURRENT['puzzle'] = None
    CURRENT['solution'] = None
