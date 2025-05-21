class TFacilityType:
    """
    Represents a facility type in base, with its stats (blueprint loaded from TOML)
    """
    def __init__(self, data=None):
        if data is None:
            data = {}
        self.id = data.get('id', '')
        self.name = data.get('name', '')
        self.description = data.get('description', '')
        self.build_time = data.get('build_time', 0)
        self.build_cost = data.get('build_cost', 0)
        self.build_items = data.get('build_items', {})

        self.upkeep_cost = data.get('upkeep_cost', 0)
        self.max_per_base = data.get('max_per_base', 1)
        self.map_block = data.get('map_block', '')
        self.facility_needed = data.get('facility_needed', [])
        self.tech_start = data.get('tech_start', [])
        self.service_needed = data.get('service_needed', [])

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

        self.sanity_recovery = data.get('sanity_recovery', 0)
        self.health_recovery = data.get('health_recovery', 0)

        self.defense_power = data.get('defense_power', 0)
        self.defense_hit = data.get('defense_hit', 0)
        self.defense_ammo = data.get('defense_ammo', 0)
        self.defense_sound_fire = data.get('defense_sound_fire', None)
        self.defense_sound_hit = data.get('defense_sound_hit', None)

        self.radar_power = data.get('radar_power', 0)
        self.radar_range = data.get('radar_range', 0)

        self.service_provided = data.get('service_provided', [])
        self.service_required = data.get('service_required', [])

        self.lift = data.get('lift', False)