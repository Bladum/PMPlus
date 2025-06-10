import pytest
from engine.ai.strategy import TAlienStrategy

class TestTAlienStrategy:
    def test_init(self):
        strategy = TAlienStrategy()
        assert isinstance(strategy, TAlienStrategy)

