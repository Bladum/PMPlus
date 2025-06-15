"""
engine/economy/research_project.py

Defines the ResearchProject class, representing an active research project in a base, tracking progress, assigned capacity, and status.

Classes:
    ResearchProject: Represents an active research project in a base.

Last standardized: 2025-06-15
"""

from datetime import date

class ResearchProject:
    """
    Represents an ongoing research project in a specific base.
    See module docstring for attribute details.
    
    Methods:
        advance_progress(amount): Advance project by a given amount (man-days).
        get_completion_percentage(entry_cost): Get percent complete.
        get_remaining_time(entry_cost): Get estimated days until completion.
        change_capacity(new_capacity): Change assigned capacity.
        pause(), resume(), cancel(), complete(): Status management.
    """
    def __init__(self, id, entry_id, base_id, assigned_capacity, start_date=None):
        self.id = id
        self.entry_id = entry_id
        self.base_id = base_id
        self.assigned_capacity = assigned_capacity
        self.progress = 0
        self.status = 'active'
        self.start_date = start_date or date.today()
        self.completion_date = None

    def advance_progress(self, amount=None):
        """
        Advance project progress by a given amount (or assigned capacity if not specified).
        """
        if self.status != 'active':
            return
        self.progress += amount if amount is not None else self.assigned_capacity

    def get_completion_percentage(self, entry_cost):
        """
        Get the completion percentage for this project.
        Args:
            entry_cost (int): Total cost of the research entry.
        Returns:
            float: Completion percentage (0-100).
        """
        return min(100.0 * self.progress / entry_cost, 100.0)

    def get_remaining_time(self, entry_cost):
        """
        Get the estimated days remaining until completion.
        Args:
            entry_cost (int): Total cost of the research entry.
        Returns:
            float: Days remaining (float('inf') if no capacity).
        """
        if self.assigned_capacity == 0:
            return float('inf')
        remaining = max(0, entry_cost - self.progress)
        return remaining / self.assigned_capacity

    def change_capacity(self, new_capacity):
        """
        Change the assigned research capacity for this project.
        Args:
            new_capacity (int): New man-days per day.
        """
        self.assigned_capacity = new_capacity

    def pause(self):
        """
        Pause the research project.
        """
        self.status = 'paused'

    def resume(self):
        """
        Resume the research project if paused.
        """
        if self.status == 'paused':
            self.status = 'active'

    def cancel(self):
        """
        Cancel the research project.
        """
        self.status = 'cancelled'

    def complete(self, completion_date=None):
        """
        Mark the project as completed.
        Args:
            completion_date (date, optional): Date of completion.
        """
        self.status = 'completed'
        self.completion_date = completion_date or date.today()
