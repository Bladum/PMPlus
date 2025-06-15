import unittest
from engine.gui.gui_world import TGuiGlobe
from PySide6.QtWidgets import QApplication
import sys

app = QApplication.instance() or QApplication(sys.argv)

class TestTGuiGlobe(unittest.TestCase):
    def test_init(self):
        gui = TGuiGlobe()
        self.assertIsNotNone(gui.layout)
        self.assertIsNotNone(gui.top_panel)
        self.assertIsNotNone(gui.screen_container)
        self.assertIsInstance(gui.screens, dict)

if __name__ == '__main__':
    unittest.main()
