"""
Test suite for engine.battle.battle_floor (TBattleFloor)
Covers initialization, attribute defaults, and on_destroy method using pytest.
"""
import pytest
from engine.battle.battle_floor import TBattleFloor

@pytest.fixture
def floor():
    return TBattleFloor(move_cost=2, sight_cost=1, accuracy_cost=-1, armor=5, sound='step.wav', is_light_source=True, destroyed_floor_id='rubble')

def test_init_defaults(floor):
    """Test initialization and attribute values from kwargs."""
    assert floor.move_cost == 2
    assert floor.sight_cost == 1
    assert floor.accuracy_cost == -1
    assert floor.armor == 5
    assert floor.sound == 'step.wav'
    assert floor.is_light_source is True
    assert floor.destroyed_floor_id == 'rubble'

def test_on_destroy_returns_destroyed_floor_id(floor):
    """Test on_destroy returns the destroyed_floor_id."""
    assert floor.on_destroy() == 'rubble'
