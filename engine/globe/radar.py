"""
radar.py

Defines the TGlobalRadar class, which manages radar detection of UFOs and locations on the world map. Handles radar scanning from bases and crafts, updating cover and visibility for all locations.

Classes:
    TGlobalRadar: Global radar detection manager.

Last standardized: 2025-06-14
"""

from engine.globe.world_point import TWorldPoint

class TGlobalRadar:
    """
    TGlobalRadar manages radar detection of UFOs and locations on the world map.

    Attributes:
        world: TWorld instance representing the world map.
    """
    def __init__(self, world):
        """
        Initialize a TGlobalRadar instance.

        Args:
            world: TWorld instance.
        """
        self.world = world

    def scan(self, locations, bases, crafts):
        """
        Perform radar scan from all bases and crafts, update cover and visibility for all locations.

        Args:
            locations (list): List of TLocation instances.
            bases (list): List of XCOM base objects (must provide get_radar_facilities()).
            crafts (list): List of XCOM craft objects (must provide radar_power, radar_range, and position).
        """
        # 1. Scan from bases
        for base in bases:
            radar_list = base.get_radar_facilities()  # Each should have .power and .range
            base_pos = TWorldPoint.from_iterable(base.position)
            for radar in radar_list:
                for loc in locations:
                    if loc.name.startswith('XCOM'):  # skip xcom bases/crafts
                        continue
                    if not loc.position:
                        continue
                    loc_pos = TWorldPoint.from_iterable(loc.position)
                    if base_pos.tile_distance(loc_pos) <= radar.range:
                        loc.cover = max(0, loc.cover - radar.power)
                        loc.update_visibility()

        # 2. Scan from crafts
        for craft in crafts:
            if not craft.is_on_world():
                continue
            craft_pos = TWorldPoint.from_iterable(craft.position)
            radar_power = getattr(craft, 'radar_power', 0)
            radar_range = getattr(craft, 'radar_range', 0)
            for loc in locations:
                if loc.name.startswith('XCOM'):
                    continue
                if not loc.position:
                    continue
                loc_pos = TWorldPoint.from_iterable(loc.position)
                if craft_pos.tile_distance(loc_pos) <= radar_range:
                    loc.cover = max(0, loc.cover - radar_power)
                    loc.update_visibility()

        # 3. Replenish cover for all locations
        for loc in locations:
            loc.replenish_cover()
