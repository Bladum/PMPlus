import pytest
from engine.battle.support.reactions import TReactionFire

class TestTReactionFire:
    def test_class_exists(self):
        reaction = TReactionFire()
        assert isinstance(reaction, TReactionFire)

