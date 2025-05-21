class TBattleFloor:
    """
    Represents a floor on battle map, it is walkable
    """
    def __init__(self, move_cost=1, sight_cost=0, accuracy_cost=0, armor=10, sound=None, is_light_source=False, destroyed_floor_id=None):
        self.move_cost = move_cost  # Movement cost for units
        self.sight_cost = sight_cost  # Additional sight cost (affects LOS)
        self.accuracy_cost = accuracy_cost  # Penalty/bonus to accuracy (cover)
        self.armor = armor  # How much damage it can take before being destroyed
        self.sound = sound  # Sound to play when unit moves over
        self.is_light_source = is_light_source  # Emits light?
        self.destroyed_floor_id = destroyed_floor_id  # Floor to replace with when destroyed

    def on_destroy(self):
        """
        Called when floor is destroyed. Returns id of replacement floor or None.
        """
        return self.destroyed_floor_id

