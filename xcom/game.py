"""
X-COM Game Engine
----------------
A Python-based recreation of the classic X-COM game system with both
strategic (Geoscape) and tactical (Battlescape) gameplay elements.
"""

#----------------------------------------------
#   GEO SCAPE
#----------------------------------------------

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
        self.tech_needed = data.get('tech_needed', [])

class TGlobalRadar:
    """
    Manage radar / detection of UFOs and locations
    """

class TWorldTile:
    """
    Single tile on world map
    Its assigned to region, can be to country, it has biome
    It may have locations on it
    """
    pass

class TBiome:
    """
    Each tile on worls map is assigned to a biome like forest, desert, ocean
    Biomes are used to generate battle with specific terrain type
    """
    def __init__(self, data : dict = {}):
        # Required fields
        self.name = data.get("name", "")
        self.id = data.get("id", 0)

        # Optional fields with defaults
        self.description = data.get("description", "")
        self.image = data.get("image", None)
        self.type = data.get("type", 'land')
        self.terrains = data.get("terrains", {})


class TCountry:
    """
    Most tiles are owned by a country
    score in his tiles is used to calculate funding of XCOM
    Country may be part or leave XCOM
    """
    def __init__(self, data : dict = {}):
        # Required fields
        self.name = data.get("name", "")
        self.id = data.get("id", 0)

        # Optional fields with defaults
        self.description = data.get("description", "")
        self.color = data.get("color", "#000000")
        self.funding = data.get("funding", 10)
        self.funding_cap = data.get("funding_cap", 500)

        # Lists
        self.service_provided = data.get("service_provided", [])
        self.service_forbidden = data.get("service_forbidden", [])

class TRegion:
    """
    Each tile on worls map is assigned to a region
    Regions are used to control location of missions
    Regions have analytics for score
    """

    def __init__(self, data : dict = {}):
        # Required fields
        self.name = data.get("name", "")
        self.is_land = data.get("is_land", False)
        self.id = data.get("id", 0)

        # Optional fields with defaults
        self.description = data.get("description", "")
        self.color = data.get("color", "#000000")
        self.mission_weight = data.get("mission_weight", 10)
        self.base_cost = data.get("base_cost", 500)

        # Lists
        self.service_provided = data.get("service_provided", [])
        self.service_forbidden = data.get("service_forbidden", [])

class TFaction:
    """
    Owner of each mission, owns locations
    Faction may be ally or enemy of XCOM
    """

    def __init__(self, data : dict = {}):
        # Required fields
        self.name = data.get("name", "")
        self.description = data.get("description", "")
        self.id = data.get("id", 0)

        self.aggression = data.get("aggression", 0)
        self.pedia = data.get("pedia", '')

        self.tech_start = data.get("tech_start", [])
        self.tech_end = data.get("tech_end", [])

class TLocation:
    """
    Single location on world map, it could be a base, a city, a UFO crash site
    it may or may not be detected by xcom
    """
    def __init__(self, loc_id,  data : dict = {}):
        # Required fields
        self.loc_id = loc_id
        self.name = data.get("name", "")
        self.description = data.get("description", "")
        self.position = data.get("position", [])


class TCity(TLocation):
    """
    Represents a city on the world map as location
    It is a subclass of TLocation
    It may have a name, size, location, specific terrains
    """
    def __init__(self, loc_id, data : dict = {}):
        super().__init__(loc_id, data)

        self.city_size = data.get("city_size", 4)
        self.map_blocks = data.get("map_blocks", {} )

#----------------------------------------------
#   ENGINE
#----------------------------------------------

class TFunding:
    """
    Class to manage funding of XCOM based on score in each country and make monthly report
    This is from country perspective
    """
    pass

class TDiplomacy:
    """
    Class to manage diplomacy between XCOM and factions
    This is from faction perspective
    """
    pass

class TMod:
    """
    Represents a mod in game, it is a list of files and folders
    It is used to load data from files and folders
    It is used to manage all data in game
    It is used to manage all events in game
    """
    pass

class TModLoader:
    """
    Class to load mod from files and folders
    """
    pass

class TGame:
    """
    Main game class, holds all data
    It is a singleton
    """
    pass

class TDifficulty:
    """
    Controls game difficulty settings
    Adjusts AI behavior, alien research progress, funding, and other parameters
    """
    pass

class TAnimation:
    """
    Manages visual animations in both tactical and strategic views
    Controls unit movements, weapon effects, explosions, etc.
    """
    pass

class TSoundManager:
    """
    Manages all game sounds and music
    Handles ambient sounds, battle effects, and UI feedback
    """
    pass

class TSaveGame:
    """
    Handles saving and loading game state
    Manages serialization of all game objects and state
    """
    pass

class TStatistics:
    """
    Tracks player performance metrics across the campaign
    Records kills, mission success rates, and other achievements
    Provides data for end-game scoring and monthly reports
    """
    pass

#----------------------------------------------
#   LORE
#----------------------------------------------

