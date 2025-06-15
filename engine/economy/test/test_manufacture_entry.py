"""
Test suite for engine.economy.manufacture_entry (TManufactureEntry)
Covers initialization and attribute defaults using pytest.
"""
import pytest
from engine.economy.manufacture_entry import TManufactureEntry

@pytest.fixture
def entry():
    data = {
        'name': 'Laser Rifle',
        'category': 'Weapons',
        'build_time': 10,
        'build_cost': 20000,
        'give_score': 50,
        'tech_start': ['Laser Weapons'],
        'items_needed': {'alloy': 1},
        'services_needed': ['Workshop'],
        'region_needed': ['Europe'],
        'country_needed': ['France'],
        'items_build': 'laser_rifle',
        'units_build': None,
        'crafts_build': None,
    }
    return TManufactureEntry('LR1', data)

def test_init_defaults(entry):
    """Test initialization and attribute values from data dict."""
    assert entry.pid == 'LR1'
    assert entry.name == 'Laser Rifle'
    assert entry.category == 'Weapons'
    assert entry.build_time == 10
    assert entry.build_cost == 20000
    assert entry.give_score == 50
    assert entry.tech_start == ['Laser Weapons']
    assert entry.items_needed == {'alloy': 1}
    assert entry.services_needed == ['Workshop']
    assert entry.region_needed == ['Europe']
    assert entry.country_needed == ['France']
    assert entry.items_build == 'laser_rifle'
    assert entry.units_build is None
    assert entry.crafts_build is None
