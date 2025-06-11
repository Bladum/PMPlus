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

