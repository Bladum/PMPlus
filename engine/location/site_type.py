"""
Represents a type of Site (static mission location) with all its parameters and stats.

Site types define the characteristics of mission locations that appear on the world map.
They determine how the tactical battle map will be generated, what enemies will be present,
and what visual indicators will be shown on the geoscape.

Relationships:
- Used by TSite instances to determine their appearance and behavior
- References map_blocks for tactical battle generation
- References deployment information for enemy unit generation
- Linked to TMod where all site types are registered
- Used in mission generation and geoscape visualization
"""

class TSiteType:

    def __init__(self, pid, data):
        self.pid = pid
        self.name = data.get('name', pid)
        self.pedia = data.get('pedia', '')
        self.marker = data.get('marker', 'site')  # image on geoscape
        self.size = data.get('size', 1)
        self.map_blocks = data.get('map_blocks', {})
        self.deployment = data.get('deployment', None)
        # Add more fields as needed for site types

