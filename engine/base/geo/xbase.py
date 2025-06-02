from craft.craft import TCraft
from engine.base.facility import TFacility, TFacilityType
from engine.globe.location import TLocation
from unit.unit import TUnit
from engine.base.geo.base_inventory import TBaseInventory


class TBaseXCom(TLocation):
    """
    Represents a base on the world map as location (xcom or alien)
    Holds facilities, units, items, captures, crafts, and provides methods for base management.
    """
    def __init__(self, pid, data : dict = {}):
        super().__init__( pid, data )

        from engine.engine.game import TGame
        self.game = TGame()

        self.facilities : dict[ tuple, TFacility] = {}  # Dict of (x, y) -> TFacility

        # Initialize the inventory system for this base
        storage_capacity = self.get_storage_space()
        craft_capacity = self.get_craft_space()
        self.inventory = TBaseInventory(storage_capacity=storage_capacity, craft_capacity=craft_capacity)

    def add_facility(self, facility_type: TFacilityType, position=None, force_add=False):
        # Check if facility can be built (skip check if force_add is True)
        if not force_add and not self.can_build_facility(facility_type):
            raise Exception("Cannot build facility: requirements not met.")
        facility = TFacility(facility_type, position)
        self.facilities[position] = facility

        # Update inventory capacities when a new facility is built
        self.update_inventory_capacities()
        return facility

    def remove_facility(self, facility: TFacility):
        # Remove by position if present
        pos_to_remove = None
        for pos, fac in self.facilities.items():
            if fac == facility:
                pos_to_remove = pos
                break
        if pos_to_remove is not None:
            del self.facilities[pos_to_remove]

            # Update inventory capacities when a facility is removed
            self.update_inventory_capacities()

    def update_inventory_capacities(self):
        """Update the inventory capacities based on current facilities"""
        self.inventory.storage_capacity = self.get_storage_space()
        self.inventory.craft_capacity = self.get_craft_space()

    def can_build_facility(self, facility_type: TFacilityType):
        # Check max per base
        if facility_type.max_per_base > 0:
            # Safely handle potential None facility_type values
            count = 0
            for f in self.facilities.values():
                if f.facility_type is not None and f.facility_type.pid == facility_type.pid:
                    count += 1
            if count > facility_type.max_per_base:
                print(f"Cannot build {facility_type.name}: Maximum limit of {facility_type.max_per_base} reached.")
                return False

        # Check required facilities
        for req in facility_type.facility_needed:
            # Safely handle potential None facility_type values
            if not any(f.facility_type is not None and f.facility_type.pid == req and f.is_active() for f in self.facilities.values()):
                from engine.engine.game import TGame
                game = TGame()
                req_name = game.mod.facilities.get(req).name if req in game.mod.facilities else req
                print(f"Cannot build {facility_type.name}: Required facility '{req_name}' not found or not active.")
                return False

        # Check required services
        for req in facility_type.service_needed:
            if req not in self.get_services_provided():
                print(f"Cannot build {facility_type.name}: Required service '{req}' not available.")
                return False

        # Check required tech (stub, should check against base/player techs)
        for req in facility_type.tech_needed:
            if req not in self.game.mod.researches.keys():
                print(f"Cannot build {facility_type.name}: Required research '{req}' not completed.")
                return False
                # TODO improve this tech check

        # Check resources using inventory system
        for item, qty in facility_type.build_items.items():
            current_qty = self.inventory.get_item_quantity(item)
            if current_qty < qty:
                print(f"Cannot build {facility_type.name}: Not enough '{item}' resources. Have {current_qty}, need {qty}.")
                return False

        return True

    def can_place_facility_at(self, position):
        """
        Returns True if the given position is free for a new facility, False if already occupied.
        Extend this method for more complex placement rules if needed.
        """
        return position not in self.facilities.keys()

    def build_day(self):
        for facility in self.facilities.values():
            if not facility.completed:
                facility.build_day()

    def get_active_facilities(self):
        return [f for f in self.facilities.values() if f.is_active()]

    def get_services_provided(self):
        services = set()
        for f in self.get_active_facilities():
            for s in f.facility_type.service_provided:
                services.add(s)
        return services

    def get_total_capacity(self, attr):
        # Sum a given stat (e.g. storage_space, agent_space) from all active facilities
        return sum(getattr(f.facility_type, attr, 0) for f in self.get_active_facilities())

    def get_storage_space(self):
        return self.get_total_capacity('storage_space')

    def get_unit_space(self):
        return self.get_total_capacity('unit_space')

    def get_prison_space(self):
        return self.get_total_capacity('prison_space')

    def get_alien_space(self):
        return self.get_total_capacity('alien_space')

    def get_craft_space(self):
        return self.get_total_capacity('craft_space')

    def get_hospital_space(self):
        return self.get_total_capacity('hospital_space')

    def get_training_space(self):
        return self.get_total_capacity('training_space')

    def get_workshop_space(self):
        return self.get_total_capacity('workshop_space')

    def get_research_space(self):
        return self.get_total_capacity('research_space')

    def get_psi_space(self):
        return self.get_total_capacity('psi_space')

    def get_relax_space(self):
        return self.get_total_capacity('relax_space')

    def get_repair_space(self):
        return self.get_total_capacity('repair_space')

    def get_radar_facilities(self):
        """
        Returns a list of active facilities that provide radar coverage (have radar_range and radar_power).
        Each returned object will have .range and .power attributes.
        """
        radars = []
        for facility in self.facilities.values():
            if not facility.is_active():
                continue
            ftype = facility.facility_type
            radar_range = getattr(ftype, 'radar_range', None)
            radar_power = getattr(ftype, 'radar_power', None)
            if radar_range is not None and radar_power is not None:
                # Wrap as simple object for radar scan
                radar = type('Radar', (), {'range': radar_range, 'power': radar_power})()
                radars.append(radar)
        return radars

    def get_defense_facilities(self):
        """
        Returns a list of dicts with defense attributes for all active facilities that have defense capability.
        Each dict contains: power, hit, ammo, and a reference to the facility.
        """
        defense_list = []
        for facility in self.get_active_facilities():
            ftype = facility.facility_type
            defense_power = ftype.defense_power
            defense_hit = ftype.defense_hit
            defense_ammo = ftype.defense_ammo

            if defense_power is not None:
                defense_list.append({
                    'facility': facility,
                    'power': defense_power,
                    'hit': defense_hit,
                    'ammo': defense_ammo
                })
        return defense_list

    # Inventory delegation methods for convenient access

    # Item-related methods
    def add_item(self, item_id: str, quantity: float = 1.0, category=None) -> bool:
        """Delegate to inventory system"""
        return self.inventory.add_item(item_id, quantity, category)

    def remove_item(self, item_id: str, quantity: float = 1.0) -> bool:
        """Delegate to inventory system"""
        return self.inventory.remove_item(item_id, quantity)

    def get_item_quantity(self, item_id: str) -> float:
        """Delegate to inventory system"""
        return self.inventory.get_item_quantity(item_id)

    def consume_items(self, items_to_consume: dict) -> bool:
        """Delegate to inventory system"""
        return self.inventory.consume_items(items_to_consume)

    # Unit-related methods
    def add_unit(self, unit: TUnit) -> None:
        """Delegate to inventory system"""
        # TODO: Check if there's sufficient unit space before adding
        self.inventory.add_unit(unit)

    def remove_unit(self, unit: TUnit) -> bool:
        """Delegate to inventory system"""
        return self.inventory.remove_unit(unit)

    def get_units_count(self) -> int:
        """Delegate to inventory system"""
        return self.inventory.get_units_count()

    def get_units_by_type(self, unit_type: str) -> list:
        """Delegate to inventory system"""
        return self.inventory.get_units_by_type(unit_type)

    # Craft-related methods
    def add_craft(self, craft: TCraft) -> bool:
        """Delegate to inventory system"""
        return self.inventory.add_craft(craft)

    def remove_craft(self, craft: TCraft) -> bool:
        """Delegate to inventory system"""
        return self.inventory.remove_craft(craft)

    def get_crafts_count(self) -> int:
        """Delegate to inventory system"""
        return self.inventory.get_crafts_count()

    def get_crafts_by_type(self, craft_type: str) -> list:
        """Delegate to inventory system"""
        return self.inventory.get_crafts_by_type(craft_type)

    # Capture-related methods
    def add_capture(self, capture_id: str, quantity: float = 1.0) -> None:
        """Delegate to inventory system"""
        # TODO: Check if there's sufficient prison space before adding
        self.inventory.add_capture(capture_id, quantity)

    def remove_capture(self, capture_id: str, quantity: float = 1.0) -> bool:
        """Delegate to inventory system"""
        return self.inventory.remove_capture(capture_id, quantity)

    def get_capture_quantity(self, capture_id: str) -> float:
        """Delegate to inventory system"""
        return self.inventory.get_capture_quantity(capture_id)

    # Replace serialization methods with save_data and load_data
    def save_data(self) -> dict:
        """
        Save the base data to a dictionary for serialization.
        """
        # Create dictionary for facilities with position as string keys
        facilities_list = []
        for pos, facility in self.facilities.items():
            # For each facility, save essential data
            if facility.facility_type:
                facility_data = {
                    "facility_type_id": facility.facility_type.pid,
                    "position": pos,
                    "build_progress": facility.build_progress,
                    "completed": facility.completed,
                    "hp": facility.hp
                }
                facilities_list.append(facility_data)

        # Create the main data dictionary
        base_data = {
            "location": {
                "lat": self.lat,
                "lon": self.lon,
                "name": self.name
            },
            "facilities": facilities_list
        }

        # Add inventory data if the inventory has a save_data method
        if hasattr(self.inventory, 'save_data'):
            base_data["inventory"] = self.inventory.save_data()

        return base_data

    def load_data(self, data: dict) -> None:
        """
        Load the base data from a dictionary.
        """
        # Load location data
        location_data = data.get("location", {})
        self.lat = location_data.get("lat", 0)
        self.lon = location_data.get("lon", 0)
        self.name = location_data.get("name", "")

        # Load facilities
        facilities_data = data.get("facilities", [])
        self.facilities = {}

        for facility_data in facilities_data:
            pos = facility_data.get("position")
            facility_type_id = facility_data.get("facility_type_id")

            # Only create facility if we have valid position and type
            if pos and facility_type_id:
                # Create facility using the type ID directly
                from engine.engine.game import TGame
                game = TGame()

                # Create the facility with the proper facility type
                facility_type = game.mod.facilities.get(facility_type_id)
                if facility_type:
                    facility = TFacility(facility_type_id, pos)

                    # Set other facility properties
                    facility.build_progress = facility_data.get("build_progress", 0)
                    facility.completed = facility_data.get("completed", False)
                    facility.hp = facility_data.get("hp", 10)

                    # Add to facilities dictionary
                    self.facilities[pos] = facility

        # Load inventory
        inventory_data = data.get("inventory", {})
        if hasattr(self.inventory, 'load_data'):
            self.inventory.load_data(inventory_data)

        # Update capacities based on loaded facilities
        self.update_inventory_capacities()
