from base.facility_type import TFacilityType


class TFacility:
    """
    Represents a facility in base, position, build progress, health, etc.
    """
    def __init__(self, facility_name, position=None):

        from engine.engine.game import TGame
        self.game = TGame()

        self.facility_type = self.game.mod.facilities.get(facility_name)

        self.position : tuple = position  # (x, y) or similar
        self.build_progress = 0  # days built so far
        self.completed = False
        self.hp = 10  # default, can be extended

    def is_active(self):
        return self.completed

    def build_day(self):
        if not self.completed:
            self.build_progress += 1
            if self.build_progress >= self.facility_type.build_time:
                self.completed = True

    def get_stats(self):
        if self.completed:
            return self.facility_type
        return None

