"""
Test suite for engine.globe.country (TCountry)
Covers initialization and attribute defaults using pytest.
"""

import pytest
from engine.globe.country import TCountry

@pytest.fixture
def country():
    data = {
        'name': 'France',
        'description': 'A country in Europe',
        'color': '#123456',
        'funding': 20,
        'funding_cap': 1000,
        'service_provided': ['radar'],
        'service_forbidden': ['psi'],
        'owned_tiles': [(1, 2)],
        'initial_relation': 10
    }
    return TCountry('FR', data)

def test_init_defaults(country):
    """Test initialization and attribute values from data dict."""
    assert country.pid == 'FR'
    assert country.name == 'France'
    assert country.description == 'A country in Europe'
    assert country.color == '#123456'
    assert country.funding == 20
    assert country.funding_cap == 1000
    assert country.service_provided == ['radar']
    assert country.service_forbidden == ['psi']
    assert country.owned_tiles == [(1, 2)]
    assert country.initial_relation == 10
    assert country.relation == 10
    assert country.active is True or country.active is False

def test_tcountry_init_and_tile_management():
    country = TCountry(pid='A', data={'name': 'Atlantis', 'owned_tiles': [(1,2)]})
    assert country.pid == 'A'
    assert country.name == 'Atlantis'
    assert (1,2) in country.owned_tiles
    country.add_tile((3,4))
    assert (3,4) in country.owned_tiles
    country.remove_tile((1,2))
    assert (1,2) not in country.owned_tiles

def test_tcountry_monthly_update():
    country = TCountry(pid='B', data={'funding': 100, 'funding_cap': 200, 'initial_relation': 5})
    country.monthly_update(2000)
    assert country.relation >= 5
    country.monthly_update(-2000)
    assert country.relation >= 0

