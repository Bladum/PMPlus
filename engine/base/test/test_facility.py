"""
Test suite for engine.base.facility (TFacility)
Covers initialization, is_active, and build_day methods using pytest.
"""
import pytest
from engine.base.facility import TFacility

class DummyFacilityType:
    def __init__(self, build_time=3):
        self.build_time = build_time

class DummyGame:
    class Mod:
        def __init__(self):
            self.facilities = {'TestFacility': DummyFacilityType()}
    def __init__(self):
        self.mod = self.Mod()

@pytest.fixture
def facility(monkeypatch):
    # Patch TGame to use DummyGame
    import engine.base.facility as facility_mod
    monkeypatch.setattr(facility_mod, 'TGame', DummyGame)
    return TFacility('TestFacility', position=(1, 2))

def test_init_defaults(facility):
    """Test initialization and default attributes."""
    assert facility.position == (1, 2)
    assert facility.build_progress == 0
    assert facility.completed is False
    assert facility.hp == 10
    assert hasattr(facility, 'facility_type')

def test_is_active_false_and_true(facility):
    """Test is_active returns False before completion and True after."""
    assert facility.is_active() is False
    facility.completed = True
    assert facility.is_active() is True

def test_build_day_progress_and_completion(facility):
    """Test build_day increments progress and marks as completed."""
    facility.build_day()
    assert facility.build_progress == 1
    facility.build_day()
    facility.build_day()
    assert facility.completed is True
