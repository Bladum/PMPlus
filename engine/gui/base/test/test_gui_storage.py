import unittest
from engine.gui.base.gui_storage import TGuiStorage

class TestTGuiStorage(unittest.TestCase):
    def test_init(self):
        """Test initialization of TGuiStorage."""
        gui = TGuiStorage()
        self.assertIsInstance(gui, TGuiStorage)
