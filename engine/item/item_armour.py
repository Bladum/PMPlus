class TItemArmour:
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

    def tick_regen(self):
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
