"""
Defines the specifications and capabilities of a specific UFO class.

UFO Types represent the various alien craft that can appear in the game, from small scouts
to large battleships. Each type has unique stats affecting its movement, combat capabilities,
detection properties, and the mission site it generates when landing or crashing.

Relationships:
- Referenced by TUfo instances to determine their appearance and capabilities
- Balanced against player's TCraftType vehicles for interception gameplay
- Contains deployment information for alien units appearing in the UFO
- Linked to tactical combat map generation when the UFO becomes a mission site
- Affects scoring calculations for player achievements
- Stored in TMod's ufo_types collection for global access
"""

class TUfoType:

    def __init__(self, pid, data):
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

