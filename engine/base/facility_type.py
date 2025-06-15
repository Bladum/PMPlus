"""
facility_type.py

Defines the TFacilityType class, representing a facility type blueprint for XCOM bases. Holds all stats, requirements, and properties for a facility, loaded from TOML or YAML.

Classes:
    TFacilityType: Facility type blueprint for XCOM bases.

Last standardized: 2025-06-14
"""

class TFacilityType:
    """
    Represents a facility type in base, with its stats (blueprint loaded from TOML or YAML).
    Contains all properties, requirements, and stats for a facility type.

    Attributes:
        pid (str): Unique facility type ID.
        name (str): Facility name.
        lift (bool): Whether this is a lift/elevator.
        description (str): Description for UI.
        map_block (str): Map block ID for battle map generation.
        health (int): Facility HP for base defense.
        build_time (int): Days to build.
        build_cost (int): Money cost to build.
        build_items (dict): Items required to build.
        upkeep_cost (int): Monthly upkeep cost.
        max_per_base (int): Max allowed per base.
        facility_needed (list): Required facilities to build.
        tech_needed (list): Required techs to build.
        service_needed (list): Required services to build.
        unit_space, alien_space, prison_space, storage_space, research_space, workshop_space, psi_space, craft_space, training_space, hospital_space, repairs_space, relax_space (int): Various capacities provided.
        defense_power, defense_hit, defense_ammo (int): Base defense stats.
        defense_sound_fire, defense_sound_hit (str): Sound IDs for defense.
        radar_power, radar_range, radar_cover (int): Radar/detection stats.
        service_provided, service_required (list): Services provided/required.
    """
    def __init__(self, pid: str, data: dict = {}):
        """
        Initialize a facility type blueprint.

        Args:
            pid (str): Unique facility type ID.
            data (dict): Dictionary with facility properties (from TOML/YAML).
        """
        self.pid = pid

        self.name = data.get('name', '')
        self.lift = data.get('lift', False)
        self.description = data.get('description', '')
        self.map_block = data.get('map_block', '')
        self.health = data.get('health', 10)    # used during base defense, etc.

        # building and upkeep costs
        self.build_time = data.get('build_time', 0)
        self.build_cost = data.get('build_cost', 0)
        self.build_items = data.get('build_items', {})
        self.upkeep_cost = data.get('upkeep_cost', 0)

        # required tech to build this facility
        self.max_per_base = data.get('max_per_base', 0)
        self.facility_needed = data.get('facility_needed', [])
        self.tech_needed = data.get('tech_needed', [])
        self.service_needed = data.get('service_needed', [])

        # space and capacity
        self.unit_space = data.get('unit_space', 0)                 # space for units
        self.alien_space = data.get('alien_space', 0)               # space for prisoners special
        self.prison_space = data.get('prison_space', 0)             # space for prisoners standard
        self.storage_space = data.get('storage_space', 0)           # space for items
        self.research_space = data.get('research_space', 0)         # space for research
        self.workshop_space = data.get('workshop_space', 0)         # space for manufacturing
        self.psi_space = data.get('psi_space', 0)                   # psi lab capacity
        self.craft_space = data.get('craft_space', 0)               # space for crafts
        self.training_space = data.get('training_space', 0)         # give units / pilots experience
        self.hospital_space = data.get('hospital_space', 0)         # heal health of biological units
        self.repairs_space = data.get('repairs_space', 0)           # heal health of mechanical units
        self.relax_space = data.get('relax_space', 0)               # recover sanity

        # defense stats
        self.defense_power = data.get('defense_power', 0)
        self.defense_hit = data.get('defense_hit', 0)
        self.defense_ammo = data.get('defense_ammo', 0)
        self.defense_sound_fire = data.get('defense_sound_fire', None)
        self.defense_sound_hit = data.get('defense_sound_hit', None)

        # detection stats
        self.radar_power = data.get('radar_power', 0)           # allows to detect crafts
        self.radar_range = data.get('radar_range', 0)           # range of detection
        self.radar_cover = data.get('radar_cover', 0)           # cover from detection by enemy crafts

        # services
        self.service_provided = data.get('service_provided', [])
        self.service_required = data.get('service_required', [])
