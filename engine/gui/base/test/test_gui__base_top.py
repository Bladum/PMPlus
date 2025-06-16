import unittest
from engine.gui.base.gui__base_top import TGuiBaseTopPanel

class TestTGuiBaseTopPanel(unittest.TestCase):
    def test_init(self):
        """Test initialization of TGuiBaseTopPanel."""
        gui = TGuiBaseTopPanel()
        self.assertIsInstance(gui, TGuiBaseTopPanel)
