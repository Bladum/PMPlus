import pytest
from engine.engine.game import TGame

def test_game_singleton():
    g1 = TGame()
    g2 = TGame()
    assert g1 is g2

def test_game_attributes():
    game = TGame()
    assert hasattr(game, 'worldmap')
    assert hasattr(game, 'campaigns')
    assert hasattr(game, 'calendar')
    assert hasattr(game, 'budget')
    assert hasattr(game, 'funding')
    assert hasattr(game, 'scoring')
    assert hasattr(game, 'research_tree')
    assert hasattr(game, 'mod')
    assert hasattr(game, 'bases')
    assert hasattr(game, 'current_base_name')
    assert hasattr(game, 'base_labels')

def test_add_and_remove_base():
    game = TGame()
    class DummyBase: pass
    base = DummyBase()
    assert game.add_base('OMEGA', base)
    assert game.base_exists('OMEGA')
    assert game.remove_base('OMEGA')
    assert not game.base_exists('OMEGA')

def test_set_active_base():
    game = TGame()
    class DummyBase: pass
    game.add_base('OMEGA', DummyBase())
    assert game.set_active_base('OMEGA')
    assert game.get_active_base() is not None

def test_get_base_status():
    game = TGame()
    class DummyBase: pass
    game.add_base('OMEGA', DummyBase())
    assert game.get_base_status('OMEGA') in ['active', 'available']
    assert game.get_base_status('NONEXISTENT') == 'nonexistent'

