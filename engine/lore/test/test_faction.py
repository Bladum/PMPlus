"""
Test suite for TFaction class.
Covers initialization and attribute assignment.
"""
import pytest
from engine.lore.faction import TFaction

def test_faction_init_basic():
    data = {
        'name': 'Aliens',
        'description': 'Alien invaders',
        'id': 42,
        'aggression': 5,
        'pedia': 'Alien Faction',
        'sprite': 'alien.png',
        'tech_start': ['AlienTech'],
        'tech_end': ['EndTech']
    }
    f = TFaction('alien', data)
    assert f.pid == 'alien'
    assert f.name == 'Aliens'
    assert f.description == 'Alien invaders'
    assert f.id == 42
    assert f.aggression == 5
    assert f.pedia == 'Alien Faction'
    assert f.sprite == 'alien.png'
    assert f.tech_start == ['AlienTech']
    assert f.tech_end == ['EndTech']

def test_faction_init_defaults():
    """Test TFaction initializes with default values."""
    f = TFaction('FACTION1')
    assert f.pid == 'FACTION1'
    assert f.name == ''
    assert f.description == ''
    assert f.id == 0
    assert f.aggression == 0
    assert f.pedia == ''
    assert f.sprite == ''
    assert f.tech_start == []
    assert f.tech_end == []


def test_faction_init_with_data():
    """Test TFaction initializes with provided data."""
    data = {'name': 'Aliens', 'description': 'Desc', 'id': 2, 'aggression': 5, 'pedia': 'pedia', 'sprite': 'icon', 'tech_start': ['A'], 'tech_end': ['B']}
    f = TFaction('FACTION2', data)
    assert f.name == 'Aliens'
    assert f.description == 'Desc'
    assert f.id == 2
    assert f.aggression == 5
    assert f.pedia == 'pedia'
    assert f.sprite == 'icon'
    assert f.tech_start == ['A']
    assert f.tech_end == ['B']

