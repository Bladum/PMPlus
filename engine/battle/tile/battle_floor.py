class TBattleFloor:
    """
    Represents a floor on battle map, it is walkable
    """
    def __init__(self, **kwargs):
        self.move_cost = kwargs.get('move_cost', 1)  # Movement cost for units
        self.sight_cost = kwargs.get('sight_cost', 0)  # Additional sight cost (affects LOS)
        self.accuracy_cost = kwargs.get('accuracy_cost', 0)  # Penalty/bonus to accuracy (cover)
        self.armor = kwargs.get('armor', 10)  # How much damage it can take before being destroyed
        self.sound = kwargs.get('sound', None)  # Sound to play when unit moves over
        self.is_light_source = kwargs.get('is_light_source', False)  # Emits light?
        self.destroyed_floor_id = kwargs.get('destroyed_floor_id', None)  # Floor to replace with when destroyed

    def on_destroy(self):
        """
        Called when floor is destroyed. Returns id of replacement floor or None.
        """
        return self.destroyed_floor_id

