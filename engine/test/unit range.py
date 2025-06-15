"""
Projectile and FloatingNumber: Visual test classes for projectile motion and floating text in PySide6.

Provides a testbed for animating projectiles and floating numbers in a QGraphicsScene, useful for XCOM/AlienFall engine effects.

Classes:
    Projectile: Visual representation of a projectile.
    FloatingNumber: Animated floating number for damage/effects.

Last standardized: 2025-06-14
"""

from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsEllipseItem
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtCore import Qt, QRectF, QTimer, QTime
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QPoint, Property
from PySide6.QtWidgets import QGraphicsTextItem


class Projectile(QGraphicsEllipseItem):
    """
    Visual representation of a projectile in the scene.
    """

    def __init__(self, x, y, size=3):
        super().__init__(0, 0, size, size)  # Create at origin with size 3x3
        self.setBrush(QColor(0, 0, 0))      # Black color
        self.setPen(Qt.NoPen)               # No border
        self.setPos(x - size/2, y - size/2) # Center the circle at x,y
        self.setZValue(2000)                # Make sure it's above everything


class FloatingNumber(QGraphicsTextItem):
    """
    Animated floating number for displaying damage or effects.
    """

    def __init__(self, text, x, y, color=Qt.red, font_size=12):
        super().__init__(text)
        # Set up appearance
        font = self.font()
        font.setPointSize(font_size)
        self.setFont(font)
        self.setDefaultTextColor(color)

        # Position the item
        self.setPos(x, y)

        # Set up animation
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(2000)  # 2 seconds
        self.animation.setStartValue(QPoint(x, y))
        self.animation.setEndValue(QPoint(x, y - 64))  # Move up 64 pixels
        self.animation.setEasingCurve(QEasingCurve.OutQuad)

        # Set up fade out effect
        self.fade_animation = QPropertyAnimation(self, b"opacity")
        self.fade_animation.setDuration(2000)  # 2 seconds
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.setEasingCurve(QEasingCurve.InQuad)

        # Connect animation finished signal to remove the item
        self.animation.finished.connect(self.remove_item)

    def remove_item(self):
        # Remove this item from the scene
        if self.scene():
            self.scene().removeItem(self)

    def start(self):
        # Start both animations
        self.animation.start()
        self.fade_animation.start()

    # Define property for QPropertyAnimation to animate opacity
    def _set_opacity(self, opacity):
        self.setOpacity(opacity)

    def _get_opacity(self):
        return self.opacity()

    opacity = Property(float, _get_opacity, _set_opacity)


class BattleTile(QGraphicsRectItem):
    def __init__(self, x, y, size=16):
        super().__init__(x, y, size, size)
        self.setBrush(QColor(200, 200, 200))  # Light gray color
        self.setPen(Qt.NoPen)  # Remove border for performance
        self.row = int(y / size)
        self.col = int(x / size)
        # Disable hover events for performance
        self.setAcceptHoverEvents(False)


class MapBlock:
    def __init__(self, scene, start_x, start_y, tile_size=16, block_size=10):
        self.scene = scene
        self.start_x = start_x
        self.start_y = start_y
        self.tile_size = tile_size
        self.block_size = block_size
        self.tiles = []
        self.create_block()

    def create_block(self):
        # Create tiles in a batch for better performance
        for row in range(self.block_size):
            for col in range(self.block_size):
                x = self.start_x + col * self.tile_size
                y = self.start_y + row * self.tile_size
                tile = BattleTile(x, y, self.tile_size)
                self.scene.addItem(tile)
                self.tiles.append(tile)


