"""
Test suite for engine.base.abse (TBaseAlien)
Covers initialization, attribute defaults, and all public methods using pytest.
"""
import pytest
from engine.base.abase import TBaseAlien

class DummyGame:
    pass

@pytest.fixture
def base_alien():
    # Provide minimal data for initialization
    return TBaseAlien(pid='alien_base_1', data={'name': 'Alien Base Alpha'})

def test_init_defaults(base_alien):
    """Test initialization and default attributes."""
    assert base_alien.level == 1
    assert base_alien.level_max == 4
    assert base_alien.level_up_pending is False
    assert base_alien.month_progress == 0
    assert base_alien.missions_this_month == 0
    assert base_alien.supply_pending is False
    assert base_alien.score_per_day == 5
    assert isinstance(base_alien.units_per_level, dict)
    assert isinstance(base_alien.map_size_per_level, dict)
    assert isinstance(base_alien.max_missions_per_month, dict)
    assert base_alien.days_in_month == 30
    assert hasattr(base_alien, 'game')

# Add more tests for public methods as they are implemented in TBaseAlien
# Example:
# def test_some_method(base_alien):
#     ...
