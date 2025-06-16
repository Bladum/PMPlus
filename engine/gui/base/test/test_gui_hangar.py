import unittest
from engine.gui.base.gui_hangar import TGuiHangar

class TestTGuiHangar(unittest.TestCase):
    def test_init(self):
        """Test initialization of TGuiHangar."""
        gui = TGuiHangar()
        self.assertIsInstance(gui, TGuiHangar)
