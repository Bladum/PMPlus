"""
purchase.py

Defines the TPurchase class, the main purchasing system interface. Manages purchase entries, orders, and integration with base/transfer systems, including black market suppliers.

Classes:
    TPurchase: Main purchasing system interface.

Last standardized: 2025-06-14
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
            entry = TPurchaseEntry(entry_id, entry_data)
            self.entries[entry_id] = entry
            logging.debug(f"Loaded purchase entry: {entry_id}")

        # Load black market suppliers
        black_market_data = data.get('black_market', {})
        suppliers_data = black_market_data.get('suppliers', {})

        for supplier_name, supplier_data in suppliers_data.items():
            from .black_market import BlackMarketSupplier
            supplier = BlackMarketSupplier(supplier_name, supplier_data)
            self.black_market.add_supplier(supplier)

        logging.info(f"Loaded {len(self.entries)} purchase entries and {len(self.black_market.suppliers)} black market suppliers")

    def get_available_purchases(self, available_technologies: List[str] = None,
                              available_services: List[str] = None,
                              available_items: Dict[str, int] = None,
                              available_regions: List[str] = None,
                              available_countries: List[str] = None,
                              include_black_market: bool = True) -> List[TPurchaseEntry]:
        """
        Get list of purchase entries available based on requirements.

        Args:
            available_technologies (list, optional): List of researched technologies
            available_services (list, optional): List of available base services
            available_items (dict, optional): Dictionary of available items
            available_regions (list, optional): List of controlled regions
            available_countries (list, optional): List of controlled countries
            include_black_market (bool): Whether to include black market items

        Returns:
            List[TPurchaseEntry]: List of available purchase entries
        """
        available_technologies = available_technologies or []
        available_services = available_services or []
        available_items = available_items or {}
        available_regions = available_regions or []
        available_countries = available_countries or []

        available_entries = []

        for entry in self.entries.values():
            # Skip black market items if not requested
            if entry.black_market and not include_black_market:
                continue

            # Check if entry is available (monthly limits, black market availability)
            if not entry.is_available:
                continue

            # Check technology requirements
            if not all(tech in available_technologies for tech in entry.tech_needed):
                continue

            # Check service requirements
            if not all(service in available_services for service in entry.services_needed):
                continue

            # Check item requirements (rare for purchases)
            items_available = True
            for item, needed_quantity in entry.items_needed.items():
                if available_items.get(item, 0) < needed_quantity:
                    items_available = False
                    break
            if not items_available:
                continue

            # Check region requirements
            if entry.region_needed and not any(region in available_regions for region in entry.region_needed):
                continue

            # Check country requirements
            if entry.country_needed and not any(country in available_countries for country in entry.country_needed):
                continue

            available_entries.append(entry)

        return available_entries

    def validate_purchase_requirements(self, entry: TPurchaseEntry, base_id: str,
                                     quantity: int, available_technologies: List[str] = None,
                                     available_services: List[str] = None,
                                     available_items: Dict[str, int] = None,
                                     available_money: int = 0,
                                     available_regions: List[str] = None,
                                     available_countries: List[str] = None) -> Tuple[bool, List[str]]:
        """
        Validate all requirements for making a purchase.

        Args:
            entry (TPurchaseEntry): Purchase entry to validate
            base_id (str): Base ID where purchase will be delivered
            quantity (int): Quantity to purchase
            available_technologies (list, optional): Available technologies
            available_services (list, optional): Available services
            available_items (dict, optional): Available items
            available_money (int): Available money
            available_regions (list, optional): Available regions
            available_countries (list, optional): Available countries

        Returns:
            Tuple[bool, List[str]]: (can_purchase, list_of_issues)
        """
        issues = []

        # Check if item is available
        if not entry.is_available:
            issues.append("Item is currently unavailable")

        # Check monthly limits
        if not entry.can_purchase(quantity):
            remaining = entry.get_remaining_monthly_quota()
            issues.append(f"Monthly limit exceeded: {remaining} remaining this month")

        # Check technology requirements
        available_technologies = available_technologies or []
        for tech in entry.tech_needed:
            if tech not in available_technologies:
                issues.append(f"Missing required technology: {tech}")

        # Check service requirements
        available_services = available_services or []
        for service in entry.services_needed:
            if service not in available_services:
                issues.append(f"Missing required service: {service}")

        # Check item requirements
        available_items = available_items or {}
        for item, needed_per_unit in entry.items_needed.items():
            total_needed = needed_per_unit * quantity
            available = available_items.get(item, 0)
            if available < total_needed:
                issues.append(f"Insufficient {item}: need {total_needed}, have {available}")

        # Check region requirements
        available_regions = available_regions or []
        if entry.region_needed and not any(region in available_regions for region in entry.region_needed):
            issues.append(f"Required region not controlled: {entry.region_needed}")

        # Check country requirements
        available_countries = available_countries or []
        if entry.country_needed and not any(country in available_countries for country in entry.country_needed):
            issues.append(f"Required country not controlled: {entry.country_needed}")

        # Check money
        total_cost = entry.get_total_cost(quantity)
        if available_money < total_cost:
            issues.append(f"Insufficient funds: need ${total_cost}, have ${available_money}")

        return len(issues) == 0, issues

    def place_purchase_order(self, entry_id: str, base_id: str, quantity: int,
                            available_technologies: List[str] = None,
                            available_services: List[str] = None,
                            available_items: Dict[str, int] = None,
                            available_money: int = 0,
                            available_regions: List[str] = None,
                            available_countries: List[str] = None) -> Tuple[bool, Any]:
        """
        Place a purchase order.

        Args:
            entry_id (str): Purchase entry ID
            base_id (str): Base where order will be delivered
            quantity (int): Quantity to purchase
            available_technologies (list, optional): Available technologies
            available_services (list, optional): Available services
            available_items (dict, optional): Available items
            available_money (int): Available money
            available_regions (list, optional): Available regions
            available_countries (list, optional): Available countries

        Returns:
            Tuple[bool, Any]: (success, PurchaseOrder or error_message)
        """
        if entry_id not in self.entries:
            return False, f"Unknown purchase entry: {entry_id}"

        entry = self.entries[entry_id]

        # Validate requirements
        can_purchase, issues = self.validate_purchase_requirements(
            entry, base_id, quantity, available_technologies, available_services,
            available_items, available_money, available_regions, available_countries
        )

        if not can_purchase:
            return False, "; ".join(issues)

        # Calculate costs and delivery
        total_cost = entry.get_total_cost(quantity)
        delivery_time = entry.purchase_time
        delivery_contents = entry.get_delivery_contents(quantity)

        # Apply black market effects
        if entry.black_market and entry.supplier:
            supplier = self.black_market.suppliers.get(entry.supplier)
            if supplier:
                # Apply reliability to delivery time
                reliability = supplier.get_delivery_reliability()
                if reliability < 1.0:
                    import random
                    delay_chance = 1.0 - reliability
                    if random.random() < delay_chance:
                        delay_days = random.randint(1, 5)
                        delivery_time += delay_days
                        logging.info(f"Black market order delayed by {delay_days} days due to reliability")

                # Apply reputation discount
                total_cost = self.black_market.apply_reputation_effects(total_cost, entry.supplier)

        # Place the order
        order = self.purchase_manager.place_order(
            base_id=base_id,
            entry_id=entry_id,
            quantity=quantity,
            total_cost=total_cost,
            delivery_time=delivery_time,
            supplier=entry.supplier,
            delivery_contents=delivery_contents
        )

        # Record purchase against monthly limit
        entry.record_purchase(quantity)

        logging.info(f"Placed purchase order {order.id} for {quantity}x {entry_id} (${total_cost})")
        return True, order

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

    def process_monthly_reset(self):
        """Process monthly reset of purchase limits and black market stock."""
        # Reset monthly limits for all entries
        for entry in self.entries.values():
            entry.reset_monthly_limit()

        # Reset purchase manager monthly tracking
        self.purchase_manager.reset_monthly_limits()

        # Refresh black market stock
        black_market_entries = [entry for entry in self.entries.values() if entry.black_market]
        self.black_market.refresh_all_stock(black_market_entries)

        logging.info("Monthly purchase reset completed")

    def cancel_order(self, order_id: str) -> bool:
        """
        Cancel a purchase order.

        Args:
            order_id (str): Order ID to cancel

        Returns:
            bool: True if order was cancelled
        """
        result = self.purchase_manager.cancel_order(order_id)

        if result:
            # Find the order to get entry info
            order = self.purchase_manager.get_order_by_id(order_id)
            if order and order.entry_id in self.entries:
                entry = self.entries[order.entry_id]
                # Reduce monthly purchase count
                entry.current_month_purchased = max(0, entry.current_month_purchased - order.quantity)

            # Decrease black market reputation if applicable
            if order and order.supplier:
                self.black_market.decrease_reputation(0.05)

        return result

    def get_purchase_status(self, base_id: str) -> Dict[str, Any]:
        """
        Get purchase status for a base.

        Args:
            base_id (str): Base identifier

        Returns:
            dict: Purchase status information
        """
        return self.purchase_manager.get_orders_summary(base_id)

    def get_black_market_suppliers(self) -> List[str]:
        """
        Get list of discovered black market suppliers.

        Returns:
            List[str]: Supplier names
        """
        return [supplier.name for supplier in self.black_market.get_discovered_suppliers()]

    def discover_black_market_supplier(self, supplier_name: str, technologies: List[str],
                                     regions: List[str], items: Dict[str, int],
                                     money: int) -> Tuple[bool, str]:
        """
        Attempt to discover a black market supplier.

        Args:
            supplier_name (str): Supplier to discover
            technologies (list): Available technologies
            regions (list): Controlled regions
            items (dict): Available items
            money (int): Available money

        Returns:
            Tuple[bool, str]: (success, message)
        """
        return self.black_market.attempt_discovery(supplier_name, technologies, regions, items, money)

    def get_supplier_items(self, supplier_name: str) -> List[TPurchaseEntry]:
        """
        Get items available from a specific supplier.

        Args:
            supplier_name (str): Supplier name

        Returns:
            List[TPurchaseEntry]: Available items
        """
        if supplier_name == "Regular Market":
            return [entry for entry in self.entries.values() if not entry.black_market]
        else:
            return self.black_market.get_supplier_stock(supplier_name)

    def mark_order_delivered(self, order_id: str):
        """
        Mark an order as delivered (called when transfers complete).

        Args:
            order_id (str): Order ID
        """
        self.purchase_manager.mark_order_delivered(order_id)

        # Increase black market reputation if applicable
        order = self.purchase_manager.get_order_by_id(order_id)
        if order and order.supplier:
            self.black_market.increase_reputation(0.02)

    def get_monthly_purchase_report(self, month_year: str) -> Dict[str, Any]:
        """
        Get monthly purchase report.

        Args:
            month_year (str): Month in YYYY-MM format

        Returns:
            dict: Monthly purchase data
        """
        monthly_purchases = self.purchase_manager.monthly_purchases.get(month_year, {})

        total_items = sum(monthly_purchases.values())
        total_cost = 0

        # Calculate total cost (approximate, as prices may have changed)
        for entry_id, quantity in monthly_purchases.items():
            if entry_id in self.entries:
                entry = self.entries[entry_id]
                total_cost += entry.purchase_cost * quantity

        return {
            'month': month_year,
            'total_items_purchased': total_items,
            'total_cost': total_cost,
            'purchases_by_entry': monthly_purchases,
            'black_market_reputation': self.black_market.global_reputation
        }

    def __str__(self):
        regular_items = len([e for e in self.entries.values() if not e.black_market])
        black_market_items = len([e for e in self.entries.values() if e.black_market])
        active_orders = sum(len(orders) for orders in self.purchase_manager.active_orders.values())

        return f"Purchase System: {regular_items} regular items, {black_market_items} black market items, {active_orders} active orders"
