"""
Test suite for engine.globe.biome (TBiome)
Covers initialization and get_random_terrain using pytest.
"""

import pytest
from engine.globe.biome import TBiome

@pytest.fixture
def biome():
    data = {
        'name': 'Forest',
        'description': 'Dense forest',
        'sprite': 'forest.png',
        'type': 'land',
        'terrains': {'woods': 2, 'clearing': 1}
    }
    return TBiome('FOREST', data)

def test_init_defaults(biome):
    """Test initialization and attribute values from data dict."""
    assert biome.pid == 'FOREST'
    assert biome.name == 'Forest'
    assert biome.description == 'Dense forest'
    assert biome.image == 'forest.png'
    assert biome.type == 'land'
    assert biome.terrains == {'woods': 2, 'clearing': 1}

def test_get_random_terrain_returns_valid_key(biome):
    """Test get_random_terrain returns a valid terrain key or None if empty."""
    result = biome.get_random_terrain()
    assert result in biome.terrains
    # Test with no terrains
    empty_biome = TBiome('EMPTY', {})
    assert empty_biome.get_random_terrain() is None

