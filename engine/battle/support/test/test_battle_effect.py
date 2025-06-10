import pytest
from engine.battle.support.battle_effect import TBattleEffect

class TestTBattleEffect:
    def test_init_defaults(self):
        data = {}
        effect = TBattleEffect('smoke', data)
        assert effect.pid == 'smoke'
        assert effect.name == 'smoke'
        assert effect.description == ''
        assert effect.icon == ''

    def test_init_with_data(self):
        data = {'name': 'Fire', 'description': 'Burns units', 'icon': 'fire.png'}
        effect = TBattleEffect('fire', data)
        assert effect.pid == 'fire'
        assert effect.name == 'Fire'
        assert effect.description == 'Burns units'
        assert effect.icon == 'fire.png'

