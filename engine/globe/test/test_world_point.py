import pytest
from engine.globe.world_point import TWorldPoint

def test_tworldpoint_methods():
    p1 = TWorldPoint(1,2)
    p2 = TWorldPoint(4,6)
    assert p1.to_tuple() == (1,2)
    assert p1.distance_to(p2) == pytest.approx(5.0)
    assert p1.manhattan_distance(p2) == 7
    assert p1 + p2 == TWorldPoint(5,8)
    assert p2 - p1 == TWorldPoint(3,4)
    assert p1.scale(2) == TWorldPoint(2,4)
    assert p1.is_within_bounds(10,10)
    assert not p1.is_within_bounds(1,1)
    assert p1.midpoint(p2) == TWorldPoint(2,4)
    adj = p1.get_adjacent_points()
    assert TWorldPoint(1,1) in adj and TWorldPoint(2,2) not in adj
    adj_diag = p1.get_adjacent_points_with_diagonals()
    assert TWorldPoint(0,1) in adj_diag and TWorldPoint(2,2) in adj_diag
    assert p1.round_to_grid(2) == TWorldPoint(2,2)

