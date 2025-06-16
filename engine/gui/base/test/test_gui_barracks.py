import unittest
from engine.gui.base.gui_barracks import TGuiBarracks

class TestTGuiBarracks(unittest.TestCase):
    def test_init(self):
        """Test initialization of TGuiBarracks."""
        gui = TGuiBarracks()
        self.assertIsInstance(gui, TGuiBarracks)
