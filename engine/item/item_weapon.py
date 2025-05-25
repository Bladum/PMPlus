class TItemWeapon:
    """
    Represents a weapon item assigned to a unit (soldier, alien, etc).
    Tracks current state (ammo, reload, etc) and references static parameters from item type.
    """
    def __init__(self, item_type=None):
        from engine.engine.game import TGame
        self.game = TGame()

        self.item_type = self.game.mod.items.get(item_type)
        # Reference to item type (category=1), holds all static parameters
        self.active = True
        self.max_ammo = self.item_type.unit_ammo  # max ammo
        self.ammo = 0
        self.rearm_cost = self.item_type.unit_rearm_cost  # cost to rearm after battle
        self.rearm_item = self.item_type.unit_rearm_item # time to reload during battle

        self.action_points = self.item_type.unit_action_point  # action points used by this item


    def ammo_needed(self):
        return max(0, self.max_ammo - self.ammo)

    def get_rearm_cost(self):
        # Total cost to refill to max
        return self.ammo_needed() * self.rearm_cost

    def can_fire(self, current_ap):
        return self.ammo > 0 and current_ap >= self.action_points

    def fire(self):
        if self.ammo > 0:
            self.ammo -= 1
            return True
        return False

