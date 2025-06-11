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

