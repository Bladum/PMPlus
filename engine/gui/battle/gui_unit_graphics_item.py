from PySide6.QtWidgets import QGraphicsRectItem
from PySide6.QtGui import QColor

class UnitGraphicsItem(QGraphicsRectItem):
    """
    Visual representation of a unit.
    """
    def __init__(self, unit, tile_size):
        super().__init__(unit.x * tile_size, unit.y * tile_size, unit.width * tile_size, unit.height * tile_size)
        self.unit = unit
        self.tile_size = tile_size
        self.setBrush(QColor("blue"))
        self.setZValue(1)

    def update_position(self):
        self.setRect(self.unit.x * self.tile_size, self.unit.y * self.tile_size, self.unit.width * self.tile_size, self.unit.height * self.tile_size)

