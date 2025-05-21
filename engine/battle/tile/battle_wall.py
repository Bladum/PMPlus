class TBattleWall:
    """
    Represents a wall on battle map, it is not walkable
    It is drawn on top of floor
    """
    def __init__(self, block_sight=True, block_fire=True, sight_mod=100, fire_mod=100, armor=20, material='concrete', destroyed_wall_id=None, is_light_source=False, can_explode=False, explosion_power=0):
        self.block_sight = block_sight  # Does this wall block line of sight?
        self.block_fire = block_fire    # Does this wall block projectiles?
        self.sight_mod = sight_mod      # Modifier to sight (0=transparent, 100=opaque)
        self.fire_mod = fire_mod        # Modifier to fire (0=transparent, 100=blocks all)
        self.armor = armor              # How much damage it can take
        self.material = material        # Material type (affects resistances)
        self.destroyed_wall_id = destroyed_wall_id  # Wall to replace with when destroyed
        self.is_light_source = is_light_source      # Emits light?
        self.can_explode = can_explode              # Can explode on destruction?
        self.explosion_power = explosion_power      # Explosion power if explodes

    def on_destroy(self):
        """
        Called when wall is destroyed. Returns id of replacement wall or None.
        """
        return self.destroyed_wall_id

