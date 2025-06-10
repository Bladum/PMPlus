# TMapBlockEntry: Represents a map block entry in a terrain definition.
# Each entry describes a block's map name, size, group, chance, items, units, and visibility.

class TMapBlockEntry:
    """
    Represents how map blocks are managed inside terrain.
    Each entry describes a block's map name, size (1=15x15, 2=30x30, ...), group, chance, items, units, and visibility.

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

        # Name of the TMX map file (without extension)
        self.map = data.get('map', '')

        # Size of the block (1=15x15, 2=30x30, ...)
        self.size = data.get('size', 1)

        # Group identifier for block selection
        self.group = data.get('group', 0)

        # Chance for this block to be selected
        self.chance = data.get('chance', 1)

        # Dictionary of items placed in this block
        self.items = data.get('items', {})

        # Dictionary of units placed in this block
        self.units = data.get('units', {})

        # Whether to show this block in debug/visualization
        self.show = data.get('show', False)
