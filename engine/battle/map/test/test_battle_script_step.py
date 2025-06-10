import pytest
from engine.battle.map.battle_script_step import TBattleScriptStep

def test_battle_script_step_defaults():
    step = TBattleScriptStep({})
    assert step.type == ''
    assert step.group is None
    assert step.size is None
    assert step.runs == 1
    assert step.chance == 1.5
    assert step.direction == 'horizontal'
    assert step.row is None
    assert step.col is None
    assert step.ufo is None
    assert step.craft is None
    assert step.label is None
    assert step.condition == []

