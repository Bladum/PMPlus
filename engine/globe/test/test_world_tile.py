from engine.globe.world_tile import TWorldTile

def test_tworldtile_init():
    tile = TWorldTile(1,2, {'region_id': 3, 'country_id': 4, 'biome_id': 5, 'locations': [7]})
    assert tile.x == 1 and tile.y == 2
    assert tile.region_id == 3
    assert tile.country_id == 4
    assert tile.biome_id == 5
    assert tile.locations == [7]

