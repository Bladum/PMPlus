from economy.manufacture_entry import TManufactureEntry


class TManufacture:
    """
    Represents a manufacturing projects, with list of manufacture entries
    """

    def __init__(self, data=None):
        # Dictionary to store all manufacturing entries
        self.entries = {}

        if data:
            self.load(data)

    def load(self, data):
        """
        Load manufacturing data from a dictionary (parsed from TOML)

        Args:
            data: Dictionary containing manufacturing data
        """
        if not data or 'manufacturing' not in data:
            return

        manufacturing_data = data['manufacturing']

        for project_id, project_info in manufacturing_data.items():
            # Skip the main manufacturing section if it's empty
            if not isinstance(project_info, dict):
                continue

            # Create a new manufacturing entry
            entry = TManufactureEntry(project_id, project_info)
            self.entries[project_id] = entry

    def get_entry(self, project_id):
        """
        Get a specific manufacturing entry

        Args:
            project_id: ID of the manufacturing project to retrieve

        Returns:
            TManufactureEntry object if found, None otherwise
        """
        return self.entries.get(project_id, None)

    def get_projects_by_category(self, category):
        """
        Get manufacturing projects filtered by a specific category

        Args:
            category: Type of manufacturing projects to filter by

        Returns:
            List of manufacturing entries matching the category
        """
        return [entry for entry in self.entries.values() if entry.category == category]

    def get_available_projects(self, available_technologies=None, available_services=None, available_items=None):
        """
        Get list of manufacturing projects that are available based on requirements

        Args:
            available_technologies: List of researched technologies
            available_services: List of services available in the base
            available_items: Dictionary of items in storage with quantities

        Returns:
            List of available manufacturing projects
        """
        if available_technologies is None:
            available_technologies = []
        if available_services is None:
            available_services = []
        if available_items is None:
            available_items = {}

        available = []

        for project_id, entry in self.entries.items():
            # Check if all required technologies are researched
            if not all(tech in available_technologies for tech in entry.technology):
                continue

            # Check if all required services are available
            if not all(service in available_services for service in entry.service_needed):
                continue

            # Check if all required items are available in sufficient quantity
            has_all_items = True
            for item, quantity in entry.items_needed.items():
                if item not in available_items or available_items[item] < quantity:
                    has_all_items = False
                    break

            if not has_all_items:
                continue

            available.append(entry)

        return available