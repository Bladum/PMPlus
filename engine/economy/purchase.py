"""
PurchaseOrder: Represents a purchase order made by the player.
Purpose: Handles items, units, and crafts to be purchased, their quantities, and order status.
Last update: 2025-06-10
"""

class PurchaseOrder:
    """
    Represents a purchase order made by the player.
    Contains lists of items, units, and crafts with quantities.

    Attributes:
        id (str): Order ID.
        base_id (str): Base where the order is placed.
        items (dict): Items to purchase {item_id: quantity}.
        units (dict): Units to purchase {unit_id: quantity}.
        crafts (dict): Crafts to purchase {craft_id: quantity}.
        status (str): Order status ('ordered', 'processed', 'cancelled').
    """
    def __init__(self, order_id, base_id, items=None, units=None, crafts=None):
        """
        Initialize a purchase order.

        Args:
            order_id (str): Unique order identifier.
            base_id (str): Base where the order is placed.
            items (dict, optional): Items to purchase.
            units (dict, optional): Units to purchase.
            crafts (dict, optional): Crafts to purchase.
        """
        self.id = order_id
        self.base_id = base_id
        self.items = items or {}  # {item_id: quantity}
        self.units = units or {}  # {unit_id: quantity}
        self.crafts = crafts or {}  # {craft_id: quantity}
        self.status = 'ordered'  # ordered, processed, cancelled

    def is_empty(self):
        """
        Check if the order is empty (no items, units, or crafts).

        Returns:
            bool: True if empty, False otherwise.
        """
        return not (self.items or self.units or self.crafts)

    def mark_processed(self):
        """
        Mark the order as processed.
        """
        self.status = 'processed'

    def mark_cancelled(self):
        """
        Mark the order as cancelled.
        """
        self.status = 'cancelled'

    def calculate_total_cost(self, item_cost_lookup, unit_cost_lookup, craft_cost_lookup):
        """
        Calculates the total cost of the purchase order using provided lookup functions.

        Args:
            item_cost_lookup (callable): Function to get item cost by id.
            unit_cost_lookup (callable): Function to get unit cost by id.
            craft_cost_lookup (callable): Function to get craft cost by id.

        Returns:
            int: Total cost of the order.
        """
        total = 0
        for item_id, qty in self.items.items():
            total += item_cost_lookup(item_id) * qty
        for unit_id, qty in self.units.items():
            total += unit_cost_lookup(unit_id) * qty
        for craft_id, qty in self.crafts.items():
            total += craft_cost_lookup(craft_id) * qty
        return total
