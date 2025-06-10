"""
TResearchEntry: Represents a single research entry.
Purpose: Stores all data and requirements for a research project.
Last update: 2025-06-10
"""

class TResearchEntry:
    '''
    Represents a research entry (project) that can be researched.
    Attributes:
        pid (str): Research entry ID.
        name (str): Name of the research.
        cost (int): Research cost.
        score (int): Score given on completion.
        tech_needed (list): Technologies required to research.
        items_needed (dict): Items required to research.
        services_needed (list): Services required to research.
        event_spawn (any): Event triggered on completion.
        item_spawn (dict): Items spawned on completion.
        tech_disable (list): Techs disabled on completion.
        tech_give (list): Techs given on completion.
        tech_unlock (list): Techs unlocked on completion.
        pedia (any): Pedia entry for research.
        complete_game (bool): If true, completes the game.
    '''
    def __init__(self, pid, data=None):
        '''
        Initialize a research entry.
        Args:
            pid (str): Research entry ID.
            data (dict, optional): Data for the entry.
        '''
        data = data or {}
        self.pid = pid
        self.name = data.get('name', '')
        self.cost = data.get('cost', 0)
        self.score = data.get('score', 0)
        self.tech_needed = data.get('tech_needed', [])
        self.items_needed = data.get('items_needed', {})
        self.services_needed = data.get('services_needed', [])
        self.event_spawn = data.get('event_spawn', None)
        self.item_spawn = data.get('item_spawn', {})
        self.tech_disable = data.get('tech_disable', [])
        self.tech_give = data.get('tech_give', [])
        self.tech_unlock = data.get('tech_unlock', [])
        self.pedia = data.get('pedia', None)
        self.complete_game = data.get('complete_game', False)