class TEvent:
    """
    Represents a event in game, that may give / take something to player
    Event may trigger a mission
    """
    def __init__(self, event_id, data):
        self.id = event_id
        self.name = data.get('name', event_id)
        self.description = data.get('description', '')
        self.image = data.get('image', '')

        # Preconditions
        self.tech_needed = data.get('tech_needed', [])
        self.regions = data.get('regions', [])
        self.is_city = data.get('is_city', False)

        # Timing
        self.month_start = data.get('month_start', 0)
        self.month_random = data.get('month_random', 0)
        self.month_end = data.get('month_end', 9999)

        # Occurrence limits
        self.qty_max = data.get('qty_max', 1)
        self.chance = data.get('chance', 1.0)

        # Effects added
        self.score = data.get('score', 0)
        self.funds = data.get('funds', 0)

        # Items and units added
        self.items = data.get('items', [])
        self.units = data.get('units', [])
        self.crafts = data.get('crafts', [])
        self.facilities = data.get('facilities', [])

        # Missions created
        self.ufos = data.get('ufos', [])
        self.sites = data.get('sites', [])
        self.bases = data.get('bases', [])


class TEventEngine:
    """
    Class to manage events in game
    Events are not managed by calendar, they are random
    """
    pass

class TCalendar:
    """
    Represents a calendar in game, it is used to manage campaigns
    Every month new campaign for specific faction is created in specific region
    manage all date related methods
    manage all events
    """
    def __init__(self, data=None):

        # Campaign and arc entries
        self.campaign_months = {}

        for month_key, month_info in data.items():
            if not isinstance(month_info, dict):
                continue

            # Parse month number from key (e.g., "m03" -> 3)
            try:
                month_num = int(month_key[1:])
                entry = TCampaignMonth(month_num, month_info)
                self.campaign_months[month_num] = entry
            except (ValueError, IndexError):
                # Skip invalid month keys
                continue

        complete_months = {}
        last_month_data = None
        for i in range(120):  # Fill up to month 120 = 10 years of gameplay
            if i in self.campaign_months:
                # If this month has data, use it
                complete_months[i] = self.campaign_months[i]
                last_month_data = self.campaign_months[i]
            else:
                complete_months[i] = last_month_data

        # Replace the sparse months with the complete set
        self.campaign_months = complete_months

class TCampaign:
    """
    Single campaign is set of missions for specific faction in specific region
    It is created by calendar
    It has a start date, end date, and list of missions, limited by research status
    It has a goal to achieve, when alien will score points
    """

    OBJECTIVE_SCOUT = 0             # scout, find bases, crafts, cities
    OBJECTIVE_INFILTRATE = 1        # impact country
    OBJECTIVE_BASE = 2              # create alien base
    OBJECTIVE_TERROR = 3            # terror city
    OBJECTIVE_RETALIATION = 4       # attack xcom base
    OBJECTIVE_RESEARCH = 5          # improve technology
    OBJECTIVE_DESTRUCTION = 6       # destroy city
    OBJECTIVE_SUPPLY = 7            # supply existing base
    OBJECTIVE_HUNT = 8              # hunt xcom crafts

    def __init__(self, campaign_id, data):
        self.id = campaign_id
        self.score = data.get('score', 0)
        self.objective = data.get('objective', 0)
        self.faction = data.get('faction', '')

        # Technology requirements
        self.tech_start = data.get('tech_start', [])
        self.tech_end = data.get('tech_end', [])

        # Region weights
        self.regions = {}
        if 'regions' in data and isinstance(data['regions'], dict):
            self.regions = data['regions']

        # Missions list
        self.missions = []
        if 'missions' in data and isinstance(data['missions'], list):
            for mission_data in data['missions']:
                self.missions.append(TMission(mission_data))


class TCampaignMonth:
    """
    Represents mission generation rules for a specific game month
    """

    def __init__(self, month, data):
        self.month = month

        # Mission generation limits
        self.qty_min = data.get('qty_min', 0)
        self.qty_max = data.get('qty_max', 0)

        # total number of events in this month
        self.events = data.get('events', 0)

        # Arc weights for random selection
        self.weights = {}
        if 'weights' in data and isinstance(data['weights'], dict):
            self.weights = data['weights']

class TMission:
    """
    Mission is created by campaign
    it is a physical location on world map
        - it's flying ufo (temporary and moving) and must be first intercepted
        - it's new alien base (static and permanent), usually 2 level mission, grounded
        - it's a static site (temporary and static), 1 level mission, grounded
    manage points when mission is failed / succeeded
    """

    def __init__(self, data):

        # what will be created by this mission
        self.ufo = data.get('ufo', None)
        self.site = data.get('site', None)
        self.base = data.get('ufo', None)

        # how many and what is delay before next mission
        self.count = data.get('count', 1)
        self.chance = data.get('chance', 1)
        self.timer = data.get('timer', 0)

        self.tech_needed = data.get('tech_needed', [])
        self.tech_forbidden = data.get('tech_forbidden', [])

        # Handle deployment options if available
        self.deployments = data.get('deployments', {})

class TQuest:
    """
    Represents a quest in game, which is basically a FLAG
    This is used to manage progress in game instead of using research (optional)
    This is usually used to manage progress in game in %
    """
    pass

class TQuestEngine:
    """
    Method to manage quests in game
    """
    pass

#----------------------------------------------
#   UFO
#----------------------------------------------

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

        self.map_blocks = data.get('map_blocks', {})