class BattleScape(QGraphicsView):
    def __init__(self, map_blocks_y=8, map_blocks_x = 4, block_size=10, tile_size=16):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.map_blocks_x = map_blocks_x
        self.map_blocks_y = map_blocks_y
        self.block_size = block_size
        self.tile_size = tile_size

        # Turn off antialiasing for performance
        self.setRenderHint(QPainter.Antialiasing, False)

        # Optimize view settings for performance
        self.setViewportUpdateMode(QGraphicsView.MinimalViewportUpdate)
        self.setOptimizationFlags(QGraphicsView.DontAdjustForAntialiasing |
                                  QGraphicsView.DontSavePainterState)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setDragMode(QGraphicsView.NoDrag)

        # Enable mouse tracking for hover detection
        self.setMouseTracking(True)

        # Disable transformations for better performance
        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setResizeAnchor(QGraphicsView.NoAnchor)

        self.selected_tile = None
        self.hover_tile = None
        self.hover_highlight = None
        self.range_radius = 20

        # Create the battlescape
        self.create_battlescape()

        total_width = self.map_blocks_x * self.block_size * self.tile_size
        total_height = self.map_blocks_y * self.block_size * self.tile_size
        self.scene.setSceneRect(0, 0, total_width, total_height)

        # Create hover highlight rectangle
        self.hover_highlight = QGraphicsRectItem(0, 0, self.tile_size, self.tile_size)
        self.hover_highlight.setPen(QPen(QColor(255, 255, 0), 2))  # Yellow border, 2px width
        self.hover_highlight.setBrush(Qt.NoBrush)  # No fill
        self.hover_highlight.setZValue(1000)  # Ensure it's above other items
        self.hover_highlight.setVisible(False)
        self.scene.addItem(self.hover_highlight)

    def mouseMoveEvent(self, event):
        # Get the current mouse position in scene coordinates
        scene_pos = self.mapToScene(event.pos())

        # Find the tile under the cursor
        items = self.scene.items(scene_pos)
        current_hover_tile = None

        for item in items:
            if isinstance(item, BattleTile):
                current_hover_tile = item
                break

        # Update highlight position if we're hovering over a tile
        if current_hover_tile:
            # Force the highlight to exactly match the tile's position
            tile_x = current_hover_tile.col * self.tile_size
            tile_y = current_hover_tile.row * self.tile_size

            # Ensure the highlight is properly positioned and visible
            self.hover_highlight.setPos(0, 0)  # Reset position before setting rect
            self.hover_highlight.setRect(tile_x, tile_y, self.tile_size, self.tile_size)
            self.hover_highlight.setVisible(True)
            self.hover_tile = current_hover_tile
        else:
            self.hover_highlight.setVisible(False)
            self.hover_tile = None

        # Update the view to ensure the highlight is drawn
        self.scene.update(self.hover_highlight.sceneBoundingRect())
        super().mouseMoveEvent(event)

    def create_battlescape(self):
        for block_row in range(self.map_blocks_x):
            for block_col in range(self.map_blocks_y):
                start_x = block_col * self.block_size * self.tile_size
                start_y = block_row * self.block_size * self.tile_size
                MapBlock(self.scene, start_x, start_y, self.tile_size, self.block_size)

    def wheelEvent(self, event):
        # Use a simple zoom without complicated transformations
        zoom_factor = 1.2
        if event.angleDelta().y() > 0:
            self.scale(zoom_factor, zoom_factor)
        else:
            self.scale(1 / zoom_factor, 1 / zoom_factor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            scene_pos = self.mapToScene(event.pos())
            items = self.scene.items(scene_pos)
            for item in items:
                if isinstance(item, BattleTile):
                    self.selected_tile = item
                    self.reset_all_tiles()
                    self.selected_tile.setBrush(QColor(255, 0, 0))
                    self.select_tiles_in_range(self.selected_tile, self.range_radius)

                    # Add floating damage number at click position
                    damage_number = FloatingNumber("8", self.selected_tile.col * 16, self.selected_tile.row * 16,
                                                   color=Qt.black, font_size=10)
                    self.scene.addItem(damage_number)
                    damage_number.start()
                    break
        elif event.button() == Qt.RightButton and self.selected_tile:
            # Handle right mouse button click - create projectile
            scene_pos = self.mapToScene(event.pos())
            target_items = self.scene.items(scene_pos)

            # Find target tile
            target_tile = None
            for item in target_items:
                if isinstance(item, BattleTile):
                    target_tile = item
                    break

            if target_tile and target_tile != self.selected_tile:
                self.animate_projectile(self.selected_tile, target_tile)

        super().mousePressEvent(event)

    def animate_projectile(self, source_tile, target_tile):
        # Calculate center points
        source_x = source_tile.col * self.tile_size + (self.tile_size / 2)
        source_y = source_tile.row * self.tile_size + (self.tile_size / 2)
        target_x = target_tile.col * self.tile_size + (self.tile_size / 2)
        target_y = target_tile.row * self.tile_size + (self.tile_size / 2)

        # Create a line item
        from PySide6.QtGui import QPen, QColor
        from PySide6.QtWidgets import QGraphicsLineItem

        line = QGraphicsLineItem(source_x, source_y, target_x, target_y)

        # Set line appearance
        pen = QPen(QColor(255, 0, 0))  # Red color
        pen.setWidth(3)
        pen.setCapStyle(Qt.RoundCap)
        line.setPen(pen)
        line.setZValue(2000)  # Make sure it's above everything

        # Enable antialiasing for this item
        line.setCacheMode(QGraphicsLineItem.DeviceCoordinateCache)

        # Add projectile impact point at target location
        impact = QGraphicsEllipseItem(target_x - 4, target_y - 4, 8, 8)
        impact.setBrush(QColor(255, 200, 0))  # Orange-yellow color
        impact.setPen(QPen(QColor(255, 0, 0), 1))  # Red border
        impact.setZValue(2001)  # Above the line
        self.scene.addItem(impact)


        # Add the line to the scene
        self.scene.addItem(line)

        # Create animations for the line
        # We'll keep the line visible for 2 seconds total
        # The last 500ms will be used for fading out

        # Create a timer to handle the fading
        timer = QTimer()
        start_time = 0
        total_duration = 600  # 2 seconds
        fade_duration = 300  # Last 0.5 seconds for fading

        def update_line():
            nonlocal start_time

            # Start the timer if it's the first call
            if start_time == 0:
                start_time = QTime.currentTime().msecsSinceStartOfDay()
                return

            # Calculate elapsed time
            current_time = QTime.currentTime().msecsSinceStartOfDay()
            elapsed = current_time - start_time

            # Check if animation should end
            if elapsed >= total_duration:
                timer.stop()
                self.scene.removeItem(line)
                self.scene.removeItem(impact)

                # Create an explosion effect
                explosion = QGraphicsEllipseItem(target_x - 8, target_y - 8, 16, 16)
                explosion.setBrush(QColor(255, 165, 0, 180))  # Semi-transparent orange
                explosion.setPen(QPen(QColor(255, 0, 0, 200), 2))  # Semi-transparent red border
                explosion.setZValue(2002)  # Above everything
                self.scene.addItem(explosion)

                # Remove explosion after a short delay
                QTimer.singleShot(100, lambda: self.scene.removeItem(explosion))
                return

            # Start fading only in the last 0.5 seconds
            if elapsed >= (total_duration - fade_duration):
                # Calculate opacity based on time remaining
                time_remaining = total_duration - elapsed
                opacity = time_remaining / fade_duration

                # Update line appearance
                pen = line.pen()
                color = pen.color()
                color.setAlphaF(opacity)
                pen.setColor(color)
                line.setPen(pen)

                # Also fade the impact point
                impact_pen = impact.pen()
                impact_color = impact_pen.color()
                impact_color.setAlphaF(opacity)
                impact_pen.setColor(impact_color)
                impact.setPen(impact_pen)

                impact_brush = impact.brush()
                impact_brush_color = impact_brush.color()
                impact_brush_color.setAlphaF(opacity)
                impact_brush.setColor(impact_brush_color)
                impact.setBrush(impact_brush)

                # Force update of both items
                self.scene.update(line.boundingRect().united(impact.boundingRect()))
            # No else branch needed - for the first 1.5s we do nothing

        # Connect timer to update function and start
        timer.timeout.connect(update_line)
        timer.start(25)  # Less frequent updates (20fps) are sufficient for this effect


    def reset_all_tiles(self):
        # Use scene.update() less frequently
        for item in self.scene.items():
            if isinstance(item, BattleTile):
                item.setBrush(QColor(200, 200, 200))

    def select_tiles_in_range(self, center_tile, range_cells):
        if not center_tile:
            return

        center_row = center_tile.row
        center_col = center_tile.col

        # Distance calculation constants
        CIRCLE_OFFSET = 0.5# 1.7 # Makes the circle more visually round on a grid=

        range_squared = (range_cells + CIRCLE_OFFSET) ** 2

        # Optimize range calculation by pre-calculating grid boundaries
        min_row = max(0, center_row - range_cells)
        max_row = min(center_row + range_cells, self.map_blocks_x * self.block_size)
        min_col = max(0, center_col - range_cells)
        max_col = min(center_col + range_cells, self.map_blocks_y * self.block_size)

        print("Range is", range_cells, "from", center_row, center_col)

        # Process only items within the bounding box
        for item in self.scene.items():
            if isinstance(item, BattleTile):
                if item == center_tile:
                    continue

                if min_row <= item.row <= max_row and min_col <= item.col <= max_col:
                    dr = item.row - center_row
                    dc = item.col - center_col

                    # Standard circular distance with slight visual adjustment
                    distance = dr * dr + dc * dc
                    in_range = distance <= range_squared

                    if in_range:
                        item.setBrush(QColor(255, 90, 0))

    def keyPressEvent(self, event):
        """Allow adjusting range with + and - keys"""
        if event.key() == Qt.Key_Plus or event.key() == Qt.Key_Equal:
            self.range_radius += 1
            if self.selected_tile:
                self.reset_all_tiles()
                self.selected_tile.setBrush(QColor(255, 0, 0))
                self.select_tiles_in_range(self.selected_tile, self.range_radius)
        elif event.key() == Qt.Key_Minus:
            if self.range_radius > 1:
                self.range_radius -= 1
                if self.selected_tile:
                    self.reset_all_tiles()
                    self.selected_tile.setBrush(QColor(255, 0, 0))
                    self.select_tiles_in_range(self.selected_tile, self.range_radius)
        super().keyPressEvent(event)

    def select_single_tile(self, row, col):
        """Select a single tile and color it red"""
        self.reset_all_tiles()

        # Find and color the selected tile
        for item in self.scene.items():
            if isinstance(item, BattleTile):
                if item.row == row and item.col == col:
                    item.setBrush(QColor(255, 0, 0))  # Red
                    self.selected_tile = item
                    return item
        return None

if __name__ == "__main__":
    app = QApplication([])
    battlescape = BattleScape(map_blocks_x=7, map_blocks_y=7, block_size=15, tile_size=16)
    battlescape.setWindowTitle("X-COM Battlescape")
    battlescape.resize(800, 600)
    battlescape.show()

    # Example of selecting a specific tile (row 5, column 5)
    center_tile = battlescape.select_single_tile(8, 13)
    # Select all tiles within range 20 from the center tile
    battlescape.select_tiles_in_range(center_tile, 20)

    app.exec()

