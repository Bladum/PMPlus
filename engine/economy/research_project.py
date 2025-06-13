"""
ResearchProject: Represents an active research project in a base.
Purpose: Tracks progress, assigned capacity, and status for a research entry.
"""
from datetime import date

class ResearchProject:
    """
    Represents an ongoing research project in a specific base.
    Attributes:
        id (str): Unique project ID.
        entry_id (str): Research entry ID (links to TResearchEntry).
        base_id (str): Base where research is conducted.
        assigned_capacity (int): Man-days per day assigned.
        progress (int): Current progress (man-days).
        status (str): 'active', 'paused', 'completed', 'cancelled'.
        start_date (date): When project started.
        completion_date (date or None): When completed.
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
        if self.status != 'active':
            return
        self.progress += amount if amount is not None else self.assigned_capacity

    def get_completion_percentage(self, entry_cost):
        return min(100.0 * self.progress / entry_cost, 100.0)

    def get_remaining_time(self, entry_cost):
        if self.assigned_capacity == 0:
            return float('inf')
        remaining = max(0, entry_cost - self.progress)
        return remaining / self.assigned_capacity

    def change_capacity(self, new_capacity):
        self.assigned_capacity = new_capacity

    def pause(self):
        self.status = 'paused'

    def resume(self):
        if self.status == 'paused':
            self.status = 'active'

    def cancel(self):
        self.status = 'cancelled'

    def complete(self, completion_date=None):
        self.status = 'completed'
        self.completion_date = completion_date or date.today()
