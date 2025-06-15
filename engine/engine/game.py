"""
engine/engine/game.py

Defines the TGame class, the main game singleton holding all data and state for the campaign, world, bases, and more.

Classes:
    TGame: Main game class, holds all data. Singleton.

Last standardized: 2025-06-15
"""

from ..craft.craft import TCraft
from ..globe.world import TWorld
from ..lore.campaign import TCampaign
from ..lore.calendar import TCalendar
from ..economy.research_tree import TResearchTree
from ..economy.purchase import TPurchase
from ..economy.ttransfer import TransferManager

from ..lore.faction import TFaction
from ..base.xbase import TBaseXCom  # Fixed import path
from .mod import TMod, TUnitCategory, TItemCategory
from ..base.facility import TFacility, TFacilityType
from pathlib import Path
import os
import yaml

from typing import List, Dict, Any, Tuple, Optional

from ..unit.unit import TUnit


class TGame:
    """
    Main game class, holds all data
    It is a singleton
    """
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TGame, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self.__class__._initialized:
            return
        # World map: tiles, countries, regions, biomes, locations
        self.worldmap : TWorld = None

        # Current campaigns, missions, and campaign generator
        self.campaigns : list[TCampaign] = []

        # Calendar for date, turn, and event triggers
        self.calendar : TCalendar = None

        # XCOM budget, funding, and scoring
        self.budget = 0
        self.funding = 0
        self.scoring = 0

        # Global research tree
        self.research_tree : TResearchTree = None

        # Manufacturing tracking for monthly invoices
        self.monthly_manufacturing_hours = {}  # month_year -> {base_id: {entry_id: hours}}
        self.current_month_manufacturing = {}  # base_id -> {entry_id: hours} for current month

        # Purchase system
        self.purchase_system = None  # Will be initialized with purchase data

        # Transfer system for deliveries
        self.transfer_manager = TransferManager()

        # Loaded mod data (e.g., item stats)
        self.mod:TMod = None

        # Dictionary of bases where key is the base name and value is the TBaseXCom object
        # The active base is tracked separately
        self.bases: Dict[str, TBaseXCom] = {}
        self.current_base_name: str = None

        # Base labels/names mapping - what the player sees vs internal name
        self.base_labels = {
            "OMEGA": "OMEGA",      # Base 1
            "ALPHA": "ALPHA",      # Base 2
            "BETA": "BETA",        # Base 3
            "GAMMA": "GAMMA",      # Base 4
            "DELTA": "DELTA",      # Base 5
            "EPSILON": "EPSILON",  # Base 6
            "ZETA": "ZETA",        # Base 7
            "ETA": "ETA",          # Base 8
            "THETA": "THETA",      # Base 9
            "IOTA": "IOTA",        # Base 10
            "KAPPA": "KAPPA",      # Base 11
            "LAMBDA": "LAMBDA",    # Base 12
        }

        self.__class__._initialized = True

    def get_active_base(self) -> Optional[TBaseXCom]:
        """
        Get the currently active base. If none is active or the active base does not exist but bases exist,
        set the first base as active and return it.

        Returns:
            TBaseXCom object for the active base, or None if no bases exist
        """
        if not self.bases:
            return None
        # If current_base_name is not set or is invalid, set to first base
        if not self.current_base_name or self.current_base_name not in self.bases:
            self.current_base_name = next(iter(self.bases))
        return self.bases[self.current_base_name]

    def set_active_base(self, base_name: str) -> bool:
        """
        Set a base as the active base.

        Args:
            base_name: Name of the base to activate

        Returns:
            True if base was successfully activated, False otherwise

        Only existing bases can be activated.
        """
        if base_name in self.bases:
            self.current_base_name = base_name
            return True
        return False

    def set_active_base_by_index(self, index: int) -> bool:
        """
        Set a base as the active base using its index.

        Args:
            index: Zero-based index of the base to activate

        Returns:
            True if base was successfully activated, False otherwise
        """
        base_names = list(self.bases.keys())
        if 0 <= index < len(base_names):
            self.current_base_name = base_names[index]
            return True
        return False

    def add_base(self, name: str, base: TBaseXCom) -> bool:
        """
        Add a new base to the game.

        Args:
            name: Name/key for the base
            base: TBaseXCom object to add

        Returns:
            True if base was successfully added, False if name already exists
        """
        if name in self.bases:
            return False

        self.bases[name] = base

        # If this is our first base, make it active
        if self.current_base_name is None:
            self.current_base_name = name

        return True

    def remove_base(self, name: str) -> bool:
        """
        Remove a base from the game.

        Args:
            name: Name/key of the base to remove

        Returns:
            True if base was successfully removed, False if it didn't exist
        """
        if name not in self.bases:
            return False

        # If removing the active base, we need to set a new active base
        if self.current_base_name == name:
            self.bases.pop(name)
            if self.bases:
                self.current_base_name = next(iter(self.bases))
            else:
                self.current_base_name = None
        else:
            self.bases.pop(name)

        return True

    def base_exists(self, name: str) -> bool:
        """
        Check if a base exists.

        Args:
            name: Name of the base to check

        Returns:
            True if base exists, False otherwise
        """
        return name in self.bases

    def get_base_status(self, name: str) -> str:
        """
        Get the status of a base by name.

        Args:
            name: Name of the base to check

        Returns:
            String status: 'nonexistent', 'available', or 'active'
        """
        if name not in self.bases:
            return 'nonexistent'
        elif self.current_base_name == name:
            return 'active'
        else:
            return 'available'

    def get_base_status_by_index(self, index: int) -> str:
        """
        Get the status of a base by index.

        Args:
            index: Zero-based index of the base to check

        Returns:
            String status: 'nonexistent', 'available', or 'active'
        """
        base_names = list(self.bases.keys())
        if 0 <= index < len(base_names):
            name = base_names[index]
            return self.get_base_status(name)
        return 'nonexistent'

    def get_current_base_units(self) -> List[TUnit]:
        """
        Get units for the currently active base.

        Returns:
            List of TUnit objects for the active base

        Returns empty list if no active base or no units available.
        """
        active_base = self.get_active_base()
        return active_base.units if active_base and hasattr(active_base, 'units') else []

    def get_current_base_items(self) -> List[Tuple[str, str, Dict[str, Any], int]]:
        """
        Get items for the currently active base.

        Returns:
            Items from the base inventory

        Returns empty list if no active base or no items available.
        """
        active_base = self.get_active_base()
        return active_base.inventory.get_all_items() if active_base and hasattr(active_base, 'inventory') else []

    def get_current_base_crafts(self) -> List[TCraft]:
        """
        Get craft vehicles for the currently active base.

        Returns:
            List of TCraft objects for the active base

        Returns empty list if no active base or no crafts available.
        """
        active_base = self.get_active_base()
        return active_base.crafts if active_base and hasattr(active_base, 'crafts') else []

    def get_base_summary(self) -> Dict[str, int]:
        """
        Get summary statistics for the current active base.

        Returns:
            Dictionary containing unit counts by category and base capacity

        Keys include: 'soldiers', 'tanks', 'dogs', 'aliens', 'capacity'
        Returns zeros for all categories if no active base.
        """
        active_base = self.get_active_base()
        if not active_base or not hasattr(active_base, 'units'):
            return {"soldiers": 0, "tanks": 0, "dogs": 0, "aliens": 0, "capacity": 50}

        counts = {"soldiers": 0, "tanks": 0, "dogs": 0, "aliens": 0}
        for unit in active_base.inventory.units:
            category = getattr(unit, 'category', 'soldier')
            if category == 'soldier':
                counts['soldiers'] += 1
            elif category == 'tank':
                counts['tanks'] += 1
            elif category == 'dog':
                counts['dogs'] += 1
            elif category == 'alien':
                counts['aliens'] += 1

        # Get capacity from base facilities or use default
        capacity = active_base.get_personnel_capacity() if hasattr(active_base, 'get_personnel_capacity') else 50
        counts['capacity'] = capacity
        return counts

    def initialize_starting_bases(self) -> bool:
        """
        Initialize the starting bases for a new game based on the mod configuration.

        This method reads base configurations from the mod's start_bases dictionary
        and creates the initial bases accordingly.

        Returns:
            True if bases were successfully initialized, False otherwise
        """
        # Check if we already have bases configured
        if self.bases:
            return True

        # Check if mod is loaded and has starting base configurations
        if not self.mod or not hasattr(self.mod, 'start_bases') or not self.mod.starting_base:
            print("No starting base configurations found in mod data")
            return False

        try:
            # Create bases from the mod's start_bases configuration
            for base_name, base_data in self.mod.starting_base.items():
                # Create the base at specified location
                latitude = base_data.get('latitude', 0)
                longitude = base_data.get('longitude', 0)
                new_base = TBaseXCom(latitude=latitude, longitude=longitude, name=base_name)

                # Add facilities
                for facility_data in base_data.get('facilities', []):
                    facility_type_id = facility_data.get('type')
                    position = facility_data.get('position')

                    if facility_type_id and position and facility_type_id in self.mod.facilities:
                        facility_type = self.mod.facilities[facility_type_id]
                        new_base.add_facility(facility_type, position)

                # Add items to inventory
                for item_data in base_data.get('items', []):
                    item_id = item_data.get('id')
                    quantity = item_data.get('quantity', 1)

                    if item_id and item_id in self.mod.items:
                        new_base.inventory.add_item(item_id, quantity)

                # Add units
                for unit_data in base_data.get('units', []):
                    unit_type_id = unit_data.get('type')
                    if unit_type_id and unit_type_id in self.mod.units:
                        unit_type = self.mod.units[unit_type_id]
                        # Create unit instance (simplified, may need more parameters)
                        new_unit = TUnit(unit_type_id)
                        if hasattr(unit_data, 'name'):
                            new_unit.name = unit_data.get('name')
                        new_base.inventory.add_unit(new_unit)

                # Add crafts
                for craft_data in base_data.get('crafts', []):
                    craft_type_id = craft_data.get('type')
                    if craft_type_id and craft_type_id in self.mod.craft_types:
                        craft_type = self.mod.craft_types[craft_type_id]
                        # Create craft instance
                        new_craft = TCraft(craft_type_id)
                        if hasattr(craft_data, 'name'):
                            new_craft.name = craft_data.get('name')
                        if not hasattr(new_base, 'crafts'):
                            new_base.crafts = []
                        new_base.crafts.append(new_craft)

                # Add the completed base to the game
                self.add_base(base_name, new_base)

            return True
        except Exception as e:
            print(f"Error loading base {base_name}: {e}")
            return False

    def track_manufacturing_hours(self, base_id, entry_id, hours):
        """
        Track manufacturing hours for monthly invoicing.
        
        Args:
            base_id (str): Base where manufacturing takes place
            entry_id (str): Manufacturing project entry ID
            hours (float): Number of man-hours worked
        """
        if base_id not in self.current_month_manufacturing:
            self.current_month_manufacturing[base_id] = {}
        
        if entry_id not in self.current_month_manufacturing[base_id]:
            self.current_month_manufacturing[base_id][entry_id] = 0
        
        self.current_month_manufacturing[base_id][entry_id] += hours

    def finalize_monthly_manufacturing(self, month_year):
        """
        Finalize manufacturing hours for the month and prepare invoice.
        
        Args:
            month_year (str): Month and year in format "YYYY-MM"
            
        Returns:
            dict: Manufacturing hours by base and project for the month
        """
        if month_year not in self.monthly_manufacturing_hours:
            self.monthly_manufacturing_hours[month_year] = {}
        
        # Copy current month data to monthly archive
        for base_id, projects in self.current_month_manufacturing.items():
            if base_id not in self.monthly_manufacturing_hours[month_year]:
                self.monthly_manufacturing_hours[month_year][base_id] = {}
            
            for entry_id, hours in projects.items():
                if entry_id not in self.monthly_manufacturing_hours[month_year][base_id]:
                    self.monthly_manufacturing_hours[month_year][base_id][entry_id] = 0
                self.monthly_manufacturing_hours[month_year][base_id][entry_id] += hours
        
        # Store the finalized data for this month
        finalized_data = dict(self.current_month_manufacturing)
        
        # Reset current month tracking
        self.current_month_manufacturing = {}
        
        return finalized_data

    def get_monthly_manufacturing_invoice(self, month_year, hourly_rate=50):
        """
        Get manufacturing invoice for a specific month.
        
        Args:
            month_year (str): Month and year in format "YYYY-MM"
            hourly_rate (float): Cost per man-hour
            
        Returns:
            dict: Invoice details with costs per base and project
        """
        if month_year not in self.monthly_manufacturing_hours:
            return {"total_cost": 0, "details": {}}
        
        invoice = {"total_cost": 0, "details": {}}
        
        for base_id, projects in self.monthly_manufacturing_hours[month_year].items():
            base_total = 0
            base_details = {}
            
            for entry_id, hours in projects.items():
                cost = hours * hourly_rate
                base_total += cost
                base_details[entry_id] = {"hours": hours, "cost": cost}
            
            invoice["details"][base_id] = {
                "total_cost": base_total,
                "projects": base_details
            }
            invoice["total_cost"] += base_total
        
        return invoice

    def process_daily_transfers_and_purchases(self):
        """
        Process daily transfers and purchase deliveries.
        Should be called once per day by the calendar system.
        """
        # Process transfers - items that complete delivery today are added to base inventory
        self.transfer_manager.tick_all(self._add_delivered_items_to_base)
        
        # Process purchase orders - orders ready for delivery today are sent to transfer system
        if self.purchase_system:
            self.purchase_system.process_daily_purchases(self.transfer_manager)

    def _add_delivered_items_to_base(self, base_id: str, object_type: str, object_id: str, quantity: int):
        """
        Callback function for transfer manager to add delivered items to base inventory.
        
        Args:
            base_id: ID of the base receiving the delivery
            object_type: Type of object ('item', 'unit', 'craft')
            object_id: ID of the specific object
            quantity: Quantity delivered
        """
        if base_id not in self.bases:
            print(f"Warning: Trying to deliver to unknown base {base_id}")
            return
            
        base = self.bases[base_id]
        
        if object_type == 'item':
            success = base.add_item(object_id, quantity)
            if success:
                print(f"Delivered {quantity}x {object_id} to base {base_id}")
            else:
                print(f"Warning: Failed to deliver {quantity}x {object_id} to base {base_id} - insufficient storage")
        elif object_type == 'unit':
            # For units, we'd need to create TUnit instances - placeholder for now
            print(f"Unit delivery not yet implemented: {quantity}x {object_id} to base {base_id}")
        elif object_type == 'craft':
            # For crafts, we'd need to create TCraft instances - placeholder for now
            print(f"Craft delivery not yet implemented: {quantity}x {object_id} to base {base_id}")
        else:
            print(f"Warning: Unknown object type for delivery: {object_type}")

    def initialize_purchase_system(self, purchase_data: dict):
        """
        Initialize the purchase system with purchase entries and black market data.
        
        Args:
            purchase_data: Dictionary containing purchase entries and black market configuration
        """
        if self.purchase_system is None:
            self.purchase_system = TPurchase(purchase_data)
            print("Purchase system initialized")

    def get_purchase_system(self) -> Optional[TPurchase]:
        """Get the purchase system instance."""
        return self.purchase_system

    def setup_calendar_integration(self):
        """
        Setup integration between game systems and calendar events.
        This should be called after all systems are initialized.
        """
        if self.calendar:
            # Override calendar methods to call our game logic
            original_on_day = self.calendar.on_day
            original_on_month = self.calendar.on_month
            
            def enhanced_on_day(*args, **kwargs):
                original_on_day(*args, **kwargs)
                self.on_daily_tick()
            
            def enhanced_on_month(*args, **kwargs):
                original_on_month(*args, **kwargs)
                self.on_monthly_tick()
            
            self.calendar.on_day = enhanced_on_day
            self.calendar.on_month = enhanced_on_month
            
            print("Calendar integration setup completed")

    def on_daily_tick(self):
        """
        Called every day by the calendar system.
        Processes all daily game events including transfers and purchases.
        """
        print(f"Processing daily tick for {self.calendar.get_date()}")
        
        # Process transfers and purchases
        self.process_daily_transfers_and_purchases()
        
        # Process research if available
        if self.research_tree:
            completed_research = self.research_tree.daily_progress()
            if completed_research:
                print(f"Research completed: {', '.join(completed_research)}")
        
        # Process base facilities (construction progress)
        for base in self.bases.values():
            for facility in base.facilities:
                if not facility.completed:
                    facility.build_day()
                    if facility.completed:
                        print(f"Facility construction completed at {base.name}: {facility.facility_type.name}")

    def on_monthly_tick(self):
        """
        Called every month by the calendar system.
        Processes monthly events including purchase limit resets.
        """
        current_month = self.calendar.get_date()
        print(f"Processing monthly tick for {current_month[0]}-{current_month[1]:02d}")
        
        # Process monthly purchase system reset
        if self.purchase_system:
            self.purchase_system.process_monthly_reset()
        
        # Finalize monthly manufacturing hours
        month_year = f"{current_month[0]}-{current_month[1]:02d}"
        self.finalize_monthly_manufacturing(month_year)
        
        print(f"Monthly processing completed for {month_year}")
