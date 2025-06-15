"""
BattlePathfinder: Provides static pathfinding for battle map tiles using the A* algorithm and tile walkability.

Implements pathfinding logic for units, considering movement cost, walkability, and unit size.

Classes:
    BattlePathfinder: Main class for static pathfinding.

Last standardized: 2025-06-14
"""

class BattlePathfinder:
    """
    Static pathfinding using TBattleTile.get_move_cost() and is_walkable().
    Implements A* algorithm for pathfinding.
    """
    @staticmethod
    def find_path(battle, start, end, unit_size=1):
        """
        Find a path from start to end on the battle map using the A* algorithm.
        Args:
            battle: Battle object containing map tiles.
            start (tuple): (x, y) start coordinates.
            end (tuple): (x, y) end coordinates.
            unit_size (int): Size of the unit (default 1).
        Returns:
            list: List of (x, y) tuples representing the path, or empty list if no path found.
        """
        from queue import PriorityQueue
        import math
        width, height = battle.width, battle.height
        def heuristic(x1, y1, x2, y2):
            return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        def can_unit_fit(x, y):
            if x + unit_size > width or y + unit_size > height:
                return False
            for dy in range(unit_size):
                for dx in range(unit_size):
                    tile = battle.tiles[y + dy][x + dx]
                    if not tile.is_walkable():
                        return False
            return True
        directions = [
            (0, 1), (1, 0), (0, -1), (-1, 0),
            (1, 1), (-1, -1), (1, -1), (-1, 1)
        ]
        direction_costs = [1.0, 1.0, 1.0, 1.0, 1.5, 1.5, 1.5, 1.5]
        visited = set()
        queue = PriorityQueue()
        queue.put((0, start[0], start[1], [], 0))
        while not queue.empty():
            priority, x, y, path, path_cost = queue.get()
            if (x, y) == end:
                return path + [end]
            if (x, y) in visited:
                continue
            visited.add((x, y))
            for i, (dx, dy) in enumerate(directions):
                nx, ny = x + dx, y + dy
                move_cost = direction_costs[i]
                if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited and can_unit_fit(nx, ny):
                    new_path = path + [(nx, ny)]
                    new_cost = path_cost + move_cost
                    priority = new_cost + heuristic(nx, ny, end[0], end[1])
                    queue.put((priority, nx, ny, new_path, new_cost))
        return []
