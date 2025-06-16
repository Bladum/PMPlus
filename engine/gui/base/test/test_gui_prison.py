import unittest
from engine.gui.base.gui_prison import TGuiPrison

class TestTGuiPrison(unittest.TestCase):
    def test_init(self):
        """Test initialization of TGuiPrison."""
        gui = TGuiPrison()
        self.assertIsInstance(gui, TGuiPrison)
