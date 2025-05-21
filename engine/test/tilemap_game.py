from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PySide6.QtGui import QColor
from PySide6.QtCore import QRectF, Qt
from engine.battle.battle import TBattle
from engine.battle.tile.battle_tile import TBattleTile

class BattleMapView(QGraphicsView):
    """
    Visualizes the battle map and units using QGraphicsView/QGraphicsScene.
    Handles efficient drawing and updating of tiles and units.
    """
    def __init__(self, battle: TBattle, tile_size=16):
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
        self.unit_items.clear()
        for side_units in self.battle.sides:
            for unit in side_units:
                item = UnitGraphicsItem(unit, self.tile_size)
                self.scene.addItem(item)
                self.unit_items.append(item)

    def update_tile(self, x, y):
        tile = self.battle.tiles[y][x]
        item = self.tile_items[(x, y)]
        color = QColor("lightgray") if tile.is_walkable() else QColor("darkgray")
        item.setBrush(color)

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

class BattleInteractionController:
    """
    Handles user interaction (mouse, wheel, selection, path planning).
    """
    def __init__(self, map_view: BattleMapView, battle: TBattle):
        self.map_view = map_view
        self.battle = battle
        # Connect events as needed (to be implemented)

class BattlePathfinder:
    """
    Static pathfinding using TBattleTile.get_move_cost() and is_walkable().
    """
    @staticmethod
    def find_path(battle: TBattle, start, end, unit_size=1):
        # Implement A* using TBattleTile
        pass

class BattleLOS:
    """
    Static LOS calculation using tile properties (floor, wall, smoke, fire).
    """
    @staticmethod
    def has_los(battle: TBattle, start, end):
        # Implement Bresenham or similar, using tile.get_sight_cost(), wall, smoke, fire
        pass

