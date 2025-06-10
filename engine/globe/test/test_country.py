import pytest
from engine.globe.country import TCountry

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

