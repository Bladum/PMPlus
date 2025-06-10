from engine.globe.radar import TGlobalRadar

def test_tglobalradar_scan():
    class DummyRadar:
        def __init__(self, power, range_):
            self.power = power; self.range = range_
    class DummyBase:
        def __init__(self, pos):
            self.position = pos
        def get_radar_facilities(self):
            return [DummyRadar(5, 10)]
    class DummyCraft:
        def __init__(self, pos):
            self.position = pos
        def is_on_world(self):
            return True
        radar_power = 3
        radar_range = 8
    class DummyLoc:
        def __init__(self, name, pos):
            self.name = name; self.position = pos; self.cover = 10; self.visible = False
        def update_visibility(self):
            self.visible = self.cover <= 0
        def replenish_cover(self):
            pass
    world = object()
    radar = TGlobalRadar(world)
    loc = DummyLoc('UFO', (0,0))
    base = DummyBase((0,0))
    craft = DummyCraft((0,0))
    radar.scan([loc], [base], [craft])
    assert loc.cover < 10

