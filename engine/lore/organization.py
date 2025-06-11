"""
TOrganization: Player organization level definition.
Purpose: Represents a player organization level, unlock requirements, and quest dependencies.
Last update: 2025-06-10
"""

class TOrganization:
    """
    TOrganization represents a player organization level.
    Each level has its own name, description, icon, pedia, and quests.
    Prerequisites (tech/quests) are required to unlock the next level.

    Attributes:
        key (str): Organization key.
        name (str): Organization name.
        description (str): Description of the organization level.
        sprite (str): Icon or sprite for the organization.
        pedia (str): Encyclopedia entry.
        quests (list): Quests associated with this level.
        quests_needed (list): Quests required to unlock this level.
        tech_needed (list): Technologies required to unlock this level.
        unlocked (bool): Whether the organization is unlocked.
    """
    def __init__(self, key, data=None):
        """
        Initialize an organization level.
        Args:
            key (str): Organization key.
            data (dict): Organization data and parameters.
        """
        data = data or {}
        self.key = key
        self.name = data.get('name', '')
        self.description = data.get('description', '')
        self.sprite = data.get('sprite', '')
        self.pedia = data.get('pedia', '')
        self.quests = data.get('quests', [])
        self.quests_needed = data.get('quests_needed', [])
        self.tech_needed = data.get('tech_needed', [])
        self.unlocked = False

    def can_be_unlocked(self, completed_quests, completed_techs):
        return all(q in completed_quests for q in self.quests_needed) and \
               all(t in completed_techs for t in self.tech_needed)

    def unlock(self):
        self.unlocked = True

    def __repr__(self):
        return f"<TOrganization {self.key} ({'Unlocked' if self.unlocked else 'Locked'})>"
