import unittest
from engine.gui.base.gui_academy import TGuiAcademy

class TestTGuiAcademy(unittest.TestCase):
    def test_init(self):
        """Test initialization of TGuiAcademy."""
        gui = TGuiAcademy()
        self.assertIsInstance(gui, TGuiAcademy)
