"""
XCOM Pedia Module: pedia.py

Main container for the in-game encyclopedia (UFOpedia).

Classes:
    TPedia: Main class for the UFOpedia system.

Last updated: 2025-06-14
"""

class TPedia:
    """
    Represents the entire UFOpedia system, containing all entries and categories.
    Used to manage, search, and display pedia content in the game UI.
    """
    def __init__(self, entries=None, categories=None):
        """
        Initialize the TPedia system.
        Args:
            entries (Optional[dict]): Dictionary of pedia entries (pid -> TPediaEntry).
            categories (Optional[dict]): Dictionary of entry types (type id -> TPediaEntryType).
        """
        self.entries = entries if entries is not None else {}
        self.categories = categories if categories is not None else {}

    def add_entry(self, entry):
        """
        Add a new pedia entry.
        Args:
            entry (TPediaEntry): The entry to add.
        """
        self.entries[entry.pid] = entry

    def get_entry(self, pid):
        """
        Retrieve a pedia entry by its pid.
        Args:
            pid (str): Entry identifier.
        Returns:
            TPediaEntry or None: The entry if found, else None.
        """
        return self.entries.get(pid)

    def list_entries_by_type(self, type_id):
        """
        List all entries of a given type/category.
        Args:
            type_id (int): The type/category id.
        Returns:
            list: List of TPediaEntry objects.
        """
        return [e for e in self.entries.values() if e.type == type_id]

    def add_category(self, category):
        """
        Add a new entry type/category.
        Args:
            category (TPediaEntryType): The category to add.
        """
        self.categories[category.type_id] = category

    def get_category(self, type_id):
        """
        Retrieve a category/type by its id.
        Args:
            type_id (int): The type/category id.
        Returns:
            TPediaEntryType or None: The category if found, else None.
        """
        return self.categories.get(type_id)
