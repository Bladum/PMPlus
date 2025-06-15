"""
facility.py

Defines the TFacility class, representing a facility instance in an XCOM base. Tracks position, build progress, health, and links to the facility type blueprint.

Classes:
    TFacility: Facility instance in an XCOM base.

Last standardized: 2025-06-14
"""

from base.facility_type import TFacilityType


class TFacility:
    """
    Represents a facility in base, position, build progress, health, etc.
    Tracks construction progress, health, and links to the facility type blueprint.

    Attributes:
        facility_type (TFacilityType): The facility type blueprint.
        position (tuple): (x, y) grid position in base.
        build_progress (int): Days built so far.
        completed (bool): Whether construction is finished.
        hp (int): Facility hit points.
        game: Reference to the game object.
    """
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
        """
        Return True if facility is completed and active (usable by the base).

        Returns:
            bool: True if completed, False otherwise.
        """
        return self.completed

    def build_day(self):
        """
        Advance construction by one day. If build progress reaches build_time, mark as completed.
        """
        if not self.completed:
            self.build_progress += 1
            if self.build_progress >= self.facility_type.build_time:
                self.completed = True

    def get_stats(self):
        """
        Return the facility type if construction is completed, else None.

        Returns:
            TFacilityType or None: Facility type if completed, else None.
        """
        if self.completed:
            return self.facility_type
        return None
