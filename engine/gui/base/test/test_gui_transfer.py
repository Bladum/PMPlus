import unittest
from engine.gui.base.gui_transfer import TGuiTransfer

class TestTGuiTransfer(unittest.TestCase):
    def test_init(self):
        """Test initialization of TGuiTransfer."""
        gui = TGuiTransfer()
        self.assertIsInstance(gui, TGuiTransfer)
