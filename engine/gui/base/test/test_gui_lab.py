import unittest
from engine.gui.base.gui_lab import TGuiLab

class TestTGuiLab(unittest.TestCase):
    def test_init(self):
        """Test initialization of TGuiLab."""
        gui = TGuiLab()
        self.assertIsInstance(gui, TGuiLab)
