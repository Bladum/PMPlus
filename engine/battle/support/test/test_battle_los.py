import pytest
from engine.battle.support.battle_los import BattleLOS

class DummyTile:
    def __init__(self, wall=None, smoke=False, fire=False, gas=False):
        self.wall = wall
        self.smoke = smoke
        self.fire = fire
        self.gas = gas

class DummyWall:
    def __init__(self, sight_mod=0):
        self.sight_mod = sight_mod
        self.is_destroyed = False

class DummyBattle:
    def __init__(self):
        self.tiles = [[DummyTile() for _ in range(3)] for _ in range(3)]

class TestBattleLOS:
    def test_has_los_simple(self):
        battle = DummyBattle()
        assert BattleLOS.has_los(battle, (0,0), (2,2)) is True

