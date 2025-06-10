import pytest
from engine.battle.tile.battle_object import TBattleObject

def test_battle_object_defaults():
    obj = TBattleObject()
    assert obj.armor == 5
    assert obj.is_light_source is False

def test_battle_object_on_destroy():
    obj = TBattleObject(destroyed_object_id='obj_frag')
    assert obj.on_destroy() == 'obj_frag'

