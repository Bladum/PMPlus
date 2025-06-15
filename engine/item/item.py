"""
TItem: Base class for all game items.

Provides common properties and behaviors for all items in the game, including serialization, inventory compatibility, and UI display.

Classes:
    TItem: Main class for game items.

Last standardized: 2025-06-14
"""

from typing import Dict, Any, Optional
from enums import Enum
from .item_type import TItemType


class TItem:
    """
    Base class for all game items.

    Encapsulates common properties and behaviors for item instances that can be stored in inventories, equipped by units, etc.

    Attributes:
        name (str): Human-readable item name.
        sprite (str): Path to item's visual icon.
        properties (dict): Additional item-specific properties.
        item_type (TItemType): Type reference for this item.
        weight (int): Item weight for inventory management.
        id (str): Unique identifier for this item instance.
    """

    def __init__(self, item_type_id: str, item_id: Optional[str] = None):
        """
        Initialize a new item with properties from its type definition.

        Args:
            item_type_id (str): ID of the item's type definition to use for static parameters.
            item_id (Optional[str]): Unique identifier (generated if not provided).
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
            size (Optional[int]): Optional pixel size for the image (maintains aspect ratio).

        Returns:
            QPixmap: QPixmap object for the item's icon.
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
            list[str]: List of slot identifiers this item can be equipped to.
        """
        return self.properties.get('compatible_slots', [])

    def get_category(self) -> int:
        """
        Get the item's category.

        Returns:
            int: Integer representing the item category from TItemType constants.
        """
        if hasattr(self.item_type, 'category'):
            return self.item_type.category
        return TItemType.ITEM_GENERAL

    def get_display_name(self) -> str:
        """
        Get a formatted display name for the item.

        Returns:
            str: String with item name.
        """
        return self.name

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the item to a dictionary for serialization.

        Returns:
            dict: Dictionary representation of the item.
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
            data (dict): Dictionary representation of the item.
            type_registry (dict): Dictionary mapping type IDs to TItemType objects.

        Returns:
            TItem: New TItem instance.
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
        """
        Check if two items are equal (same ID).

        Args:
            other (TItem): Another item to compare.

        Returns:
            bool: True if IDs match, False otherwise.
        """
        if not isinstance(other, TItem):
            return False
        return self.id == other.id

    def __hash__(self):
        """
        Hash based on item ID.

        Returns:
            int: Hash value.
        """
        return hash(self.id)

    def __str__(self):
        """
        String representation of the item.

        Returns:
            str: Human-readable string.
        """
        return f"{self.name} [{self.id[:8]}]"

    def __repr__(self):
        """
        Detailed representation of the item.

        Returns:
            str: Debug string.
        """
        return f"TItem(type='{self.item_type.pid}', id='{self.id[:8]}')"
