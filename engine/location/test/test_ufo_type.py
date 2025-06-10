import pytest
from engine.location.ufo_type import TUfoType

class TestTUfoType:
    def test_init_defaults(self):
        utype = TUfoType('type1', {})
        assert utype.pid == 'type1'
        assert utype.name == 'type1'
        assert utype.pedia == ''
        assert utype.vessel == ''
        assert utype.marker == 'alien'
        assert utype.size == 1
        assert utype.health == 50
        assert utype.speed == 0
        assert utype.shield == 0
        assert utype.shield_regen == 0
        assert utype.damage == 0
        assert utype.rate == 0
        assert utype.range == 0
        assert utype.accuracy == 0.0
        assert utype.fire_sound == ''
        assert utype.radar_range == 0
        assert utype.radar_power == 0
        assert utype.radar_cover == 0
        assert utype.radar_cover_change == 0
        assert utype.is_hunter is False
        assert utype.hunt_bravery == 0.0
        assert utype.bombard_power == 0
        assert utype.score_complete == 0
        assert utype.score_destroy == 0
        assert utype.score_avoid == 0
        assert utype.score_damage == 0
        assert utype.score_turn == 0
        assert utype.map_block == ''
        assert utype.map_width == 0
        assert utype.map_height == 0
        assert utype.force_terrain == []
        assert utype.deployments == {}

    def test_init_with_data(self):
        data = {'name': 'Scout', 'health': 10, 'speed': 2, 'force_terrain': ['urban'], 'deployments': {'sectoid': 2}}
        utype = TUfoType('type2', data)
        assert utype.name == 'Scout'
        assert utype.health == 10
        assert utype.speed == 2
        assert utype.force_terrain == ['urban']
        assert utype.deployments == {'sectoid': 2}

