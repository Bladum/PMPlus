"""
TSiteType: Represents a type of Site (static mission location) with all its parameters and stats.
Purpose: Defines characteristics for mission locations, tactical map generation, and enemy deployments.
Last update: 2025-06-10
"""

class TSiteType:
    """
    Represents a type of Site (static mission location) with all its parameters and stats.

    Attributes:
        pid (str): Unique identifier for the site type.
        name (str): Name of the site type.
        pedia (str): Encyclopedia entry or description.
        marker (str): Image marker for geoscape visualization.
        size (int): Size of the site type (default 1).
        map_blocks (dict): Tactical map block configuration.
        deployment (Any): Deployment information for enemy units.
    """
    def __init__(self, pid, data):
        """
        Initialize a TSiteType instance.
        Args:
            pid (str): Unique identifier for the site type.
            data (dict): Dictionary with site type attributes.
        """
        self.pid = pid
        self.name = data.get('name', pid)
        self.pedia = data.get('pedia', '')
        self.marker = data.get('marker', 'site')  # image on geoscape
        self.size = data.get('size', 1)
        self.map_blocks = data.get('map_blocks', {})
        self.deployment = data.get('deployment', None)
        # Add more fields as needed for site types
