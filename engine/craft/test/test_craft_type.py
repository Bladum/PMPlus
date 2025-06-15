"""
Test suite for engine.craft.craft_type (TCraftType)
Covers initialization and attribute defaults using pytest.
"""
import pytest
from engine.craft.craft_type import TCraftType

@pytest.fixture
def craft_type():
    data = {
        'name': 'Skyranger',
        'description': 'Troop transport',
        'health': 150,
        'range': 5000,
        'speed': 2000,
        'can_land': True,
        'is_spaceship': False,
        'pilots': 2,
        'items': [10, 5],
        'units': 14,
    }
    return TCraftType('SKY', data)

def test_init_defaults(craft_type):
    """Test initialization and attribute values from data dict."""
    assert craft_type.pid == 'SKY'
    assert craft_type.name == 'Skyranger'
    assert craft_type.description == 'Troop transport'
    assert craft_type.health == 150
    assert craft_type.range == 5000
    assert craft_type.speed == 2000
    assert craft_type.can_land is True
    assert craft_type.is_spaceship is False
    assert craft_type.pilots == 2
    assert craft_type.items == [10, 5]
    assert craft_type.units == 14
