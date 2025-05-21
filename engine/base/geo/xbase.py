from craft.craft import TCraft
from engine.base.facility import TFacility, TFacilityType
from engine.globe.location import TLocation
from unit.unit import TUnit


class TBaseXCom(TLocation):
    """
    Represents a base on the world map as location (xcom or alien)
    Holds facilities, units, items, captures, crafts, and provides methods for base management.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        from engine.engine.game import TGame
        self.game = TGame()

        self.facilities : dict[ tuple, TFacility] = {}  # Dict of (x, y) -> TFacility
        self.units  : list[TUnit] = []       # List of units in base
        self.items : dict[str, float] = {}      # Dict of item_id -> quantity
        self.captures : dict[str, float] = {}   # List of captured units (prisoners)
        self.crafts = list[TCraft] = []     # List of crafts in hangar/garage

    def add_facility(self, facility_type: TFacilityType, position=None):
        # Check if facility can be built
        if not self.can_build_facility(facility_type):
            raise Exception("Cannot build facility: requirements not met.")
        facility = TFacility(facility_type, position)
        self.facilities[position] = facility
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

    def can_build_facility(self, facility_type: TFacilityType):
        # Check max per base
        count = sum(1 for f in self.facilities.values() if f.type.id == facility_type.id)
        if count >= facility_type.max_per_base:
            return False
        # Check required facilities
        for req in facility_type.facility_needed:
            if not any(f.type.id == req and f.is_active() for f in self.facilities.values()):
                return False
        # Check required services
        for req in facility_type.service_needed:
            if req not in self.get_services_provided():
                return False
        # Check required tech (stub, should check against base/player techs)
        # for req in facility_type.tech_start:
        #     if req not in self.get_techs():
        #         return False
        # Check resources (stub, should check against base/player resources)
        # for item, qty in facility_type.build_items.items():
        #     if self.items.get(item, 0) < qty:
        #         return False
        return True

    def build_day(self):
        for facility in self.facilities.values():
            if not facility.completed:
                facility.build_day()

    def get_active_facilities(self):
        return [f for f in self.facilities.values() if f.is_active()]

    def get_services_provided(self):
        services = set()
        for f in self.get_active_facilities():
            for s in getattr(f.type, 'service_provided', []):
                services.add(s)
        return services

    def get_total_capacity(self, attr):
        # Sum a given stat (e.g. storage_space, agent_space) from all active facilities
        return sum(getattr(f.type, attr, 0) for f in self.get_active_facilities())

    def get_storage_space(self):
        return self.get_total_capacity('storage_space')

    def get_agent_space(self):
        return self.get_total_capacity('agent_space')

    def get_prison_space(self):
        return self.get_total_capacity('prison_space')

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

    def get_sanity_recovery(self):
        return self.get_total_capacity('sanity_recovery')

    def get_health_recovery(self):
        return self.get_total_capacity('health_recovery')

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
