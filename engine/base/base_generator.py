from base.geo.xbase import TBaseXCom


class TBaseXComBattleGenerator:
    """
    special class to create battle map for xcom base based on facilities
    """

    def __init__(self, base: TBaseXCom):
        self.base = base  # The base object (should have facilities and positions)

    def generate_battle_map(self ):
        """
        For the given base, generate a battle map layout based on its facilities and their positions.
        Returns a 6x6 2D array of map_blocks, filling empty spots with 'map_empty'.
        """
        size = 6
        # Initialize 6x6 grid with 'map_empty'
        battle_map = [['map_empty' for _ in range(size)] for _ in range(size)]
        for pos, facility in self.base.facilities.items():
            x, y = pos
            facility_type = facility.facility_type
            map_block = facility_type.map_block
            if 0 <= x < size and 0 <= y < size:
                battle_map[y][x] = map_block
        return battle_map
