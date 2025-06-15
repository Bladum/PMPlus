"""
Test suite for engine.unit.unit_stat (TUnitStats)
Covers initialization and attribute defaults using pytest.
"""
import pytest
from engine.unit.unit_stat import TUnitStats

@pytest.fixture
def stats():
    data = {
        'health': 40,
        'speed': 12,
        'strength': 15,
        'energy': 30,
        'aim': 60,
        'melee': 50,
        'reflex': 20,
        'psi': 10,
        'bravery': 80,
        'sanity': 100,
        'sight': (20, 10),
        'sense': (5, 5),
        'cover': (2, 1),
        'morale': 12,
        'action_points': 6,
        'size': 1,
    }
    return TUnitStats(data)

def test_init_defaults(stats):
    """Test initialization and attribute values from data dict."""
    assert stats.health == 40
    assert stats.speed == 12
    assert stats.strength == 15
    assert stats.energy == 30
    assert stats.aim == 60
    assert stats.melee == 50
    assert stats.reflex == 20
    assert stats.psi == 10
    assert stats.bravery == 80
    assert stats.sanity == 100
    assert stats.sight == (20, 10)
    assert stats.sense == (5, 5)
    assert stats.cover == (2, 1)
    assert stats.morale == 12
    assert stats.action_points == 6
    assert stats.size == 1
    assert stats.action_points_left == 6
    assert stats.energy_left == 30
    assert stats.hurt == 0
    assert stats.stun == 0

