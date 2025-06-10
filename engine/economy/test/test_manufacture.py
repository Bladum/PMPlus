import pytest
from engine.economy.manufacture import TManufacture
from engine.economy.manufacture_entry import TManufactureEntry

class TestTManufacture:
    def test_load_and_get_entry(self):
        data = {
            'manufacturing': {
                'project1': {'name': 'Laser Rifle', 'category': 'Weapons', 'build_time': 10, 'build_cost': 500, 'tech_start': ['Laser Weapons']},
                'project2': {'name': 'Medikit', 'category': 'Equipment', 'build_time': 5, 'build_cost': 200, 'tech_start': []}
            }
        }
        m = TManufacture(data)
        assert isinstance(m.get_entry('project1'), TManufactureEntry)
        assert m.get_entry('project1').name == 'Laser Rifle'
        assert m.get_entry('project2').category == 'Equipment'
        assert m.get_entry('not_exist') is None

    def test_get_projects_by_category(self):
        data = {
            'manufacturing': {
                'p1': {'name': 'A', 'category': 'Cat1'},
                'p2': {'name': 'B', 'category': 'Cat2'},
                'p3': {'name': 'C', 'category': 'Cat1'}
            }
        }
        m = TManufacture(data)
        cat1 = m.get_projects_by_category('Cat1')
        assert len(cat1) == 2
        assert all(e.category == 'Cat1' for e in cat1)

    def test_get_available_projects(self):
        data = {
            'manufacturing': {
                'p1': {'name': 'A', 'tech_start': ['T1'], 'items_needed': {'item1': 2}, 'services_needed': ['S1']},
                'p2': {'name': 'B', 'tech_start': [], 'items_needed': {}, 'services_needed': []}
            }
        }
        m = TManufacture(data)
        # Only p2 is available with no requirements
        available = m.get_available_projects()
        assert len(available) == 1 and available[0].name == 'B'
        # p1 available if all requirements met
        available = m.get_available_projects(
            available_technologies=['T1'],
            available_services=['S1'],
            available_items={'item1': 2}
        )
        assert any(e.name == 'A' for e in available)

    def test_entry_attributes(self):
        entry = TManufactureEntry('pid', {
            'name': 'Test',
            'category': 'Cat',
            'build_time': 5,
            'build_cost': 100,
            'give_score': 10,
            'tech_start': ['T1'],
            'items_needed': {'item1': 1},
            'services_needed': ['S1'],
            'region_needed': ['R1'],
            'country_needed': ['C1'],
            'items_build': {'item2': 1},
            'units_build': {'unit1': 1},
            'crafts_build': {'craft1': 1}
        })
        assert entry.pid == 'pid'
        assert entry.name == 'Test'
        assert entry.category == 'Cat'
        assert entry.build_time == 5
        assert entry.build_cost == 100
        assert entry.give_score == 10
        assert entry.tech_start == ['T1']
        assert entry.items_needed == {'item1': 1}
        assert entry.services_needed == ['S1']
        assert entry.region_needed == ['R1']
        assert entry.country_needed == ['C1']
        assert entry.items_build == {'item2': 1}
        assert entry.units_build == {'unit1': 1}
        assert entry.crafts_build == {'craft1': 1}
