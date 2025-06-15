"""
XCOM Location Module: ufo_type.py

Defines the specifications and capabilities of a specific UFO class.

Classes:
    TUfoType: Represents alien craft stats, combat, detection, and deployment for world and tactical gameplay.

Last updated: 2025-06-14
"""

class TUfoType:
    """
    Represents the specifications and capabilities of a specific UFO class.
    """
    def __init__(self, pid, data):
        """
        Initialize a TUfoType instance.
        Args:
            pid (str): Unique identifier for the UFO type.
            data (dict): Dictionary with UFO type attributes.
        """
        self.pid = pid  # Unique identifier for the UFO type
        self.name = data.get('name', pid)  # Name of the UFO type
        self.pedia = data.get('pedia', '')  # Encyclopedia entry or description
        self.vessel = data.get('vessel', '')        # Image during dogfight
        self.marker = data.get('marker', 'alien')   # Image marker for geoscape visualization
        # Basic stats
        self.size = data.get('size', 1)  # Size of the UFO
        self.health = data.get('health', 50)  # Maximum health
        self.speed = data.get('speed', 0)  # Maximum speed
        self.shield = data.get('shield', 0)  # Shield value
        self.shield_regen = data.get('shield_regen', 0)  # Shield regeneration per turn
        # Combat capabilities
        self.damage = data.get('damage', 0)  # Weapon damage
        self.rate = data.get('rate', 0)  # Weapon fire rate
        self.range = data.get('range', 0)  # Weapon range
        self.accuracy = data.get('accuracy', 0.0)  # Weapon accuracy
        self.fire_sound = data.get('fire_sound', '')  # Sound played when firing
        # Radar properties
        self.radar_range = data.get('radar_range', 0)  # Radar detection range
        self.radar_power = data.get('radar_power', 0)  # Radar detection power
        self.radar_cover = data.get('radar_cover', 0)  # Radar cover value
        self.radar_cover_change = data.get('radar_cover_change', 0)  # Radar cover change per turn
        # Hunter capabilities
        self.is_hunter = data.get('is_hunter', False)  # Whether the UFO hunts player craft
        self.hunt_bravery = data.get('hunt_bravery', 0.0)  # Aggressiveness in hunting
        self.bombard_power = data.get('bombard_power', 0)  # Bombardment power
        # Scoring
        self.score_complete = data.get('score_complete', 0)  # Score for completing mission
        self.score_destroy = data.get('score_destroy', 0)  # Score for destroying UFO
        self.score_avoid = data.get('score_avoid', 0)  # Score for avoiding UFO
        self.score_damage = data.get('score_damage', 0)  # Score for damaging UFO
        self.score_turn = data.get('score_turn', 0)  # Score per turn
        # Map generation
        self.map_block = data.get('map_block', '')  # Map block for tactical battle
        self.map_width = data.get('map_width', 0)  # Map width for tactical battle
        self.map_height = data.get('map_height', 0)  # Map height for tactical battle
        self.force_terrain = data.get('force_terrain', [])  # Forced terrain types
        # Deployments (alien units that can appear in this UFO)
        self.deployments = data.get('deployments', {})
