"""
TBaseXComBattleGenerator: Generates a battle map layout for an XCOM base based on its facilities.
Purpose: Converts base facility layout into a 2D map block array for tactical battles.
Last update: 2025-06-10
"""

from base.geo.xbase import TBaseXCom


class TBaseXComBattleGenerator:
    '''
    Generates a battle map for an XCOM base using its facilities and their positions.
    Attributes:
        base (TBaseXCom): The base object containing facilities and positions.
    '''

    def __init__(self, base: TBaseXCom):
        """
        Initialize the battle map generator for a base.
        Args:
            base (TBaseXCom): The base object with facilities and positions.
        """
        self.base = base

    def generate_battle_map(self) -> list:
        """
        Generate a 6x6 2D array of map_blocks for the base, filling empty spots with 'map_empty'.
        Returns:
            list: 2D list (6x6) of map block IDs for tactical battle generation.
        """
        size = 6
        battle_map = [['map_empty' for _ in range(size)] for _ in range(size)]
        for pos, facility in self.base.facilities.items():
            x, y = pos
            facility_type = facility.facility_type
            map_block = getattr(facility_type, 'map_block', 'map_empty')
            if 0 <= x < size and 0 <= y < size:
                battle_map[y][x] = map_block
        return battle_map
