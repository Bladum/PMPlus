"""
engine/economy/research_manager.py

Defines the TResearchManager class, which orchestrates all research operations, including entry management, project lifecycle, daily progress, and completion logic.

Classes:
    TResearchManager: Main interface for the research system.

Last standardized: 2025-06-15
"""
from .research_entry import TResearchEntry
from .research_project import ResearchProject
from datetime import date
import uuid

class TResearchManager:
    """
    Manages all research entries, ongoing projects, completed research, and available research.
    Handles validation, daily progress, and completion logic.
    See module docstring for attribute details.
    
    Methods:
        add_entry(entry): Add a research entry and check requirements.
        get_available_research(...): List available research for a base.
        start_research_project(...): Start a new research project.
        process_daily_research(): Advance all projects by one day.
        get_research_status(...): Get status of all projects.
        complete_research_project(...): Mark a project as completed.
        pause_project(...), resume_project(...), cancel_project(...): Project management.
    """
    def __init__(self):
        self.entries = {}  # id -> TResearchEntry
        self.projects = {}  # project_id -> ResearchProject
        self.completed = set()  # set of completed research ids
        self.available = set()  # set of available research ids

    def add_entry(self, entry: TResearchEntry):
        """
        Add a research entry to the manager and check if requirements are met.
        Args:
            entry (TResearchEntry): The research entry to add.
        """
        self.entries[entry.pid] = entry
        if self._requirements_met(entry):
            self.available.add(entry.pid)

    def get_available_research(self, base_id, technologies, items, services, facilities):
        """
        Get a list of available research entries for a base given current state.
        Args:
            base_id (str): Base identifier.
            technologies (list): Known technologies.
            items (dict): Available items.
            services (list): Available services.
            facilities (list): Available facilities.
        Returns:
            list: List of available TResearchEntry objects.
        """
        available = []
        for entry in self.entries.values():
            if entry.pid in self.completed:
                continue
            if not self._requirements_met(entry, technologies, items, services, facilities):
                continue
            available.append(entry)
        return available

    def start_research_project(self, entry_id, base_id, assigned_capacity):
        """
        Start a new research project for a given entry and base.
        Args:
            entry_id (str): Research entry ID.
            base_id (str): Base identifier.
            assigned_capacity (int): Man-days per day assigned.
        Returns:
            None
        """
        entry = self.entries.get(entry_id)
        if not entry:
            return False, 'Entry not found'
        if entry_id in self.completed:
            return False, 'Already completed'
        # Check requirements (should be checked before calling)
        project_id = str(uuid.uuid4())
        project = ResearchProject(project_id, entry_id, base_id, assigned_capacity)
        self.projects[project_id] = project
        return True, project

    def process_daily_research(self):
        """
        Advance all active research projects by one day.
        Returns:
            list: List of completed project IDs today.
        """
        completed_today = []
        for project_id, project in list(self.projects.items()):
            if project.status != 'active':
                continue
            entry = self.entries[project.entry_id]
            project.advance_progress()
            if project.progress >= entry.cost:
                project.complete()
                self.completed.add(entry.pid)
                completed_today.append(project)
        return completed_today

    def get_research_status(self, base_id=None):
        """
        Get the status of all research projects (optionally filtered by base).
        Args:
            base_id (str, optional): Base identifier to filter by.
        Returns:
            list: List of project status dicts.
        """
        status = []
        for project in self.projects.values():
            if base_id and project.base_id != base_id:
                continue
            entry = self.entries[project.entry_id]
            status.append({
                'project_id': project.id,
                'entry_id': project.entry_id,
                'name': entry.name,
                'progress': project.progress,
                'cost': entry.cost,
                'completion_pct': project.get_completion_percentage(entry.cost),
                'status': project.status,
                'assigned_capacity': project.assigned_capacity,
                'start_date': project.start_date,
                'completion_date': project.completion_date
            })
        return status

    def complete_research_project(self, project_id):
        """
        Mark a research project as completed and update state.
        Args:
            project_id (str): Project ID to complete.
        Returns:
            bool: True if completed, False otherwise.
        """
        project = self.projects.get(project_id)
        if not project or project.status == 'completed':
            return False
        entry = self.entries[project.entry_id]
        project.complete()
        self.completed.add(entry.pid)
        return True

    def pause_project(self, project_id):
        """
        Pause a research project by project ID.
        Args:
            project_id (str): Project ID to pause.
        """
        project = self.projects.get(project_id)
        if project:
            project.pause()

    def resume_project(self, project_id):
        """
        Resume a paused research project by project ID.
        Args:
            project_id (str): Project ID to resume.
        """
        project = self.projects.get(project_id)
        if project:
            project.resume()

    def cancel_project(self, project_id):
        """
        Cancel a research project by project ID.
        Args:
            project_id (str): Project ID to cancel.
        """
        project = self.projects.get(project_id)
        if project:
            project.cancel()

    def _requirements_met(self, entry, technologies=None, items=None, services=None, facilities=None):
        """
        Check if all requirements for a research entry are met.
        Args:
            entry (TResearchEntry): The research entry to check.
            technologies (list, optional): Known technologies.
            items (dict, optional): Available items.
            services (list, optional): Available services.
            facilities (list, optional): Available facilities.
        Returns:
            bool: True if all requirements are met.
        """
        # Check tech dependencies
        if technologies is not None:
            for tech in entry.tech_needed:
                if tech not in technologies:
                    return False
        # Check items
        if items is not None:
            for item, qty in entry.items_needed.items():
                if items.get(item, 0) < qty:
                    return False
        # Check services
        if services is not None:
            for service in entry.services_needed:
                if service not in services:
                    return False
        # Check facilities (if present)
        if hasattr(entry, 'facility_needed') and facilities is not None:
            for fac in getattr(entry, 'facility_needed', []):
                if fac not in facilities:
                    return False
        return True
