"""
engine/battle/map_block_entry.py

Defines the TMapBlockEntry class, representing a map block entry in a terrain definition for battle map generation.

Classes:
    TMapBlockEntry: Represents a map block entry in a terrain definition for battle map generation.

Last standardized: 2025-06-15
"""

class TMapBlockEntry:
    """
    Represents a map block entry in a terrain definition for battle map generation.
    Each entry describes a block's map name, size, group, selection chance, items, units, and debug visibility.

    Attributes:
        map (str): Name of the TMX map file (without extension).
        size (int): Size of the block (1=15x15, 2=30x30, ...).
        group (int): Group identifier for block selection.
        chance (int): Chance for this block to be selected.
        items (dict): Dictionary of items placed in this block.
        units (dict): Dictionary of units placed in this block.
        show (bool): Whether to show this block in debug/visualization.
    """
    def __init__(self, data):
        """
        Initialize a TMapBlockEntry instance with the given properties.

        Args:
            data (dict): Dictionary containing block properties (map, size, group, chance, items, units, show).
        """
        self.map = data.get('map', '')
        self.size = data.get('size', 1)
        self.group = data.get('group', 0)
        self.chance = data.get('chance', 1)
        self.items = data.get('items', {})
        self.units = data.get('units', {})
        self.show = data.get('show', False)
