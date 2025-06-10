import pytest
from engine.base.base_generator import TBaseXComBattleGenerator
from unittest.mock import MagicMock

class TestTBaseXComBattleGenerator:
    def test_generate_battle_map_empty(self):
        mock_base = MagicMock()
        mock_base.facilities = {}
        gen = TBaseXComBattleGenerator(mock_base)
        battle_map = gen.generate_battle_map()
        assert len(battle_map) == 6
        assert all(len(row) == 6 for row in battle_map)
        for row in battle_map:
            assert all(cell == 'map_empty' for cell in row)

    def test_generate_battle_map_with_facilities(self):
        mock_facility = MagicMock()
        mock_facility.facility_type.map_block = 'map_lift'
        mock_base = MagicMock()
        mock_base.facilities = {(2, 3): mock_facility}
        gen = TBaseXComBattleGenerator(mock_base)
        battle_map = gen.generate_battle_map()
        assert battle_map[3][2] == 'map_lift'
        # All other cells should be 'map_empty'
        for y, row in enumerate(battle_map):
            for x, cell in enumerate(row):
                if (x, y) != (2, 3):
                    assert cell == 'map_empty'

