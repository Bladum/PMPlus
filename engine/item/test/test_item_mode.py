import pytest
from engine.item.item_mode import TWeaponMode

def test_weapon_mode_init_and_apply():
    data = {
        'name': 'Aimed',
        'key': 'A',
        'ap_cost_modifier': 1.5,
        'range_modifier': 2.0,
        'accuracy_modifier': 1.2,
        'shots': 2,
        'damage_modifier': 1.1
    }
    mode = TWeaponMode('aimed', data)
    assert mode.name == 'Aimed'
    assert mode.key == 'A'
    assert mode.ap_cost_modifier == 1.5
    assert mode.range_modifier == 2.0
    assert mode.accuracy_modifier == 1.2
    assert mode.shots == 2
    assert mode.damage_modifier == 1.1
    base_params = {'ap_cost': 10, 'range': 5, 'accuracy': 50, 'shots': 1, 'damage': 20}
    result = mode.apply(base_params)
    assert result['ap_cost'] == 15.0
    assert result['range'] == 10.0
    assert result['accuracy'] == 60.0
    assert result['shots'] == 2
    assert result['damage'] == 22.0

def test_weapon_mode_apply_defaults():
    mode = TWeaponMode('snap', {})
    base_params = {}
    result = mode.apply(base_params)
    assert result['ap_cost'] == 1.0
    assert result['range'] == 1.0
    assert result['accuracy'] == 1.0
    assert result['shots'] == 1
    assert result['damage'] == 1.0

