class PurchaseOrder:
    """
    Represents a purchase order made by the player.
    Contains lists of items, units, and crafts with quantities.
    """
    def __init__(self, order_id, base_id, items=None, units=None, crafts=None):
        self.id = order_id
        self.base_id = base_id
        self.items = items or {}  # {item_id: quantity}
        self.units = units or {}  # {unit_id: quantity}
        self.crafts = crafts or {}  # {craft_id: quantity}
        self.status = 'ordered'  # ordered, processed, cancelled

    def is_empty(self):
        return not (self.items or self.units or self.crafts)

    def mark_processed(self):
        self.status = 'processed'

    def mark_cancelled(self):
        self.status = 'cancelled'

    def calculate_total_cost(self, item_cost_lookup, unit_cost_lookup, craft_cost_lookup):
        """
        Calculates the total cost of the purchase order using provided lookup functions.
        Each lookup should accept (id) and return the cost for that item/unit/craft.
        """
        total = 0
        for item_id, qty in self.items.items():
            total += item_cost_lookup(item_id) * qty
        for unit_id, qty in self.units.items():
            total += unit_cost_lookup(unit_id) * qty
        for craft_id, qty in self.crafts.items():
            total += craft_cost_lookup(craft_id) * qty
        return total
