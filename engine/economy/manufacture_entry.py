"""
TManufactureEntry: Represents a single manufacturing project entry.
Purpose: Stores all data and requirements for a manufacturing project.
Last update: 2025-06-10
"""

class TManufactureEntry:
    '''
    Represents a manufacturing entry (project) that can be manufactured.
    Attributes:
        pid (str): Project ID.
        name (str): Name of the project.
        category (str): Category of the project.
        build_time (int): Time required to build.
        build_cost (int): Cost to build.
        give_score (int): Score given on completion.
        tech_start (list): Technologies required to start.
        items_needed (dict): Items required to manufacture.
        services_needed (list): Services required to manufacture.
        region_needed (list): Required regions.
        country_needed (list): Required countries.
        items_build (any): Items produced.
        units_build (any): Units produced.
        crafts_build (any): Crafts produced.
    '''
    def __init__(self, pid, data=None):
        '''
        Initialize a manufacturing entry.
        Args:
            pid (str): Project ID.
            data (dict, optional): Data for the entry.
        '''
        data = data or {}
        self.pid = pid
        self.name = data.get('name', '')
        self.category = data.get('category', '')
        self.build_time = data.get('build_time', 0)
        self.build_cost = data.get('build_cost', 0)
        self.give_score = data.get('give_score', 0)
        self.tech_start = data.get('tech_start', [])
        self.items_needed = data.get('items_needed', {})
        self.services_needed = data.get('services_needed', [])
        self.region_needed = data.get('region_needed', [])
        self.country_needed = data.get('country_needed', [])
        self.items_build = data.get('items_build', None)
        self.units_build = data.get('units_build', None)
        self.crafts_build = data.get('crafts_build', None)