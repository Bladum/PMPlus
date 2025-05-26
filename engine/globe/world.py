from pytmx import TiledTileLayer

from economy.ttransfer import TTransfer
from engine.globe.world_tile import TWorldTile
from lore.faction import TFaction
from pathlib import Path


class TWorld:
    """
    Map of the world, 2D array of WorldTiles
    Can be many worlds in game
    """

    def __init__(self, pid, data):
        self.pid = pid
        self.name = data.get('name', pid)
        self.description = data.get('description', '')

        # World map properties
        self.size = data.get('size', [0, 0])
        self.map_file = data.get('map_file', None)

        # World features
        self.countries = data.get('countries', False)
        self.bases = data.get('bases', False)
        self.factions = data.get('factions', False)
        self.regions = data.get('regions', False)

        # Access to world via requirements
        self.tech_start = data.get('tech_start', [])

        # Global transfer list
        self.transfer_list = list[TTransfer]

        self.tiles : list[list[TWorldTile]] = []

        # Factions and diplomacy/relations
        self.factions : list[TFaction] = []
        self.diplomacy : dict[str, int] = {}

    def get_day_night_map(self, day_of_month):
        """
        Returns a 2D array (size: [height][width]) with True for day, False for night for each tile.
        The day/night band moves westward, completing a full cycle in 30 days.
        """
        width = self.size[0] if self.size and self.size[0] else 90
        height = self.size[1] if self.size and self.size[1] else 45
        day_night_map = [[False for _ in range(width)] for _ in range(height)]

        # The sun's center longitude (tile_x) moves by 3 tiles per day
        sun_center = (3 * (day_of_month - 1)) % width

        # Define day as +/- 22 tiles from sun_center (about half the map is day)
        for y in range(height):
            for x in range(width):
                # Calculate distance from sun_center, wrap around
                dist = (x - sun_center) % width
                if dist > width // 2:
                    dist = width - dist
                # Day if within 22 tiles of sun_center (about 44/90 = 49% of map)
                day_night_map[y][x] = dist <= 22

        return day_night_map

    @classmethod
    def from_tmx(cls, tmx_path):
        """
        Load a world TMX file and create a TWorld instance with all tiles, using GID mapping for biomes, countries, and regions.
        Uses process_layer logic similar to TMapBlock.from_tmx for GID matching.
        """
        import pytmx
        from engine.globe.world_tile import TWorldTile
        tmx_path = Path(tmx_path)
        tmx = pytmx.TiledMap(str(tmx_path))
        width, height = tmx.width, tmx.height

        from engine.engine.game import TGame
        game = TGame()

        # Calculate used tilesets for this block
        used_tilesets = {
                (tileset.name,
                 tileset.firstgid,
                 tileset.firstgid + (getattr(tileset, 'tilecount', 0) or getattr(tileset, 'tile_count', 0) or 0) - 1,
                 getattr(tileset, 'tilecount', 0) or getattr(tileset, 'tile_count', 0) or 0)
                for tileset in tmx.tilesets
            }

        # Helper function to process layer data
        def process_layer(layer):
            if layer is None:
                return None

            data = [[0 for _ in range(width)] for _ in range(height)]
            # Pre-compute the division factor (1/18) for better performance
            div_factor = 1.0 / 18

            for x, y, image in layer.tiles():
                ix, iy, _, __ = image[1]
                # Use multiplication instead of division for better performance
                dx = (ix - 1) * div_factor
                dy = (iy - 1) * div_factor
                dn = dy * 10 + dx + 1
                data[y][x] = dn

            return data

        layers = {l.name: l for l in tmx.visible_layers if hasattr(l, 'data') and l.name in ('floor', 'wall', 'roof')}
        biome_layer: TiledTileLayer = layers.get('biome')
        country_layer: TiledTileLayer = layers.get('country')
        region_layer: TiledTileLayer = layers.get('region')

        biome_layer_data = process_layer(biome_layer)
        country_layer_data = process_layer(country_layer)
        region_layer_data = process_layer(region_layer)

        # Create world instance
        world = cls(pid="from_tmx", data={"size": [width, height]})
        world.tiles = [[None for _ in range(width)] for _ in range(height)]
        world.used_tilesets = used_tilesets

        for y in range(height):
            for x in range(width):
                biome_gid = biome_layer_data[y][x] if biome_layer_data else 0
                country_gid = country_layer_data[y][x] if country_layer_data else 0
                region_gid = region_layer_data[y][x] if region_layer_data else 0
                tile = TWorldTile(x, y, {
                    'biome': biome_gid,
                    'owner_country_id': country_gid,
                    'region_id': region_gid
                })
                world.tiles[y][x] = tile

        countries_dict = game.mod.countries
        regions_dict = game.mod.regions
        biomes_dict = game.mod.biomes

        # Assign owned tiles to each country
        for country in countries_dict.values():
            country.calculate_owned_tiles(world.tiles)

        # Assign region tiles
        for y in range(height):
            for x in range(width):
                tile = world.tiles[y][x]
                if tile.region_id in regions_dict.keys():
                    regions_dict[tile.region_id].tiles.append(tile)

        # Find region neighbors
        region_neighbors = {region.pid: set() for region in regions_dict.values()}
        region_ids = list(regions_dict.keys())
        for i, id1 in enumerate(region_ids):
            for id2 in region_ids[i+1:]:
                common = regions_dict[id1].tiles & regions_dict[id2].tiles
                if len(common) >= 2:
                    region_neighbors[id1].add(id2)
                    region_neighbors[id2].add(id1)

        for region in regions_dict.values():
            region.calculate_region_tiles(world.tiles, width, height, region_neighbors)


        return world

