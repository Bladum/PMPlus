import pytest
from engine.base.facility_type import TFacilityType
from engine.base.facility import TFacility
from unittest.mock import MagicMock, patch

class TestTFacilityType:
    def test_init_defaults(self):
        ft = TFacilityType('FAC_TEST')
        assert ft.pid == 'FAC_TEST'
        assert ft.name == ''
        assert ft.lift is False
        assert ft.health == 10
        assert ft.build_time == 0
        assert ft.build_cost == 0
        assert ft.upkeep_cost == 0
        assert ft.max_per_base == 0
        assert ft.unit_space == 0
        assert ft.defense_power == 0
        assert ft.radar_power == 0
        assert ft.service_provided == []
        assert ft.service_required == []

    def test_init_with_data(self):
        data = {
            'name': 'Test Facility',
            'lift': True,
            'description': 'desc',
            'map_block': 'block',
            'health': 20,
            'build_time': 5,
            'build_cost': 1000,
            'upkeep_cost': 100,
            'max_per_base': 2,
            'unit_space': 5,
            'defense_power': 10,
            'radar_power': 15,
            'service_provided': ['power'],
            'service_required': ['water']
        }
        ft = TFacilityType('FAC2', data)
        assert ft.name == 'Test Facility'
        assert ft.lift is True
        assert ft.description == 'desc'
        assert ft.map_block == 'block'
        assert ft.health == 20
        assert ft.build_time == 5
        assert ft.build_cost == 1000
        assert ft.upkeep_cost == 100
        assert ft.max_per_base == 2
        assert ft.unit_space == 5
        assert ft.defense_power == 10
        assert ft.radar_power == 15
        assert ft.service_provided == ['power']
        assert ft.service_required == ['water']

class TestTFacility:
    @patch('engine.base.facility.TGame')
    def test_init_and_attributes(self, MockTGame):
        mock_game = MockTGame.return_value
        mock_facility_type = MagicMock()
        mock_game.mod.facilities.get.return_value = mock_facility_type
        fac = TFacility('FAC_TEST', (1, 2))
        assert fac.facility_type == mock_facility_type
        assert fac.position == (1, 2)
        assert fac.build_progress == 0
        assert fac.completed is False
        assert fac.hp == 10

    @patch('engine.base.facility.TGame')
    def test_is_active_and_build_day(self, MockTGame):
        mock_game = MockTGame.return_value
        mock_facility_type = MagicMock()
        mock_facility_type.build_time = 2
        mock_game.mod.facilities.get.return_value = mock_facility_type
        fac = TFacility('FAC_TEST', (0, 0))
        assert fac.is_active() is False
        fac.build_day()
        assert fac.build_progress == 1
        assert fac.completed is False
        fac.build_day()
        assert fac.completed is True
        assert fac.is_active() is True

    @patch('engine.base.facility.TGame')
    def test_get_stats(self, MockTGame):
        mock_game = MockTGame.return_value
        mock_facility_type = MagicMock()
        mock_game.mod.facilities.get.return_value = mock_facility_type
        fac = TFacility('FAC_TEST', (0, 0))
        fac.completed = False
        assert fac.get_stats() is None
        fac.completed = True
        assert fac.get_stats() == mock_facility_type

