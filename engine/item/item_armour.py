class TItemArmour():
    """
    Represents an armour item assigned to a unit.
    Tracks current state (shield, regen, etc) and references static parameters from item type.
    """
    def __init__(self, item_type=None):
        from engine.engine.game import TGame
        self.game = TGame()

        self.item_type = self.game.mod.items.get(item_type)   # Reference to item type (holds static parameters)
        self.shield = 0
        self.max_shield = self.item_type.armour_shield
        self.shield_regen =  self.item_type.armour_shield_regen

    def shield_regeneration(self):
        """
        Regenerate shield by shield_regen per turn, up to max_shield.
        """
        if self.shield < self.max_shield:
            self.shield = min(self.max_shield, self.shield + self.shield_regen)
        return self.shield

    def is_broken(self):
        return self.shield <= 0

    def reset_shield(self):
        self.shield = 0

    def calculate_damage(self, base_damage: float, damage_type: str) -> float:
        """
        Calculate the final damage after applying armour resistance.
        If the resistance for the damage type is not present, use 1.0 (no modification).
        """
        # Ensure resistance is a dict of float
        resistances = self.item_type.armour_resistance
        if not resistances:
            return base_damage
        modifier = resistances.get(damage_type, 1.0)
        return base_damage * float(modifier)

