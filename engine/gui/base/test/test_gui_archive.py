import unittest
from engine.gui.base.gui_archive import TGuiArchive

class TestTGuiArchive(unittest.TestCase):
    def test_init(self):
        """Test initialization of TGuiArchive."""
        gui = TGuiArchive()
        self.assertIsInstance(gui, TGuiArchive)
