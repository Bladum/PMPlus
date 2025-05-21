class TBattleObject:
    """
    Represents an object that may exist on a single tile.
    It can be picked up, thrown, destroyed by units on the battlefield.
    It does not block movement or fire.
    It can be a light source, have armor, and be destroyed.
    """
    def __init__(self, is_light_source=False, armor=5, destroyed_object_id=None):
        self.is_light_source = is_light_source  # Emits light?
        self.armor = armor  # How much damage it can take before being destroyed
        self.destroyed_object_id = destroyed_object_id  # Object to replace with when destroyed

    def on_destroy(self):
        """
        Called when object is destroyed. Returns id of replacement object or None.
        """
        return self.destroyed_object_id

