import pytest
from engine.battle.map.deployment import TDeployment

def test_deployment_init():
    data = {'effect': 'smoke', 'civilians': 2, 'units': [{'qty_low': 1, 'qty_high': 2, 'units': {'soldier': 1}}]}
    deployment = TDeployment('test', data, ['civilian'])
    assert deployment.pid == 'test'
    assert deployment.effect == 'smoke'
    assert deployment.civilians == 2
    assert isinstance(deployment.groups, list)
    assert deployment.civilian_types == ['civilian']

def test_generate_unit_list():
    data = {'civilians': 1, 'units': [{'qty_low': 1, 'qty_high': 1, 'units': {'soldier': 1}}]}
    deployment = TDeployment('test', data, ['civilian'])
    units = deployment.generate_unit_list()
    assert 'civilian' in units or 'soldier' in units

