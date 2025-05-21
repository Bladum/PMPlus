class BattleLOS:
    """
    Static LOS calculation using tile properties (floor, wall, smoke, fire).
    Implements Bresenham's line algorithm and checks tile sight cost, wall, smoke, fire.
    """
    @staticmethod
    def has_los(battle, start, end, max_range=22):
        x0, y0 = start
        x1, y1 = end
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        range_sq = max_range * max_range
        dist_sq = (x1 - x0) ** 2 + (y1 - y0) ** 2
        if dist_sq > range_sq:
            return False
        while True:
            tile = battle.tiles[y0][x0]
            # Check for wall or high sight cost (opaque)
            if tile.wall and tile.wall.sight_mod >= 100:
                return False
            # Check for smoke/fire/gas
            if tile.smoke or tile.fire or tile.gas:
                return False
            if (x0, y0) == (x1, y1):
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
        return True

