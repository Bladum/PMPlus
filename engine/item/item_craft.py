"""
TCraftItem: Represents a craft-specific item for vehicles/craft.

Manages craft equipment state, maintenance, and provides methods for craft system integration.

Classes:
    TCraftItem: Main class for craft/vehicle equipment items.

Last standardized: 2025-06-14
"""

from typing import Dict, Any, Optional
from .item import TItem
from .item_type import TItemType


class TCraftItem(TItem):
    """
    Represents a craft-specific item for vehicles/craft.

    Manages craft equipment state, maintenance, and provides methods for craft system integration.

    Attributes:
        maintenance_status (int): Percentage of operational status.
        last_maintenance (int): Game time of last maintenance.
        rearm_time_left (int): Time left to rearm.
        reload_time_left (int): Time left to reload.
        active (bool): Whether the item is active.
        hardpoint_type (str): Type of hardpoint (e.g., 'WEAPON').
        ammo (int): Current ammo count.
    """

    def __init__(self, item_type_id: str, item_id: Optional[str] = None):
        """
        Initialize a new craft item.

        Args:
            item_type_id (str): ID of the craft item type to use.
            item_id (Optional[str]): Unique identifier (generated if not provided).
        """
        # Initialize base item
        super().__init__(item_type_id, item_id)

        # Craft-specific attributes
        self.maintenance_status = 100  # Percentage of operational status
        self.last_maintenance = 0      # Game time of last maintenance
        self.rearm_time_left = 0
        self.reload_time_left = 0
        self.active = True
        self.hardpoint_type = 'WEAPON'
        self.ammo = 0

    def ammo_needed(self) -> int:
        """
        Calculate how much ammo is needed to fully reload.

        Returns:
            int: Number of ammo units needed.
        """
        return max(0, self.item_type.craft_ammo - self.ammo)

    def get_rearm_cost(self) -> int:
        """
        Calculate the cost to fully rearm the craft item.

        Returns:
            int: Rearm cost.
        """
        return self.ammo_needed() * getattr(self.item_type, 'craft_rearm_cost', 0)

    def is_active(self) -> bool:
        """
        Check if the item is active.

        Returns:
            bool: True if active, False otherwise.
        """
        return self.active

    def activate(self) -> None:
        """
        Activate the item.
        """
        self.active = True

    def deactivate(self) -> None:
        """
        Deactivate the item.
        """
        self.active = False

    def is_ready(self) -> bool:
        """
        Check if the item is ready for use (reloaded and has ammo).

        Returns:
            bool: True if ready, False otherwise.
        """
        return self.reload_time_left <= 0 and self.ammo > 0 and self.active

    def start_reload(self) -> None:
        """
        Start the reload process for the item.
        """
        self.reload_time_left = getattr(self.item_type, 'craft_reload_time', 0)

    def start_rearm(self) -> None:
        """
        Start the rearm process for the item.
        """
        self.rearm_time_left = getattr(self.item_type, 'craft_rearm_time', 12)

    def tick_reload(self) -> int:
        """
        Progress the reload timer by one tick.

        Returns:
            int: Remaining reload time.
        """
        if self.reload_time_left > 0:
            self.reload_time_left -= 1
            if self.reload_time_left == 0 and self.ammo_needed() > 0:
                self.ammo = min(self.ammo + 1, self.item_type.craft_ammo)
        return self.reload_time_left

    def tick_rearm(self) -> int:
        """
        Progress the rearm timer by one tick.

        Returns:
            int: Remaining rearm time.
        """
        if self.rearm_time_left > 0:
            self.rearm_time_left -= 1
            if self.rearm_time_left == 0:
                self.ammo = self.item_type.craft_ammo
        return self.rearm_time_left

    def get_compatible_hardpoints(self) -> list[str]:
        """
        Get a list of compatible hardpoint types for this item.

        Returns:
            list[str]: List of compatible hardpoint types.
        """
        return [self.hardpoint_type]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the craft item to a dictionary for serialization.

        Returns:
            dict: Dictionary representation of the craft item.
        """
        data = {
            'id': self.id,
            'name': getattr(self, 'name', None),
            'icon_path': getattr(self, 'sprite', None),
            'item_type_id': self.item_type.id if self.item_type else None,
            'weight': getattr(self, 'weight', 1),
            'active': self.active,
            'ammo': self.ammo,
            'max_ammo': self.item_type.craft_ammo,
            'reload_time_left': self.reload_time_left,
            'rearm_time_left': self.rearm_time_left,
            'hardpoint_type': self.hardpoint_type,
        }
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any], game_instance) -> 'TCraftItem':
        """
        Create a craft item instance from a dictionary representation.

        Args:
            data (dict): Dictionary representation of the craft item.
            game_instance: Game instance for type lookup.

        Returns:
            TCraftItem: New TCraftItem instance.
        """
        item_type = None
        if data.get('item_type_id'):
            item_type = game_instance.mod.item_types.get(data['item_type_id'])
        craft_item = cls(
            item_type_id=data['item_type_id'],
            item_id=data.get('id')
        )
        craft_item.active = data.get('active', True)
        craft_item.ammo = data.get('ammo', 0)
        craft_item.reload_time_left = data.get('reload_time_left', 0)
        craft_item.rearm_time_left = data.get('rearm_time_left', 0)
        craft_item.hardpoint_type = data.get('hardpoint_type', 'WEAPON')
        return craft_item
