from engine.globe.location import TLocation

class Transit:
    """
    Represents a single transit for one item, craft, or unit.
    Contains info about what, where, when, and quantity.
    """
    def __init__(self, transit_id, base_id, object_type, object_id, quantity, days_required):
        self.id = transit_id
        self.base_id = base_id
        self.object_type = object_type  # 'item', 'craft', 'unit'
        self.object_id = object_id
        self.quantity = quantity
        self.days_left = days_required
        self.status = 'in_transit'  # in_transit, delivered, cancelled

    def tick(self):
        if self.status == 'in_transit' and self.days_left > 0:
            self.days_left -= 1
            if self.days_left <= 0:
                self.status = 'delivered'

    def is_delivered(self):
        return self.status == 'delivered'

    def cancel(self):
        if self.status == 'in_transit':
            self.status = 'cancelled'

class TransferManager:
    """
    Manages all transits. Each transit is a single item/craft/unit delivery.
    Handles daily updates and delivery to base storage.
    """
    def __init__(self):
        self.transits = []  # List of Transit objects

    def add_transit(self, transit):
        self.transits.append(transit)

    def tick_all(self, base_storage_lookup):
        """
        Progress all transits by one day. Deliver to base storage if ready.
        base_storage_lookup: function(base_id, object_type, object_id, quantity) to add delivered goods.
        """
        for transit in list(self.transits):
            transit.tick()
            if transit.is_delivered():
                base_storage_lookup(transit.base_id, transit.object_type, transit.object_id, transit.quantity)
                self.transits.remove(transit)
