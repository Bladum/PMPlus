import pytest
from engine.battle.tile.battle_wall import TBattleWall

def test_battle_wall_defaults():
    wall = TBattleWall()
    assert wall.block_sight is True
    assert wall.armor == 20
    assert wall.is_light_source is False

def test_battle_wall_on_destroy():
    wall = TBattleWall(destroyed_wall_id='wall_ruined')
    assert wall.on_destroy() == 'wall_ruined'

