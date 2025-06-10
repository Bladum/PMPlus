import pytest
from engine.battle.tile.battle_floor import TBattleFloor

def test_battle_floor_defaults():
    floor = TBattleFloor()
    assert floor.move_cost == 1
    assert floor.armor == 10
    assert floor.is_light_source is False

def test_battle_floor_on_destroy():
    floor = TBattleFloor(destroyed_floor_id='floor_burnt')
    assert floor.on_destroy() == 'floor_burnt'

