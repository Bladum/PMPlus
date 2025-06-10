from engine.globe.region import TRegion

def test_tregion_init_and_calculate():
    region = TRegion(1, {'name': 'Europe', 'is_land': True})
    class DummyTile:
        def __init__(self, x, y, region_id):
            self.x = x; self.y = y; self.region_id = region_id
    tiles = [[DummyTile(x, y, 1 if x < 2 else 2) for x in range(4)] for y in range(2)]
    region_neighbors = {1: {2}, 2: {1}}
    region.calculate_region_tiles(tiles, 4, 2, region_neighbors)
    assert region.name == 'Europe'
    assert region.is_land
    assert (0,0) in region.tiles
    assert 2 in region.neighbors

