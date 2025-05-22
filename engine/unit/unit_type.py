
class TUnitType:
    """
    Represents a type of unit with its stats
    This is a combination of RACE, SKILLS, and ITEMS
    """

    def __init__(self, pid, data):
        self.pid = pid

        self.name = data.get('name', '')
        self.race = data.get('race', '')
        self.rank = data.get('rank', 0)
        self.skills = data.get('skills', [])

        # Handle equipment that can be either a string, list, or nan
        self.armour = data.get('armour', None)
        self.primary = data.get('primary', None)
        self.secondary = data.get('secondary', None)

        # Scoring and rewards
        self.score_dead = data.get('score_dead', 0)
        self.score_alive = data.get('score_alive', 0)
        self.items_dead = data.get('items_dead', [])
        self.items_alive = data.get('items_alive', [])

        # AI behavior
        self.ai_ignore = data.get('ai_ignore', False)
        self.vip = data.get('vip', False)

        # drop items on death
        self.drop_items = data.get('drop_items', False)
        self.drop_armour = data.get('drop_armour', False)