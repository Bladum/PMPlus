class TBattleObject:
    """
    Represents an object that may exist on a single tile.
    It can be picked up, thrown, destroyed by units on the battlefield.
    It does not block movement or fire.
    It can be a light source, have armor, and be destroyed.
    """
    def __init__(self, **kwargs):
        self.is_light_source = kwargs.get('is_light_source', False)  # Emits light?
        self.armor = kwargs.get('armor', 5)  # How much damage it can take before being destroyed
        self.destroyed_object_id = kwargs.get('destroyed_object_id', None)  # Object to replace with when destroyed

    def on_destroy(self):
        """
        Called when object is destroyed. Returns id of replacement object or None.
        """
        return self.destroyed_object_id

