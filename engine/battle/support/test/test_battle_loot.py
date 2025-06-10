import pytest
from engine.battle.support.battle_loot import BattleLoot

class DummyBattle:
    SIDE_PLAYER = 0
    SIDE_ENEMY = 1
    SIDE_ALLY = 2
    SIDE_NEUTRAL = 3
    objectives = []
    tiles = []
    def find_units(self, side=None, alive=None):
        return []
    def find_objects(self):
        return []

class TestBattleLoot:
    def test_generate_empty(self):
        battle = DummyBattle()
        report = BattleLoot.generate(battle)
        assert set(report.keys()) == {'score','loot','captures','experience','sanity','ammo','medals'}

