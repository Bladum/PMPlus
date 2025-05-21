class TCraftItem:
    """
    Represents a item used by craft by XCOM, with specific item type but current usage
    """
    def __init__(self, item_id, data):
        self.id = item_id
        self.name = data.get('name', item_id)
        self.description = data.get('description', '')
        self.ammo = data.get('ammo', 0)  # current ammo
        self.max_ammo = data.get('ammo', 0)  # max ammo
        self.reload_cost = data.get('reload_cost', 0)
        self.rearm_rate = data.get('rearm_rate', 1)
        self.reload_time = data.get('reload_time', 1)
        self.damage = data.get('damage', 1)
        self.accuracy = data.get('accuracy', 0.5)
        self.range = data.get('range', 1)
        self.size = data.get('size', 1)
        self.rate = data.get('rate', 1)
        # ...other fields as needed...

    def ammo_needed(self):
        return max(0, self.max_ammo - self.ammo)

    def rearm_cost(self):
        # Total cost to refill to max
        return self.ammo_needed() * self.reload_cost

