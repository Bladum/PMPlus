"""
TFacility: Represents a facility instance in an XCOM base.
Purpose: Tracks position, build progress, health, and links to facility type blueprint.
Last update: 2025-06-10
"""

from base.facility_type import TFacilityType


class TFacility:
    '''
    Represents a facility in base, position, build progress, health, etc.
    Attributes:
        facility_type (TFacilityType): The facility type blueprint.
        position (tuple): (x, y) grid position in base.
        build_progress (int): Days built so far.
        completed (bool): Whether construction is finished.
        hp (int): Facility hit points.
    '''
    def __init__(self, facility_name: str, position=None):
        """
        Initialize a facility instance in a base.
        Args:
            facility_name (str): Facility type ID or name.
            position (tuple): (x, y) grid position in base.
        """
        from engine.engine.game import TGame
        self.game = TGame()
        self.facility_type : TFacilityType = self.game.mod.facilities.get(facility_name)
        self.position : tuple = position  # (x, y) or similar
        self.build_progress = 0  # days built so far
        self.completed = False
        self.hp = 10  # default, can be extended

    def is_active(self) -> bool:
        """Return True if facility is completed and active."""
        return self.completed

    def build_day(self):
        """Advance construction by one day. Mark as completed if done."""
        if not self.completed:
            self.build_progress += 1
            if self.build_progress >= self.facility_type.build_time:
                self.completed = True

    def get_stats(self):
        """Return facility type if completed, else None."""
        if self.completed:
            return self.facility_type
        return None
