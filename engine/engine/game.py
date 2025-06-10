from craft.craft import TCraft
from engine.globe.world import TWorld
from engine.lore.campaign import TCampaign
from engine.lore.calendar import TCalendar
from engine.economy.research_tree import TResearchTree

from engine.lore.faction import TFaction
from engine.base.geo.xbase import TBaseXCom
from engine.engine.mod import TMod, TUnitCategory, TItemCategory
from engine.base.facility import TFacility, TFacilityType
from pathlib import Path
import os
import yaml

from typing import List, Dict, Any, Tuple, Optional

from unit.unit import TUnit


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
            print(f"Error initializing starting bases: {e}")
            return False
