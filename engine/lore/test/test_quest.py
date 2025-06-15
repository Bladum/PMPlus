"""
Test suite for TQuest class.
Covers initialization, completion logic, and __repr__.
"""
import pytest
from engine.lore.quest import TQuest

def test_quest_init_and_complete():
    data = {
        'name': 'First Quest',
        'description': 'Do something',
        'pedia': 'Quest Pedia',
        'value': 10,
        'quests_needed': ['q0'],
        'tech_needed': ['AlienTech']
    }
    quest = TQuest('q1', data)
    assert quest.key == 'q1'
    assert quest.name == 'First Quest'
    assert quest.description == 'Do something'
    assert quest.pedia == 'Quest Pedia'
    assert quest.value == 10
    assert quest.quests_needed == ['q0']
    assert quest.tech_needed == ['AlienTech']
    assert not quest.completed
    # Completion logic
    assert not quest.can_be_completed([], [])
    assert quest.can_be_completed(['q0'], ['AlienTech'])
    quest.complete()
    assert quest.completed

def test_quest_repr():
    quest = TQuest('q2', {})
    s = repr(quest)
    assert 'TQuest' in s

def test_quest_init_defaults():
    """Test TQuest initializes with default values."""
    q = TQuest('Q1', {})
    assert q.key == 'Q1'
    assert q.name == ''
    assert q.description == ''
    assert q.pedia == ''
    assert q.value == 0
    assert q.quests_needed == []
    assert q.tech_needed == []
    assert q.completed is False


def test_quest_can_be_completed():
    """Test can_be_completed returns True only if all requirements are met."""
    q = TQuest('Q2', {'quests_needed': ['A', 'B'], 'tech_needed': ['T']})
    assert not q.can_be_completed({'A'}, {'T'})
    assert not q.can_be_completed({'A', 'B'}, set())
    assert q.can_be_completed({'A', 'B'}, {'T'})


def test_quest_complete():
    """Test complete() marks quest as completed."""
    q = TQuest('Q3', {})
    q.complete()
    assert q.completed is True

