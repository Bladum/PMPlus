class TBattleWall:
    """
    Represents a wall on the battle map. Walls are not walkable and are drawn on top of floors.

    Attributes:
        block_sight (bool): Does this wall block line of sight? (default True)
        block_fire (bool): Does this wall block projectiles? (default True)
        sight_mod (int): Modifier to sight (0=transparent, 100=opaque)
        fire_mod (int): Modifier to fire (0=transparent, 100=blocks all)
        armor (int): How much damage it can take (default 20)
        material (str): Material type (affects resistances, default 'concrete')
        destroyed_wall_id (str|None): Wall to replace with when destroyed (optional)
        is_light_source (bool): Emits light? (default False)
        can_explode (bool): Can explode on destruction? (default False)
        explosion_power (int): Explosion power if explodes (default 0)
    """
    def __init__(self, **kwargs):
        # Initialize attributes with defaults from kwargs.get()
        self.block_sight = kwargs.get('block_sight', True)          # Does this wall block line of sight?
        self.block_fire = kwargs.get('block_fire', True)            # Does this wall block projectiles?
        self.sight_mod = kwargs.get('sight_mod', 100)               # Modifier to sight (0=transparent, 100=opaque)
        self.fire_mod = kwargs.get('fire_mod', 100)                 # Modifier to fire (0=transparent, 100=blocks all)
        self.armor = kwargs.get('armor', 20)                        # How much damage it can take
        self.material = kwargs.get('material', 'concrete')          # Material type (affects resistances)
        self.destroyed_wall_id = kwargs.get('destroyed_wall_id', None)  # Wall to replace with when destroyed
        self.is_light_source = kwargs.get('is_light_source', False) # Emits light?
        self.can_explode = kwargs.get('can_explode', False)         # Can explode on destruction?
        self.explosion_power = kwargs.get('explosion_power', 0)     # Explosion power if explodes

    def on_destroy(self):
        """
        Called when wall is destroyed. Returns id of replacement wall or None.
        """
        return self.destroyed_wall_id
