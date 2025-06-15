"""
Test suite for engine.base.xbase (TBaseXCom)
Covers initialization and add_facility method using pytest.
"""
import pytest
from engine.base.xbase import TBaseXCom

class DummyFacilityType:
    def __init__(self, build_time=3):
        self.build_time = build_time

class DummyFacility:
    def __init__(self, facility_type, position):
        self.facility_type = facility_type
        self.position = position

class DummyGame:
    class Mod:
        def __init__(self):
            self.facilities = {'TestFacility': DummyFacilityType()}
    def __init__(self):
        self.mod = self.Mod()

@pytest.fixture
def xbase(monkeypatch):
    # Patch TGame to use DummyGame
    import engine.base.xbase as xbase_mod
    monkeypatch.setattr(xbase_mod, 'TGame', DummyGame)
    return TBaseXCom('base1', data={'name': 'XCOM Base'})

def test_init_defaults(xbase):
    """Test initialization and default attributes."""
    assert isinstance(xbase.facilities, dict)
    assert hasattr(xbase, 'inventory')
    assert hasattr(xbase, 'game')

def test_add_facility_adds_to_dict(xbase):
    """Test add_facility adds a facility to the facilities dict."""
    facility_type = DummyFacilityType()
    facility = xbase.add_facility(facility_type, position=(2, 3), force_add=True)
    assert (2, 3) in xbase.facilities
    assert xbase.facilities[(2, 3)] == facility
