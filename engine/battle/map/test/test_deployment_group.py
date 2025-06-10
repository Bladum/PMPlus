import pytest
from engine.battle.map.deployment_group import TDeploymentGroup

def test_deployment_group_init():
    data = {'qty_low': 1, 'qty_high': 2, 'units': {'soldier': 2, 'medic': 1}}
    group = TDeploymentGroup(data)
    assert group.qty_low == 1
    assert group.qty_high == 2
    assert group.unit_weights == {'soldier': 2, 'medic': 1}
    assert group.outside_ufo == 0.0
    assert group.inside_ufo == 1.0
    assert group.leader is False
    assert group.patrol is False
    assert group.guard is False

def test_pick_units():
    data = {'qty_low': 1, 'qty_high': 1, 'units': {'soldier': 1}}
    group = TDeploymentGroup(data)
    units = group.pick_units()
    assert isinstance(units, list)

