

class TCraftItem:
    """
    Represents a item used by craft by XCOM, with specific item type but current usage
    """
    def __init__(self, item_type=None):

        from engine.engine.game import TGame
        self.game = TGame()

        self.item_type = self.game.mod.items.get(item_type)  # Reference to item type (category=1), holds all static parameters
        self.active = True
        self.max_ammo = self.item_type.craft_ammo  # max ammo
        self.ammo = 0
        self.rearm_cost = self.item_type.craft_rearm_cost  # cost to rearm after battle
        self.reload_time = self.item_type.craft_reload_time # time to reload during battle

        self.rearm_time_left = 0
        self.reload_time_left = 0
        self.action_points = self.item_type.craft_action_point  # action points used by this item


    def ammo_needed(self):
        return max(0, self.max_ammo - self.ammo)

    def rearm_cost(self):
        # Total cost to refill to max
        return self.ammo_needed() * self.rearm_cost

    def is_active(self):
        return self.active

    def start_reload(self):
        self.reload_time_left = self.reload_time

    def tick_reload(self):
        if self.reload_time_left > 0:
            self.reload_time_left -= 1
        return self.reload_time_left
