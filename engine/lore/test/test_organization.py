"""
Test suite for TOrganization class.
Covers initialization, unlock logic, and __repr__.
"""
import pytest
from engine.lore.organization import TOrganization

def test_organization_init_and_unlock():
    data = {
        'name': 'XCOM',
        'description': 'Player org',
        'sprite': 'xcom.png',
        'pedia': 'XCOM Org',
        'quests': ['q1'],
        'quests_needed': ['q0'],
        'tech_needed': ['AlienTech']
    }
    org = TOrganization('org1', data)
    assert org.key == 'org1'
    assert org.name == 'XCOM'
    assert org.description == 'Player org'
    assert org.sprite == 'xcom.png'
    assert org.pedia == 'XCOM Org'
    assert org.quests == ['q1']
    assert org.quests_needed == ['q0']
    assert org.tech_needed == ['AlienTech']
    assert not org.unlocked
    # Unlock logic
    assert not org.can_be_unlocked([], [])
    assert org.can_be_unlocked(['q0'], ['AlienTech'])
    org.unlock()
    assert org.unlocked

def test_organization_repr():
    org = TOrganization('org2')
    s = repr(org)
    assert 'TOrganization' in s

def test_organization_init_defaults():
    """Test TOrganization initializes with default values."""
    org = TOrganization('ORG1')
    assert org.key == 'ORG1'
    assert org.name == ''
    assert org.description == ''
    assert org.sprite == ''
    assert org.pedia == ''
    assert org.quests == []
    assert org.quests_needed == []
    assert org.tech_needed == []
    assert org.unlocked is False


def test_organization_can_be_unlocked():
    """Test can_be_unlocked returns True only if all requirements are met."""
    org = TOrganization('ORG2', {'quests_needed': ['Q1', 'Q2'], 'tech_needed': ['T1']})
    assert not org.can_be_unlocked({'Q1'}, {'T1'})
    assert not org.can_be_unlocked({'Q1', 'Q2'}, set())
    assert org.can_be_unlocked({'Q1', 'Q2'}, {'T1'})

