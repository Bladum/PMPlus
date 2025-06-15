"""
purchase_system.py

Defines the TPurchase class, the main purchasing system interface. Manages purchase entries, orders, and integration with base and transfer systems, including black market support.

Classes:
    TPurchase: Main purchasing system interface for regular and black market purchases.

Last standardized: 2025-06-15
"""

from typing import Dict, List, Optional, Tuple, Any
import logging
from datetime import datetime

from .purchase_entry import TPurchaseEntry
from .purchase_manager import PurchaseManager
from .black_market import BlackMarket

class TPurchase:
    """
    Primary purchasing system interface.
    Manages purchase entries, validation, order processing, and black market integration.
    
    Attributes:
        entries (dict): entry_id -> TPurchaseEntry
        purchase_manager (PurchaseManager): Manages active orders
        black_market (BlackMarket): Manages black market suppliers
    """
    
    def __init__(self, purchase_data: Optional[Dict[str, Any]] = None):
        """
        Initialize purchase system.
        
        Args:
            purchase_data (dict, optional): Purchase configuration data
        """
        self.entries: Dict[str, TPurchaseEntry] = {}
        self.purchase_manager = PurchaseManager()
        self.black_market = BlackMarket()
        
        # Load purchase entries from data
        if purchase_data:
            self._load_purchase_data(purchase_data)
        
        logging.info("Purchase system initialized")
    
    def _load_purchase_data(self, data: Dict[str, Any]):
        """
        Load purchase entries and black market data from configuration.
        
        Args:
            data (dict): Purchase configuration data
        """
        # Load regular purchase entries
        purchase_entries = data.get('purchasing', {})
        for entry_id, entry_data in purchase_entries.items():
            self.entries[entry_id] = TPurchaseEntry(entry_id, entry_data)
            logging.info(f"Loaded purchase entry: {entry_id}")
        
        # Load black market data
        black_market_data = data.get('black_market', {})
        if black_market_data:
            self.black_market.load_configuration(black_market_data)
            logging.info("Black market configuration loaded")
    
    def get_available_purchases(self, base_id: str, available_technologies: List[str], 
                              available_services: List[str], available_money: int) -> List[TPurchaseEntry]:
        """
        Get list of purchase entries available for a base.
        
        Args:
            base_id (str): Base making the purchase
            available_technologies (list): Available research technologies
            available_services (list): Available base services
            available_money (int): Available budget
            
        Returns:
            list: Available TPurchaseEntry objects
        """
        available = []
        
        for entry in self.entries.values():
            if entry.can_purchase(available_technologies, available_services, available_money):
                # Check monthly limits
                if entry.monthly_limit > 0:
                    current_month = datetime.now().strftime("%Y-%m")
                    purchased_this_month = self.purchase_manager.get_monthly_purchases(base_id, entry.id, current_month)
                    if purchased_this_month >= entry.monthly_limit:
                        continue
                
                available.append(entry)
        
        return available
    
    def get_black_market_purchases(self, base_id: str, available_money: int, 
                                 reputation: int = 0) -> List[Dict[str, Any]]:
        """
        Get available black market purchases.
        
        Args:
            base_id (str): Base making the purchase
            available_money (int): Available budget
            reputation (int): Player's black market reputation
            
        Returns:
            list: Available black market items with pricing
        """
        return self.black_market.get_available_purchases(available_money, reputation)
    
    def validate_purchase(self, entry_id: str, base_id: str, quantity: int,
                        available_technologies: List[str], available_services: List[str],
                        available_money: int) -> Tuple[bool, List[str]]:
        """
        Validate if a purchase can be made.
        
        Args:
            entry_id (str): Purchase entry ID
            base_id (str): Base making the purchase
            quantity (int): Quantity to purchase
            available_technologies (list): Available research technologies
            available_services (list): Available base services
            available_money (int): Available budget
            
        Returns:
            tuple: (can_purchase: bool, issues: List[str])
        """
        if entry_id not in self.entries:
            return False, [f"Unknown purchase entry: {entry_id}"]
        
        entry = self.entries[entry_id]
        issues = []
        
        # Check basic requirements
        if not entry.can_purchase(available_technologies, available_services, available_money * quantity):
            if not all(tech in available_technologies for tech in entry.required_technologies):
                missing_tech = [tech for tech in entry.required_technologies if tech not in available_technologies]
                issues.append(f"Missing technologies: {', '.join(missing_tech)}")
            
            if not all(service in available_services for service in entry.required_services):
                missing_services = [service for service in entry.required_services if service not in available_services]
                issues.append(f"Missing services: {', '.join(missing_services)}")
            
            total_cost = entry.cost * quantity
            if available_money < total_cost:
                issues.append(f"Insufficient funds: need ${total_cost}, have ${available_money}")
        
        # Check monthly limits
        if entry.monthly_limit > 0:
            current_month = datetime.now().strftime("%Y-%m")
            purchased_this_month = self.purchase_manager.get_monthly_purchases(base_id, entry_id, current_month)
            if purchased_this_month + quantity > entry.monthly_limit:
                remaining = entry.monthly_limit - purchased_this_month
                issues.append(f"Monthly limit exceeded: can only purchase {remaining} more this month")
        
        return len(issues) == 0, issues
    
    def place_order(self, entry_id: str, base_id: str, quantity: int,
                   available_technologies: List[str], available_services: List[str],
                   available_money: int) -> Tuple[bool, Optional[str], List[str]]:
        """
        Place a purchase order.
        
        Args:
            entry_id (str): Purchase entry ID
            base_id (str): Base making the purchase
            quantity (int): Quantity to purchase
            available_technologies (list): Available research technologies
            available_services (list): Available base services
            available_money (int): Available budget
            
        Returns:
            tuple: (success: bool, order_id: str, issues: List[str])
        """
        # Validate purchase
        can_purchase, issues = self.validate_purchase(
            entry_id, base_id, quantity, available_technologies, available_services, available_money
        )
        
        if not can_purchase:
            return False, None, issues
        
        entry = self.entries[entry_id]
        
        # Create order
        order_id = self.purchase_manager.create_order(
            base_id=base_id,
            entry=entry,
            quantity=quantity
        )
        
        logging.info(f"Purchase order {order_id} placed: {quantity}x {entry_id} for base {base_id}")
        return True, order_id, []
    
    def place_black_market_order(self, supplier_id: str, item_id: str, base_id: str, 
                                quantity: int, available_money: int) -> Tuple[bool, Optional[str], List[str]]:
        """
        Place a black market purchase order.
        
        Args:
            supplier_id (str): Black market supplier ID
            item_id (str): Item to purchase
            base_id (str): Base making the purchase
            quantity (int): Quantity to purchase
            available_money (int): Available budget
            
        Returns:
            tuple: (success: bool, order_id: str, issues: List[str])
        """
        return self.black_market.place_order(supplier_id, item_id, base_id, quantity, available_money)
    
    def get_order_status(self, order_id: str) -> Optional[Dict[str, Any]]:
        """Get status information for a purchase order."""
        return self.purchase_manager.get_order_status(order_id)
    
    def get_active_orders(self, base_id: Optional[str] = None) -> Dict[str, List[Any]]:
        """Get all active orders, optionally filtered by base."""
        return self.purchase_manager.get_active_orders(base_id)
    
    def cancel_order(self, order_id: str) -> bool:
        """Cancel a purchase order if it hasn't been delivered yet."""
        return self.purchase_manager.cancel_order(order_id)
    
    def process_monthly_reset(self):
        """
        Process monthly reset of purchase limits and black market stock.
        Should be called at the beginning of each month.
        """
        logging.info("Processing monthly purchase system reset")
        
        # Reset black market stock
        self.black_market.monthly_refresh()
        
        # Monthly limits are handled automatically by checking the current month
        logging.info("Monthly purchase reset completed")
    
    def process_daily_purchases(self, transfer_manager) -> Dict[str, List[str]]:
        """
        Process daily purchase deliveries.
        
        Args:
            transfer_manager: TransferManager instance
            
        Returns:
            Dict[str, List[str]]: Orders sent to transit by base {base_id: [order_ids]}
        """
        orders_in_transit = self.purchase_manager.process_daily_orders(transfer_manager)
        
        # Group by base
        result = {}
        for base_id, order in orders_in_transit:
            if base_id not in result:
                result[base_id] = []
            result[base_id].append(order.id)
        
        return result
    
    def get_purchase_history(self, base_id: Optional[str] = None, 
                           month: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get purchase history for analysis and reporting."""
        return self.purchase_manager.get_purchase_history(base_id, month)
    
    def save_data(self) -> Dict[str, Any]:
        """
        Save purchase system state.
        
        Returns:
            dict: Serialized purchase system data
        """
        return {
            'purchase_manager': self.purchase_manager.save_data(),
            'black_market': self.black_market.save_data()
        }
    
    def load_data(self, data: Dict[str, Any]):
        """
        Load purchase system state.
        
        Args:
            data (dict): Serialized purchase system data
        """
        if 'purchase_manager' in data:
            self.purchase_manager.load_data(data['purchase_manager'])
        
        if 'black_market' in data:
            self.black_market.load_data(data['black_market'])
        
        logging.info("Purchase system data loaded")
