import unittest
from engine.gui.theme_manager import XcomTheme, XcomStyle, px

class TestThemeManager(unittest.TestCase):
    def test_px_scaling(self):
        self.assertEqual(px(16), 32)  # Assuming SCALE = 2

    def test_theme_constants(self):
        self.assertTrue(hasattr(XcomTheme, 'BG_MID'))
        self.assertTrue(hasattr(XcomTheme, 'BG_DARK'))

    def test_style_methods(self):
        self.assertTrue(callable(XcomStyle.groupbox))
        self.assertTrue(callable(XcomStyle.lineedit))

if __name__ == '__main__':
    unittest.main()
