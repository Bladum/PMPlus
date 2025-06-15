"""
XCOM Location Module: site.py

Represents a static mission site on the world map.

Classes:
    TSite: Mission site with attributes, type, and tactical map block generation.

Last updated: 2025-06-14
"""

from globe.location import TLocation
from .site_type import TSiteType


class TSite(TLocation):
    """
    Represents a mission location on the world map that is not a UFO or a base.
    Sites are static, temporary locations that represent mission opportunities.
    """

    def __init__(self, loc_id, data: dict):
        """
        Initialize a TSite instance.
        Args:
            loc_id (str): Unique identifier for the site location.
            data (dict): Dictionary with site attributes (site_type, etc.).
        """
        super().__init__(loc_id, data)

        from engine.engine.game import TGame
        self.game: TGame = TGame()  # Reference to the game instance

        site_type = data.get('site_type')
        self.site_type = self.game.mod.sites.get(site_type)  # Site type definition

        # Use map_blocks from type if not present in instance data
        self.map_blocks = self.generate_random_map_blocks()

    def generate_random_map_blocks(self, num_blocks: int = 4) -> dict:
        """
        Generate a random map_blocks dictionary for the site.
        Args:
            num_blocks (int): Number of blocks to generate (default 4).
        Returns:
            dict: Block names as keys and random types as values.
        """
        import random
        block_types = ['urban', 'forest', 'farm', 'desert', 'mountain']
        return {f'block_{i+1}': random.choice(block_types) for i in range(num_blocks)}
