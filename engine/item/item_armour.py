from item.item_type import TItemType


class TItemArmour:
    """
    Represents an armour item assigned to a unit.
    Tracks current state (shield, regen, etc) and references static parameters from item type.
    """
    def __init__(self, item_type=None):
        from engine.engine.game import TGame
        self.game = TGame()

        self.item_type : TItemType = self.game.mod.items.get(item_type)   # Reference to item type (holds static parameters)
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

    def is_shield_empty(self):
        return self.shield <= 0

    def reset_shield(self):
        self.shield = self.max_shield

    def apply_damage(self, damage: int, damage_type: str) -> float:
        """
        Applies incoming damage to the shield first (no resistance), then applies resistance to remaining damage.
        Returns the final damage to be applied to the unit (after shield and resistance).
        """
        # Apply damage to shield first
        shield_damage = min(self.shield, damage)
        self.shield -= shield_damage
        remaining_damage = damage - shield_damage

        # there is no shield left, apply resistance to remaining damage
        if remaining_damage > 0:

            # Ensure resistance is a dict of float
            resistances = self.item_type.armour_resistance
            if not resistances:
                return remaining_damage

            # there is resistance, apply it
            modifier = resistances.get(damage_type, 1.0)
            final_damage = remaining_damage * float(modifier)
            return final_damage

        return 0.0

    def get_stat_modifiers(self):
        """
        Returns a dictionary of stat modifiers provided by this armour.
        Override in subclasses or extend item_type to provide modifiers.
        """
        return self.item_type.unit_stats
