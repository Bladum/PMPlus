"""
TBattleFloor: Represents a floor tile on the battle map, affecting movement, sight, accuracy, and other gameplay mechanics.

Encapsulates the properties and behaviors of floor tiles, including movement cost, sight cost, cover, armor, sound, light emission, and destruction logic.

Classes:
    TBattleFloor: Main class for battle map floor tiles.

Last standardized: 2025-06-14
"""

class TBattleFloor:
    """
    Represents a floor on the battle map. It is walkable and may affect movement, sight, and accuracy.

    Attributes:
        move_cost (int): Movement cost for units (default 1).
        sight_cost (int): Additional sight cost (affects LOS, default 0).
        accuracy_cost (int): Penalty/bonus to accuracy (cover, default 0).
        armor (int): How much damage it can take before being destroyed (default 10).
        sound (str|None): Sound to play when unit moves over (optional).
        is_light_source (bool): Emits light? (default False).
        destroyed_floor_id (str|None): Floor to replace with when destroyed (optional).
    """
    def __init__(self, **kwargs):
        """
        Initialize a TBattleFloor instance with optional properties.

        Args:
            move_cost (int, optional): Movement cost for units. Default is 1.
            sight_cost (int, optional): Additional sight cost (affects LOS). Default is 0.
            accuracy_cost (int, optional): Penalty/bonus to accuracy (cover). Default is 0.
            armor (int, optional): How much damage it can take before being destroyed. Default is 10.
            sound (str|None, optional): Sound to play when unit moves over. Default is None.
            is_light_source (bool, optional): Emits light? Default is False.
            destroyed_floor_id (str|None, optional): Floor to replace with when destroyed. Default is None.
        """
        self.move_cost = kwargs.get('move_cost', 1)  # Movement cost for units
        self.sight_cost = kwargs.get('sight_cost', 0)  # Additional sight cost (affects LOS)
        self.accuracy_cost = kwargs.get('accuracy_cost', 0)  # Penalty/bonus to accuracy (cover)
        self.armor = kwargs.get('armor', 10)  # How much damage it can take before being destroyed
        self.sound = kwargs.get('sound', None)  # Sound to play when unit moves over
        self.is_light_source = kwargs.get('is_light_source', False)  # Emits light?
        self.destroyed_floor_id = kwargs.get('destroyed_floor_id', None)  # Floor to replace with when destroyed

    def on_destroy(self):
        """
        Called when the floor is destroyed. Implement logic for replacement or effects here.

        Returns:
            str|None: Replacement floor id or None.
        """
        return self.destroyed_floor_id
