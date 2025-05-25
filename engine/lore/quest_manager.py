from .quest import TQuest
from .organization import TOrganization

class QuestManager:
    def __init__(self, quests_data, orgs_data, completed_techs=None):
        self.quests = {k: TQuest(k, **v) for k, v in quests_data.items()}
        self.organizations = {k: TOrganization(k, **v) for k, v in orgs_data.items()}
        self.completed_techs = set(completed_techs or [])
        self.completed_quests = set()
        self.update_quests()
        self.update_organizations()

    def update_quests(self):
        for quest in self.quests.values():
            if not quest.completed and quest.can_be_completed(self.completed_quests, self.completed_techs):
                quest.complete()
                self.completed_quests.add(quest.key)

    def update_organizations(self):
        for org in self.organizations.values():
            if not org.unlocked and org.can_be_unlocked(self.completed_quests, self.completed_techs):
                org.unlock()

    def get_progress(self):
        total_value = sum(q.value for q in self.quests.values())
        completed_value = sum(q.value for q in self.quests.values() if q.completed)
        return completed_value, total_value, (completed_value / total_value * 100) if total_value else 0

    def unlock_new_content(self):
        self.update_quests()
        self.update_organizations()

    def get_unlocked_organizations(self):
        return [org for org in self.organizations.values() if org.unlocked]

    def get_locked_organizations(self):
        return [org for org in self.organizations.values() if not org.unlocked]

    def __repr__(self):
        completed, total, percent = self.get_progress()
        return f"Quests: {len(self.completed_quests)}/{len(self.quests)} completed, Progress: {percent:.1f}%"

