import pytest
from engine.globe.biome import TBiome

def test_tbiome_init_and_random_terrain():
    biome = TBiome(pid=1, data={
        'name': 'Forest',
        'description': 'Dense forest',
        'sprite': 'forest.png',
        'type': 'land',
        'terrains': {'forest': 3, 'clearing': 1}
    })
    assert biome.pid == 1
    assert biome.name == 'Forest'
    assert biome.type == 'land'
    assert biome.terrains == {'forest': 3, 'clearing': 1}
    assert biome.get_random_terrain() in {'forest', 'clearing'}

def test_tbiome_no_terrains():
    biome = TBiome(pid=2)
    assert biome.get_random_terrain() is None

