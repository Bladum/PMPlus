import pytest
from engine.battle.tile.battle_tile import TBattleTile

def test_battle_tile_init():
    tile = TBattleTile()
    assert tile.floor_id == '0'
    assert tile.wall_id is None
    assert tile.roof_id is None

def test_battle_tile_copy():
    tile = TBattleTile('A', 'B', 'C')
    tile2 = tile.copy()
    assert tile2.floor_id == 'A'
    assert tile2.wall_id == 'B'
    assert tile2.roof_id == 'C'
    assert tile2 is not tile

