"""
Represents a craft-specific item.

This class manages items specifically designed for craft/vehicle use with
features like power consumption, maintenance requirements, and craft-specific
bonuses. It references static parameters from the underlying item type.

Interactions:
- References TItemType for static craft parameters
- Used by craft systems to apply performance modifiers
- Maintains current state of craft equipment
- Provides interface for craft equipment management

Key Features:
- Power management for craft systems
- Maintenance status and requirements
- Craft performance modifiers (speed, fuel efficiency, etc.)
- Specialized equipment functionality
"""

from typing import Dict, Any, Optional
from .item import TItem
from .item_type import TItemType


class TCraftItem(TItem):

    def __init__(self, item_type_id: str, item_id: Optional[str] = None):
        """
        Initialize a new craft item.

        Args:
            item_type_id: ID of the craft item type to use
            item_id: Unique identifier (generated if not provided)
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
        return max(0, self.item_type.craft_ammo - self.ammo)

    def get_rearm_cost(self) -> int:
        return self.ammo_needed() * getattr(self.item_type, 'craft_rearm_cost', 0)

    def is_active(self) -> bool:
        return self.active

    def activate(self) -> None:
        self.active = True

    def deactivate(self) -> None:
        self.active = False

    def is_ready(self) -> bool:
        return self.reload_time_left <= 0 and self.ammo > 0 and self.active

    def start_reload(self) -> None:
        self.reload_time_left = getattr(self.item_type, 'craft_reload_time', 0)

    def start_rearm(self) -> None:
        self.rearm_time_left = getattr(self.item_type, 'craft_rearm_time', 12)

    def tick_reload(self) -> int:
        if self.reload_time_left > 0:
            self.reload_time_left -= 1
            if self.reload_time_left == 0 and self.ammo_needed() > 0:
                self.ammo = min(self.ammo + 1, self.item_type.craft_ammo)
        return self.reload_time_left

    def tick_rearm(self) -> int:
        if self.rearm_time_left > 0:
            self.rearm_time_left -= 1
            if self.rearm_time_left == 0:
                self.ammo = self.item_type.craft_ammo
        return self.rearm_time_left

    def get_compatible_hardpoints(self) -> list[str]:
        return [self.hardpoint_type]

    def to_dict(self) -> Dict[str, Any]:
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
