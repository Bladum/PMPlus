"""
purchase_order.py

Defines the PurchaseOrder class, representing a purchase order made by the player. Handles items, units, and crafts to be purchased, their quantities, delivery tracking, and order status. Enhanced with delivery and transfer integration.

Classes:
    PurchaseOrder: Represents a purchase order and its delivery state.

Last standardized: 2025-06-15
"""

from typing import Dict, Optional, Any
from datetime import datetime
import uuid

class PurchaseOrder:
    """
    Represents a purchase order made by the player.
    Contains lists of items, units, and crafts with quantities and delivery tracking.

    Attributes:
        id (str): Order ID.
        base_id (str): Base where the order will be delivered.
        entry_id (str): Purchase entry ID this order is for.
        quantity (int): Quantity ordered.
        total_cost (int): Total cost of the order.
        order_date (datetime): When the order was placed.
        delivery_date (datetime): Expected delivery date.
        status (str): Order status ('ordered', 'in_transit', 'delivered', 'cancelled').
        supplier (str): Supplier name (None for regular market).
        delivery_contents (dict): What will be delivered {type: {id: quantity}}.
        transfer_ids (list): List of transfer IDs created for this order.
    """
    
    def __init__(self, base_id: str, entry_id: str, quantity: int, 
                 total_cost: int, delivery_time: int, supplier: Optional[str] = None,
                 delivery_contents: Optional[Dict[str, Any]] = None):
        """
        Initialize a purchase order.

        Args:
            base_id (str): Base where the order will be delivered.
            entry_id (str): Purchase entry ID.
            quantity (int): Quantity ordered.
            total_cost (int): Total cost.
            delivery_time (int): Delivery time in days.
            supplier (str, optional): Supplier name.
            delivery_contents (dict, optional): What will be delivered.
        """
        self.id = str(uuid.uuid4())
        self.base_id = base_id
        self.entry_id = entry_id
        self.quantity = quantity
        self.total_cost = total_cost
        self.order_date = datetime.now()
        
        # Calculate delivery date
        from datetime import timedelta
        self.delivery_date = self.order_date + timedelta(days=delivery_time)
        
        self.status = 'ordered'  # ordered, in_transit, delivered, cancelled
        self.supplier = supplier
        self.delivery_contents = delivery_contents or {}
        self.transfer_ids = []  # Will be populated when transfers are created
    
    def is_empty(self) -> bool:
        """
        Check if the order is empty (no delivery contents).

        Returns:
            bool: True if empty, False otherwise.
        """
        if not self.delivery_contents:
            return True
            
        return not any(self.delivery_contents.get(content_type, {}) 
                      for content_type in ['items', 'units', 'crafts'])

    def mark_in_transit(self, transfer_ids: list):
        """
        Mark the order as in transit and record transfer IDs.
        
        Args:
            transfer_ids (list): List of transfer IDs for this order
        """
        self.status = 'in_transit'
        self.transfer_ids = transfer_ids

    def mark_delivered(self):
        """Mark the order as delivered."""
        self.status = 'delivered'

    def mark_cancelled(self):
        """Mark the order as cancelled."""
        self.status = 'cancelled'
    
    def get_days_until_delivery(self) -> int:
        """
        Get number of days until delivery.
        
        Returns:
            int: Days until delivery (negative if overdue)
        """
        delta = self.delivery_date - datetime.now()
        return delta.days
    
    def is_due_for_delivery(self) -> bool:
        """
        Check if order is due for delivery.
        
        Returns:
            bool: True if due for delivery
        """
        return datetime.now() >= self.delivery_date
    
    def get_total_items(self) -> int:
        """
        Get total number of different item types in order.
        
        Returns:
            int: Total number of item types
        """
        total = 0
        for content_type in ['items', 'units', 'crafts']:
            content = self.delivery_contents.get(content_type, {})
            total += len(content)
        return total
    
    def get_summary(self) -> str:
        """
        Get a summary string of the order.
        
        Returns:
            str: Summary of order contents
        """
        summary_parts = []
        
        items = self.delivery_contents.get('items', {})
        if items:
            item_count = sum(items.values())
            summary_parts.append(f"{item_count} item(s)")
            
        units = self.delivery_contents.get('units', {})
        if units:
            unit_count = sum(units.values())
            summary_parts.append(f"{unit_count} unit(s)")
            
        crafts = self.delivery_contents.get('crafts', {})
        if crafts:
            craft_count = sum(crafts.values())
            summary_parts.append(f"{craft_count} craft(s)")
        
        if not summary_parts:
            return "Empty order"
            
        return ", ".join(summary_parts)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert order to dictionary for serialization.
        
        Returns:
            dict: Order data
        """
        return {
            'id': self.id,
            'base_id': self.base_id,
            'entry_id': self.entry_id,
            'quantity': self.quantity,
            'total_cost': self.total_cost,
            'order_date': self.order_date.isoformat(),
            'delivery_date': self.delivery_date.isoformat(),
            'status': self.status,
            'supplier': self.supplier,
            'delivery_contents': self.delivery_contents,
            'transfer_ids': self.transfer_ids
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PurchaseOrder':
        """
        Create order from dictionary.
        
        Args:
            data (dict): Order data
            
        Returns:
            PurchaseOrder: Recreated order
        """
        # Create minimal order first
        order = cls.__new__(cls)
        order.id = data['id']
        order.base_id = data['base_id']
        order.entry_id = data['entry_id']
        order.quantity = data['quantity']
        order.total_cost = data['total_cost']
        order.order_date = datetime.fromisoformat(data['order_date'])
        order.delivery_date = datetime.fromisoformat(data['delivery_date'])
        order.status = data['status']
        order.supplier = data.get('supplier')
        order.delivery_contents = data.get('delivery_contents', {})
        order.transfer_ids = data.get('transfer_ids', [])
        
        return order
    
    def __str__(self):
        status_text = self.status.upper()
        supplier_text = f" from {self.supplier}" if self.supplier else ""
        days_text = ""
        
        if self.status == 'ordered' or self.status == 'in_transit':
            days = self.get_days_until_delivery()
            if days > 0:
                days_text = f" (arrives in {days} days)"
            elif days == 0:
                days_text = " (arrives today)"
            else:
                days_text = f" (overdue by {abs(days)} days)"
        
        return f"Order {self.id[:8]}...: {self.get_summary()}{supplier_text} - ${self.total_cost} [{status_text}]{days_text}"
