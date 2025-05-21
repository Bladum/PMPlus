from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QColor


class TileMapGame(QGraphicsView):
    """
    Main game class representing a tactical grid-based game similar to XCOM.
    Handles rendering, unit selection, pathfinding and line of sight calculations.
    """
    def __init__(self):
        """
        Initialize the game with map, units and visual elements.
        Sets up the graphics scene, initializes the tile map and units.
        """
        super().__init__()

        # Constants
        self.TILE_SIZE = 16
        self.MAP_WIDTH = 20 * 6
        self.MAP_HEIGHT = 20 * 6

        # Variables for unit selection and pathfinding
        self.selected_unit = None
        self.path = []  # Initialize path to avoid AttributeError
        self.units = []  # List to store multiple units
        self.tile_items = {}  # Cache for tile items
        self.path_items = []  # Cache for path items

        # Initialize scene
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        # Enable resizing
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Create tilemap
        self.tilemap = [[0 for _ in range(self.MAP_WIDTH)] for _ in range(self.MAP_HEIGHT)]
        self.add_random_blocks()

        # Draw tilemap first
        self.draw_tilemap()

        # Then create units
        self.add_units()

    def add_random_blocks(self):
        """
        Add random blocks (obstacles) to the map.
        Blocks come in different sizes and are placed randomly across the map.
        """
        import random
        for _ in range(300):  # Add 300 random blocks
            block_type = random.choice([(3, 3), (5, 4), (12, 1), (6, 1), (7, 2), (2, 7)])
            x = random.randint(0, self.MAP_WIDTH - block_type[0])
            y = random.randint(0, self.MAP_HEIGHT - block_type[1])
            for dy in range(block_type[1]):
                for dx in range(block_type[0]):
                    self.tilemap[y + dy][x + dx] = 1

    def add_units(self):
        """
        Add units of different sizes to the map.
        Units are placed randomly in valid positions (not overlapping with blocks or other units).
        Unit configurations specify size and quantity of each unit type.
        """
        import random

        # Define unit sizes and quantities
        unit_configs = [
            (2, 3),  # 3 units of size 2x2
            (1, 2),  # 2 units of size 1x1
            (3, 1),  # 1 unit of size 3x3
            (4, 2)   # 2 units of size 4x4
        ]

        # Clear existing units if any
        self.units = []

        for size, count in unit_configs:
            for _ in range(count):
                # Try to find a valid position for the unit
                max_attempts = 50  # Limit attempts to avoid infinite loop
                for attempt in range(max_attempts):
                    # Random position within map boundaries
                    x = random.randint(0, self.MAP_WIDTH - size)
                    y = random.randint(0, self.MAP_HEIGHT - size)

                    # Check if position is valid (no blocks)
                    valid_position = True
                    for dy in range(size):
                        for dx in range(size):
                            if self.tilemap[y + dy][x + dx] != 0:
                                valid_position = False
                                break
                        if not valid_position:
                            break

                    # Check for overlap with existing units
                    for unit in self.units:
                        if (x < unit.x + unit.width and
                            x + size > unit.x and
                            y < unit.y + unit.height and
                            y + size > unit.y):
                            valid_position = False
                            break

                    if valid_position:
                        # Create the unit and add it
                        unit = MultiTileUnit(size, size, x, y, self.TILE_SIZE)

                        # Remove blocks where the unit is placed
                        for dy in range(unit.height):
                            for dx in range(unit.width):
                                if 0 <= y + dy < self.MAP_HEIGHT and 0 <= x + dx < self.MAP_WIDTH:
                                    self.tilemap[y + dy][x + dx] = 0

                        self.units.append(unit)
                        self.scene.addItem(unit)
                        break

    def draw_tilemap(self):
        """
        Draw or update the tilemap visualization.
        Creates visual representations of tiles, path, and final destination.
        Handles different states of tiles (empty, blocked) and path visualization (green for path, yellow for destination).
        """
        # Update or create tiles
        for y in range(self.MAP_HEIGHT):
            for x in range(self.MAP_WIDTH):
                if (x, y) not in self.tile_items:
                    rect = QRectF(x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                    tile = QGraphicsRectItem(rect)
                    self.scene.addItem(tile)
                    self.tile_items[(x, y)] = tile

                tile = self.tile_items[(x, y)]
                if self.tilemap[y][x] == 0:
                    tile.setBrush(QColor("lightgray"))
                    tile.setPen(Qt.NoPen)  # Remove border for empty tiles
                else:
                    tile.setBrush(QColor("darkgray"))
                    tile.setPen(QColor("black"))  # Add border only for solid blocks

        # Update path visualization
        for item in self.path_items:
            self.scene.removeItem(item)
        self.path_items.clear()

        if self.path and self.selected_unit:
            unit_width = self.selected_unit.width
            unit_height = self.selected_unit.height

            # Get all unit positions to avoid drawing path on them
            unit_positions = set()
            for unit in self.units:
                for dy in range(unit.height):
                    for dx in range(unit.width):
                        unit_positions.add((unit.x + dx, unit.y + dy))

            # Check if final position overlaps with blocks or other units
            end_x, end_y = self.path[-1]
            can_fit_at_destination = True

            # Check if the unit can fit at the destination (not overlapping with blocks or other units)
            for dy in range(unit_height):
                for dx in range(unit_width):
                    dest_x, dest_y = end_x + dx, end_y + dy

                    # Check if out of bounds
                    if not (0 <= dest_x < self.MAP_WIDTH and 0 <= dest_y < self.MAP_HEIGHT):
                        can_fit_at_destination = False
                        break

                    # Check if overlapping with a block
                    if self.tilemap[dest_y][dest_x] != 0:
                        can_fit_at_destination = False
                        break

                    # Check if overlapping with another unit (excluding the selected unit)
                    if (dest_x, dest_y) in unit_positions and not self.selected_unit.contains_tile(dest_x, dest_y):
                        can_fit_at_destination = False
                        break

                if not can_fit_at_destination:
                    break

            # Process all path points except the last one (with green color)
            for i, (px, py) in enumerate(self.path[:-1]):
                # Draw path tiles that match unit size
                for dy in range(unit_height):
                    for dx in range(unit_width):
                        # Skip if position is occupied by any unit
                        if (px + dx, py + dy) in unit_positions:
                            continue

                        if 0 <= px + dx < self.MAP_WIDTH and 0 <= py + dy < self.MAP_HEIGHT:
                            rect = QRectF((px + dx) * self.TILE_SIZE, (py + dy) * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                            path_tile = QGraphicsRectItem(rect)
                            path_tile.setBrush(QColor("green"))
                            self.scene.addItem(path_tile)
                            self.path_items.append(path_tile)

            # Process the last point in the path (with yellow color if valid position)
            if self.path and can_fit_at_destination:
                px, py = self.path[-1]
                for dy in range(unit_height):
                    for dx in range(unit_width):
                        # Skip if position is occupied by any unit
                        if (px + dx, py + dy) in unit_positions:
                            continue

                        if 0 <= px + dx < self.MAP_WIDTH and 0 <= py + dy < self.MAP_HEIGHT:
                            rect = QRectF((px + dx) * self.TILE_SIZE, (py + dy) * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                            path_tile = QGraphicsRectItem(rect)
                            path_tile.setBrush(QColor("yellow"))
                            self.scene.addItem(path_tile)
                            self.path_items.append(path_tile)
            elif self.path:
                # If final position isn't valid, show it in red to indicate it's not a valid destination
                px, py = self.path[-1]
                for dy in range(unit_height):
                    for dx in range(unit_width):
                        # Skip if position is occupied by any unit
                        if (px + dx, py + dy) in unit_positions:
                            continue

                        if 0 <= px + dx < self.MAP_WIDTH and 0 <= py + dy < self.MAP_HEIGHT:
                            rect = QRectF((px + dx) * self.TILE_SIZE, (py + dy) * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                            path_tile = QGraphicsRectItem(rect)
                            path_tile.setBrush(QColor("red"))
                            path_tile.setOpacity(0.5)  # Make it semi-transparent
                            self.scene.addItem(path_tile)
                            self.path_items.append(path_tile)

        # Ensure units are updated in the scene
        for unit in self.units:
            if unit not in self.scene.items():
                self.scene.addItem(unit)

    def wheelEvent(self, event):
        """
        Handle mouse wheel events for zooming in and out.
        Zooming is centered on the current view position.
        """
        zoom_factor = 1.2 if event.angleDelta().y() > 0 else 0.8
        self.scale(zoom_factor, zoom_factor)

    def mousePressEvent(self, event):
        """
        Handle mouse press events for unit selection and path planning.
        Left-click: Select or deselect units
        Right-click: Plan path for selected unit to target position or move unit to path destination

        For right-click, the target position is adjusted so the center of the unit
        is placed at the clicked location.
        """
        scene_pos = self.mapToScene(event.pos())
        x, y = int(scene_pos.x() // self.TILE_SIZE), int(scene_pos.y() // self.TILE_SIZE)

        if event.button() == Qt.MouseButton.LeftButton:
            for unit in self.units:
                if unit.contains_tile(x, y):
                    # If we're selecting a different unit than the previously selected one
                    if self.selected_unit and self.selected_unit != unit:
                        self.selected_unit.set_selected(False)
                        # Clear the path when selecting a different unit
                        self.path = []

                    self.selected_unit = unit
                    self.selected_unit.set_selected(True)

                    # Najpierw odświeżamy mapę, aby usunąć poprzednie wizualizacje
                    self.draw_tilemap()

                    # Potem pokazujemy pole widzenia jednostki (po odświeżeniu mapy)
                    self.highlight_line_of_sight()
                    return

            # If clicking on empty space
            if self.selected_unit:
                self.selected_unit.set_selected(False)
                self.selected_unit = None  # Deselect if clicking empty space
                self.path = []  # Clear path when deselecting
                self.draw_tilemap()  # Redraw to clear path visualization

        elif event.button() == Qt.MouseButton.RightButton and self.selected_unit:
            # Sprawdź, czy kliknięto w końcowy punkt istniejącej ścieżki (żółte pole)
            if self.path and self.is_end_point_clicked(x, y):
                # Pobierz końcowy punkt ścieżki
                end_x, end_y = self.path[-1]

                # Przenieś jednostkę na końcową pozycję ścieżki
                self.selected_unit.move_to(end_x, end_y)

                # Wyczyść ścieżkę
                self.path = []

                # Odświeżamy mapę bez ścieżki
                self.draw_tilemap()

                # Zaktualizuj pole widzenia dla nowej pozycji jednostki
                self.highlight_line_of_sight()
            else:
                # Oblicz docelowe położenie lewego górnego rogu jednostki tak, aby środek znalazł się w miejscu kliknięcia
                # Odejmujemy połowę szerokości i wysokości jednostki
                target_x = x - self.selected_unit.width // 2
                target_y = y - self.selected_unit.height // 2

                # Upewniamy się, że jednostka nie wyjdzie poza mapę
                target_x = max(0, min(target_x, self.MAP_WIDTH - self.selected_unit.width))
                target_y = max(0, min(target_y, self.MAP_HEIGHT - self.selected_unit.height))

                # Calculate path to the adjusted target position
                self.path = self.calculate_path(self.selected_unit.x, self.selected_unit.y, target_x, target_y)
                self.draw_tilemap()  # Redraw the tilemap with the new path

                # Pokaż pole widzenia po narysowaniu ścieżki
                self.highlight_line_of_sight()

    def is_end_point_clicked(self, x, y):
        """
        Check if the coordinates (x,y) are within the destination area of the path.
        The destination area is the yellow-colored area at the end of the path.

        Args:
            x, y: Coordinates to check

        Returns:
            Boolean indicating whether the coordinates are in the destination area
        """
        if not self.path:
            return False

        # Check if the path is valid (ending in yellow, not red)
        end_x, end_y = self.path[-1]
        # Check if the path ends at a position where the unit can actually fit
        # by verifying if the end position was rendered in yellow (valid) rather than red (invalid)

        # Get all unit positions to avoid drawing path on them
        unit_positions = set()
        for unit in self.units:
            # Skip the selected unit, as it will be moved
            if unit == self.selected_unit:
                continue
            for dy in range(unit.height):
                for dx in range(unit.width):
                    unit_positions.add((unit.x + dx, unit.y + dy))

        unit_width = self.selected_unit.width
        unit_height = self.selected_unit.height

        # Check if the destination is blocked by another unit or obstacle
        can_fit_at_destination = True
        for dy in range(unit_height):
            for dx in range(unit_width):
                dest_x, dest_y = end_x + dx, end_y + dy
                # Check if out of bounds
                if not (0 <= dest_x < self.MAP_WIDTH and 0 <= dest_y < self.MAP_HEIGHT):
                    can_fit_at_destination = False
                    break
                # Check if overlapping with a block
                if self.tilemap[dest_y][dest_x] != 0:
                    can_fit_at_destination = False
                    break
                # Check if overlapping with another unit
                if (dest_x, dest_y) in unit_positions:
                    can_fit_at_destination = False
                    break
            if not can_fit_at_destination:
                break

        # Only return true if the destination is valid and the clicked point is within it
        if can_fit_at_destination and end_x <= x < end_x + unit_width and end_y <= y < end_y + unit_height:
            return True
        return False

    def mouseMoveEvent(self, event):
        """
        Handle mouse move events for highlighting tiles under the cursor.
        Shows yellow outlines for tiles that are within line of sight of the selected unit.
        """
        scene_pos = self.mapToScene(event.pos())
        x, y = int(scene_pos.x() // self.TILE_SIZE), int(scene_pos.y() // self.TILE_SIZE)

        if self.selected_unit:
            unit_x, unit_y = self.selected_unit.x, self.selected_unit.y
            range_of_sight = 1

            def is_in_sight(x, y):
                """
                Determine if a tile at (x,y) is in sight of the unit.
                Uses Bresenham's line algorithm to check for obstacles between the unit and target.
                """
                dx, dy = x - unit_x, y - unit_y
                distance_squared = dx * dx + dy * dy
                if distance_squared > range_of_sight * range_of_sight:
                    return False

                # Use Bresenham's line algorithm for accurate line of sight
                x0, y0, x1, y1 = unit_x, unit_y, x, y
                steep = abs(y1 - y0) > abs(x1 - x0)
                if steep:
                    x0, y0 = y0, x0
                    x1, y1 = y1, x1
                if x0 > x1:
                    x0, x1 = x1, x0
                    y0, y1 = y1, y0
                dx = x1 - x0
                dy = abs(y1 - y0)
                error = dx / 2
                ystep = 1 if y0 < y1 else -1
                y = y0

                for x in range(x0, x1 + 1):
                    coord = (y, x) if steep else (x, y)
                    if self.tilemap[coord[1]][coord[0]] == 1:
                        return False
                    error -= dy
                    if error < 0:
                        y += ystep
                        error += dx

                return True

            if is_in_sight(x, y):
                tile = self.tile_items.get((x, y))
                if tile and isinstance(tile, QGraphicsRectItem):
                    tile.setPen(QColor("yellow"))  # Highlight the tile under the mouse

        super().mouseMoveEvent(event)

    def calculate_path(self, start_x, start_y, end_x, end_y):
        """
        Calculate the optimal path from start to end position using A* algorithm.
        Takes into account unit size for collision detection.
        Diagonal movement costs 1.5x more than orthogonal movement.

        Args:
            start_x, start_y: Starting position coordinates
            end_x, end_y: Target position coordinates

        Returns:
            List of (x,y) coordinates representing the path
        """
        from queue import PriorityQueue
        import math

        def heuristic(x1, y1, x2, y2):
            """
            Calculate heuristic distance between two points.
            Uses Euclidean distance for a more accurate estimation.
            """
            return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

        def can_unit_fit(x, y, unit_width, unit_height):
            """
            Check if a unit of given size can fit at position (x,y).
            Unit must be fully within map bounds and not overlap with any blocks.
            """
            if x + unit_width > self.MAP_WIDTH or y + unit_height > self.MAP_HEIGHT:
                return False
            for dy in range(unit_height):
                for dx in range(unit_width):
                    if self.tilemap[y + dy][x + dx] != 0:
                        return False
            return True

        # Define possible movement directions (orthogonal and diagonal)
        directions = [
            (0, 1), (1, 0), (0, -1), (-1, 0),  # Cardinal directions - cost 1.0
            (1, 1), (-1, -1), (1, -1), (-1, 1)  # Diagonal directions - cost 1.5
        ]

        # Define movement costs for each direction
        # Cardinal directions cost 1.0, diagonal directions cost 1.5
        direction_costs = [1.0, 1.0, 1.0, 1.0, 1.5, 1.5, 1.5, 1.5]

        visited = set()
        queue = PriorityQueue()
        queue.put((0, start_x, start_y, [], 0))  # (priority, x, y, path, path_cost)

        unit_width = self.selected_unit.width
        unit_height = self.selected_unit.height

        while not queue.empty():
            priority, x, y, path, path_cost = queue.get()
            if (x, y) == (end_x, end_y):
                return path + [(end_x, end_y)]  # Include the destination in the path

            if (x, y) in visited:
                continue
            visited.add((x, y))

            for i, (dx, dy) in enumerate(directions):
                nx, ny = x + dx, y + dy
                move_cost = direction_costs[i]  # Get the cost for this direction

                if 0 <= nx < self.MAP_WIDTH and 0 <= ny < self.MAP_HEIGHT and (nx, ny) not in visited and \
                        can_unit_fit(nx, ny, unit_width, unit_height):
                    new_path = path + [(nx, ny)]
                    new_cost = path_cost + move_cost
                    # Priority is based on total estimated cost: path_cost + heuristic
                    priority = new_cost + heuristic(nx, ny, end_x, end_y)
                    queue.put((priority, nx, ny, new_path, new_cost))

        return []

    def update_path_visualization(self):
        """
        Update the visual representation of the path.
        Removes old path items and draws new ones based on the current path.
        """
        # Clear only the path tiles
        items_to_remove = [item for item in self.scene.items()
                           if isinstance(item, QGraphicsRectItem) and item.brush().color() == QColor("green")]
        for item in items_to_remove:
            self.scene.removeItem(item)

        # Redraw the path tiles if path exists
        if self.path:
            for px, py in self.path:
                rect = QRectF(px * self.TILE_SIZE, py * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                path_tile = QGraphicsRectItem(rect)
                path_tile.setBrush(QColor("green"))
                self.scene.addItem(path_tile)

    def highlight_line_of_sight(self):
        """
        Highlight tiles that are within line of sight of the selected unit.
        Uses raycasting from unit corners to determine visibility.
        Adds blue borders to tiles in line of sight.
        """
        if not self.selected_unit:
            return

        # Keep track of tiles already in line of sight
        if not hasattr(self, 'previous_line_of_sight'):
            self.previous_line_of_sight = set()

        # Clear previous line of sight highlights for tiles no longer in sight
        for x, y in self.previous_line_of_sight:
            tile = self.tile_items.get((x, y))
            if tile and isinstance(tile, QGraphicsRectItem):
                if self.tilemap[y][x] == 0:
                    tile.setBrush(QColor("lightgray"))
                else:
                    tile.setBrush(QColor("darkgray"))
                tile.setPen(Qt.NoPen)  # Remove any previous border

        # Preserve path visualization
        for px, py in self.path:
            tile = self.tile_items.get((px, py))
            if tile and isinstance(tile, QGraphicsRectItem):
                tile.setBrush(QColor("green"))

        # Preserve unit visualization
        for unit in self.units:
            unit.update_appearance()

        # Calculate unit corners for sight calculation
        unit_corners = [
            (self.selected_unit.x + 0.5, self.selected_unit.y + 0.5),  # Top-left
            (self.selected_unit.x + self.selected_unit.width - 0.5, self.selected_unit.y + 0.5),  # Top-right
            (self.selected_unit.x + 0.5, self.selected_unit.y + self.selected_unit.height - 0.5),  # Bottom-left
            (self.selected_unit.x + self.selected_unit.width - 0.5, self.selected_unit.y + self.selected_unit.height - 0.5)  # Bottom-right
        ]

        # Calculate the center for distance calculation
        unit_center_x = self.selected_unit.x + self.selected_unit.width / 2
        unit_center_y = self.selected_unit.y + self.selected_unit.height / 2
        range_of_sight = 22

        def get_closest_edge_point(target_x, target_y):
            """
            Calculate the closest point on the unit's edge to the target.
            Ensures all units have the same effective sight range regardless of size.
            """
            closest_x = max(self.selected_unit.x, min(target_x, self.selected_unit.x + self.selected_unit.width))
            closest_y = max(self.selected_unit.y, min(target_y, self.selected_unit.y + self.selected_unit.height))
            return closest_x, closest_y

        def is_in_sight_from_point(target_x, target_y, source_x, source_y):
            """
            Determine if a target point is visible from a source point.
            Uses raycasting with Bresenham's algorithm to check for obstacles.

            Args:
                target_x, target_y: Target tile coordinates
                source_x, source_y: Source point coordinates (usually unit corner)

            Returns:
                Boolean indicating whether target is visible from source
            """
            # Use the center of target tile for calculations
            target_x_center = target_x + 0.5
            target_y_center = target_y + 0.5

            # Calculate the closest point on the unit's edge to the target
            # This ensures all units have the same effective sight range regardless of size
            closest_edge_point = get_closest_edge_point(target_x_center, target_y_center)

            # Check distance from the closest edge point for range limitation
            dx_edge = target_x_center - closest_edge_point[0]
            dy_edge = target_y_center - closest_edge_point[1]
            distance_squared = dx_edge * dx_edge + dy_edge * dy_edge
            if distance_squared > range_of_sight * range_of_sight:
                return False

            # Improved Bresenham's line algorithm with floating point precision
            # Algorithm source: http://www.roguebasin.com/index.php/Bresenham%27s_Line_Algorithm

            x1, y1 = source_x, source_y
            x2, y2 = target_x_center, target_y_center

            # Calculate the change in x and y
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)

            # Determine the sign of the increment
            sx = 1 if x1 < x2 else -1
            sy = 1 if y1 < y2 else -1

            # Initial error offset
            err = dx - dy

            # Go through the line points
            while True:
                # Skip the starting and ending points
                if (x1 != source_x or y1 != source_y) and (abs(x1 - target_x_center) > 0.1 or abs(y1 - target_y_center) > 0.1):
                    # Convert to grid coordinates
                    grid_x, grid_y = int(x1), int(y1)

                    # Check if it's within bounds
                    if 0 <= grid_x < self.MAP_WIDTH and 0 <= grid_y < self.MAP_HEIGHT:
                        # Check if there's a block
                        if self.tilemap[grid_y][grid_x] == 1:
                            return False
                    else:
                        # Out of bounds
                        return False

                # Break if we've reached the target (with a bit of tolerance for floating point comparison)
                if abs(x1 - x2) < 0.1 and abs(y1 - y2) < 0.1:
                    break

                # Calculate the next point
                e2 = 2 * err
                if e2 > -dy:
                    err -= dy
                    x1 += sx
                if e2 < dx:
                    err += dx
                    y1 += sy

            # If we've reached this point, there are no obstacles in the line of sight
            return True

        def get_best_corner(target_x, target_y):
            """
            Determine the best unit corner to use for line of sight calculation.
            Chooses the corner based on the quadrant the target is in relative to the unit.
            """
            quadrant_x = 1 if target_x >= unit_center_x else 0
            quadrant_y = 1 if target_y >= unit_center_y else 0
            corner_index = quadrant_y * 2 + quadrant_x
            return unit_corners[corner_index]

        # Highlight tiles in line of sight with a blue border
        new_line_of_sight = set()
        search_range_x_start = max(0, int(self.selected_unit.x - range_of_sight))
        search_range_x_end = min(self.MAP_WIDTH, int(self.selected_unit.x + self.selected_unit.width + range_of_sight))
        search_range_y_start = max(0, int(self.selected_unit.y - range_of_sight))
        search_range_y_end = min(self.MAP_HEIGHT, int(self.selected_unit.y + self.selected_unit.height + range_of_sight))

        for y in range(search_range_y_start, search_range_y_end):
            for x in range(search_range_x_start, search_range_x_end):
                # Skip block tiles and the unit's own tiles
                if not self.selected_unit.contains_tile(x, y) and self.tilemap[y][x] == 0:  # Only check non-block tiles
                    source_corner_x, source_corner_y = get_best_corner(x, y)
                    if is_in_sight_from_point(x, y, source_corner_x, source_corner_y):
                        new_line_of_sight.add((x, y))
                        tile = self.tile_items.get((x, y))
                        if tile and isinstance(tile, QGraphicsRectItem):
                            tile.setPen(QColor("blue"))  # Add a blue border

        # Update the previous line of sight
        self.previous_line_of_sight = new_line_of_sight


class MultiTileUnit(QGraphicsRectItem):
    """
    Represents a game unit that can occupy multiple tiles.
    Units can be of different sizes and can be selected and moved on the map.
    """
    def __init__(self, width, height, x, y, tile_size):
        """
        Initialize a new unit with specified dimensions and position.

        Args:
            width, height: Unit dimensions in tiles
            x, y: Unit position (top-left corner)
            tile_size: Size of each tile in pixels
        """
        super().__init__(x * tile_size, y * tile_size, width * tile_size, height * tile_size)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.selected = False
        self.update_appearance()

    def set_selected(self, selected):
        """
        Change the selection state of the unit.
        Updates visual appearance based on selection state.
        """
        self.selected = selected
        self.update_appearance()

    def update_appearance(self):
        """
        Update the visual appearance of the unit based on its selection state.
        Selected units are red, unselected units are blue.
        """
        self.setBrush(QColor("red") if self.selected else QColor("blue"))

    def move_to(self, x, y):
        """
        Move the unit to a new position.
        Updates both logical coordinates and visual representation.

        Args:
            x, y: New position coordinates (top-left corner)
        """
        self.x = x
        self.y = y
        self.setRect(self.x * self.tile_size, self.y * self.tile_size, self.width * self.tile_size, self.height * self.tile_size)

    def contains_tile(self, x, y):
        """
        Check if this unit contains a specific tile position.
        Used for unit selection and collision detection.

        Args:
            x, y: Tile coordinates to check

        Returns:
            Boolean indicating whether the unit contains the specified tile
        """
        return self.x <= x < self.x + self.width and self.y <= y < self.y + self.height


if __name__ == "__main__":
    app = QApplication([])
    game = TileMapGame()
    game.show()
    app.exec()

