from engine.globe.region import TRegion
from engine.lore.faction import TFaction
from engine.location.city import TCity
from engine.base.geo.abase import TBaseAlien
from engine.craft.craft import TCraft

class TUfoScript:
    """
    Represents a trajectory of UFO, consisting of ordered steps.
    Each step is a dict {type, duration, ...kwargs}.
    Handles all step logic internally (no TUfoScriptStep).
    """
    # Step type constants
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

    def __init__(self, pid, data):
        self.pid = pid

        self.name = data.get('name', pid)
        self.description = data.get('desc', '')
        # Steps: list of dicts {type, duration, ...kwargs}
        self.steps = data.get('steps', [])

    def get_step(self, idx):
        if 0 <= idx < len(self.steps):
            return self.steps[idx]
        return None

    def total_steps(self):
        return len(self.steps)

    def process_current_step(self, ufo, game, step_idx, **kwargs):
        """
        Process the current step for the UFO using internal step logic.
        Returns True if step was processed, False if invalid.
        """
        import random
        step = self.get_step(step_idx)
        if not step:
            return False
        step_type = step.get('type')
        step_kwargs = dict(step)
        step_kwargs.pop('type', None)
        step_kwargs.pop('duration', None)
        step_kwargs.update(kwargs)
        world = game.worldmap

        # Helper functions with type casting
        def random_tile(region_id=None, land=None):
            region = None
            if region_id:
                region = next((r for r in world.regions if r.id == region_id), None)
                if region and not isinstance(region, TRegion):
                    region = TRegion(region)
            tiles = region.region_tiles if region else [ (x, y) for y in range(world.size[1]) for x in range(world.size[0]) ]
            if land is not None:
                tiles = [t for t in tiles if world.tiles[t[1]][t[0]].biome.type == ('land' if land else 'sea')]
            return random.choice(tiles) if tiles else None

        def random_city(region_id=None):
            cities = [c for c in game.worldmap.cities if (not region_id or c.region_id == region_id)]
            # Cast to TCity
            return random.choice([c if isinstance(c, TCity) else TCity(c) for c in cities]) if cities else None

        def random_base(region_id=None, faction=None):
            bases = [b for b in game.worldmap.bases if (not region_id or b.region_id == region_id) and (not faction or b.faction == faction)]
            # Cast to TAbase or TXbase depending on faction
            if not bases:
                return None
            b = random.choice(bases)
            if getattr(b, 'faction', None) == 'xcom':
                return b if isinstance(b, TXbase) else TXbase(b)
            return b if isinstance(b, TAbase) else TAbase(b)

        def random_craft(region_id=None):
            crafts = [c for c in game.worldmap.crafts if (not region_id or c.region_id == region_id)]
            return random.choice([c if isinstance(c, TCraft) else TCraft(c) for c in crafts]) if crafts else None

        # Step logic
        # --- Start steps ---
        if step_type == self.STEP_START_RANDOM:
            # Start in a random tile in region
            region_id = step_kwargs.get('region_id')
            tile = random_tile(region_id)
            if tile:
                ufo.set_position(*tile)

        elif step_type == self.STEP_START_CITY:
            # Start in a random city in region
            region_id = step_kwargs.get('region_id')
            city = random_city(region_id)
            if city:
                ufo.set_position(city.x, city.y)
        elif step_type == self.STEP_START_ABASE:
            # Start in a random alien base in region
            region_id = step_kwargs.get('region_id')
            base = random_base(region_id, faction=ufo.faction)
            if base:
                ufo.set_position(base.x, base.y)
        elif step_type == self.STEP_START_XBASE:
            # Start in a random XCOM base in region
            region_id = step_kwargs.get('region_id')
            base = random_base(region_id, faction='xcom')
            if base:
                ufo.set_position(base.x, base.y)
        # --- Move steps ---
        elif step_type == self.STEP_MOVE_RANDOM:
            # Move to a random tile in region
            region_id = step_kwargs.get('region_id', ufo.region_id)
            tile = random_tile(region_id)
            if tile:
                ufo.set_position(*tile)
        elif step_type == self.STEP_MOVE_CITY:
            # Move to a random city in region
            region_id = step_kwargs.get('region_id', ufo.region_id)
            city = random_city(region_id)
            if city:
                ufo.set_position(city.x, city.y)
        elif step_type == self.STEP_MOVE_CRAFT:
            # Move to a random XCOM craft in region
            region_id = step_kwargs.get('region_id', ufo.region_id)
            craft = random_craft(region_id)
            if craft:
                ufo.set_position(craft.x, craft.y)
        elif step_type == self.STEP_MOVE_ABASE:
            # Move to a random alien base in region
            region_id = step_kwargs.get('region_id', ufo.region_id)
            base = random_base(region_id, faction=ufo.faction)
            if base:
                ufo.set_position(base.x, base.y)
        elif step_type == self.STEP_MOVE_XBASE:
            # Move to a random XCOM base in region
            region_id = step_kwargs.get('region_id', ufo.region_id)
            base = random_base(region_id, faction='xcom')
            if base:
                ufo.set_position(base.x, base.y)
        elif step_type == self.STEP_MOVE_REGION:
            # Move to a neighboring region
            region = next((r for r in world.regions if r.id == ufo.region_id), None)
            if region and hasattr(region, 'neighbors'):
                neighbor = random.choice(region.neighbors) if region.neighbors else None
                if neighbor:
                    tile = random_tile(neighbor.id)
                    if tile:
                        ufo.set_position(*tile)
        elif step_type == self.STEP_MOVE_COUNTRY:
            # Move to a tile owned by a specific country
            region_id = step_kwargs.get('region_id', ufo.region_id)
            country_id = step_kwargs.get('country_id')
            region = next((r for r in world.regions if r.id == region_id), None)
            if region:
                tiles = [t for t in region.region_tiles if world.tiles[t[1]][t[0]].owner_country_id == country_id]
                if tiles:
                    ufo.set_position(*random.choice(tiles))
        elif step_type == self.STEP_MOVE_LAND:
            # Move to a land tile in region
            region_id = step_kwargs.get('region_id', ufo.region_id)
            tile = random_tile(region_id, land=True)
            if tile:
                ufo.set_position(*tile)
        elif step_type == self.STEP_MOVE_SEA:
            # Move to a sea tile in region
            region_id = step_kwargs.get('region_id', ufo.region_id)
            tile = random_tile(region_id, land=False)
            if tile:
                ufo.set_position(*tile)
        elif step_type == self.STEP_MOVE_REMOTE:
            # Move to a tile far from any city
            region_id = step_kwargs.get('region_id', ufo.region_id)
            city_coords = [(c.x, c.y) for c in game.worldmap.cities]
            region = next((r for r in world.regions if r.id == region_id), None)
            tiles = region.region_tiles if region else []
            def min_dist(tile):
                return min([abs(tile[0]-cx)+abs(tile[1]-cy) for (cx,cy) in city_coords]) if city_coords else 999
            remote_tiles = sorted(tiles, key=min_dist, reverse=True)
            if remote_tiles:
                ufo.set_position(*remote_tiles[0])
        # --- Other actions ---
        elif step_type == self.STEP_PATROL:
            # Stay in air, do not move
            pass
        elif step_type == self.STEP_LAND:
            # Land on land, remove if on water
            tile = world.tiles[ufo.y][ufo.x]
            if tile.biome.type == 'land':
                ufo.status = 'landed'
            else:
                ufo.remove()
        elif step_type == self.STEP_DIVE:
            # Dive under water, crash if on land
            tile = world.tiles[ufo.y][ufo.x]
            if tile.biome.type == 'sea':
                ufo.status = 'dived'
            else:
                ufo.status = 'crashed'
        elif step_type == self.STEP_CRASH:
            # Force crash
            ufo.status = 'crashed'
        elif step_type == self.STEP_BUILD_BASE:
            # Create alien base for the same faction
            game.worldmap.create_alien_base(ufo.x, ufo.y, ufo.faction)
        elif step_type == self.STEP_END:
            # Remove UFO, score points for mission
            ufo.remove()
        return True
