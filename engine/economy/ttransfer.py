"""
engine/economy/ttransfer.py

Defines the TTransfer and TransferManager classes, which manage item, craft, and unit transits between bases, including delivery, status, and daily updates.

Classes:
    TTransfer: Represents a single delivery in transit.
    TransferManager: Manages all active deliveries and their progress.

Last standardized: 2025-06-15
"""

class TTransfer:
    """
    Represents a single transit for one item, craft, or unit.
    Contains info about what, where, when, and quantity.
    
    Attributes:
        id (str): Transit ID.
        base_id (str): Base receiving the delivery.
        object_type (str): 'item', 'craft', or 'unit'.
        object_id (str): ID of the object being transferred.
        quantity (int): Quantity being transferred.
        days_left (int): Days remaining for delivery.
        status (str): 'in_transit', 'delivered', or 'cancelled'.
    
    Methods:
        tick(): Progress the transit by one day.
        is_delivered(): Check if the transit is delivered.
        cancel(): Cancel the transit if still in transit.
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
        """
        Progress the transit by one day. Mark as delivered if days_left reaches zero.
        """
        if self.status == 'in_transit' and self.days_left > 0:
            self.days_left -= 1
            if self.days_left <= 0:
                self.status = 'delivered'

    def is_delivered(self):
        """
        Check if the transit is delivered.
        Returns:
            bool: True if delivered, False otherwise.
        """
        return self.status == 'delivered'

    def cancel(self):
        """
        Cancel the transit if it is still in transit.
        """
        if self.status == 'in_transit':
            self.status = 'cancelled'

class TransferManager:
    """
    Manages all transits. Each transit is a single item/craft/unit delivery.
    Handles daily updates and delivery to base storage.
    
    Attributes:
        transits (list): List of TTransfer objects.
    
    Methods:
        add_transit(transit): Add a new transit to the manager.
        tick_all(base_storage_lookup): Progress all transits by one day and deliver if ready.
    """
    def __init__(self):
        self.transits = []  # List of Transit objects

    def add_transit(self, transit):
        """
        Add a new transit to the manager.
        Args:
            transit (TTransfer): The transit to add.
        """
        self.transits.append(transit)

    def tick_all(self, base_storage_lookup):
        """
        Progress all transits by one day. Deliver to base storage if ready.
        Args:
            base_storage_lookup (callable): Function(base_id, object_type, object_id, quantity) to add delivered goods.
        """
        for transit in list(self.transits):
            transit.tick()
            if transit.is_delivered():
                base_storage_lookup(transit.base_id, transit.object_type, transit.object_id, transit.quantity)
                self.transits.remove(transit)
