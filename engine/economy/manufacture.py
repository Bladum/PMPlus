"""
TManufacture: Manages manufacturing projects and their entries.
Purpose: Handles loading, filtering, and availability checks for manufacturing projects.
Last update: 2025-06-10
"""

from economy.manufacture_entry import TManufactureEntry
import logging


class TManufacture:
    """
    Manages a collection of manufacturing projects (TManufactureEntry).
    Provides methods to load, filter, and check availability of manufacturing projects.

    Attributes:
        entries (dict): Dictionary of project_id -> TManufactureEntry
    """

    def __init__(self, data=None):
        """
        Initialize the TManufacture manager.

        Args:
            data (dict, optional): Dictionary containing manufacturing data (parsed from TOML).
        """
        # Dictionary to store all manufacturing entries
        self.entries = {}

        if data:
            self.load(data)

    def load(self, data):
        """
        Load manufacturing data from a dictionary (parsed from TOML)

        Args:
            data (dict): Dictionary containing manufacturing data
        """
        if not data or 'manufacturing' not in data:
            logging.warning("No 'manufacturing' section found in data.")
            return

        manufacturing_data = data['manufacturing']

        for project_id, project_info in manufacturing_data.items():
            # Skip the main manufacturing section if it's empty
            if not isinstance(project_info, dict):
                continue

            # Create a new manufacturing entry
            try:
                entry = TManufactureEntry(project_id, project_info)
                self.entries[project_id] = entry
            except Exception as e:
                logging.error(f"Failed to load manufacture entry {project_id}: {e}")

    def get_entry(self, project_id):
        """
        Get a specific manufacturing entry by project_id.

        Args:
            project_id (str): ID of the manufacturing project to retrieve.

        Returns:
            TManufactureEntry or None: The entry if found, else None.
        """
        return self.entries.get(project_id, None)

    def get_projects_by_category(self, category):
        """
        Get manufacturing projects filtered by a specific category.

        Args:
            category (str): Type of manufacturing projects to filter by

        Returns:
            list: List of manufacturing entries matching the category
        """
        return [entry for entry in self.entries.values() if getattr(entry, 'category', None) == category]

    def get_available_projects(self, available_technologies=None, available_services=None, available_items=None):
        """
        Get list of manufacturing projects that are available based on requirements

        Args:
            available_technologies (list, optional): List of researched technologies
            available_services (list, optional): List of services available in the base
            available_items (dict, optional): Dictionary of items in storage with quantities

        Returns:
            list: List of available manufacturing projects (TManufactureEntry)
        """
        available_technologies = available_technologies or []
        available_services = available_services or []
        available_items = available_items or {}

        available = []

        for project_id, entry in self.entries.items():
            techs = getattr(entry, 'tech_start', [])
            # Check if all required technologies are researched
            if not all(tech in available_technologies for tech in techs):
                continue

            services = getattr(entry, 'services_needed', [])
            # Check if all required services are available
            if not all(service in available_services for service in services):
                continue

            # Check if all required items are available in sufficient quantity
            has_all_items = True
            for item, quantity in getattr(entry, 'items_needed', {}).items():
                if item not in available_items or available_items[item] < quantity:
                    has_all_items = False
                    break

            if not has_all_items:
                continue

            available.append(entry)

        return available