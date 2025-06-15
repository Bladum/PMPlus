"""
craft.py

Defines the TCraft class, representing a craft (aircraft, submarine, spaceship, etc.) on the world map in XCOM. A TCraft is a movable, interactive entity with crew, inventory, mission, and automation features.

Classes:
    TCraft: Craft entity on the world map.

Last standardized: 2025-06-14
"""

from engine.globe.location import TLocation
from engine.globe.world_point import TWorldPoint
from typing import List, Optional, Dict, Any


class TCraft(TLocation):
    """
    Represents a craft on the world map as a location.

    A TCraft can move, attack, carry crew and items, and participate in missions. It supports automation routines for patrol, interception, return, and resupply.

    Attributes:
        position (list): World map coordinates.
        units (list): Onboarded unit objects/IDs.
        pilots (list): Pilot unit objects/IDs.
        items (dict): Inventory items and ammo status.
        craft_type (TCraftType): Reference to the craft's type definition.
        crew (list): List of crew/unit objects/IDs.
        crew_status (dict): Status of each crew member.
        mission (dict): Current mission assignment.
        notifications (list): Notification queue.
        ai_patrol_enabled (bool): Whether patrol automation is enabled.
        ai_auto_intercept_enabled (bool): Whether auto-intercept is enabled.
        ai_auto_return_enabled (bool): Whether auto-return is enabled.
        ai_auto_resupply_enabled (bool): Whether auto-resupply is enabled.
        patrol_route (list): List of patrol waypoints.
    """
    def __init__(self, pid, data : dict = {}):
        """
        Initialize a new TCraft instance.

        Args:
            pid (str): Unique identifier for the craft.
            data (dict): Dictionary of all craft state and configuration.
        """
        super().__init__( pid, data )
        position = data.get('position', [0, 0])
        units = data.get('units', [])
        pilots = data.get('pilots', [])
        items = data.get('items', {})
        craft_type = data.get('type', 'default')
        from engine.engine.game import TGame
        self.game = TGame()
        self.craft_type = self.game.mod.craft_types.get(craft_type, 'default')
        self.position = position
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
        self.crew: List[Any] = data.get('crew', [])  # List of crew/unit objects/IDs
        self.crew_status: Dict[Any, str] = {unit: 'active' for unit in self.crew}  # e.g., 'active', 'wounded', 'dead'
        self.mission: Optional[Dict[str, Any]] = None  # Mission assignment
        self.notifications: List[str] = []  # Notification queue
        # AI/Automation attributes
        self.ai_patrol_enabled = data.get('ai_patrol_enabled', False)
        self.ai_auto_intercept_enabled = data.get('ai_auto_intercept_enabled', False)
        self.ai_auto_return_enabled = data.get('ai_auto_return_enabled', True)
        self.ai_auto_resupply_enabled = data.get('ai_auto_resupply_enabled', True)
        self.patrol_route = data.get('patrol_route', [])  # List of waypoints

    def get_ammo_status(self):
        """
        Returns remaining ammo for each item in the craft's inventory.

        Returns:
            dict: Mapping of item names to current ammo count.
        """
        return {name: data['current_ammo'] for name, data in self.items.items()}

    # Crew management
    def embark_unit(self, unit):
        """
        Embark a unit onto the craft as crew.

        Args:
            unit: The unit to embark.
        """
        if unit not in self.crew:
            self.crew.append(unit)
            self.crew_status[unit] = 'active'
            self.add_notification(f"Unit {unit} embarked.")

    def disembark_unit(self, unit):
        """
        Remove a unit from the craft's crew.

        Args:
            unit: The unit to disembark.
        """
        if unit in self.crew:
            self.crew.remove(unit)
            self.crew_status.pop(unit, None)
            self.add_notification(f"Unit {unit} disembarked.")

    def set_crew_status(self, unit, status):
        """
        Set the status of a crew member (e.g., 'active', 'wounded', 'dead').

        Args:
            unit: The unit whose status to set.
            status (str): The new status.
        """
        if unit in self.crew:
            self.crew_status[unit] = status
            self.add_notification(f"Unit {unit} status changed to {status}.")

    def get_crew(self):
        """
        Get the list of crew members.

        Returns:
            list: List of crew/unit objects/IDs.
        """
        return self.crew

    def get_crew_status(self, unit):
        """
        Get the status of a specific crew member.

        Args:
            unit: The unit to check.

        Returns:
            str: Status of the unit, or None if not found.
        """
        return self.crew_status.get(unit, None)

    # Mission assignment
    def assign_mission(self, mission: Dict[str, Any]):
        """
        Assign a mission to the craft.

        Args:
            mission (dict): Mission assignment data.
        """
        self.mission = mission
        self.add_notification(f"Mission assigned: {mission.get('name', 'Unknown')}")

    def complete_mission(self):
        """
        Mark the current mission as completed and clear it.
        """
        if self.mission:
            self.add_notification(f"Mission completed: {self.mission.get('name', 'Unknown')}")
            self.mission = None

    def get_mission_status(self):
        """
        Get the current mission assignment.

        Returns:
            dict: Current mission data, or None if not assigned.
        """
        return self.mission

    # Notification system
    def add_notification(self, message: str):
        """
        Add a notification message to the craft's queue.

        Args:
            message (str): The notification message.
        """
        self.notifications.append(message)

    def get_notifications(self) -> List[str]:
        """
        Retrieve and clear all notifications for the craft.

        Returns:
            list: List of notification messages.
        """
        notes = self.notifications[:]
        self.notifications.clear()
        return notes

    # AI/Automation routines
    def enable_patrol(self, route):
        """
        Enable patrol automation and set the patrol route.

        Args:
            route (list): List of waypoints.
        """
        self.ai_patrol_enabled = True
        self.patrol_route = route
        self.add_notification("Patrol enabled.")

    def disable_patrol(self):
        """
        Disable patrol automation.
        """
        self.ai_patrol_enabled = False
        self.patrol_route = []
        self.add_notification("Patrol disabled.")

    def enable_auto_intercept(self):
        """
        Enable auto-intercept automation.
        """
        self.ai_auto_intercept_enabled = True
        self.add_notification("Auto-intercept enabled.")

    def disable_auto_intercept(self):
        """
        Disable auto-intercept automation.
        """
        self.ai_auto_intercept_enabled = False
        self.add_notification("Auto-intercept disabled.")

    def enable_auto_return(self):
        """
        Enable auto-return automation.
        """
        self.ai_auto_return_enabled = True
        self.add_notification("Auto-return enabled.")

    def disable_auto_return(self):
        """
        Disable auto-return automation.
        """
        self.ai_auto_return_enabled = False
        self.add_notification("Auto-return disabled.")

    def enable_auto_resupply(self):
        """
        Enable auto-resupply automation.
        """
        self.ai_auto_resupply_enabled = True
        self.add_notification("Auto-resupply enabled.")

    def disable_auto_resupply(self):
        """
        Disable auto-resupply automation.
        """
        self.ai_auto_resupply_enabled = False
        self.add_notification("Auto-resupply disabled.")

    def ai_tick(self):
        """
        Process automation routines for the craft. Should be called each turn/day.

        Handles patrol, auto-intercept, auto-return, and auto-resupply logic.
        """
        if self.ai_patrol_enabled and self.patrol_route:
            self.add_notification("Patrolling route.")
            # Move to next waypoint (not implemented)
        if self.ai_auto_intercept_enabled:
            self.add_notification("Auto-intercept check.")
            # Check for nearby UFOs and intercept (not implemented)
        if self.ai_auto_return_enabled:
            if hasattr(self, 'current_fuel') and hasattr(self, 'max_fuel'):
                if self.current_fuel < self.max_fuel * 0.2:
                    self.add_notification("Auto-returning to base due to low fuel.")
                    # Return to base (not implemented)
        if self.ai_auto_resupply_enabled:
            # If at base and low on fuel/ammo, trigger resupply (not implemented)
            pass

