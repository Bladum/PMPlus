"""
XCOM GUI Module: gui_unit_graphics_item.py

Visual representation of a unit on the battle map.

Classes:
    UnitGraphicsItem: QGraphicsRectItem subclass for unit display.

Last updated: 2025-06-14
"""

from PySide6.QtWidgets import QGraphicsRectItem
from PySide6.QtGui import QColor

class UnitGraphicsItem(QGraphicsRectItem):
    """
    Visual representation of a unit on the battle map.
    Inherits from QGraphicsRectItem.
    """
    def __init__(self, unit, tile_size):
        """
        Initialize the unit graphics item.
        Args:
            unit: The unit object to display.
            tile_size (int): Size of a tile in pixels.
        """
        super().__init__(unit.x * tile_size, unit.y * tile_size, unit.width * tile_size, unit.height * tile_size)
        self.unit = unit
        self.tile_size = tile_size
        self.setBrush(QColor("blue"))
        self.setZValue(1)

    def update_position(self):
        """
        Update the position of the unit graphics item.
        """
        self.setRect(self.unit.x * self.tile_size, self.unit.y * self.tile_size, self.unit.width * self.tile_size, self.unit.height * self.tile_size)

