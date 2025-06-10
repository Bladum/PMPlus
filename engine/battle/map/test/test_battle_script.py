import pytest
from engine.battle.map.battle_script import TBattleScript
from engine.battle.map.battle_script_step import TBattleScriptStep

def test_battle_script_init():
    data = {'steps': [{'type': 'add_block', 'group': 1, 'size': 1}]}
    script = TBattleScript('test', data)
    assert script.pid == 'test'
    assert isinstance(script.steps[0], TBattleScriptStep)