class TUfoType:
    """
    Represents a type of UFO with basic stats
    """

    def __init__(self, ufo_id, data):

        self.pedia = data.get('pedia', '')
        self.vessel = data.get('vessel', '')        # image during dogfight
        self.marker = data.get('marker', 'alien')   # image on geoscape

        # Basic stats
        self.size = data.get('size', 1)
        self.health = data.get('health', 50)
        self.speed = data.get('speed', 0)
        self.shield = data.get('shield', 0)
        self.shield_regen = data.get('shield_regen', 0)

        # Combat capabilities
        self.damage = data.get('damage', 0)
        self.rate = data.get('rate', 0)
        self.range = data.get('range', 0)
        self.accuracy = data.get('accuracy', 0.0)
        self.fire_sound = data.get('fire_sound', '')

        # Radar properties
        self.radar_range = data.get('radar_range', 0)
        self.radar_power = data.get('radar_power', 0)
        self.radar_cover = data.get('radar_cover', 0)
        self.radar_cover_change = data.get('radar_cover_change', 0)

        # Hunter capabilities
        self.is_hunter = data.get('is_hunter', False)
        self.hunt_bravery = data.get('hunt_bravery', 0.0)
        self.bombard_power = data.get('bombard_power', 0)

        # Scoring
        self.score_complete = data.get('score_complete', 0)
        self.score_destroy = data.get('score_destroy', 0)
        self.score_avoid = data.get('score_avoid', 0)
        self.score_damage = data.get('score_damage', 0)

        # Map generation
        self.map_block = data.get('map_block', '')
        self.map_width = data.get('map_width', 0)
        self.map_height = data.get('map_height', 0)
        self.force_terrain = data.get('force_terrain', [])

        # Deployments (alien units that can appear in this UFO)
        self.deployments = data.get('deployments', {})

class TUfo(TLocation):
    """
    Represents a UFO on the world map as location
    Its temporary, but has assigned a ufo script to manage its movement
    It has deployment to control what units are during battle
    ufo must be first shot down by interception
    """
    def __init__(self, ufo_id, data):
        super().__init__(data)

        self.map_block = data.get('map_block', None)

class TUfoScript:
    """
    Represents a trajectory of UFO
    Used to calculate move path of UFO and how it score points, even when not moving
        alien base has different logic and not need script
        sites are just waiting to be picked up
    """
    def __init__(self, script_id, data):
        self.id = script_id
        self.name = data.get('name', script_id)
        self.description = data.get('desc', '')

        # Steps in the trajectory, with their duration
        self.steps = data.get('steps', {})

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



#----------------------------------------------
#   CRAFTS
#----------------------------------------------

class TCraftType:
    """
    Represents a type of craft used by XCOM with basic stats
    """
    def __init__(self, craft_id, data):
        self.id = craft_id
        self.name = data.get('name', craft_id)
        self.description = data.get('description', '')
        self.pedia = data.get('pedia', '')
        self.map_block = data.get('map_block', '')

        # Purchase and maintenance
        self.purchase_tech = data.get('purchase_tech', None)
        self.sell_cost = data.get('sell_cost', 0)
        self.upkeep_cost = data.get('upkeep_cost', 0)
        self.score_lost = data.get('score_lost', 0)

        # Craft capabilities
        self.can_land = data.get('can_land', False)
        self.is_underwater = data.get('is_underwater', False)
        self.is_spaceship = data.get('is_spaceship', False)
        self.is_underground = data.get('is_underground', False)
        self.pilots = data.get('pilots', 1)

        # Combat stats
        self.shield = data.get('shield', 0)
        self.shield_regen = data.get('shield_regen', 0)
        self.health = data.get('health', 0)
        self.range = data.get('range', 0)                   # size of fuel tank
        self.speed = data.get('speed', 0)                   # number of tiles per turn
        self.acceleration = data.get('acceleration', 0)     # speed during dogfight

        # Combat bonuses
        self.hit_bonus = data.get('hit_bonus', 0)
        self.avoid_bonus = data.get('avoid_bonus', 0)
        self.damage_bonus = data.get('damage_bonus', 0)

        # Fuel system
        self.fuel_use = data.get('fuel_burn', 1)            # much fuel is used per tile of move
        self.fuel_cost = data.get('fuel_cost', 0)           # refuel per unit of fuel, part of monthly invoice
        self.fuel_item = data.get('fuel_item', 0)           # item used to refuel instead of cost

        # Maintenance rates
        self.repair_cost = data.get('repair_cost', 1)       # per 1 HP, as part of monthly invoice
        self.repair_item = data.get('rate_rearm', {})       # items used to repair instead of cost

        # Cargo capacity
        self.items = data.get('items', [0, 0] )
        self.units = data.get('units', 0)
        self.large_units = data.get('large_units', 0)       # unitx 2x2

        # Sensor capabilities
        self.radar_range = data.get('radar_range', 0)
        self.radar_power = data.get('radar_power', 0)
        self.stealth = data.get('stealth', 0)

class TCraft(TLocation):
    """
    Represents a craft on the world map as location, it can move and attack
    """

class TCraftItem:
    """
    Represents a item used by craft by XCOM, with specific item type but current usage
    """
    pass

class TInterception:
    """
    Handles the interception combat mechanics
    Manages dogfighting between XCOM craft and UFOs
    Calculates hit chances, damage, and evasion
    """
    pass

#----------------------------------------------
#   BATTLE SCAPE
#----------------------------------------------

