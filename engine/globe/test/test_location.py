from engine.globe.location import TLocation
from engine.globe.world_point import TWorldPoint

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

