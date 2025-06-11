import pytest
from unit.side import TSide

class TestTSide:
    def test_constants(self):
        assert TSide.XCOM == 0
        assert TSide.ALIEN == 1
        assert TSide.CIVILIAN == 2
        assert TSide.ALLIED == 3