class TTerrain:
    """
    Represents a terrain type, it is used to generate map for battle
    Each terrain may be linked with BIOME or be separated
    Terrain has list of map blocks and map script used to generate battle map
    """
    def __init__(self, terrain_id, data):
        self.id = terrain_id
        self.name = data.get('name', terrain_id)
        self.description = data.get('description', '')
        self.tileset = data.get('tileset', '')
        self.script = data.get('script', None)
        self.units_civilian = data.get('units_civilian', [])
        self.map_blocks = []  # Will be filled later

        # Process map blocks (these are at the top level in array format)
        map_blocks = []
        for map_block in data.get('map_blocks', []):
            if map_block:
                map_blocks.append(TMapBlockEntry(map_block))

        self.map_blocks = map_blocks

class TMapBlockEntry:
    """
    represents how map blocks are managed inside terrain
    """
    def __init__(self, data):
        self.name = data.get('name', '')
        self.size = data.get('size', 1)
        self.group = data.get('group', 0)
        self.chance = data.get('chance', 1)
        self.items = data.get('items', {})
        self.units = data.get('units', {})
        self.show = data.get('show', False)

class TBattle:
    """
    Represents a battle, it is created by mission
    It holds all units, map tiles, items etc
    """
    pass

class TBattleEffect:
    """
    special effect that is used on battle map for all tiles / units e.g. smoke, fire, panic, sanity etc
    """

class TBattleFOW:
    """
    Manage visibility (fog of war) of units and tiles on battle map for all sides
    """

class TBattleSide:
    """
    Represents a side in battle, it can be XCOM or Alien or Neutral or Supporing XCOM
    """
    pass

class TDeployment:
    """
    Represents what would be inside a ufo or site or alien base
    """

    def __init__(self, deployment_id, data):
        self.id = deployment_id
        self.effect = data.get('effect', None)
        self.civilians = data.get('civilians', 0)

        # Process unit groups
        self.units = []
        if 'units' in data and isinstance(data['units'], list):
            for unit_group in data['units']:
                self.units.append(TDeploymentGroup(unit_group))

class TDeploymentGroup:
    """
    Represents a group of similar units in a deployment
    """

    def __init__(self, data):
        self.qty_low = data.get('qty_low', 0)
        self.qty_high = data.get('qty_high', 0)
        self.units = set()

        # Units can be specified as a set or an array
        units_data = data.get('units', set())
        if isinstance(units_data, dict):  # Handle TOML inline tables used for sets
            self.units = set(units_data.keys())
        elif isinstance(units_data, list):
            self.units = set(units_data)

        # Positioning info
        self.outside_ufo = data.get('outside_ufo', 0.0)
        self.inside_ufo = data.get('inside_ufo', 1.0 - self.outside_ufo)
        self.leader = data.get('leader', False)

        # Other specifications
        self.patrol = data.get('patrol', False)
        self.guard = data.get('guard', False)

class TMapBlock:
    """
    Represents a block of map, which is 2D array of battle tiles
    It is used to generate map for battle
    """


class TBattleSize:
    """
    Represents a size of battle, it is used to generate map for battle
    It is used to calculate number of tiles in map block
    """
    pass

class TBattleScript:
    """
    Represents a script for map block,
    it is used to generate map for battle from map block in specific way
    """

    def __init__(self, script_id, data):
        self.id = script_id

        # Process steps
        self.steps = []
        if 'steps' in data and isinstance(data['steps'], list):
            for step_data in data['steps']:
                self.steps.append(TBattleScriptStep(step_data))


class TBattleScriptStep:
    """
    Represents a single step in a map generation script
    """

    def __init__(self, data):
        self.type = data.get('type', '')
        self.group = data.get('group', 0)
        self.label = data.get('label', None)
        self.condition = data.get('condition', [])
        self.chance = data.get('chance', 1.0)
        self.runs = data.get('runs', 1)
        self.size = data.get('size', 1)

        # Direction for line generation
        self.direction = data.get('direction', 'horizontal')

        # UFO type for UFO placement
        self.ufo = data.get('ufo', None)

class TBattleTile:
    """
    Represents a tile on battle map, it is 2D array of tiles
    It contains FLOOR, WALL, ITEM, UNIT
    """
    pass

class TBattleFloor:
    """
    Represents a floor on battle map, it is walkable
    """
    pass

class TBattleWall:
    """
    Represents a wall on battle map, it is not walkable
    It is draw on top of floor
    """
    pass

class TBattleObject:
    """
    Represents on objects that may exist on single tile
    It can be picked up, thrown, destroyed by units on battle field
    They are collected after battle to storage
    Its does not block movement
    """
    pass

class TBattleGenerator:
    """
    Represents a generator for battle based on terrain + map script
    """
    pass

class TBattleSalvage:
    """
    Manage what is done after battle is over and move back to GenoSpace
    """

#----------------------------------------------
#   BATTLE MECHANICS
#----------------------------------------------

class TPathfinding:
    """
    Handles pathfinding for units on the battle map
    Implements algorithms like A* for efficient movement calculations
    Accounts for terrain, obstacles, and unit capabilities
    """
    pass

class TDamageModel:
    """
    Handles damage calculation for weapons, explosions, and other sources
    Implements armor penetration, critical hits, and damage types
    Manages damage distribution to different body parts
    """
    pass

class TLineOfSight:
    """
    Handles visibility calculations in the battlescape
    Implements field of view calculations for units
    Manages what tiles and enemies are visible to each unit
    """
    pass

class TReactionFire:
    """
    Handles reaction fire mechanics
    """
    pass

class TBattleActions:
    """
    Handles unit actions during battle
        move
        crouch (stealth move)
        use item (fire)
        cover
        throw item
        overwatch
        suppression
        rest
    """
    pass

