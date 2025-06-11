"""
TPediaEntryType: Represents a type/category of pedia entry.
Purpose: Used to define and manage different entry types in the UFOpedia system.
Last update: 2025-06-11
"""

class TPediaEntryType:
    """
    Represents a single entry type in the UFOpedia.
    Used for categorizing and managing pedia entries by type.

    Attributes:
        type_id (int): Unique identifier for the entry type/category.
        name (str): Display name for the category.
        description (str): Description of the category/type.
        icon (str): Icon or sprite reference for the category.
        order (int): Display order for the category.
    """
    def __init__(self, type_id, name, description='', icon='', order=0):
        """
        Initialize a TPediaEntryType.

        Args:
            type_id (int): Unique identifier for the entry type/category.
            name (str): Display name for the category.
            description (str): Description of the category/type.
            icon (str): Icon or sprite reference for the category.
            order (int): Display order for the category.
        """
        self.type_id = type_id
        self.name = name
        self.description = description
        self.icon = icon
        self.order = order
