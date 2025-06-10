import pytest
from unittest.mock import MagicMock
from engine.battle.map.battle_generator import TBattleGenerator

def test_battle_generator_init():
    terrain = MagicMock()
    script = MagicMock()
    gen = TBattleGenerator(terrain, script, 4, 4)
    assert gen.map_width == 4
    assert gen.map_height == 4
    assert gen.block_size == 15

