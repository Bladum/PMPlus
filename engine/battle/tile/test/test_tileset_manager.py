import pytest
from engine.battle.tile.tileset_manager import TTilesetManager

def test_tileset_manager_init():
    mgr = TTilesetManager()
    assert isinstance(mgr.all_tiles, dict)
    assert mgr.folder_path == ''

