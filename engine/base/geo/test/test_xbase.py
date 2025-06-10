import pytest
from engine.base.geo.xbase import TBaseXCom
from unittest.mock import MagicMock, patch

class TestTBaseXCom:
    @patch('engine.base.geo.xbase.TLocation.__init__', return_value=None)
    @patch('engine.base.geo.xbase.TBaseInventory')
    def test_init_and_attributes(self, MockInventory, MockLocationInit):
        base = TBaseXCom('BASE1', {'name': 'TestBase'})
        assert hasattr(base, 'facilities')
        assert hasattr(base, 'inventory')
        assert hasattr(base, 'game')
        assert isinstance(base.facilities, dict)
        assert isinstance(base.inventory, MockInventory)

    @patch('engine.base.geo.xbase.TLocation.__init__', return_value=None)
    @patch('engine.base.geo.xbase.TBaseInventory')
    def test_add_and_remove_facility(self, MockInventory, MockLocationInit):
        base = TBaseXCom('BASE2')
        mock_facility_type = MagicMock()
        mock_facility = MagicMock()
        with patch('engine.base.geo.xbase.TFacility', return_value=mock_facility):
            base.can_build_facility = MagicMock(return_value=True)
            facility = base.add_facility(mock_facility_type, (1, 1))
            assert base.facilities[(1, 1)] == mock_facility
            base.remove_facility(mock_facility)
            assert (1, 1) not in base.facilities

    @patch('engine.base.geo.xbase.TLocation.__init__', return_value=None)
    @patch('engine.base.geo.xbase.TBaseInventory')
    def test_save_and_load_data(self, MockInventory, MockLocationInit):
        base = TBaseXCom('BASE3')
        base.lat = 10
        base.lon = 20
        base.name = 'BaseX'
        mock_facility = MagicMock()
        mock_facility.facility_type = MagicMock(pid='FAC1')
        mock_facility.build_progress = 2
        mock_facility.completed = True
        mock_facility.hp = 8
        base.facilities = {(0, 0): mock_facility}
        base.inventory.save_data = MagicMock(return_value={'items': {}})
        data = base.save_data()
        assert data['location']['lat'] == 10
        assert data['facilities'][0]['facility_type_id'] == 'FAC1'
        # Test load_data
        with patch('engine.base.geo.xbase.TFacility', return_value=mock_facility):
            with patch('engine.base.geo.xbase.TBaseXCom.update_inventory_capacities'):
                base.load_data(data)
                assert (0, 0) in base.facilities

