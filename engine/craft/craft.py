from engine.globe.location import TLocation
from engine.globe.world_point import TWorldPoint


class TCraft(TLocation):
    """
    Represents a craft on the world map as location, it can move and attack
    """
    def __init__(self, pid, data : dict = {}):
        super().__init__( pid, data )

        position = data.get('position', [0, 0])
        units = data.get('units', [])
        pilots = data.get('pilots', [])
        items = data.get('items', {})
        craft_type = data.get('type', 'default')

        from engine.engine.game import TGame
        self.game = TGame()

        self.craft_type = self.game.mod.craft_types.get(craft_type, 'default')  # Default craft type

        self.position = position  # Position on world map (redundant if TLocation handles it)
        self.max_fuel = self.craft_type.range
        self.current_fuel = self.max_fuel
        self.health = self.craft_type.health
        self.health_current = self.health
        self.acceleration = self.craft_type.acceleration
        self.max_action_points = 4
        self.current_action_points = 4

        self.items = items if items is not None else {}  # {item_name: {'max_ammo': int, 'current_ammo': int}}
        self.units = units if units is not None else []  # List of onboarded unit objects/IDs
        self.pilots = pilots if pilots is not None else []  # List of pilot unit objects/IDs

    def get_ammo_status(self):
        """Returns remaining ammo for each item."""
        return {name: data['current_ammo'] for name, data in self.items.items()}

