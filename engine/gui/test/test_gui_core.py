import unittest
from engine.gui.gui_core import TGuiCoreScreen
from PySide6.QtWidgets import QApplication
import sys

app = QApplication.instance() or QApplication(sys.argv)

class TestTGuiCoreScreen(unittest.TestCase):
    def test_init(self):
        screen = TGuiCoreScreen()
        self.assertIsNotNone(screen)
        self.assertTrue(hasattr(screen, 'screen_activated'))
        self.assertTrue(hasattr(screen, 'screen_deactivated'))
        self.assertTrue(hasattr(screen, 'refresh_base_data'))
        self.assertTrue(hasattr(screen, 'update_summary_display'))

if __name__ == '__main__':
    unittest.main()
