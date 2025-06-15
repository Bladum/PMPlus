import unittest
from engine.gui.other.slots.inventory_slot import TInventorySlot
from engine.gui.other.slots.unit_inventory_slot import TUnitInventorySlot
from engine.gui.other.slots.craft_inventory_slot import TCraftInventorySlot
from engine.gui.other.slots.unit_slot import TUnitSlot
from PySide6.QtWidgets import QApplication
import sys

app = QApplication.instance() or QApplication(sys.argv)

class TestTInventorySlot(unittest.TestCase):
    def test_init(self):
        slot = TInventorySlot()
        self.assertIsNotNone(slot)

class TestTUnitInventorySlot(unittest.TestCase):
    def test_init(self):
        slot = TUnitInventorySlot()
        self.assertIsNotNone(slot)

class TestTCraftInventorySlot(unittest.TestCase):
    def test_init(self):
        slot = TCraftInventorySlot()
        self.assertIsNotNone(slot)

class TestTUnitSlot(unittest.TestCase):
    def test_init(self):
        slot = TUnitSlot()
        self.assertIsNotNone(slot)

if __name__ == '__main__':
    unittest.main()