#----------------------------------------------
#   AI
#----------------------------------------------

class TAlienStrategy:
    """
    Controls the grand strategy of alien forces
    Decides which regions to target for terror missions and base establishment
    Adapts alien tactics based on player actions and game progression
    """
    pass

class TBattleAI:
    """
    Handles artificial intelligence for enemy units during battles
    Controls unit movement, target selection, and tactical decisions
    """
    pass

#----------------------------------------------
#   BASE SCAPE
#----------------------------------------------

class TBase(TLocation):
    """
    Represents a base on the world map as location (xcom or alien)
    """
    pass


class TBaseXCom(TBase):
    """
    Represents a XCOM base on the world map as location
    battle is generated based on facilities layout
    it has specific map script
    """
    pass

class TBaseXComBattleGenerator:
    """
    special class to create battle map for xcom base based on facilities
    """

class TBaseAlien(TBase):
    """
    Represents a Alien base on the world map as location
    battle is randomly generated, but there is a logic that allow to alien base to grow in time
    it has specific map script
    number of levels depends on size of alien base
    """
    pass

class TFacilityType:
    """
    Represents a facility type in base, with its stats
    facility has a map block assigned to it
    """
    pass

class TFacility:
    """
    Represents a facility in base, position, health etc
    """

    def __init__(self, data=None):
        """
        Initialize a facility type with configuration data from TOML

        Args:
            data (dict): Dictionary containing facility configuration
        """
        if data is None:
            data = {}

        # Basic properties
        self.name = data.get('name', '')
        self.description = data.get('description', '')
        self.build_time = data.get('build_time', 0)
        self.build_cost = data.get('build_cost', 0)
        self.build_items = data.get('build_items', {})
        self.upkeep_cost = data.get('upkeep_cost', 0)
        self.max_per_base = data.get('max_per_base', 1)

        # Map configuration
        self.map_block = data.get('map_block', '')

        # Requirements
        self.facility_needed = data.get('facility_needed', [])
        self.tech_needed = data.get('tech_needed', [])

        # Space allocations
        self.agent_space = data.get('agent_space', 0)
        self.alien_space = data.get('alien_space', 0)
        self.prison_space = data.get('prison_space', 0)
        self.storage_space = data.get('storage_space', 0)
        self.research_space = data.get('research_space', 0)
        self.workshop_space = data.get('workshop_space', 0)
        self.psi_space = data.get('psi_space', 0)
        self.craft_space = data.get('craft_space', 0)
        self.training_space = data.get('training_space', 0)
        self.hospital_space = data.get('hospital_space', 0)

        # Recovery rates
        self.sanity_recovery = data.get('sanity_recovery', 0)
        self.health_recovery = data.get('health_recovery', 0)

        # Defense capabilities
        self.defense_power = data.get('defense_power', 0)
        self.defense_hit = data.get('defense_hit', 0)
        self.defense_ammo = data.get('defense_ammo', 0)
        self.defense_sound_fire = data.get('defense_sound_fire', None)
        self.defense_sound_hit = data.get('defense_sound_hit', None)

        # Radar capabilities
        self.radar_power = data.get('radar_power', 0)
        self.radar_range = data.get('radar_range', 0)

        # Services
        self.service_provided = data.get('service_provided', [])
        self.service_required = data.get('service_required', [])

        # Special properties
        self.lift = data.get('lift', False)

class TFacilityService:
    """
    Represents a service in base, which is usually provided by facility
    It is used to do research, manufacture, build, etc
    This is same as check if base has a facility but streamlined
    """
    pass

#----------------------------------------------
#   RESEARCH
#----------------------------------------------

class TResearchTree:
    """
    Represents a research tree, it is a list of research entries
    """
    pass

class TResearchEntry:
    """
    Represents a research entry, it is a list of research tasks
    """

    def __init__(self, tech_id, data):
        self.id = tech_id
        self.name = data.get('name', tech_id)
        self.cost = data.get('cost', 0)
        self.score = data.get('score', 0)

        # Requirements
        self.tech_needed = data.get('tech_needed', [])
        self.items_needed = data.get('items_needed', {})
        self.services_needed = data.get('services_needed', [])

        # Results
        self.event_spawn = data.get('event_spawn', None)
        self.item_spawn = data.get('item_spawn', {})
        self.tech_disable = data.get('tech_disable', [])
        self.tech_give = data.get('tech_give', [])
        self.tech_unlock = data.get('tech_unlock', [])

        self.pedia = data.get('pedia', None)
        self.complete_game = data.get('complete_game', False)

#----------------------------------------------
#   MANUFACTURE
#----------------------------------------------

