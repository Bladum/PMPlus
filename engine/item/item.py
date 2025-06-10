"""
Base class for all game items.

This class encapsulates common properties and behaviors for all items in the game.
It serves as a foundation for specialized item types (weapons, armor, equipment)
and provides a consistent interface for inventory management.

Interactions:
- Used by TItemTransferManager for drag/drop operations
- Referenced by inventory UIs for displaying items
- Extended by specialized item classes (TItemWeapon, TItemArmour)
- Used for serialization and storage of item instances
- Provides interface for property and metadata access

Key Features:
- Core item properties (name, type, weight)
- Visual representation for inventory display
- Property access for UI and game systems
- Compatibility checking with inventory slots
- Serialization support for saving/loading
"""

from typing import Dict, Any, Optional
from enums import Enum
from .item_type import TItemType


class TItem:
    """
    Base class for all game items.

    Encapsulates common properties and behaviors for item instances
    that can be stored in inventories, equipped by units, etc.

    Attributes:
        name: Human-readable item name
        sprite: Path to item's visual icon
        properties: Dictionary of additional item-specific properties
        item_type: Type reference for this item
        weight: Item weight for inventory management
        id: Unique identifier for this item instance
    """

    def __init__(self, item_type_id: str, item_id: Optional[str] = None):
        """
        Initialize a new item with properties from its type definition.

        Args:
            item_type_id: ID of the item's type definition to use for static parameters
            item_id: Unique identifier (generated if not provided)
        """
        # Get reference to the game's item type registry
        from engine.engine.game import TGame
        self.game = TGame()

        # Get item type reference
        self.item_type = self.game.mod.items.get(item_type_id)

        # Set properties based on item type
        self.name = self.item_type.name
        self.sprite = self.item_type.sprite
        self.weight = self.item_type.weight
        self.properties = {}

        # Generate UUID if no ID provided
        import uuid
        self.id = item_id or str(uuid.uuid4())

    def get_pixmap(self, size: Optional[int] = None) -> 'QPixmap':
        """
        Get a QPixmap representation of the item for UI display.

        Args:
            size: Optional pixel size for the image (maintains aspect ratio)

        Returns:
            QPixmap object for the item's icon
        """
        from PySide6.QtGui import QPixmap
        from PySide6.QtCore import Qt

        pixmap = QPixmap(self.sprite)

        if size is not None and not pixmap.isNull():
            pixmap = pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        return pixmap

    def get_compatible_slots(self) -> list[str]:
        """
        Get list of slot types this item is compatible with.

        Returns:
            List of slot identifiers this item can be equipped to
        """
        return self.properties.get('compatible_slots', [])

    def get_category(self) -> int:
        """
        Get the item's category.

        Returns:
            Integer representing the item category from TItemType constants
        """
        if hasattr(self.item_type, 'category'):
            return self.item_type.category
        return TItemType.ITEM_GENERAL

    def get_display_name(self) -> str:
        """
        Get a formatted display name.

        Returns:
            String with item name
        """
        return self.name

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the item to a dictionary for serialization.

        Returns:
            Dictionary representation of the item
        """
        return {
            'id': self.id,
            'item_type_id': self.item_type.pid if hasattr(self.item_type, 'pid') else None,
            'properties': self.properties,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any], type_registry: Dict[str, TItemType]) -> 'TItem':
        """
        Create an item instance from a dictionary representation.

        Args:
            data: Dictionary representation of the item
            type_registry: Dictionary mapping type IDs to TItemType objects

        Returns:
            New TItem instance
        """
        item_type_id = data.get('item_type_id')

        if not item_type_id:
            raise ValueError("Missing item_type_id in data")

        item = cls(
            item_type_id=item_type_id,
            item_id=data.get('id')
        )

        # Apply any saved properties
        if 'properties' in data:
            item.properties = data.get('properties', {})

        return item

    def __eq__(self, other):
        """Check if two items are equal (same ID)."""
        if not isinstance(other, TItem):
            return False
        return self.id == other.id

    def __hash__(self):
        """Hash based on item ID."""
        return hash(self.id)

    def __str__(self):
        """String representation of the item."""
        return f"{self.name} [{self.id[:8]}]"

    def __repr__(self):
        """Detailed representation of the item."""
        return f"TItem(type='{self.item_type.pid}', id='{self.id[:8]}')"
