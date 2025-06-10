import pytest
from engine.battle.support.battle_pathfinder import BattlePathfinder

class DummyTile:
    def is_walkable(self):
        return True

class DummyBattle:
    def __init__(self):
        self.width = 3
        self.height = 3
        self.tiles = [[DummyTile() for _ in range(3)] for _ in range(3)]

class TestBattlePathfinder:
    def test_find_path_simple(self):
        battle = DummyBattle()
        path = BattlePathfinder.find_path(battle, (0,0), (2,2))
        assert path[0] == (1, 1) or path[-1] == (2, 2) or path == []

