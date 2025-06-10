import pytest
from engine.location.ufo import TUfo
from unittest.mock import MagicMock

class TestTUfo:
    def test_init_sets_attributes(self, monkeypatch):
        mock_game = MagicMock()
        mock_game.mod.ufo_types.get.return_value = MagicMock(speed=5, health=100)
        mock_game.mod.ufo_scripts.get.return_value = MagicMock()
        monkeypatch.setattr('engine.engine.game.TGame', lambda: mock_game)
        data = {'ufo_type': 'type1', 'ufo_script': 'script1', 'position': (1, 2)}
        ufo = TUfo('ufo1', data)
        assert ufo.ufo_id == 'ufo1'
        assert ufo.position == (1, 2)
        assert ufo.speed_max == 5
        assert ufo.health == 100

    def test_set_and_get_position(self):
        ufo = TUfo('ufo2', {'ufo_type': None, 'ufo_script': None, 'position': (3, 4)})
        ufo.set_position(5, 6)
        assert ufo.get_position() == (5, 6)

    def test_take_damage_and_destroyed(self):
        ufo = TUfo('ufo3', {'ufo_type': MagicMock(speed=1, health=10), 'ufo_script': None, 'position': (0, 0)})
        ufo.health = 10
        assert not ufo.is_destroyed()
        ufo.take_damage(5)
        assert ufo.health == 5
        assert not ufo.is_destroyed()
        ufo.take_damage(10)
        assert ufo.health == 0
        assert ufo.is_destroyed()

