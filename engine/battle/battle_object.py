"""
TBattleObject: Represents an interactive object on a battle map tile (pickup, thrown, destroyed, light source, etc.).

Encapsulates the properties and destruction logic for battlefield objects, including light emission and replacement on destruction.

Classes:
    TBattleObject: Main class for battle map objects.

Last standardized: 2025-06-14
"""

class TBattleObject:
    """
    Represents an object that may exist on a single tile.
    It can be picked up, thrown, destroyed by units on the battlefield.
    It does not block movement or fire.
    It can be a light source, have armor, and be destroyed.

    Attributes:
        is_light_source (bool): Emits light? (default False).
        armor (int): How much damage it can take before being destroyed (default 5).
        destroyed_object_id (str|None): Object to replace with when destroyed (optional).
    """
    def __init__(self, **kwargs):
        """
        Initialize a TBattleObject instance with optional properties.

        Args:
            is_light_source (bool, optional): Emits light? Default is False.
            armor (int, optional): How much damage it can take before being destroyed. Default is 5.
            destroyed_object_id (str|None, optional): Object to replace with when destroyed. Default is None.
        """
        self.is_light_source = kwargs.get('is_light_source', False)  # Emits light?
        self.armor = kwargs.get('armor', 5)  # How much damage it can take before being destroyed
        self.destroyed_object_id = kwargs.get('destroyed_object_id', None)  # Object to replace with when destroyed

    def on_destroy(self):
        """
        Called when object is destroyed. Returns id of replacement object or None.
        Returns:
            str|None: Replacement object id or None.
        """
        return self.destroyed_object_id
