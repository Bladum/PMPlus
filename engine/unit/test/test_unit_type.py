"""
Test suite for engine.unit.unit_type (TUnitType)
Covers initialization and attribute defaults using pytest.
"""

import pytest
from engine.unit.unit_type import TUnitType

@pytest.fixture
def unit_type():
    data = {
        'name': 'Sectoid',
        'race': 'sectoid',
        'sprite': 'sectoid_sprite',
        'rank': 2,
        'traits': ['psionic'],
        'armour': 'sectoid_armor',
        'primary': 'plasma_pistol',
        'secondary': 'mind_probe',
        'score_dead': 20,
        'score_alive': 40,
        'items_dead': ['plasma_pistol'],
        'items_alive': ['mind_probe'],
        'ai_ignore': False,
        'vip': False,
        'drop_items': True,
        'drop_armour': False,
    }
    return TUnitType('SECTOID', data)

def test_init_defaults(unit_type):
    """Test initialization and attribute values from data dict."""
    assert unit_type.pid == 'SECTOID'
    assert unit_type.name == 'Sectoid'
    assert unit_type.race == 'sectoid'
    assert unit_type.sprite == 'sectoid_sprite'
    assert unit_type.rank == 2
    assert unit_type.traits == ['psionic']
    assert unit_type.armour == 'sectoid_armor'
    assert unit_type.primary == 'plasma_pistol'
    assert unit_type.secondary == 'mind_probe'
    assert unit_type.score_dead == 20
    assert unit_type.score_alive == 40
    assert unit_type.items_dead == ['plasma_pistol']
    assert unit_type.items_alive == ['mind_probe']
    assert unit_type.ai_ignore is False
    assert unit_type.vip is False
    assert unit_type.drop_items is True
    assert unit_type.drop_armour is False