class TManufacture:
    """
    Represents a manufacturing projects, with list of manufacture entries
    """

    def __init__(self, data=None):
        # Dictionary to store all manufacturing entries
        self.entries = {}

        if data:
            self.load(data)

    def load(self, data):
        """
        Load manufacturing data from a dictionary (parsed from TOML)

        Args:
            data: Dictionary containing manufacturing data
        """
        if not data or 'manufacturing' not in data:
            return

        manufacturing_data = data['manufacturing']

        for project_id, project_info in manufacturing_data.items():
            # Skip the main manufacturing section if it's empty
            if not isinstance(project_info, dict):
                continue

            # Create a new manufacturing entry
            entry = TManufactureEntry(project_id, project_info)
            self.entries[project_id] = entry

    def get_entry(self, project_id):
        """
        Get a specific manufacturing entry

        Args:
            project_id: ID of the manufacturing project to retrieve

        Returns:
            TManufactureEntry object if found, None otherwise
        """
        return self.entries.get(project_id, None)

    def get_projects_by_category(self, category):
        """
        Get manufacturing projects filtered by a specific category

        Args:
            category: Type of manufacturing projects to filter by

        Returns:
            List of manufacturing entries matching the category
        """
        return [entry for entry in self.entries.values() if entry.category == category]

    def get_available_projects(self, available_technologies=None, available_services=None, available_items=None):
        """
        Get list of manufacturing projects that are available based on requirements

        Args:
            available_technologies: List of researched technologies
            available_services: List of services available in the base
            available_items: Dictionary of items in storage with quantities

        Returns:
            List of available manufacturing projects
        """
        if available_technologies is None:
            available_technologies = []
        if available_services is None:
            available_services = []
        if available_items is None:
            available_items = {}

        available = []

        for project_id, entry in self.entries.items():
            # Check if all required technologies are researched
            if not all(tech in available_technologies for tech in entry.technology):
                continue

            # Check if all required services are available
            if not all(service in available_services for service in entry.service_needed):
                continue

            # Check if all required items are available in sufficient quantity
            has_all_items = True
            for item, quantity in entry.items_needed.items():
                if item not in available_items or available_items[item] < quantity:
                    has_all_items = False
                    break

            if not has_all_items:
                continue

            available.append(entry)

        return available

class TManufactureEntry:
    """
    Represents a manufacturing entry, what can be manufactured
    """

    def __init__(self, project_id, data):
        self.id = project_id
        self.category = data.get('category', '')

        # cost
        self.build_time = data.get('build_time', 0)
        self.build_cost = data.get('build_cost', 0)
        self.give_score = data.get('give_score', 0)

        # Requirements
        self.tech_needed = data.get('tech_needed', [])
        self.items_needed = data.get('items_needed', {})
        self.services_needed = data.get('services_needed', [])
        self.region_needed = data.get('region_needed', [])
        self.country_needed = data.get('country_needed', [])

        # Results
        self.items_build = data.get('items_build', None)
        self.units_build = data.get('units_build', None)
        self.crafts_build = data.get('crafts_build', None)

#----------------------------------------------
#   MARKETPLACE
#----------------------------------------------

class TPurchase:
    """
    Represents a purchasable projects, with list of purchases entries
    if you buy something it will be created transfer object and then added to your base
        new unit
        new item
        new craft
        new craft item
    """
    pass

class TPurchaseEntry:
    """
    Represents a purchasable entry, what can be purchased
    """
    def __init__(self, project_id, data):
        self.id = project_id
        self.category = data.get('category', '')
        self.supplier = data.get('supplier', None)

        # cost
        self.purchase_cost = data.get('purchase_cost', 0)
        self.purchase_time = data.get('purchase_time', 0)

        # Requirements
        self.tech_needed = data.get('tech_needed', [])
        self.items_needed = data.get('items_needed', {})
        self.services_needed = data.get('services_needed', [])
        self.region_needed = data.get('region_needed', [])
        self.country_needed = data.get('country_needed', [])

        # Results
        self.items_buy = data.get('items_buy', None)
        self.units_buy = data.get('units_buy', None)
        self.crafts_buy = data.get('crafts_buy', None)

class TTransfer:
    """
    Represents a transfer of items between bases of when purchased
    """
    pass

#----------------------------------------------
#   SOLDIERS
#----------------------------------------------

class TRace:
    """
    Represents race = type of unit and its basic stats
    """

    def __init__(self, race_id, data):
        self.id = race_id
        self.name = data.get('name', race_id)
        self.description = data.get('description', '')
        self.icon = data.get('icon', '')
        self.size = data.get('size', 1.0)
        self.is_big = data.get('is_big', False)
        self.is_mechanical = data.get('is_mechanical', False)
        self.gain_experience = data.get('gain_experience', True)

        self.sound_death = data.get('sound_death', None)
        self.corpse_image = data.get('corpse_image', None)

        # Stats
        self.speed = data.get('speed', 0)
        self.health = data.get('health', 0)
        self.health_regen = data.get('health_regen', 0)
        self.energy = data.get('energy', 0)
        self.strength = data.get('strength', 0)
        self.reaction = data.get('reaction', 0)
        self.melee = data.get('melee', 0)
        self.aim = data.get('aim', 0)
        self.psi = data.get('psi', 0)
        self.will = data.get('will', 0)
        self.sanity = data.get('sanity', 0)
        self.sight = data.get('sight', [0, 0])
        self.sense = data.get('sense', [0, 0])
        self.cover = data.get('cover', [0, 0])

        # AI behavior
        self.aggression = data.get('aggression', 0.0)
        self.intelligence = data.get('intelligence', 0.0)

        # Abilities and immunities
        self.immune_panic = data.get('immune_panic', False)
        self.immune_pain = data.get('immune_pain', False)
        self.immune_bleed = data.get('immune_bleed', False)
        self.can_run = data.get('can_run', True)
        self.can_kneel = data.get('can_kneel', True)
        self.can_sneak = data.get('can_sneak', True)
        self.can_surrender = data.get('can_surrender', False)
        self.can_capture = data.get('can_capture', False)
        self.spawn_on_death = data.get('spawn_on_death', None)
        self.avoids_fire = data.get('avoids_fire', False)

        # Combat roles
        self.spotter = data.get('spotter', 0)
        self.sniper = data.get('sniper', 0)

        # Purchase info
        self.sell_cost = data.get('sell_cost', 0)
        self.female_frequency = data.get('female_frequency', 0.0)
        self.level_max = data.get('level_max', 0)
        self.level_train = data.get('level_train', 0)
        self.level_start = data.get('level_start', 0)


