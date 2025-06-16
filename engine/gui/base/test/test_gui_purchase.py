import unittest
from engine.gui.base.gui_purchase import TPurchaseGui

class TestTPurchaseGui(unittest.TestCase):
    def test_init(self):
        """Test initialization of TPurchaseGui."""
        gui = TPurchaseGui()
        self.assertIsInstance(gui, TPurchaseGui)
