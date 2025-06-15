import unittest
from engine.gui.other.widget.base_inventory_widget import TBaseInventoryWidget
from engine.gui.other.widget.craft_list_widget import TCraftListWidget
from engine.gui.other.widget.unit_item_list_widget import TUnitItemListWidget
from engine.gui.other.widget.unit_list_widget import TUnitListWidget
from PySide6.QtWidgets import QApplication
import sys

app = QApplication.instance() or QApplication(sys.argv)

class TestTBaseInventoryWidget(unittest.TestCase):
    def test_init(self):
        widget = TBaseInventoryWidget()
        self.assertIsNotNone(widget)

class TestTCraftListWidget(unittest.TestCase):
    def test_init(self):
        widget = TCraftListWidget()
        self.assertIsNotNone(widget)

class TestTUnitItemListWidget(unittest.TestCase):
    def test_init(self):
        widget = TUnitItemListWidget()
        self.assertIsNotNone(widget)

class TestTUnitListWidget(unittest.TestCase):
    def test_init(self):
        widget = TUnitListWidget()
        self.assertIsNotNone(widget)

if __name__ == '__main__':
    unittest.main()
