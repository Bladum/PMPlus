"""
TResearchManager: Main interface for research system.
Purpose: Manages research entries, projects, progress, and completion.
"""
from .research_entry import TResearchEntry
from .research_project import ResearchProject
from datetime import date
import uuid

class TResearchManager:
    """
    Manages all research entries, ongoing projects, completed research, and available research.
    Handles validation, daily progress, and completion logic.
    """
    def __init__(self):
        self.entries = {}  # id -> TResearchEntry
        self.projects = {}  # project_id -> ResearchProject
        self.completed = set()  # set of completed research ids
        self.available = set()  # set of available research ids

    def add_entry(self, entry: TResearchEntry):
        self.entries[entry.pid] = entry
        if self._requirements_met(entry):
            self.available.add(entry.pid)

    def get_available_research(self, base_id, technologies, items, services, facilities):
        available = []
        for entry in self.entries.values():
            if entry.pid in self.completed:
                continue
            if not self._requirements_met(entry, technologies, items, services, facilities):
                continue
            available.append(entry)
        return available

    def start_research_project(self, entry_id, base_id, assigned_capacity):
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
        # Returns status of all projects (optionally filtered by base)
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
        project = self.projects.get(project_id)
        if not project or project.status == 'completed':
            return False
        entry = self.entries[project.entry_id]
        project.complete()
        self.completed.add(entry.pid)
        return True

    def pause_project(self, project_id):
        project = self.projects.get(project_id)
        if project:
            project.pause()

    def resume_project(self, project_id):
        project = self.projects.get(project_id)
        if project:
            project.resume()

    def cancel_project(self, project_id):
        project = self.projects.get(project_id)
        if project:
            project.cancel()

    def _requirements_met(self, entry, technologies=None, items=None, services=None, facilities=None):
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
