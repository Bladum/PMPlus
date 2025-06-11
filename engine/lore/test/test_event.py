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

