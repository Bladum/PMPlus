from economy.transfer import TTransfer
from engine.globe.world_tile import TWorldTile
from lore.faction import TFaction


class TWorld:
    """
    Map of the world, 2D array of WorldTiles
    Can be many worlds in game
    """

    def __init__(self, world_id, data):
        self.id = world_id
        self.name = data.get('name', world_id)
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

    def load_from_tmx(self, tmx_path, countries, regions, biomes):
        """
        Load world map from TMX file. Assigns each tile a biome, country, and region.
        - countries: dict of country_id -> TCountry
        - regions: dict of region_id -> TRegion
        - biomes: dict of biome_id -> biome info
        Populates:
          - self.tiles: 2D array of TWorldTile
          - Each country's owned_tiles
          - Each region's tile list (with overlap)
        """
        import pytmx
        tmx = pytmx.TiledMap(tmx_path)
        width, height = tmx.width, tmx.height
        self.size = [width, height]

        # Prepare 2D array of tiles
        self.tiles = [[None for _ in range(width)] for _ in range(height)]

        # Get layer indices
        biome_layer = tmx.get_layer_by_name('biome')
        country_layer = tmx.get_layer_by_name('country')
        region_layer = tmx.get_layer_by_name('region')

        # Pass 1: assign tile data, country, biome, region
        for y in range(height):
            for x in range(width):
                biome_id = biome_layer.data[y][x]
                country_id = country_layer.data[y][x]
                region_id = region_layer.data[y][x]
                tile = TWorldTile(x, y, {
                    'biome': biomes.get(biome_id),
                    'owner_country_id': country_id,
                    'region_id': region_id
                })
                self.tiles[y][x] = tile
                # Assign to country
                if country_id in countries:
                    countries[country_id].add_tile((x, y))

        # Pass 2: assign region tiles (with overlap)
        region_tile_map = {region.id: set() for region in regions.values()}
        for y in range(height):
            for x in range(width):
                tile = self.tiles[y][x]
                if tile.region_id in region_tile_map:
                    region_tile_map[tile.region_id].add((x, y))

        # Find neighbours: two regions are neighbours if they share at least 2 tiles
        region_neighbors = {region.id: set() for region in regions.values()}
        region_ids = list(region_tile_map.keys())
        for i, id1 in enumerate(region_ids):
            for id2 in region_ids[i+1:]:
                common = region_tile_map[id1] & region_tile_map[id2]
                if len(common) >= 2:
                    region_neighbors[id1].add(id2)
                    region_neighbors[id2].add(id1)

        # Assign region_tiles and neighbors
        for region in regions.values():

            # Start with tiles assigned to this region
            region_tiles = region_tile_map[region.id]
            # Expand: add all neighboring tiles (8-way)
            expanded = set(region_tiles)

            for x, y in region_tiles:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            expanded.add((nx, ny))

            region.region_tiles = list(expanded)
            region.neighbors = [rid for rid in region_neighbors[region.id]]
