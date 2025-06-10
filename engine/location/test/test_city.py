import pytest
from engine.location.city import TCity

class TestTCity:
    def test_init_defaults(self):
        city = TCity('city1')
        assert city.size == 4
        assert city.name == ''
        assert city.description == ''
        assert city.terrains == {}

    def test_init_with_data(self):
        data = {'size': 10, 'name': 'London', 'description': 'Capital', 'terrains': {'urban': 2, 'park': 1}}
        city = TCity('city2', data)
        assert city.size == 10
        assert city.name == 'London'
        assert city.description == 'Capital'
        assert city.terrains == {'urban': 2, 'park': 1}

    def test_get_random_terrain_dict(self, monkeypatch):
        data = {'terrains': {'urban': 2, 'park': 1}}
        city = TCity('city3', data)
        monkeypatch.setattr('random.choices', lambda keys, weights, k: [keys[0]])
        assert city.get_random_terrain() == 'urban'

    def test_get_random_terrain_list(self, monkeypatch):
        data = {'terrains': ['urban', 'park']}
        city = TCity('city4', data)
        monkeypatch.setattr('random.choice', lambda l: l[1])
        assert city.get_random_terrain() == 'park'

    def test_get_random_terrain_none(self):
        city = TCity('city5')
        assert city.get_random_terrain() is None

