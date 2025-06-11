import pytest
from unit.unit_type import TUnitType

class TestTUnitType:
    def test_init_defaults(self):
        data = {}
        unit_type = TUnitType('SOLDIER', data)
        assert unit_type.pid == 'SOLDIER'
        assert unit_type.name == ''
        assert unit_type.race == ''
        assert unit_type.sprite == ''
        assert unit_type.rank == 0
        assert unit_type.traits == []
        assert unit_type.armour is None
        assert unit_type.primary is None
        assert unit_type.secondary is None
        assert unit_type.score_dead == 0
        assert unit_type.score_alive == 0
        assert unit_type.items_dead == []
        assert unit_type.items_alive == []
        assert unit_type.ai_ignore is False
        assert unit_type.vip is False
        assert unit_type.drop_items is False
        assert unit_type.drop_armour is False

    def test_init_custom(self):
        data = {
            'name': 'Elite',
            'race': 'HUMAN',
            'sprite': 'elite.png',
            'rank': 2,
            'traits': ['BRAVE'],
            'armour': 'Power',
            'primary': 'LaserRifle',
            'secondary': 'Grenade',
            'score_dead': 100,
            'score_alive': 200,
            'items_dead': ['Medkit'],
            'items_alive': ['Medkit', 'Stimulant'],
            'ai_ignore': True,
            'vip': True,
            'drop_items': True,
            'drop_armour': True
        }
        unit_type = TUnitType('ELITE', data)
        assert unit_type.pid == 'ELITE'
        assert unit_type.name == 'Elite'
        assert unit_type.race == 'HUMAN'
        assert unit_type.sprite == 'elite.png'
        assert unit_type.rank == 2
        assert unit_type.traits == ['BRAVE']
        assert unit_type.armour == 'Power'
        assert unit_type.primary == 'LaserRifle'
        assert unit_type.secondary == 'Grenade'
        assert unit_type.score_dead == 100
        assert unit_type.score_alive == 200
        assert unit_type.items_dead == ['Medkit']
        assert unit_type.items_alive == ['Medkit', 'Stimulant']
        assert unit_type.ai_ignore is True
        assert unit_type.vip is True
        assert unit_type.drop_items is True
        assert unit_type.drop_armour is True

