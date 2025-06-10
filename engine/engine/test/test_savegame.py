import pytest
from engine.engine.savegame import TSaveGame

def test_savegame_init():
    sg = TSaveGame('test.sav')
    assert isinstance(sg, TSaveGame)
    assert sg.save_path == 'test.sav'
    assert sg.last_saved is None

def test_save_stub():
    sg = TSaveGame()
    sg.save(object())

def test_load_stub():
    sg = TSaveGame()
    sg.load('test.sav')

def test_get_save_metadata():
    sg = TSaveGame('test.sav')
    meta = sg.get_save_metadata()
    assert meta['save_path'] == 'test.sav'
    assert 'last_saved' in meta

