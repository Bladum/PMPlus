class TUfoScriptStep:
    """
    Represents a single step in UFO script
    It is used to calculate move path of UFO and how it score points, even when not moving
    """

    STEP_START_RANDOM = 'Starts in random tile in region'
    STEP_START_CITY = 'Starts in random city in region'
    STEP_START_ABASE = 'Starts in random abase in region'
    STEP_START_XBASE = 'Starts in random xbase in region'

    STEP_MOVE_RANDOM = 'Move to random tile in region'
    STEP_MOVE_CITY = 'Move to random city in region'
    STEP_MOVE_CRAFT = 'Move to random xcom craft in region'
    STEP_MOVE_ABASE = 'Move to random abase in region'
    STEP_MOVE_XBASE = 'Move to random xbase in region'
    STEP_MOVE_REGION = 'Move to another region close to this region'
    STEP_MOVE_COUNTRY = 'Move to tile that is owned by country'
    STEP_MOVE_LAND = 'Move to land tile in this region'
    STEP_MOVE_SEA = 'Move to sea tile in this region'
    STEP_MOVE_REMOTE = 'Move to random tile that is far from any existing city'

    STEP_PATROL = 'Stay in air but do not move'
    STEP_LAND = 'Land on land, if on water then remove'
    STEP_DIVE = 'Dive under water, if on land then crash'
    STEP_CRASH = 'Force crash on land or water'

    STEP_BUILD_BASE = 'Create alien base for the same faction'

    STEP_END = 'Remove ufo, score points for mission'

    def process_step(self, ufo, game, step_type, **kwargs):
        """
        Process a single script step for a UFO using the game context.
        """
        import random
        world = game.worldmap
        # Helper functions
        def random_tile(region_id=None, land=None):
            region = next((r for r in world.regions if r.id == region_id), None) if region_id else None
            tiles = region.region_tiles if region else [ (x, y) for y in range(world.size[1]) for x in range(world.size[0]) ]
            if land is not None:
                tiles = [t for t in tiles if world.tiles[t[1]][t[0]].biome.type == ('land' if land else 'sea')]
            return random.choice(tiles) if tiles else None
        def random_city(region_id=None):
            cities = [c for c in game.worldmap.cities if (not region_id or c.region_id == region_id)]
            return random.choice(cities) if cities else None
        def random_base(region_id=None, faction=None):
            bases = [b for b in game.worldmap.bases if (not region_id or b.region_id == region_id) and (not faction or b.faction == faction)]
            return random.choice(bases) if bases else None
        def random_craft(region_id=None):
            crafts = [c for c in game.worldmap.crafts if (not region_id or c.region_id == region_id)]
            return random.choice(crafts) if crafts else None

        # Step logic
        if step_type == self.STEP_START_RANDOM:
            region_id = kwargs.get('region_id')
            tile = random_tile(region_id)
            if tile:
                ufo.set_position(*tile)

        elif step_type == self.STEP_START_CITY:
            region_id = kwargs.get('region_id')
            city = random_city(region_id)
            if city:
                ufo.set_position(city.x, city.y)

        elif step_type == self.STEP_START_ABASE:
            region_id = kwargs.get('region_id')
            base = random_base(region_id, faction=ufo.faction)
            if base:
                ufo.set_position(base.x, base.y)

        elif step_type == self.STEP_START_XBASE:
            region_id = kwargs.get('region_id')
            base = random_base(region_id, faction='xcom')
            if base:
                ufo.set_position(base.x, base.y)

        elif step_type == self.STEP_MOVE_RANDOM:
            region_id = kwargs.get('region_id', ufo.region_id)
            tile = random_tile(region_id)
            if tile:
                ufo.set_position(*tile)

        elif step_type == self.STEP_MOVE_CITY:
            region_id = kwargs.get('region_id', ufo.region_id)
            city = random_city(region_id)
            if city:
                ufo.set_position(city.x, city.y)

        elif step_type == self.STEP_MOVE_CRAFT:
            region_id = kwargs.get('region_id', ufo.region_id)
            craft = random_craft(region_id)
            if craft:
                ufo.set_position(craft.x, craft.y)

        elif step_type == self.STEP_MOVE_ABASE:
            region_id = kwargs.get('region_id', ufo.region_id)
            base = random_base(region_id, faction=ufo.faction)
            if base:
                ufo.set_position(base.x, base.y)

        elif step_type == self.STEP_MOVE_XBASE:
            region_id = kwargs.get('region_id', ufo.region_id)
            base = random_base(region_id, faction='xcom')
            if base:
                ufo.set_position(base.x, base.y)

        elif step_type == self.STEP_MOVE_REGION:
            region = next((r for r in world.regions if r.id == ufo.region_id), None)
            if region and hasattr(region, 'neighbors'):
                neighbor = random.choice(region.neighbors) if region.neighbors else None
                if neighbor:
                    tile = random_tile(neighbor.id)
                    if tile:
                        ufo.set_position(*tile)

        elif step_type == self.STEP_MOVE_COUNTRY:
            region_id = kwargs.get('region_id', ufo.region_id)
            country_id = kwargs.get('country_id')
            # Find all tiles in region owned by the country
            region = next((r for r in world.regions if r.id == region_id), None)
            if region:
                tiles = [t for t in region.region_tiles if world.tiles[t[1]][t[0]].owner_country_id == country_id]
                if tiles:
                    ufo.set_position(*random.choice(tiles))

        elif step_type == self.STEP_MOVE_LAND:
            region_id = kwargs.get('region_id', ufo.region_id)
            tile = random_tile(region_id, land=True)
            if tile:
                ufo.set_position(*tile)

        elif step_type == self.STEP_MOVE_SEA:
            region_id = kwargs.get('region_id', ufo.region_id)
            tile = random_tile(region_id, land=False)
            if tile:
                ufo.set_position(*tile)

        elif step_type == self.STEP_MOVE_REMOTE:
            region_id = kwargs.get('region_id', ufo.region_id)
            # Find tiles far from any city
            city_coords = [(c.x, c.y) for c in game.worldmap.cities]
            region = next((r for r in world.regions if r.id == region_id), None)
            tiles = region.region_tiles if region else []
            def min_dist(tile):
                return min([abs(tile[0]-cx)+abs(tile[1]-cy) for (cx,cy) in city_coords]) if city_coords else 999
            remote_tiles = sorted(tiles, key=min_dist, reverse=True)
            if remote_tiles:
                ufo.set_position(*remote_tiles[0])

        elif step_type == self.STEP_PATROL:
            pass  # Do nothing

        elif step_type == self.STEP_LAND:
            tile = world.tiles[ufo.y][ufo.x]
            if tile.biome.type == 'land':
                ufo.status = 'landed'
            else:
                ufo.remove()  # Remove if on water

        elif step_type == self.STEP_DIVE:
            tile = world.tiles[ufo.y][ufo.x]
            if tile.biome.type == 'sea':
                ufo.status = 'dived'
            else:
                ufo.status = 'crashed'

        elif step_type == self.STEP_CRASH:
            ufo.status = 'crashed'

        elif step_type == self.STEP_BUILD_BASE:
            # Create alien base for the same faction at UFO's location
            game.worldmap.create_alien_base(ufo.x, ufo.y, ufo.faction)

        elif step_type == self.STEP_END:
            ufo.remove()
            # Score points for mission (implement as needed)
