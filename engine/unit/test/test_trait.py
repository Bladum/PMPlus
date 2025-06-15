"""
Test suite for engine.unit.trait (TTrait)
Covers initialization and attribute defaults using pytest.
"""
import pytest
from engine.unit.trait import TTrait
from unit.unit_stat import TUnitStats

@pytest.fixture
def trait():
    data = {
        'name': 'Brave',
        'sprite': 'brave_icon',
        'description': 'Increases morale',
        'type': 0,
        'cost': 100,
        'items_needed': ['medal'],
        'races': ['human'],
        'min_level': 1,
        'max_level': 5,
        'services_needed': ['training'],
        'tech_needed': ['psi_labs'],
        'recovery_time': 0,
        'transfer_time': 0,
        'battle_duration': 0,
        'battle_effect': None,
        'battle_chance_complete': 0,
        'battle_only': False,
    }
    return TTrait('BRAVE', data)

def test_init_defaults(trait):
    """Test initialization and attribute values from data dict."""
    assert trait.id == 'BRAVE'
    assert trait.name == 'Brave'
    assert trait.sprite == 'brave_icon'
    assert trait.description == 'Increases morale'
    assert trait.type == 0
    assert trait.cost == 100
    assert trait.items_needed == ['medal']
    assert trait.races == ['human']
    assert trait.min_level == 1
    assert trait.max_level == 5
    assert trait.services_needed == ['training']
    assert trait.tech_needed == ['psi_labs']
    assert trait.recovery_time == 0
    assert trait.transfer_time == 0
    assert trait.battle_duration == 0
    assert trait.battle_effect is None
    assert trait.battle_chance_complete == 0
    assert trait.battle_only is False

class TestTTrait:
    def test_init_defaults(self):
        data = {}
        trait = TTrait('PROMO', data)
        assert trait.id == 'PROMO'
        assert trait.name == 'PROMO'
        assert trait.sprite == ''
        assert trait.description == ''
        assert trait.type == 0
        assert isinstance(trait.stats, TUnitStats)
        assert trait.cost == 0
        assert trait.items_needed == []
        assert trait.races == []
        assert trait.min_level == 0
        assert trait.max_level == 99
        assert trait.services_needed == []
        assert trait.tech_needed == []
        assert trait.recovery_time == 0
        assert trait.transfer_time == 0
        assert trait.battle_duration == 0
        assert trait.battle_effect is None
        assert trait.battle_chance_complete == 0
        assert trait.battle_only is False

    def test_init_custom(self):
        data = {
            'name': 'Wound',
            'sprite': 'wound.png',
            'description': 'Permanent wound',
            'type': 5,
            'stats': {'health': -10},
            'cost': 100,
            'items_needed': ['medkit'],
            'races': ['HUMAN'],
            'min_level': 2,
            'max_level': 5,
            'services_needed': ['hospital'],
            'tech_needed': ['surgery'],
            'recovery_time': 7,
            'transfer_time': 2,
            'battle_duration': 3,
            'battle_effect': 'bleed',
            'battle_chance_complete': 50,
            'battle_only': True
        }
        trait = TTrait('WOUND', data)
        assert trait.id == 'WOUND'
        assert trait.name == 'Wound'
        assert trait.sprite == 'wound.png'
        assert trait.description == 'Permanent wound'
        assert trait.type == 5
        assert isinstance(trait.stats, TUnitStats)
        assert trait.stats.health == -10
        assert trait.cost == 100
        assert trait.items_needed == ['medkit']
        assert trait.races == ['HUMAN']
        assert trait.min_level == 2
        assert trait.max_level == 5
        assert trait.services_needed == ['hospital']
        assert trait.tech_needed == ['surgery']
        assert trait.recovery_time == 7
        assert trait.transfer_time == 2
        assert trait.battle_duration == 3
        assert trait.battle_effect == 'bleed'
        assert trait.battle_chance_complete == 50
        assert trait.battle_only is True

    def test_get_stat_modifiers(self):
        data = {'stats': {'health': 5, 'speed': 2}}
        trait = TTrait('BUFF', data)
        modifiers = trait.get_stat_modifiers()
        assert modifiers['health'] == 5
        assert modifiers['speed'] == 2

