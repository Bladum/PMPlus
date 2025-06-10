import pytest
from engine.economy.manufacture_entry import TManufactureEntry

class TestTManufactureEntry:
    def test_init_defaults(self):
        entry = TManufactureEntry('pid1')
        assert entry.pid == 'pid1'
        assert entry.name == ''
        assert entry.category == ''
        assert entry.build_time == 0
        assert entry.build_cost == 0
        assert entry.give_score == 0
        assert entry.tech_start == []
        assert entry.items_needed == {}
        assert entry.services_needed == []
        assert entry.region_needed == []
        assert entry.country_needed == []
        assert entry.items_build is None
        assert entry.units_build is None
        assert entry.crafts_build is None

    def test_init_with_data(self):
        data = {
            'name': 'Laser Cannon',
            'category': 'Weapons',
            'build_time': 12,
            'build_cost': 800,
            'give_score': 20,
            'tech_start': ['Laser Tech'],
            'items_needed': {'alloy': 3},
            'services_needed': ['Workshop'],
            'region_needed': ['Europe'],
            'country_needed': ['France'],
            'items_build': {'laser_cannon': 1},
            'units_build': None,
            'crafts_build': None
        }
        entry = TManufactureEntry('pid2', data)
        assert entry.name == 'Laser Cannon'
        assert entry.category == 'Weapons'
        assert entry.build_time == 12
        assert entry.build_cost == 800
        assert entry.give_score == 20
        assert entry.tech_start == ['Laser Tech']
        assert entry.items_needed == {'alloy': 3}
        assert entry.services_needed == ['Workshop']
        assert entry.region_needed == ['Europe']
        assert entry.country_needed == ['France']
        assert entry.items_build == {'laser_cannon': 1}
        assert entry.units_build is None
        assert entry.crafts_build is None

