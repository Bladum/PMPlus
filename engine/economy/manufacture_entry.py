
class TManufactureEntry:
    """
    Represents a manufacturing entry, what can be manufactured
    """

    def __init__(self, project_id, data):
        self.id = project_id
        self.category = data.get('category', '')

        # cost
        self.build_time = data.get('build_time', 0)
        self.build_cost = data.get('build_cost', 0)
        self.give_score = data.get('give_score', 0)

        # Requirements
        self.tech_start = data.get('tech_start', [])
        self.items_needed = data.get('items_needed', {})
        self.services_needed = data.get('services_needed', [])
        self.region_needed = data.get('region_needed', [])
        self.country_needed = data.get('country_needed', [])

        # Results
        self.items_build = data.get('items_build', None)
        self.units_build = data.get('units_build', None)
        self.crafts_build = data.get('crafts_build', None)