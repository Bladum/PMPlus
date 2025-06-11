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

