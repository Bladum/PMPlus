class TOrganization:
    """
    Represents a player organization level.
    Each level has its own name, description, icon, pedia, and quests.
    Prerequisites (tech/quests) are required to unlock the next level.
    """
    def __init__(self, key, data=None):
        data = data or {}
        self.key = key
        self.name = data.get('name', '')
        self.description = data.get('description', '')
        self.icon = data.get('icon', '')
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
