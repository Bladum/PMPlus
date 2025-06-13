"""
TManufacture: Manages manufacturing projects and their entries.
Purpose: Handles loading, filtering, and availability checks for manufacturing projects.
Last update: 2025-06-10
"""

from .manufacture_entry import TManufactureEntry
from .manufacturing_manager import ManufacturingManager
import logging


class TManufacture:
    """
    Manages a collection of manufacturing projects (TManufactureEntry).
    Provides methods to load, filter, and check availability of manufacturing projects.

    Attributes:
        entries (dict): Dictionary of project_id -> TManufactureEntry
        manufacturing_manager (ManufacturingManager): Manages active projects and workshop allocation
    """

    def __init__(self, data=None):
        """
        Initialize the TManufacture manager.

        Args:
            data (dict, optional): Dictionary containing manufacturing data (parsed from TOML).
        """
        # Dictionary to store all manufacturing entries
        self.entries = {}
        
        # Manufacturing manager for active projects
        self.manufacturing_manager = ManufacturingManager()

        if data:
            self.load(data)

    def load(self, data):
        """
        Load manufacturing entries from data.

        Args:
            data (dict): Manufacturing data.
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
        Get a manufacturing entry by project ID.

        Args:
            project_id (str): Project ID.

        Returns:
            TManufactureEntry or None: The entry if found.
        """
        return self.entries.get(project_id, None)

    def get_projects_by_category(self, category):
        """
        Get all projects in a given category.

        Args:
            category (str): Category name.

        Returns:
            list: List of TManufactureEntry objects.
        """
        return [entry for entry in self.entries.values() if getattr(entry, 'category', None) == category]

    def get_available_projects(self, available_technologies=None, available_services=None, available_items=None):
        """
        Get all projects available for manufacturing given current resources.

        Args:
            available_technologies (list): Technologies available.
            available_services (list): Services available.
            available_items (dict): Items available.

        Returns:
            list: List of available TManufactureEntry objects.
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

    def can_afford_project(self, entry, quantity, available_money):
        """
        Check if a project can be afforded given available money.

        Args:
            entry (TManufactureEntry): The project entry.
            quantity (int): Number of items to manufacture.
            available_money (int): Money available.

        Returns:
            bool: True if affordable, False otherwise.
        """
        total_cost = entry.build_cost * quantity
        return available_money >= total_cost, total_cost

    def validate_project_requirements(self, entry, base_id, quantity, 
                                    available_technologies=None, 
                                    available_services=None, 
                                    available_items=None,
                                    available_money=0):
        """
        Validate all requirements for starting a manufacturing project.

        Args:
            entry (TManufactureEntry): The project entry.
            base_id (str): Base identifier.
            quantity (int): Number of items to manufacture.
            available_technologies (list): Technologies available.
            available_services (list): Services available.
            available_items (dict): Items available.
            available_money (int): Money available.

        Returns:
            (bool, list): (True if valid, list of issues if not)
        """
        issues = []
        
        # Check technologies
        available_technologies = available_technologies or []
        for tech in entry.tech_start:
            if tech not in available_technologies:
                issues.append(f"Missing required technology: {tech}")
        
        # Check services
        available_services = available_services or []
        for service in entry.services_needed:
            if service not in available_services:
                issues.append(f"Missing required service: {service}")
        
        # Check items
        available_items = available_items or {}
        for item, needed_per_unit in entry.items_needed.items():
            total_needed = needed_per_unit * quantity
            available = available_items.get(item, 0)
            if available < total_needed:
                issues.append(f"Insufficient {item}: need {total_needed}, have {available}")
        
        # Check money
        can_afford, total_cost = self.can_afford_project(entry, quantity, available_money)
        if not can_afford:
            issues.append(f"Insufficient funds: need {total_cost}, have {available_money}")
        
        # Check workshop capacity
        can_start_workshop, workshop_reason = self.manufacturing_manager.can_start_project(
            base_id, entry, quantity, 1
        )
        if not can_start_workshop:
            issues.append(workshop_reason)
        
        return len(issues) == 0, issues

    def start_manufacturing_project(self, entry_id, base_id, quantity, 
                                  available_technologies=None,
                                  available_services=None, 
                                  available_items=None,
                                  available_money=0,
                                  workshop_capacity=1):
        """
        Start a new manufacturing project if requirements are met.

        Args:
            entry_id (str): Project ID.
            base_id (str): Base identifier.
            quantity (int): Number of items to manufacture.
            available_technologies (list): Technologies available.
            available_services (list): Services available.
            available_items (dict): Items available.
            available_money (int): Money available.
            workshop_capacity (int): Workshop capacity to allocate.

        Returns:
            (bool, str or None, list): (Success, project ID if created, issues if any)
        """
        entry = self.get_entry(entry_id)
        if not entry:
            return False, f"Manufacturing entry '{entry_id}' not found"
        
        # Check if there's already an active project of this type
        if self.manufacturing_manager.has_active_project_of_type(base_id, entry_id):
            return False, f"Cannot start project: Already have an active project of type '{entry_id}' at this base"
        
        # Validate all requirements
        can_start, issues = self.validate_project_requirements(
            entry, base_id, quantity, available_technologies, 
            available_services, available_items, available_money
        )
        
        if not can_start:
            return False, "; ".join(issues)
        
        # Start the project
        project = self.manufacturing_manager.start_project(
            base_id, entry, quantity, workshop_capacity
        )
        
        if project:
            project.cost_paid = True  # Mark cost as paid
            return True, project
        else:
            return False, "Failed to start project"

    def get_manufacturing_status(self, base_id):
        """
        Get the status of all manufacturing projects for a base.

        Args:
            base_id (str): Base identifier.

        Returns:
            list: List of project status summaries.
        """
        return self.manufacturing_manager.get_project_summary(base_id)

    def process_daily_manufacturing(self, game=None):
        """
        Advance all manufacturing projects by one day.

        Args:
            game: Game context (optional).
        """
        return self.manufacturing_manager.daily_progress(game)

    def set_base_workshop_capacity(self, base_id, capacity):
        """
        Set the workshop capacity for a base.

        Args:
            base_id (str): Base identifier.
            capacity (int): Workshop capacity.
        """
        self.manufacturing_manager.set_base_workshop_capacity(base_id, capacity)

    def pause_project(self, project_id):
        """
        Pause a manufacturing project.

        Args:
            project_id (str): Project ID.
        """
        self.manufacturing_manager.pause_project(project_id)

    def resume_project(self, project_id):
        """
        Resume a paused manufacturing project.

        Args:
            project_id (str): Project ID.
        """
        self.manufacturing_manager.resume_project(project_id)

    def cancel_project(self, project_id):
        """
        Cancel a manufacturing project.

        Args:
            project_id (str): Project ID.
        """
        self.manufacturing_manager.cancel_project(project_id)

    def change_project_quantity(self, project_id, new_quantity):
        """
        Change the quantity for an active manufacturing project.

        Args:
            project_id (str): Project ID.
            new_quantity (int): New quantity to manufacture.
        """
        return self.manufacturing_manager.change_project_quantity(project_id, new_quantity)