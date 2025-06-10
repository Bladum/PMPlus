import pytest
from engine.battle.terrain.map_block import TMapBlock

def test_map_block_init_default():
    block = TMapBlock()
    assert block.size == 15
    assert isinstance(block.tiles, list)
    assert len(block.tiles) == 15

def test_map_block_get_tile():
    block = TMapBlock(size=2)
    tile = block.get_tile(1, 1)
    assert tile is not None

