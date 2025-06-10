import pytest
from engine.battle.support.battle_fow import TBattleFOW

class TestTBattleFOW:
    def test_class_exists(self):
        fow = TBattleFOW()
        assert isinstance(fow, TBattleFOW)

