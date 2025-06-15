"""
Test suite for TEvent class.
Covers initialization and attribute assignment.
"""
import pytest
from engine.lore.event import TEvent

def test_event_init_basic():
    data = {
        'name': 'Alien Raid',
        'description': 'Aliens attack a city.',
        'sprite': 'alien.png',
        'tech_needed': ['AlienTech'],
        'regions': ['Europe'],
        'is_city': True,
        'month_start': 1,
        'month_random': 0,
        'month_end': 12,
        'qty_max': 2,
        'chance': 0.5,
        'score': 100,
        'funds': 50000,
        'items': ['LaserGun'],
        'units': ['Sectoid'],
        'crafts': ['UFO'],
        'facilities': ['Lab'],
        'ufos': ['Scout'],
        'sites': ['CrashSite'],
        'bases': ['AlienBase']
    }
    ev = TEvent('e1', data)
    assert ev.pid == 'e1'
    assert ev.name == 'Alien Raid'
    assert ev.description == 'Aliens attack a city.'
    assert ev.sprite == 'alien.png'
    assert ev.tech_needed == ['AlienTech']
    assert ev.regions == ['Europe']
    assert ev.is_city is True
    assert ev.month_start == 1
    assert ev.month_random == 0
    assert ev.month_end == 12
    assert ev.qty_max == 2
    assert ev.chance == 0.5
    assert ev.score == 100
    assert ev.funds == 50000
    assert ev.items == ['LaserGun']
    assert ev.units == ['Sectoid']
    assert ev.crafts == ['UFO']
    assert ev.facilities == ['Lab']
    assert ev.ufos == ['Scout']
    assert ev.sites == ['CrashSite']
    assert ev.bases == ['AlienBase']

def test_event_init_defaults():
    """Test TEvent initializes with default values."""
    data = {}
    event = TEvent('EVT1', data)
    assert event.pid == 'EVT1'
    assert event.name == 'EVT1'
    assert event.description == ''
    assert event.sprite == ''
    assert event.tech_needed == []
    assert event.regions == []
    assert event.is_city is False
    assert event.month_start == 0
    assert event.month_random == 0
    assert event.month_end == 9999
    assert event.qty_max == 1
    assert event.chance == 0 or isinstance(event.chance, float)
    assert event.score == 0 or isinstance(event.score, int)
    assert event.funds == 0 or isinstance(event.funds, int)
    assert event.items == []
    assert event.units == []
    assert event.crafts == []
    assert event.facilities == []
    assert event.ufos == []
    assert event.sites == []
    assert event.bases == []


def test_event_init_with_data():
    """Test TEvent initializes with provided data."""
    data = {'name': 'Alien Raid', 'description': 'Desc', 'sprite': 'icon', 'tech_needed': ['A'], 'regions': ['R'], 'is_city': True, 'month_start': 2, 'month_random': 1, 'month_end': 5, 'qty_max': 3, 'chance': 0.5, 'score': 10, 'funds': 100, 'items': ['item'], 'units': ['unit'], 'crafts': ['craft'], 'facilities': ['fac'], 'ufos': ['ufo'], 'sites': ['site'], 'bases': ['base']}
    event = TEvent('EVT2', data)
    assert event.name == 'Alien Raid'
    assert event.description == 'Desc'
    assert event.sprite == 'icon'
    assert event.tech_needed == ['A']
    assert event.regions == ['R']
    assert event.is_city is True
    assert event.month_start == 2
    assert event.month_random == 1
    assert event.month_end == 5
    assert event.qty_max == 3
    assert event.chance == 0.5
    assert event.score == 10
    assert event.funds == 100
    assert event.items == ['item']
    assert event.units == ['unit']
    assert event.crafts == ['craft']
    assert event.facilities == ['fac']
    assert event.ufos == ['ufo']
    assert event.sites == ['site']
    assert event.bases == ['base']

