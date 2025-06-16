import unittest
from engine.gui.base.gui_facility import TGuiFacility

class TestTGuiFacility(unittest.TestCase):
    def test_init(self):
        """Test initialization of TGuiFacility."""
        gui = TGuiFacility()
        self.assertIsInstance(gui, TGuiFacility)
