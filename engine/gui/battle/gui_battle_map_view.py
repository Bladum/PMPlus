"""
XCOM GUI Module: gui_battle_map_view.py

Visualizes the battle map and units using QGraphicsView/QGraphicsScene.
Handles efficient drawing and updating of tiles and units.

Classes:
    BattleMapView: Main view for rendering the battle map and units.

Last updated: 2025-06-14
"""

from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PySide6.QtGui import QColor
from PySide6.QtCore import QRectF, Qt
from engine.battle.battle import TBattle

class BattleMapView(QGraphicsView):
    """
    Visualizes the battle map and units using QGraphicsView/QGraphicsScene.
    Handles efficient drawing and updating of tiles and units.
    """
    def __init__(self, battle: TBattle, tile_size=16):
        """
        Initialize the battle map view.
        Args:
            battle (TBattle): The battle logic instance.
            tile_size (int): Size of each tile in pixels.
        """
        super().__init__()
        self.battle = battle
        self.tile_size = tile_size
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.tile_items = {}  # (x, y) -> QGraphicsRectItem
        self.unit_items = []
        self.draw_map()
        self.draw_units()

    def draw_map(self):
        """
        Draw the battle map tiles.
        """
        for y, row in enumerate(self.battle.tiles):
            for x, tile in enumerate(row):
                rect = QRectF(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                item = QGraphicsRectItem(rect)
                color = QColor("lightgray") if tile.is_walkable() else QColor("darkgray")
                item.setBrush(color)
                item.setPen(Qt.NoPen if tile.is_walkable() else QColor("black"))
                self.scene.addItem(item)
                self.tile_items[(x, y)] = item

    def draw_units(self):
        """
        Draw all units on the map.
        """
        self.unit_items.clear()
        for side_units in self.battle.sides:
            for unit in side_units:
                from engine.gui.gui_unit_graphics_item import UnitGraphicsItem
                item = UnitGraphicsItem(unit, self.tile_size)
                self.scene.addItem(item)
                self.unit_items.append(item)

    def update_tile(self, x, y):
        """
        Update the visual state of a single tile.
        Args:
            x (int): X coordinate.
            y (int): Y coordinate.
        """
        tile = self.battle.tiles[y][x]
        item = self.tile_items[(x, y)]
        color = QColor("lightgray") if tile.is_walkable() else QColor("darkgray")
        item.setBrush(color)

