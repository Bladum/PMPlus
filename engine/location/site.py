from globe.location import TLocation
from .site_type import TSiteType


class TSite(TLocation):
    """
    Represent a mission on world map, which is not UFO, neither base
    Its does not move, it is static
    Its temporary, when mission is finished, it will be removed and points scored
    It has deployment to control what units are during battle
    it has no ufo script
    """
    def __init__(self, loc_id, data):
        super().__init__(loc_id, data)

        from engine.engine.game import TGame
        self.game: TGame = TGame()

        site_type = data.get('site_type')
        self.site_type  = self.game.mod.sites.get(site_type)

        # Use map_blocks from type if not present in instance data
        self.map_blocks = self.generate_random_map_blocks()

    def generate_random_map_blocks(self, num_blocks=4):
        """
        Generate a random map_blocks dictionary for the site.
        num_blocks: number of blocks to generate (default 4)
        Returns a dict with block names as keys and random types as values.
        """
        import random
        block_types = ['urban', 'forest', 'farm', 'desert', 'mountain']
        return {f'block_{i+1}': random.choice(block_types) for i in range(num_blocks)}

        # TODO fix this
