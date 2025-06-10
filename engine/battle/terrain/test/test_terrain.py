import pytest
from unittest.mock import MagicMock
from engine.battle.terrain.terrain import TTerrain

def test_terrain_init():
    data = {'name': 'Desert', 'description': 'Hot', 'tileset': 'desert', 'map_blocks': []}
    terrain = TTerrain('desert', data)
    assert terrain.pid == 'desert'
    assert terrain.name == 'Desert'
    assert terrain.description == 'Hot'
    assert terrain.tileset == 'desert'
    assert isinstance(terrain.map_blocks_entries, list)

