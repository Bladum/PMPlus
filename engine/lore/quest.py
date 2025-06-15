"""
quest.py

Defines the TQuest class, representing a quest or flag for tracking game progress, unlocks, and dependencies. Used to manage progress and unlock new content in the game.

Classes:
    TQuest: Quest/flag definition for game progress tracking.

Last standardized: 2025-06-14
"""

class TQuest:
    """
    TQuest represents a quest or flag for tracking game progress.
    This is used to manage progress in game instead of using research (optional).
    Usually used to manage progress in game in %.

    Attributes:
        key (str): Quest key.
        name (str): Quest name.
        description (str): Description of the quest.
        pedia (str): Encyclopedia entry.
        value (int): Value/weight of the quest for progress.
        quests_needed (list): Quests required to complete this quest.
        tech_needed (list): Technologies required to complete this quest.
        completed (bool): Whether the quest is completed.
    """
    def __init__(self, key, data):
        """
        Initialize a quest.

        Args:
            key (str): Quest key.
            data (dict): Quest data and parameters.
        """
        self.key = key
        self.name = data.get('name', '')
        self.description = data.get('description', '')
        self.pedia = data.get('pedia', '')
        self.value = data.get('value', 0)
        self.quests_needed = data.get('quests_needed', [])
        self.tech_needed = data.get('tech_needed', [])
        self.completed = False

    def can_be_completed(self, completed_quests, completed_techs):
        """
        Check if the quest can be completed based on completed quests and technologies.

        Args:
            completed_quests (set): Set of completed quest keys.
            completed_techs (set): Set of completed technology keys.
        Returns:
            bool: True if quest can be completed, False otherwise.
        """
        return all(q in completed_quests for q in self.quests_needed) and \
               all(t in completed_techs for t in self.tech_needed)

    def complete(self):
        """
        Mark the quest as completed.
        """
        self.completed = True

    def __repr__(self):
        """
        String representation of the quest.
        Returns:
            str: Representation string.
        """
        return f"<TQuest {self.key} ({'Done' if self.completed else 'Not Done'})>"
