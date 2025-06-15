"""
XCOM Location Module: site_type.py

Represents a type of Site (static mission location) with all its parameters and stats.

Classes:
    TSiteType: Defines characteristics for mission locations, tactical map generation, and enemy deployments.

Last updated: 2025-06-14
"""

class TSiteType:
    """
    Represents a type of Site (static mission location) with all its parameters and stats.
    """
    def __init__(self, pid, data):
        """
        Initialize a TSiteType instance.
        Args:
            pid (str): Unique identifier for the site type.
            data (dict): Dictionary with site type attributes.
        """
        self.pid = pid  # Unique identifier for the site type
        self.name = data.get('name', pid)  # Name of the site type
        self.pedia = data.get('pedia', '')  # Encyclopedia entry or description
        self.marker = data.get('marker', 'site')  # Image marker for geoscape visualization
        self.size = data.get('size', 1)  # Size of the site type
        self.map_blocks = data.get('map_blocks', {})  # Tactical map block configuration
        self.deployment = data.get('deployment', None)  # Deployment information for enemy units
        # Add more fields as needed for site types
