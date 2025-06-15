"""
Test suite for engine.globe.location (TLocation)
Covers initialization, update_visibility, and replenish_cover using pytest.
"""
import pytest
from engine.globe.location import TLocation

class DummyWorldPoint:
    @staticmethod
    def from_tuple(pos):
        return pos

@pytest.fixture
def location(monkeypatch):
    import engine.globe.location as location_mod
    monkeypatch.setattr(location_mod, 'TWorldPoint', DummyWorldPoint)
    data = {
        'name': 'Base',
        'description': 'XCOM Base',
        'position': (5, 5),
        'initial_cover': 10,
        'cover': 5,
        'cover_change': 2
    }
    return TLocation('BASE1', data)

def test_init_defaults(location):
    """Test initialization and attribute values from data dict."""
    assert location.pid == 'BASE1'
    assert location.name == 'Base'
    assert location.description == 'XCOM Base'
    assert location.position == (5, 5)
    assert location.initial_cover == 10
    assert location.cover == 5
    assert location.cover_change == 2
    assert location.visible is False

def test_update_visibility_and_replenish_cover(location):
    """Test update_visibility and replenish_cover methods."""
    location.cover = 0
    location.update_visibility()
    assert location.visible is True
    location.cover = 5
    location.replenish_cover()
    assert location.cover == 10

def test_tlocation_init_and_visibility():
    loc = TLocation(pid=1, data={'name': 'Base', 'position': (5, 5), 'initial_cover': 10, 'cover_change': 2})
    assert loc.name == 'Base'
    assert loc.position.x == 5 and loc.position.y == 5
    loc.cover = 0
    loc.update_visibility()
    assert loc.visible
    loc.cover = 5
    loc.update_visibility()
    assert not loc.visible
    loc.replenish_cover()
    assert loc.cover == 7

def test_tlocation_distance_to():
    loc1 = TLocation(1, {'position': (0,0)})
    loc2 = TLocation(2, {'position': (3,4)})
    assert loc1.distance_to(loc2) == 5.0
    assert loc1.distance_to((3,4)) == 5.0
    assert loc1.distance_to(TWorldPoint(3,4)) == 5.0

