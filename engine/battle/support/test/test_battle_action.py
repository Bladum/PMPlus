import pytest
from engine.battle.support.battle_action import TBattleActions

class TestTBattleActions:
    def test_class_exists(self):
        actions = TBattleActions()
        assert isinstance(actions, TBattleActions)