class TSkill:

    """
    Represents a skill of unit, which adds some stats to unit
    This is virtual class, it is used to create other classes
    """

    # Class type constants
    TYPE_PROMOTION = 0     # XCOM soldier promotion
    TYPE_ENEMY = 1         # Enemy only class
    TYPE_CAREER = 2        # Random career path when soldier is hired
    TYPE_TRANSFORMATION = 3  # Soldier transformation during gameplay
    TYPE_MEDAL = 4         # Special awards/medals
    TYPE_WOUND = 5         # Permanent wounds from battle/events
    TYPE_AURA = 6          # Temporary effects on battle like auras

    def __init__(self, class_id, data):
        self.id = class_id
        self.name = data.get('name', class_id)
        self.icon = data.get('icon', '')
        self.description = data.get('description', '')
        self.type = data.get('type', 0)  # Default to promotion type

        # Stats modifications
        self.stats = data.get('stats', {})
        self.cost = data.get('cost', 0)

        # Requirements to get it
        self.races = data.get('races', [])
        self.min_level = data.get('min_level', 0)
        self.max_level = data.get('max_level', 99)
        self.services_needed = data.get('services_needed', [])
        self.tech_needed = data.get('tech_needed', [])

        # Transformation specific
        self.recovery_time = data.get('recovery_time', 0)       # days
        self.transfer_time = data.get('transfer_time', 0)       # days

        # battle specific
        self.battle_duration = data.get('battle_duration', 0)
        self.battle_effect = data.get('battle_effect', None)
        self.battle_chance_complete = data.get('battle_chance_complete', 0)
        self.battle_only = data.get('battle_only', False)

#----------------------------------------------
#   ITEMS
#----------------------------------------------

class TItemType:
    """
    Basic type of item used by soldiers
    """

    ITEM_GENERAL = 0
    ITEM_CRAFT_ITEM = 1
    ITEM_UNIT_ITEM = 2
    ITEM_UNIT_EQUIPMENT = 3
    ITEM_UNIT_ARMOUR = 4
    ITEM_UNIT_CAPTURE = 5

    def __init__(self, item_id, data):
        self.id = item_id
        self.name = data.get('name', item_id)
        self.category = data.get('category', '')
        self.description = data.get('description', '')

        # Basic stats
        self.weight = data.get('weight', 0)         # for soldier inventory
        self.size = data.get('size', 0)             # for base capacity

        self.pedia = data.get('pedia', '')
        self.sprite = data.get('sprite', '')
        self.sound = data.get('sound', '')

        # tech required to use it on battle field / interception
        self.tech_needed = data.get('tech_needed', [])

        # Combat stats
        self.unit_damage = data.get('unit_damage', 0)
        self.unit_damage_type = data.get('unit_damage_type', '')
        self.unit_accuracy = data.get('unit_accuracy', 0)
        self.unit_range = data.get('unit_range', 0)
        self.unit_ammo = data.get('unit_ammo', 0)
        self.unit_action_point = data.get('unit_action_point', 2)

        # Armor stats
        self.armour_defense = data.get('armour_defense', 0)
        self.armour_resistance = data.get('armour_resistance', {})
        self.armour_shield = data.get('armour_shield', 0)
        self.armour_shield_regen = data.get('armour_shield_regen', 0)

        self.armour_cover = data.get('armour_cover', [0, 0])
        self.armour_sight = data.get('armour_sight', [0, 0])
        self.armour_sense = data.get('armour_sense', [0, 0])

        # Combat stats for craft
        self.craft_damage = data.get('craft_damage', 0)
        self.craft_accuracy = data.get('craft_accuracy', 0.0)
        self.craft_range = data.get('craft_range', 0)
        self.craft_ammo = data.get('craft_ammo', 0)
        self.craft_size = data.get('craft_size', 1)     # small or large
        self.craft_action_point = data.get('craft_action_point', 0)

        # Manufacturing info
        self.manufacture_tech = data.get('manufacture_tech', [])

        # Purchase info
        self.purchase_tech = data.get('purchase_tech', [])
        self.sell_cost = data.get('sell_cost', 0)

        # Ammo/reload details after battle / when move to base
        self.reload_cost = data.get('reload_cost', 0)       # after battle, as monthly report
        self.reload_item = data.get('reload_item', None)    # after battle

        # Special properties
        self.effects = data.get('effects', {})
        self.bonus = data.get('bonus', {})
        self.requirements = data.get('requirements', {})

        self.is_underwater = data.get('is_underwater', False)

#----------------------------------------------
#  UNITS
#----------------------------------------------

