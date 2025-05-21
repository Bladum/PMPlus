class TGlobalRadar:
    """
    Manage radar / detection of UFOs and locations
    """
    def __init__(self, world):
        self.world = world  # TWorld instance

    def scan(self, locations, bases, crafts):
        """
        Perform radar scan from all bases and crafts, update cover and visibility for all locations.
        locations: list of TLocation
        bases: list of XCOM base objects (must provide get_radar_facilities())
        crafts: list of XCOM craft objects (must provide radar_power, radar_range, and position)
        """
        # Helper to compute tile distance
        def tile_distance(pos1, pos2):
            return max(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))

        # 1. Scan from bases
        for base in bases:
            radar_list = base.get_radar_facilities()  # Each should have .power and .range
            base_pos = base.position
            for radar in radar_list:
                for loc in locations:
                    if loc.name.startswith('XCOM'):  # skip xcom bases/crafts
                        continue
                    if not loc.position:
                        continue
                    if tile_distance(base_pos, loc.position) <= radar.range:
                        loc.cover = max(0, loc.cover - radar.power)
                        loc.update_visibility()

        # 2. Scan from crafts
        for craft in crafts:
            if not craft.is_on_world():
                continue
            craft_pos = craft.position
            radar_power = getattr(craft, 'radar_power', 0)
            radar_range = getattr(craft, 'radar_range', 0)
            for loc in locations:
                if loc.name.startswith('XCOM'):
                    continue
                if not loc.position:
                    continue
                if tile_distance(craft_pos, loc.position) <= radar_range:
                    loc.cover = max(0, loc.cover - radar_power)
                    loc.update_visibility()

        # 3. Replenish cover for all locations
        for loc in locations:
            loc.replenish_cover()
