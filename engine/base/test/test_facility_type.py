"""
Test suite for engine.base.facility_type (TFacilityType)
Covers initialization and attribute defaults using pytest.
"""
import pytest
from engine.base.facility_type import TFacilityType

@pytest.fixture
def facility_type():
    data = {
        'name': 'Living Quarters',
        'lift': True,
        'description': 'Crew housing',
        'map_block': 'block_lq',
        'health': 20,
        'build_time': 5,
        'build_cost': 100000,
        'build_items': {'alloy': 2},
        'upkeep_cost': 5000,
    }
    return TFacilityType('LQ', data)

def test_init_defaults(facility_type):
    """Test initialization and attribute values from data dict."""
    assert facility_type.pid == 'LQ'
    assert facility_type.name == 'Living Quarters'
    assert facility_type.lift is True
    assert facility_type.description == 'Crew housing'
    assert facility_type.map_block == 'block_lq'
    assert facility_type.health == 20
    assert facility_type.build_time == 5
    assert facility_type.build_cost == 100000
    assert facility_type.build_items == {'alloy': 2}
    assert facility_type.upkeep_cost == 5000