class TUnitType:
    """
    Represents a type of unit with its stats
    This is a combination of RACE, SKILLS, and ITEMS
    """

    def __init__(self, unit_id, data):
        self.id = unit_id
        self.race = data.get('race', '')
        self.rank = data.get('rank', 0)
        self.skills = data.get('skills', [])

        # Handle equipment that can be either a string, list, or nan
        self.armour = data.get('armour', None)
        self.primary = data.get('primary', None)
        self.secondary = data.get('secondary', None)

        # Scoring and rewards
        self.score_dead = data.get('score_dead', 0)
        self.score_alive = data.get('score_alive', 0)
        self.items_dead = data.get('items_dead', [])
        self.items_alive = data.get('items_alive', [])

        # AI behavior
        self.ai_ignore = data.get('ai_ignore', False)
        self.vip = data.get('vip', False)

        # drop items on death
        self.drop_items = data.get('drop_items', False)
        self.drop_armour = data.get('drop_armour', False)

class TUnit:
    """
    Represents a unit in battle, with its current stats, position, health
    """
    pass

class TUnitStats:
    """
    Represents a unit stats, it is a list of stats
    """
    pass

#----------------------------------------------
#   PEDIA
#----------------------------------------------

class TPedia:
    """
    Represents entire ufo pedia
    """
    pass

class TPediaEntry:
    """
    represents a single entry in pedia
    """

    CRAFTS = 0
    CRAFT_WEAPONS = 1
    UNITS = 2
    ARMOURS = 3
    ITEMS = 4  # primary secondary items
    FACILITIES = 5

    RACES = 6  # all non alien race
    CLASSES = 7  # classes type 0 only
    CAREERS = 8  # classes type 2 only
    TRANSFORMATIONS = 8  # classes type 3 only
    MEDALS = 9  # classes type 4 only
    WOUNDS = 10  # classes type 5 only
    AURAS = 11  # classes type 6 only

    FACTIONS = 20   # all factions on all worlds
    COUNTRIES = 21  # all countries on all worlds
    REGIONS = 22    # all regions for all worlds
    WORLDS = 23     # earth, mars, moon
    BIOMES = 26     # available bioms on world

    DOSSIERS = 24  # all dossiers for all worlds
    XCOM = 25  # internal xcom communition

    ALIEN_BASES = 29  # alien base
    ALIEN_SITES = 29  # terror site, crash site
    ALIEN_UFO = 30  # small scout ufo
    ALIEN_RACES = 31  # autopsy sectoid
    ALIEN_UNITS = 32  # sectoid soldier corpse
    ALIEN_ITEMS = 33  # plasma weapons, grenades, alien weapons
    ALIEN_ARMOURS = 34  # sectoid armour, shields,
    ALIEN_CLASSES = 35  # medic, navigator, engineer, psionic, type 1 only
    ALIEN_MISSIONS = 36  # research, base supply
    ALIEN_ARTEFACTS = 37  # alien alloys, zrbite, power navigation

    def __init__(self, entry_id, data):
        self.id = entry_id
        self.type = data.get('type', 0)
        self.name = data.get('name', entry_id)
        self.section = data.get('section', '')
        self.description = data.get('description', '')
        self.image = data.get('image', '')
        self.tech_needed = data.get('tech_needed', [])
        self.order = data.get('order', 0)

        # additional fields that might be present in some entries
        self.related = data.get('related', [])
        self.stats = data.get('stats', {})

class TPediaEntryType:
    """
    Represents a single entry type in pedia
    """
    pass

#----------------------------------------------
#   GUI
#----------------------------------------------

class TGui:
    """
    Represents a GUI in game
    It is used to manage all windows, buttons, textboxes, etc
    It is used to manage all events in game
    """
    pass

class TGuiBase(TGui):
    """
    Represents a GUI for base to build new facilities
    """
    pass

class TGuiBarracks(TGui):
    """
    Represents a GUI for soldiers
    """
    pass

class TGuiHangar(TGui):
    """
    Represents a GUI for crafts
    """
    pass

class TGuiLab(TGui):
    """
    Represents a GUI for science
    """
    pass

class TGuiWorkshop(TGui):
    """
    Represents a GUI for manufacturing
    """
    pass

class TGuiInventory(TGui):
    """
    Represents a GUI for soldier inventory during battle
    """
    pass

class TGuiMissionBrief(TGui):
    """
    Represents a GUI for staring mission
    """
    pass

class TGuiMissionEnd(TGui):
    """
    Represents a GUI for ending mission
    """
    pass

class TGuiMarket(TGui):
    """
    Represents a GUI for purchase
    """
    pass

class TGuiTransfer(TGui):
    """
    Represents a GUI for transfer between bases
    """
    pass

class TGuiStorage(TGui):
    """
    Represents a GUI for stage in base
    """
    pass

class TGuiDodgeFight(TGui):
    """
    Represents a GUI for dodge fight interception vs UFO or base defense with craft
    """
    pass

class TGuiBaseInfo(TGui):
    """
    Represents a GUI for summary of base activities
    """
    pass

class TGuiPedia(TGui):
    """
    Represents a GUI for pedia
    """
    pass

class TGuiBudget(TGui):
    """
    Represents a GUI for finansial summary
    """
    pass

class TGuiFunding(TGui):
    """
    Represents a GUI for score and xcom funding
    """
    pass

class TGuiReports(TGui):
    """
    Represents a GUI for Visual reports of XCOM
    """
    pass

class TGuiIntercept(TGui):
    """
    Represents a GUI for sending craft to mission
    """
    pass

class TGuiLocationTracker(TGui):
    """
    Represents a GUI for track all locatoin on geo map
    """
    pass

class TGuiOptions:
    """
    Interface for game settings and configuration options
    """
    pass