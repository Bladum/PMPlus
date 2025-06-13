"""
PurchaseManager: Manages active purchase orders and processes deliveries.
Purpose: Handles order placement, daily processing, and integration with transfer system.
Last update: 2025-06-12
"""

from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
import uuid
import logging

from .purchase_order import PurchaseOrder

class PurchaseManager:
    """
    Manages active purchase orders across all bases.
    Handles order processing, delivery scheduling, and transfer integration.
    
    Attributes:
        active_orders (dict): base_id -> list of PurchaseOrder objects
        completed_orders (list): List of completed orders for history
        monthly_purchases (dict): month_year -> {entry_id: quantity} for tracking limits
        current_month (str): Current month in YYYY-MM format
    """
    def __init__(self):
        """
        Initialize the PurchaseManager.
        """
        self.active_orders: Dict[str, List[PurchaseOrder]] = {}
        self.completed_orders: List[PurchaseOrder] = []
        self.monthly_purchases: Dict[str, Dict[str, int]] = {}
        self.current_month = datetime.now().strftime("%Y-%m")
    
    def place_order(self, base_id: str, entry_id: str, quantity: int, 
                   total_cost: int, delivery_time: int, supplier: Optional[str] = None,
                   delivery_contents: Optional[Dict[str, Any]] = None) -> PurchaseOrder:
        """
        Place a new purchase order for a base.
        
        Args:
            base_id (str): Base receiving the order.
            entry_id (str): Purchase entry ID.
            quantity (int): Quantity to order.
            total_cost (int): Total cost of the order.
            delivery_time (int): Delivery time in days.
            supplier (str, optional): Supplier name.
            delivery_contents (dict, optional): What will be delivered.
            
        Returns:
            PurchaseOrder: The created order object.
        """
        order = PurchaseOrder(
            base_id=base_id,
            entry_id=entry_id,
            quantity=quantity,
            total_cost=total_cost,
            delivery_time=delivery_time,
            supplier=supplier,
            delivery_contents=delivery_contents
        )
        
        # Add to active orders
        if base_id not in self.active_orders:
            self.active_orders[base_id] = []
        self.active_orders[base_id].append(order)
        
        # Track monthly purchases for limits
        month_key = datetime.now().strftime("%Y-%m")
        if month_key not in self.monthly_purchases:
            self.monthly_purchases[month_key] = {}
        if entry_id not in self.monthly_purchases[month_key]:
            self.monthly_purchases[month_key][entry_id] = 0
        self.monthly_purchases[month_key][entry_id] += quantity
        
        logging.info(f"Placed order {order.id} for {quantity}x {entry_id} to {base_id}")
        return order
    
    def cancel_order(self, order_id: str) -> bool:
        """
        Cancel an active order by ID.
        
        Args:
            order_id (str): Order ID.
            
        Returns:
            bool: True if cancelled, False otherwise.
        """
        for base_id, orders in self.active_orders.items():
            for order in orders:
                if order.id == order_id and order.status == 'ordered':
                    order.mark_cancelled()
                    # Remove from monthly tracking
                    month_key = order.order_date.strftime("%Y-%m")
                    if (month_key in self.monthly_purchases and 
                        order.entry_id in self.monthly_purchases[month_key]):
                        self.monthly_purchases[month_key][order.entry_id] -= order.quantity
                        if self.monthly_purchases[month_key][order.entry_id] <= 0:
                            del self.monthly_purchases[month_key][order.entry_id]
                    
                    logging.info(f"Cancelled order {order_id}")
                    return True
        return False
    
    def get_monthly_purchases(self, month_year: str, entry_id: str) -> int:
        """
        Get the number of purchases for an entry in a given month.
        
        Args:
            month_year (str): Month in YYYY-MM format.
            entry_id (str): Purchase entry ID.
            
        Returns:
            int: Quantity purchased this month.
        """
        return self.monthly_purchases.get(month_year, {}).get(entry_id, 0)
    
    def get_current_month_purchases(self, entry_id: str) -> int:
        """
        Get the number of purchases for an entry in the current month.
        
        Args:
            entry_id (str): Purchase entry ID.
            
        Returns:
            int: Quantity purchased this month.
        """
        return self.get_monthly_purchases(self.current_month, entry_id)
    
    def reset_monthly_limits(self):
        """
        Reset all monthly purchase limits (called at month start).
        """
        self.current_month = datetime.now().strftime("%Y-%m")
        # Monthly purchases are kept for history, but current month starts fresh
        if self.current_month not in self.monthly_purchases:
            self.monthly_purchases[self.current_month] = {}
    
    def process_daily_orders(self, transfer_manager) -> List[Tuple[str, PurchaseOrder]]:
        """
        Process all active orders for daily delivery updates.
        
        Args:
            transfer_manager: TransferManager instance for handling deliveries.
            
        Returns:
            list: List of (base_id, PurchaseOrder) tuples delivered today.
        """
        orders_in_transit = []
        current_date = datetime.now()
        
        for base_id, orders in self.active_orders.items():
            for order in list(orders):  # Copy list to avoid modification during iteration
                if order.status == 'ordered' and order.is_due_for_delivery():
                    # Create transfers for this order
                    transfer_ids = self._create_transfers_for_order(order, transfer_manager)
                    
                    if transfer_ids:
                        order.mark_in_transit(transfer_ids)
                        orders_in_transit.append((base_id, order))
                        logging.info(f"Order {order.id} sent to transit with {len(transfer_ids)} transfers")
        
        return orders_in_transit
    
    def _create_transfers_for_order(self, order: PurchaseOrder, transfer_manager) -> List[str]:
        """
        Create transfer records for a delivered order.
        
        Args:
            order (PurchaseOrder): The order being delivered.
            transfer_manager: TransferManager instance.
            
        Returns:
            list: List of transfer IDs created.
        """
        transfer_ids = []
        
        # Create transfers for each type of content
        for content_type, content_dict in order.delivery_contents.items():
            for object_id, quantity in content_dict.items():
                # Create a transfer for each item/unit/craft type
                transfer_id = str(uuid.uuid4())
                  # Import here to avoid circular imports
                from .ttransfer import TTransfer
                transfer = TTransfer(
                    transit_id=transfer_id,
                    base_id=order.base_id,
                    object_type=content_type.rstrip('s'),  # items -> item, units -> unit, etc
                    object_id=object_id,
                    quantity=quantity,
                    days_required=1  # Already calculated delivery time, this is transit time
                )
                
                transfer_manager.add_transit(transfer)
                transfer_ids.append(transfer_id)
        
        return transfer_ids
    
    def mark_order_delivered(self, order_id: str):
        """
        Mark an order as delivered by ID.
        
        Args:
            order_id (str): Order ID.
        """
        for base_id, orders in self.active_orders.items():
            for order in orders:
                if order.id == order_id and order.status == 'in_transit':
                    order.mark_delivered()
                    self.completed_orders.append(order)
                    orders.remove(order)
                    logging.info(f"Order {order_id} delivered to {base_id}")
                    return
    
    def get_base_orders(self, base_id: str, status: Optional[str] = None) -> List[PurchaseOrder]:
        """
        Get all orders for a base, optionally filtered by status.
        
        Args:
            base_id (str): Base ID.
            status (str, optional): Filter by order status.
            
        Returns:
            list: List of PurchaseOrder objects.
        """
        orders = self.active_orders.get(base_id, [])
        if status:
            orders = [order for order in orders if order.status == status]
        return orders
    
    def get_order_by_id(self, order_id: str) -> Optional[PurchaseOrder]:
        """
        Get a purchase order by its ID.
        
        Args:
            order_id (str): Order ID.
            
        Returns:
            PurchaseOrder or None: The order if found.
        """
        for orders in self.active_orders.values():
            for order in orders:
                if order.id == order_id:
                    return order
        
        for order in self.completed_orders:
            if order.id == order_id:
                return order
        
        return None
    
    def get_orders_summary(self, base_id: str) -> Dict[str, Any]:
        """
        Get a summary of all orders for a base.
        
        Args:
            base_id (str): Base ID.
            
        Returns:
            dict: Summary of orders.
        """
        orders = self.active_orders.get(base_id, [])
        
        summary = {
            'total_orders': len(orders),
            'ordered': len([o for o in orders if o.status == 'ordered']),
            'in_transit': len([o for o in orders if o.status == 'in_transit']),
            'total_cost': sum(o.total_cost for o in orders),
            'orders': orders
        }
        
        return summary
    
    def cleanup_old_orders(self, days_old: int = 30):
        """
        Remove orders older than a given number of days from history.
        
        Args:
            days_old (int): Number of days to keep.
        """
        cutoff_date = datetime.now() - timedelta(days=days_old)
        self.completed_orders = [
            order for order in self.completed_orders 
            if order.order_date > cutoff_date
        ]
    
    def get_all_suppliers(self) -> List[str]:
        """
        Get a list of all supplier names from active and completed orders.
        
        Returns:
            list: Supplier names.
        """
        suppliers = set()
        for orders in self.active_orders.values():
            for order in orders:
                if order.supplier:
                    suppliers.add(order.supplier)
        return list(suppliers)
    
    def __str__(self):
        """
        String summary of the purchase manager state.
        
        Returns:
            str: Summary string.
        """
        total_orders = sum(len(orders) for orders in self.active_orders.values())
        total_bases = len(self.active_orders)
        return f"PurchaseManager: {total_orders} active orders across {total_bases} bases"
