class TResearchEntry:
    """
    Represents a research entry, it is a list of research tasks
    """

    def __init__(self, tech_id, data):
        self.id = tech_id
        self.name = data.get('name', tech_id)
        self.cost = data.get('cost', 0)
        self.score = data.get('score', 0)

        # Requirements
        self.tech_needed = data.get('tech_needed', [])
        self.items_needed = data.get('items_needed', {})
        self.services_needed = data.get('services_needed', [])

        # Results
        self.event_spawn = data.get('event_spawn', None)
        self.item_spawn = data.get('item_spawn', {})
        self.tech_disable = data.get('tech_disable', [])            # when researching this tech, disable these techs
        self.tech_give = data.get('tech_give', [])                  # when researching this tech, give these techs
        self.tech_unlock = data.get('tech_unlock', [])              # when researching this tech, unlock these techs

        self.pedia = data.get('pedia', None)
        self.complete_game = data.get('complete_game', False)