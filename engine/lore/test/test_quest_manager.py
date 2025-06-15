"""
Test suite for QuestManager class.
Covers initialization, quest/org progress, and edge cases.
"""
import pytest
from engine.lore.quest_manager import QuestManager
from unittest.mock import MagicMock

def make_quest_data():
    return {
        'q1': {'name': 'Q1', 'value': 10, 'quests_needed': [], 'tech_needed': []},
        'q2': {'name': 'Q2', 'value': 20, 'quests_needed': ['q1'], 'tech_needed': []},
    }

def make_org_data():
    return {
        'org1': {'name': 'Org1', 'quests_needed': ['q1'], 'tech_needed': []},
        'org2': {'name': 'Org2', 'quests_needed': ['q2'], 'tech_needed': []},
    }

def test_init_and_progress():
    qm = QuestManager(make_quest_data(), make_org_data())
    assert set(qm.quests.keys()) == {'q1', 'q2'}
    assert set(qm.organizations.keys()) == {'org1', 'org2'}
    # Only q1 can be completed at start
    assert 'q1' in qm.completed_quests
    assert 'q2' not in qm.completed_quests
    # Only org1 can be unlocked at start
    unlocked = [o.key for o in qm.get_unlocked_organizations()]
    assert 'org1' in unlocked
    assert 'org2' not in unlocked

def test_unlock_new_content():
    qm = QuestManager(make_quest_data(), make_org_data())
    # Simulate completing q2
    qm.completed_quests.add('q2')
    qm.unlock_new_content()
    unlocked = [o.key for o in qm.get_unlocked_organizations()]
    assert 'org2' in unlocked

def test_get_progress():
    qm = QuestManager(make_quest_data(), make_org_data())
    completed, total, percent = qm.get_progress()
    assert total == 30
    assert completed == 10  # Only q1 completed at start
    assert percent == pytest.approx(10/30*100)

def test_repr():
    qm = QuestManager(make_quest_data(), make_org_data())
    s = repr(qm)
    assert 'Quests:' in s and 'completed' in s

class DummyQuest:
    def __init__(self, key, **kwargs):
        self.key = key
        self.completed = False
        self.quests_needed = kwargs.get('quests_needed', [])
        self.tech_needed = kwargs.get('tech_needed', [])
    def can_be_completed(self, completed_quests, completed_techs):
        return all(q in completed_quests for q in self.quests_needed) and all(t in completed_techs for t in self.tech_needed)
    def complete(self):
        self.completed = True

class DummyOrg:
    def __init__(self, key, **kwargs):
        self.key = key
        self.unlocked = False
        self.quests_needed = kwargs.get('quests_needed', [])
        self.tech_needed = kwargs.get('tech_needed', [])
    def can_be_unlocked(self, completed_quests, completed_techs):
        return all(q in completed_quests for q in self.quests_needed) and all(t in completed_techs for t in self.tech_needed)
    def unlock(self):
        self.unlocked = True

def test_quest_manager_init_and_update(monkeypatch):
    """Test QuestManager initializes and updates quest/org progress."""
    quests_data = {'Q1': {}, 'Q2': {'quests_needed': ['Q1'], 'tech_needed': ['T1']}}
    orgs_data = {'O1': {'quests_needed': ['Q2'], 'tech_needed': ['T1']}}
    monkeypatch.setattr('engine.lore.quest_manager.TQuest', DummyQuest)
    monkeypatch.setattr('engine.lore.quest_manager.TOrganization', DummyOrg)
    qm = QuestManager(quests_data, orgs_data, completed_techs=['T1'])
    assert 'Q1' in qm.quests
    assert 'O1' in qm.organizations
    # After update, Q1 should be completed, Q2 should be completed, O1 unlocked
    assert qm.quests['Q1'].completed
    assert qm.quests['Q2'].completed
    assert qm.organizations['O1'].unlocked

