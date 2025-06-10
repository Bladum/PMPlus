import pytest
from engine.location.ufo_script import TUfoScript

class TestTUfoScript:
    def test_init_defaults(self):
        script = TUfoScript('script1', {})
        assert script.pid == 'script1'
        assert script.name == 'script1'
        assert script.description == ''
        assert script.steps == []

    def test_init_with_data(self):
        data = {'name': 'Scout Script', 'desc': 'desc', 'steps': [{'type': 'move', 'duration': 2}]}
        script = TUfoScript('script2', data)
        assert script.name == 'Scout Script'
        assert script.description == 'desc'
        assert script.steps == [{'type': 'move', 'duration': 2}]

    def test_get_step(self):
        steps = [{'type': 'a'}, {'type': 'b'}]
        script = TUfoScript('script3', {'steps': steps})
        assert script.get_step(0) == {'type': 'a'}
        assert script.get_step(1) == {'type': 'b'}
        assert script.get_step(2) is None

    def test_total_steps(self):
        script = TUfoScript('script4', {'steps': [1, 2, 3]})
        assert script.total_steps() == 3

