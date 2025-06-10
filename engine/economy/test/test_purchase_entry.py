import pytest
from engine.economy.purchase_entry import TPurchaseEntry

class TestTPurchaseEntry:
    def test_init_defaults(self):
        entry = TPurchaseEntry('pid1')
        assert entry.pid == 'pid1'
        assert entry.name == ''
        assert entry.category == ''
        assert entry.supplier is None
        assert entry.purchase_cost == 0
        assert entry.purchase_time == 0
        assert entry.tech_needed == []
        assert entry.items_needed == {}
        assert entry.services_needed == []
        assert entry.region_needed == []
        assert entry.country_needed == []
        assert entry.items_buy is None
        assert entry.units_buy is None
        assert entry.crafts_buy is None

    def test_init_with_data(self):
        data = {
            'name': 'Laser Rifle',
            'category': 'Weapons',
            'supplier': 'XCOM',
            'purchase_cost': 1000,
            'purchase_time': 2,
            'tech_needed': ['Laser Weapons'],
            'items_needed': {'alloy': 2},
            'services_needed': ['Workshop'],
            'region_needed': ['Europe'],
            'country_needed': ['France'],
            'items_buy': {'laser_rifle': 1},
            'units_buy': None,
            'crafts_buy': None
        }
        entry = TPurchaseEntry('pid2', data)
        assert entry.name == 'Laser Rifle'
        assert entry.category == 'Weapons'
        assert entry.supplier == 'XCOM'
        assert entry.purchase_cost == 1000
        assert entry.purchase_time == 2
        assert entry.tech_needed == ['Laser Weapons']
        assert entry.items_needed == {'alloy': 2}
        assert entry.services_needed == ['Workshop']
        assert entry.region_needed == ['Europe']
        assert entry.country_needed == ['France']
        assert entry.items_buy == {'laser_rifle': 1}
        assert entry.units_buy is None
        assert entry.crafts_buy is None

