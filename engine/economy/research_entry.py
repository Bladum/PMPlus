"""
engine/economy/research_entry.py

Defines the TResearchEntry class, which serves as a template for research projects, storing all data and requirements for a research project.

Classes:
    TResearchEntry: Represents a single research entry.

Last standardized: 2025-06-15
"""

class TResearchEntry:
    '''
    Represents a research entry (project) that can be researched.
    See module docstring for attribute details.
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