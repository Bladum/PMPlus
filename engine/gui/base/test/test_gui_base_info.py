import unittest
from engine.gui.base.gui_base_info import TGuiBaseInfo

class TestTGuiBaseInfo(unittest.TestCase):
    def test_init(self):
        """Test initialization of TGuiBaseInfo."""
        gui = TGuiBaseInfo()
        self.assertIsInstance(gui, TGuiBaseInfo)
