import unittest
from engine.gui.base.gui_workshop import TGuiWorkshop

class TestTGuiWorkshop(unittest.TestCase):
    def test_init(self):
        """Test initialization of TGuiWorkshop."""
        gui = TGuiWorkshop()
        self.assertIsInstance(gui, TGuiWorkshop)
