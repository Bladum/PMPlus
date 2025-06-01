class TQuest:
    """
    Represents a quest in game, which is basically a FLAG.
    This is used to manage progress in game instead of using research (optional).
    This is usually used to manage progress in game in %.
    """
    def __init__(self, key, data):
        self.key = key
        self.name = data.get('name', '')
        self.description = data.get('description', '')
        self.pedia = data.get('pedia', '')
        self.value = data.get('value', 0)
        self.quests_needed = data.get('quests_needed', [])
        self.tech_needed = data.get('tech_needed', [])
        self.completed = False

    def can_be_completed(self, completed_quests, completed_techs):
        return all(q in completed_quests for q in self.quests_needed) and \
               all(t in completed_techs for t in self.tech_needed)

    def complete(self):
        self.completed = True

    def __repr__(self):
        return f"<TQuest {self.key} ({'Done' if self.completed else 'Not Done'})>"

