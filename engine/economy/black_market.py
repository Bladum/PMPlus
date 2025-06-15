"""
black_market.py

Defines the BlackMarket and BlackMarketSupplier classes, managing black market suppliers and special item availability. Handles special suppliers with limited availability, rotating stock, price variance, and discovery mechanics.

Classes:
    BlackMarketSupplier: Represents a single black market supplier with unique rules.
    BlackMarket: Manages all black market suppliers, discovery, and global reputation.

Last standardized: 2025-06-14
"""

from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
import random
import logging

class BlackMarketSupplier:
    """
    Represents a black market supplier with special characteristics and mechanics.

    Attributes:
        name (str): Supplier name.
        reputation (str): Reputation level (unknown, questionable, reliable, trusted).
        region_specialization (list): Regions where this supplier operates.
        item_specialization (list): Item categories this supplier specializes in.
        availability_schedule (str): When items refresh (daily, weekly, monthly).
        price_variance_range (tuple): Min/max price variance (0.5, 2.0) = 50% to 200%.
        reliability (float): Chance supplier delivers on time (0.0-1.0).
        discovery_requirements (dict): Requirements to discover this supplier (techs, regions, items, money).
        is_discovered (bool): Whether player has discovered this supplier.
        last_refresh (datetime): When stock was last refreshed.
        current_stock (list): Currently available purchase entry IDs.
    """
    
    def __init__(self, name: str, data: Optional[Dict[str, Any]] = None):
        """
        Initialize a black market supplier.

        Args:
            name (str): Supplier name.
            data (dict, optional): Supplier configuration and state.
        """
        data = data or {}
        
        self.name = name
        self.reputation = data.get('reputation', 'unknown')
        self.region_specialization = data.get('region_specialization', [])
        self.item_specialization = data.get('item_specialization', [])
        self.availability_schedule = data.get('availability_schedule', 'weekly')
        self.price_variance_range = tuple(data.get('price_variance_range', [0.7, 1.8]))
        self.reliability = data.get('reliability', 0.8)
        self.discovery_requirements = data.get('discovery_requirements', {})
        
        # State
        self.is_discovered = data.get('is_discovered', False)
        self.last_refresh = datetime.now() - timedelta(days=1)  # Force initial refresh
        self.current_stock = []
        
        # Stock configuration: can be extended for custom stock logic per supplier
        self.stock_size_range = tuple(data.get('stock_size_range', [3, 8]))
        self.rare_item_chance = data.get('rare_item_chance', 0.3)
    
    def should_refresh_stock(self) -> bool:
        """
        Determine if the supplier's stock should be refreshed based on the schedule.
        
        Returns:
            bool: True if stock should be refreshed, False otherwise.
        """
        now = datetime.now()
        
        if self.availability_schedule == 'daily':
            return now.date() > self.last_refresh.date()
        elif self.availability_schedule == 'weekly':
            days_since = (now - self.last_refresh).days
            return days_since >= 7
        elif self.availability_schedule == 'monthly':
            return now.month != self.last_refresh.month or now.year != self.last_refresh.year
        
        return False
    
    def refresh_stock(self, available_entries: List[Any]):
        """
        Refresh the supplier's stock with a new selection of available entries.
        
        Args:
            available_entries (list): List of all possible purchase entries.
        """
        if not self.is_discovered:
            self.current_stock = []
            return
        
        # Filter entries by specialization
        eligible_entries = []
        for entry in available_entries:
            # Must be black market item
            if not entry.black_market:
                continue
                
            # Check if matches specialization
            if self.item_specialization and entry.category not in self.item_specialization:
                continue
                
            eligible_entries.append(entry)
        
        # Select random stock
        stock_size = random.randint(*self.stock_size_range)
        stock_size = min(stock_size, len(eligible_entries))
        
        self.current_stock = random.sample(eligible_entries, stock_size) if eligible_entries else []
        self.last_refresh = datetime.now()
        
        logging.info(f"Black market supplier {self.name} refreshed stock: {len(self.current_stock)} items")
    
    def get_price_multiplier(self) -> float:
        """
        Get the current price multiplier for this supplier (randomized within range).
        
        Returns:
            float: Price multiplier (e.g., 1.2 for 20% markup).
        """
        return random.uniform(*self.price_variance_range)
    
    def can_discover(self, technologies: List[str], regions: List[str], 
                    items: Dict[str, int], money: int) -> Tuple[bool, List[str]]:
        """
        Check if the player meets requirements to discover this supplier.
        
        Args:
            technologies (list): Player's known technologies.
            regions (list): Player's controlled regions.
            items (dict): Player's items.
            money (int): Player's available money.
            
        Returns:
            (bool, list): (True if discoverable, list of missing requirements)
        """
        if self.is_discovered:
            return True, []
        
        missing = []
        
        # Check technology requirements
        for tech in self.discovery_requirements.get('technologies', []):
            if tech not in technologies:
                missing.append(f"Technology: {tech}")
        
        # Check region requirements
        for region in self.discovery_requirements.get('regions', []):
            if region not in regions:
                missing.append(f"Region: {region}")
        
        # Check item requirements
        for item, quantity in self.discovery_requirements.get('items', {}).items():
            if items.get(item, 0) < quantity:
                missing.append(f"Item: {item} ({quantity} needed)")
        
        # Check money requirements
        required_money = self.discovery_requirements.get('money', 0)
        if money < required_money:
            missing.append(f"Money: ${required_money}")
        
        return len(missing) == 0, missing
    
    def discover(self):
        """
        Mark this supplier as discovered by the player.
        """
        self.is_discovered = True
        logging.info(f"Black market supplier {self.name} discovered!")
    
    def get_delivery_reliability(self) -> float:
        """
        Get the delivery reliability (chance of on-time delivery) for this supplier.
        
        Returns:
            float: Reliability value (0.0-1.0)
        """
        return self.reliability
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the supplier's state to a dictionary for saving/loading.
        
        Returns:
            dict: Supplier state.
        """
        return {
            'name': self.name,
            'reputation': self.reputation,
            'region_specialization': self.region_specialization,
            'item_specialization': self.item_specialization,
            'availability_schedule': self.availability_schedule,
            'price_variance_range': list(self.price_variance_range),
            'reliability': self.reliability,
            'discovery_requirements': self.discovery_requirements,
            'is_discovered': self.is_discovered,
            'last_refresh': self.last_refresh.isoformat(),
            'current_stock': [entry.pid for entry in self.current_stock],
            'stock_size_range': list(self.stock_size_range),
            'rare_item_chance': self.rare_item_chance
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BlackMarketSupplier':
        """
        Create supplier from dictionary.
        
        Args:
            data (dict): Supplier data
            
        Returns:
            BlackMarketSupplier: Recreated supplier
        """
        supplier = cls(data['name'], data)
        supplier.last_refresh = datetime.fromisoformat(data['last_refresh'])
        # Note: current_stock will need to be rebuilt from entry references
        return supplier


class BlackMarket:
    """
    Manages all black market suppliers, their discovery, and global black market operations.
    
    Attributes:
        suppliers (dict): name -> BlackMarketSupplier
        discovery_events (list): List of discovery event records
        global_reputation (float): Player's reputation with black market (0.0-1.0)
    
    Methods:
        add_supplier(supplier): Add a new supplier to the black market.
        get_discovered_suppliers(): List all discovered suppliers.
        get_discoverable_suppliers(...): List suppliers that can be discovered now.
        attempt_discovery(...): Attempt to discover a supplier, returns result and message.
        refresh_all_stock(...): Refresh stock for all suppliers.
        get_supplier_stock(...): Get current stock for a supplier.
    """
    
    def __init__(self):
        """
        Initialize the BlackMarket manager.
        """
        self.suppliers: Dict[str, BlackMarketSupplier] = {}
        self.discovery_events: List[Dict[str, Any]] = []
        self.global_reputation = 0.0  # Affects prices and availability
    
    def add_supplier(self, supplier: BlackMarketSupplier):
        """
        Add a new supplier to the black market.
        
        Args:
            supplier (BlackMarketSupplier): The supplier to add.
        """
        self.suppliers[supplier.name] = supplier
        logging.info(f"Added black market supplier: {supplier.name}")
    
    def get_discovered_suppliers(self) -> List[BlackMarketSupplier]:
        """
        Get a list of all discovered suppliers.
        
        Returns:
            list: Discovered BlackMarketSupplier objects.
        """
        return [supplier for supplier in self.suppliers.values() if supplier.is_discovered]
    
    def get_discoverable_suppliers(self, technologies: List[str], regions: List[str], 
                                 items: Dict[str, int], money: int) -> List[BlackMarketSupplier]:
        """
        Get a list of suppliers that can be discovered with current player state.
        
        Args:
            technologies (list): Player's known technologies.
            regions (list): Player's controlled regions.
            items (dict): Player's items.
            money (int): Player's available money.
            
        Returns:
            list: Discoverable BlackMarketSupplier objects.
        """
        discoverable = []
        for supplier in self.suppliers.values():
            if not supplier.is_discovered:
                can_discover, _ = supplier.can_discover(technologies, regions, items, money)
                if can_discover:
                    discoverable.append(supplier)
        return discoverable
    
    def attempt_discovery(self, supplier_name: str, technologies: List[str], 
                         regions: List[str], items: Dict[str, int], money: int) -> Tuple[bool, str]:
        """
        Attempt to discover a supplier by name, checking requirements.
        
        Args:
            supplier_name (str): Name of the supplier to discover.
            technologies (list): Player's known technologies.
            regions (list): Player's controlled regions.
            items (dict): Player's items.
            money (int): Player's available money.
            
        Returns:
            (bool, str): (True if discovered, message)
        """
        if supplier_name not in self.suppliers:
            return False, f"Unknown supplier: {supplier_name}"
        
        supplier = self.suppliers[supplier_name]
        can_discover, missing = supplier.can_discover(technologies, regions, items, money)
        
        if not can_discover:
            return False, f"Missing requirements: {', '.join(missing)}"
        
        supplier.discover()
        self.discovery_events.append({
            'supplier': supplier_name,
            'date': datetime.now().isoformat(),
            'reputation_before': self.global_reputation
        })
        
        # Increase global reputation
        self.global_reputation = min(1.0, self.global_reputation + 0.1)
        
        return True, f"Successfully discovered {supplier_name}!"
    
    def refresh_all_stock(self, available_entries: List[Any]):
        """
        Refresh stock for all suppliers in the black market.
        
        Args:
            available_entries (list): List of all possible purchase entries.
        """
        for supplier in self.suppliers.values():
            if supplier.should_refresh_stock():
                supplier.refresh_stock(available_entries)
    
    def get_supplier_stock(self, supplier_name: str) -> List[Any]:
        """
        Get the current stock for a given supplier.
        
        Args:
            supplier_name (str): Name of the supplier.
            
        Returns:
            list: List of available purchase entry IDs.
        """
        if supplier_name not in self.suppliers:
            return []
        
        supplier = self.suppliers[supplier_name]
        if not supplier.is_discovered:
            return []
        
        return supplier.current_stock
    
    def apply_reputation_effects(self, base_price: int, supplier_name: str) -> int:
        """
        Apply global reputation effects to price.
        
        Args:
            base_price (int): Base price
            supplier_name (str): Supplier name
            
        Returns:
            int: Modified price
        """
        # Higher reputation = better prices
        reputation_discount = self.global_reputation * 0.2  # Up to 20% discount
        final_price = int(base_price * (1.0 - reputation_discount))
        
        return max(1, final_price)  # Minimum price of 1
    
    def increase_reputation(self, amount: float = 0.05):
        """
        Increase global reputation (successful transactions, etc).
        
        Args:
            amount (float): Amount to increase
        """
        self.global_reputation = min(1.0, self.global_reputation + amount)
    
    def decrease_reputation(self, amount: float = 0.1):
        """
        Decrease global reputation (cancelled orders, etc).
        
        Args:
            amount (float): Amount to decrease
        """
        self.global_reputation = max(0.0, self.global_reputation - amount)
    
    def get_reputation_description(self) -> str:
        """
        Get text description of reputation level.
        
        Returns:
            str: Reputation description
        """
        if self.global_reputation < 0.2:
            return "Unknown"
        elif self.global_reputation < 0.4:
            return "Distrusted"
        elif self.global_reputation < 0.6:
            return "Neutral"
        elif self.global_reputation < 0.8:
            return "Respected"
        else:
            return "Highly Regarded"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert black market to dictionary for serialization.
        
        Returns:
            dict: Black market data
        """
        return {
            'suppliers': {name: supplier.to_dict() for name, supplier in self.suppliers.items()},
            'discovery_events': self.discovery_events,
            'global_reputation': self.global_reputation
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BlackMarket':
        """
        Create black market from dictionary.
        
        Args:
            data (dict): Black market data
            
        Returns:
            BlackMarket: Recreated black market
        """
        market = cls()
        
        # Recreate suppliers
        for name, supplier_data in data.get('suppliers', {}).items():
            supplier = BlackMarketSupplier.from_dict(supplier_data)
            market.suppliers[name] = supplier
        
        market.discovery_events = data.get('discovery_events', [])
        market.global_reputation = data.get('global_reputation', 0.0)
        
        return market
    
    def __str__(self):
        discovered = len(self.get_discovered_suppliers())
        total = len(self.suppliers)
        reputation_desc = self.get_reputation_description()
        return f"Black Market: {discovered}/{total} suppliers discovered, Reputation: {reputation_desc}"
