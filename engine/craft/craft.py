from engine.globe.location import TLocation


class TCraft(TLocation):
    """
    Represents a craft on the world map as location, it can move and attack
    """

    def __init__(self, position, max_fuel, max_damage, max_action_points, items=None, units=None, pilots=None):
        super().__init__(position)
        self.position = position  # Position on world map (redundant if TLocation handles it)
        self.max_fuel = max_fuel
        self.current_fuel = max_fuel
        self.max_damage = max_damage
        self.current_damage = 0
        self.max_action_points = max_action_points
        self.current_action_points = max_action_points
        self.items = items if items is not None else {}  # {item_name: {'max_ammo': int, 'current_ammo': int}}
        self.units = units if units is not None else []  # List of onboarded unit objects/IDs
        self.pilots = pilots if pilots is not None else []  # List of pilot unit objects/IDs

    def get_ammo_status(self):
        """Returns remaining ammo for each item."""
        return {name: data['current_ammo'] for name, data in self.items.items()}

