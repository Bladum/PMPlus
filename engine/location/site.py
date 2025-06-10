"""
TSite: Represents a static mission site on the world map.
Purpose: Handles mission site attributes, type, and tactical map block generation.
Last update: 2025-06-10
"""

from globe.location import TLocation
from .site_type import TSiteType


class TSite(TLocation):
    """
    Represents a mission location on the world map that is not a UFO or a base.

    Sites are static, temporary locations that represent mission opportunities.
    When a mission at the site is completed, the site is removed and points are scored.
    Sites typically represent alien activities, civilian emergencies, or special operations.

    Attributes:
        site_type (TSiteType): Type of the site, determines appearance and tactical configuration.
        map_blocks (dict): Tactical map blocks for the mission.
        game (TGame): Reference to the game instance.
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
        self.game: TGame = TGame()

        site_type = data.get('site_type')
        self.site_type = self.game.mod.sites.get(site_type)

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
