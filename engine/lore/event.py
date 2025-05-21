
class TEvent:
    """
    Represents a event in game, that may give / take something to player
    Event may trigger a mission
    """
    def __init__(self, event_id, data):
        self.id = event_id
        self.name = data.get('name', event_id)
        self.description = data.get('description', '')
        self.image = data.get('image', '')

        # Preconditions
        self.tech_needed = data.get('tech_needed', [])
        self.regions = data.get('regions', [])
        self.is_city = data.get('is_city', False)

        # Timing
        self.month_start = data.get('month_start', 0)
        self.month_random = data.get('month_random', 0)
        self.month_end = data.get('month_end', 9999)

        # Occurrence limits
        self.qty_max = data.get('qty_max', 1)
        self.chance = data.get('chance', 1.0)

        # Effects added
        self.score = data.get('score', 0)
        self.funds = data.get('funds', 0)

        # Items and units added
        self.items = data.get('items', [])
        self.units = data.get('units', [])
        self.crafts = data.get('crafts', [])
        self.facilities = data.get('facilities', [])

        # Missions created
        self.ufos = data.get('ufos', [])
        self.sites = data.get('sites', [])
        self.bases = data.get('bases', [])
