class TSiteType:
    """
    Represents a type of Site (static mission location) with all its parameters and stats.
    """
    def __init__(self, pid, data):
        self.pid = pid
        self.name = data.get('name', pid)
        self.pedia = data.get('pedia', '')
        self.marker = data.get('marker', 'site')  # image on geoscape
        self.size = data.get('size', 1)
        self.map_blocks = data.get('map_blocks', {})
        self.deployment = data.get('deployment', None)
        # Add more fields as needed for site types

