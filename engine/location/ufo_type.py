"""
TUfoType: Defines the specifications and capabilities of a specific UFO class.
Purpose: Represents alien craft stats, combat, detection, and deployment for world and tactical gameplay.
Last update: 2025-06-10
"""

class TUfoType:
    """
    Represents the specifications and capabilities of a specific UFO class.

    Attributes:
        pid (str): Unique identifier for the UFO type.
        name (str): Name of the UFO type.
        pedia (str): Encyclopedia entry or description.
        vessel (str): Image during dogfight.
        marker (str): Image marker for geoscape visualization.
        size (int): Size of the UFO (default 1).
        health (int): Maximum health.
        speed (int): Maximum speed.
        shield (int): Shield value.
        shield_regen (int): Shield regeneration per turn.
        damage (int): Weapon damage.
        rate (int): Weapon fire rate.
        range (int): Weapon range.
        accuracy (float): Weapon accuracy.
        fire_sound (str): Sound played when firing.
        radar_range (int): Radar detection range.
        radar_power (int): Radar detection power.
        radar_cover (int): Radar cover value.
        radar_cover_change (int): Radar cover change per turn.
        is_hunter (bool): Whether the UFO hunts player craft.
        hunt_bravery (float): Aggressiveness in hunting.
        bombard_power (int): Bombardment power.
        score_complete (int): Score for completing mission.
        score_destroy (int): Score for destroying UFO.
        score_avoid (int): Score for avoiding UFO.
        score_damage (int): Score for damaging UFO.
        score_turn (int): Score per turn.
        map_block (str): Map block for tactical battle.
        map_width (int): Map width for tactical battle.
        map_height (int): Map height for tactical battle.
        force_terrain (list): Forced terrain types.
        deployments (dict): Alien units that can appear in this UFO.
    """
    def __init__(self, pid, data):
        """
        Initialize a TUfoType instance.
        Args:
            pid (str): Unique identifier for the UFO type.
            data (dict): Dictionary with UFO type attributes.
        """
        self.pid = pid
        self.name = data.get('name', pid)
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
        self.score_turn = data.get('score_turn', 0)
        # Map generation
        self.map_block = data.get('map_block', '')
        self.map_width = data.get('map_width', 0)
        self.map_height = data.get('map_height', 0)
        self.force_terrain = data.get('force_terrain', [])
        # Deployments (alien units that can appear in this UFO)
        self.deployments = data.get('deployments', {})
