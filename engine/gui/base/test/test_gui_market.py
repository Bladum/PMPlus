import unittest
from engine.gui.base.gui_market import TGuiMarket

class TestTGuiMarket(unittest.TestCase):
    def test_init(self):
        """Test initialization of TGuiMarket."""
        gui = TGuiMarket()
        self.assertIsInstance(gui, TGuiMarket)
