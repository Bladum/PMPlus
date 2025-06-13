"""
ManufacturingManager: Manages active manufacturing projects and workshop capacity.
Purpose: Handles starting projects, daily progress, and resource management.
Last update: 2025-06-12
"""

from .manufacturing_project import ManufacturingProject
import logging


class ManufacturingManager:
    """
    Manages all active manufacturing projects across all bases.
    Handles workshop capacity allocation, daily progress, and project lifecycle.
    
    Attributes:
        active_projects (dict): Dictionary of base_id -> list of ManufacturingProject
        workshop_capacity (dict): Dictionary of base_id -> available workshop capacity
    """
    
    def __init__(self):
        """Initialize the manufacturing manager."""
        self.active_projects = {}  # base_id -> [ManufacturingProject]
        self.workshop_capacity = {}  # base_id -> capacity

    def set_base_workshop_capacity(self, base_id, capacity):
        """
        Set the workshop capacity for a base.
        
        Args:
            base_id (str): Base identifier
            capacity (int): Workshop capacity in man-days per day
        """
        self.workshop_capacity[base_id] = capacity
        if base_id not in self.active_projects:
            self.active_projects[base_id] = []

    def get_base_workshop_capacity(self, base_id):
        """Get total workshop capacity for a base."""
        return self.workshop_capacity.get(base_id, 0)

    def get_used_workshop_capacity(self, base_id):
        """Get currently used workshop capacity for a base."""
        if base_id not in self.active_projects:
            return 0
        return sum(project.workshop_capacity for project in self.active_projects[base_id] 
                  if project.is_active())

    def get_available_workshop_capacity(self, base_id):
        """Get available workshop capacity for a base."""
        total = self.get_base_workshop_capacity(base_id)
        used = self.get_used_workshop_capacity(base_id)
        return total - used

    def can_start_project(self, base_id, entry, quantity, required_capacity=1):
        """
        Check if a manufacturing project can be started.
        
        Args:
            base_id (str): Base where project would run
            entry (TManufactureEntry): Manufacturing entry to check
            quantity (int): Number of items to build
            required_capacity (int): Workshop capacity needed
              Returns:
            tuple: (can_start: bool, reason: str)
        """
        # Check workshop capacity
        available_capacity = self.get_available_workshop_capacity(base_id)
        if available_capacity < required_capacity:
            return False, f"Insufficient workshop capacity (need {required_capacity}, have {available_capacity})"
        
        return True, "Can start project"

    def start_project(self, base_id, entry, quantity, workshop_capacity=1):
        """
        Start a new manufacturing project.
        
        Args:
            base_id (str): Base where project will run
            entry (TManufactureEntry): Manufacturing entry
            quantity (int): Number of items to build
            workshop_capacity (int): Workshop capacity to allocate
            
        Returns:
            ManufacturingProject or None: Created project if successful
        """
        # Check if there's already an active project of this type
        if self.has_active_project_of_type(base_id, entry.pid):
            logging.warning(f"Cannot start project {entry.pid}: Already have an active project of this type at base {base_id}")
            return None
            
        can_start, reason = self.can_start_project(base_id, entry, quantity, workshop_capacity)
        if not can_start:
            logging.warning(f"Cannot start project {entry.pid}: {reason}")
            return None

        # Create new project
        project = ManufacturingProject(
            entry_id=entry.pid,
            base_id=base_id,
            quantity=quantity,
            build_time_per_item=entry.build_time,
            workshop_capacity=workshop_capacity
        )

        # Add to active projects
        if base_id not in self.active_projects:
            self.active_projects[base_id] = []
        self.active_projects[base_id].append(project)

        logging.info(f"Started manufacturing project: {entry.name} x{quantity} at base {base_id}")
        return project

    def pause_project(self, project_id):
        """Pause a manufacturing project."""
        project = self.get_project(project_id)
        if project:
            project.pause()
            logging.info(f"Paused project {project_id}")

    def resume_project(self, project_id):
        """Resume a manufacturing project."""
        project = self.get_project(project_id)
        if project:
            project.resume()
            logging.info(f"Resumed project {project_id}")

    def cancel_project(self, project_id):
        """Cancel a manufacturing project."""
        project = self.get_project(project_id)
        if project:
            project.cancel()
            logging.info(f"Cancelled project {project_id}")

    def change_project_quantity(self, project_id, new_quantity):
        """
        Change the quantity of items to build in a project.
        
        Args:
            project_id (str): Project identifier
            new_quantity (int): New quantity to build
            
        Returns:
            tuple: (success: bool, message: str)
        """
        project = self.get_project(project_id)
        if not project:
            return False, f"Project {project_id} not found"
            
        if project.status not in ['active', 'paused']:
            return False, f"Cannot change quantity of {project.status} project"
            
        success = project.change_quantity(new_quantity)
        if success:
            logging.info(f"Changed project {project_id} quantity to {new_quantity}")
            return True, f"Successfully changed quantity to {new_quantity}"
        else:
            return False, f"Cannot reduce quantity below {project.items_completed} (already completed items)"

    def get_project(self, project_id):
        """Find a project by ID across all bases."""
        for base_projects in self.active_projects.values():
            for project in base_projects:
                if project.project_id == project_id:
                    return project
        return None

    def has_active_project_of_type(self, base_id, entry_id):
        """
        Check if there's already an active project of the same type at this base.
        
        Args:
            base_id (str): Base identifier
            entry_id (str): Manufacturing entry ID to check
              Returns:
            bool: True if there's already an active project of this type
        """
        if base_id not in self.active_projects:
            return False
            
        for project in self.active_projects[base_id]:
            if project.entry_id == entry_id and project.status in ['active', 'paused']:
                return True
        return False

    def get_base_projects(self, base_id, status=None):
        """
        Get all projects for a specific base.
        
        Args:
            base_id (str): Base identifier
            status (str, optional): Filter by status ('active', 'paused', 'completed', 'cancelled')
            
        Returns:
            list: List of ManufacturingProject objects
        """
        if base_id not in self.active_projects:
            return []
        
        projects = self.active_projects[base_id]
        if status:
            projects = [p for p in projects if p.status == status]
        return projects

    def daily_progress(self, game=None):
        """
        Process daily progress for all active manufacturing projects.
        
        Args:
            game: Game instance for tracking manufacturing hours
        
        Returns:
            dict: base_id -> list of completed items info
        """
        completed_items = {}
        
        for base_id, projects in self.active_projects.items():
            base_completions = []
            
            for project in projects:
                if project.is_active():
                    items_completed_today, hours_worked = project.advance_progress(project.workshop_capacity)
                    
                    # Track manufacturing hours for monthly invoicing
                    if game and hours_worked > 0:
                        game.track_manufacturing_hours(base_id, project.entry_id, hours_worked)
                    
                    if items_completed_today > 0 or hours_worked > 0:
                        base_completions.append({
                            'project_id': project.project_id,
                            'entry_id': project.entry_id,
                            'items_completed': items_completed_today,
                            'hours_worked': hours_worked,
                            'project_completed': project.is_completed()
                        })
            
            if base_completions:
                completed_items[base_id] = base_completions
        
        # Clean up completed projects (optional - you might want to keep them for history)
        self._cleanup_completed_projects()
        
        return completed_items

    def _cleanup_completed_projects(self):
        """Remove completed projects from active list (optional)."""
        for base_id in self.active_projects:
            self.active_projects[base_id] = [
                p for p in self.active_projects[base_id] 
                if p.status != 'completed'
            ]

    def get_project_summary(self, base_id):
        """
        Get a summary of manufacturing status for a base.
        
        Returns:
            dict: Summary information
        """
        projects = self.get_base_projects(base_id)
        active_projects = [p for p in projects if p.is_active()]
        
        return {
            'total_capacity': self.get_base_workshop_capacity(base_id),
            'used_capacity': self.get_used_workshop_capacity(base_id),
            'available_capacity': self.get_available_workshop_capacity(base_id),
            'active_projects': len(active_projects),
            'total_projects': len(projects),
            'projects': projects
        }
