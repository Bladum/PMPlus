"""
manufacturing_project.py

Defines the ManufacturingProject class, representing an active manufacturing project in progress. Tracks progress, resources, and completion of manufacturing projects.

Classes:
    ManufacturingProject: Active manufacturing project tracker.

Last standardized: 2025-06-14
"""

from datetime import datetime, timedelta
import uuid


class ManufacturingProject:
    """
    Represents an active manufacturing project being worked on.

    Attributes:
        project_id (str): Unique project identifier
        entry_id (str): Reference to TManufactureEntry
        base_id (str): Base where manufacturing takes place
        quantity (int): Number of items to build
        progress (float): Current progress in man-days
        total_time (float): Total time required in man-days
        workshop_capacity (int): Workshop capacity allocated to this project
        start_date (datetime): When the project started
        estimated_completion (datetime): Estimated completion date
        status (str): Project status ('active', 'paused', 'completed', 'cancelled')
        items_completed (int): Number of items already completed
        cost_paid (bool): Whether the upfront cost has been paid
    """
    
    def __init__(self, entry_id, base_id, quantity, build_time_per_item, workshop_capacity=1):
        """
        Initialize a manufacturing project.

        Args:
            entry_id (str): Reference to TManufactureEntry
            base_id (str): Base where manufacturing takes place
            quantity (int): Number of items to build
            build_time_per_item (int): Time to build one item in man-days
            workshop_capacity (int): Workshop capacity allocated
        """
        self.project_id = str(uuid.uuid4())
        self.entry_id = entry_id
        self.base_id = base_id
        self.quantity = quantity
        self.progress = 0.0
        self.total_time = build_time_per_item * quantity
        self.workshop_capacity = workshop_capacity
        self.start_date = datetime.now()
        self.estimated_completion = self._calculate_completion_date()
        self.status = 'active'
        self.items_completed = 0
        self.cost_paid = False
        self.build_time_per_item = build_time_per_item

    def _calculate_completion_date(self):
        """Calculate estimated completion date based on workshop capacity."""
        days_needed = self.total_time / self.workshop_capacity
        return self.start_date + timedelta(days=days_needed)

    def advance_progress(self, daily_capacity):
        """
        Advance project progress by one day.
        
        Args:
            daily_capacity (int): Workshop capacity available for this project today
            
        Returns:
            tuple: (items_completed_today: int, hours_worked: float)
        """
        if self.status != 'active':
            return 0, 0.0
            
        # Calculate actual capacity used (minimum of what's available and what's allocated)
        capacity_used = min(daily_capacity, self.workshop_capacity)
        
        # Add progress based on allocated capacity
        self.progress += capacity_used
        
        # Calculate how many items are now complete
        items_that_should_be_complete = int(self.progress // self.build_time_per_item)
        items_completed_today = items_that_should_be_complete - self.items_completed
        self.items_completed = items_that_should_be_complete
        
        # Check if project is complete
        if self.items_completed >= self.quantity:
            self.status = 'completed'
            self.items_completed = self.quantity  # Cap at requested quantity
            items_completed_today = min(items_completed_today, self.quantity - (self.items_completed - items_completed_today))
            
        # Return items completed and man-hours worked (convert man-days to man-hours: 1 day = 8 hours)
        hours_worked = capacity_used * 8.0
        return max(0, items_completed_today), hours_worked

    def get_completion_percentage(self):
        """Get project completion percentage."""
        if self.total_time == 0:
            return 100.0
        return min(100.0, (self.progress / self.total_time) * 100)

    def get_remaining_time(self):
        """Get estimated remaining time in days."""
        if self.status == 'completed':
            return 0
        if self.workshop_capacity == 0:
            return float('inf')
            
        remaining_progress = self.total_time - self.progress
        return remaining_progress / self.workshop_capacity

    def pause(self):
        """Pause the manufacturing project."""
        if self.status == 'active':
            self.status = 'paused'

    def resume(self):
        """Resume the manufacturing project."""
        if self.status == 'paused':
            self.status = 'active'
            self.estimated_completion = self._calculate_completion_date()

    def cancel(self):
        """Cancel the manufacturing project."""
        self.status = 'cancelled'

    def set_workshop_capacity(self, capacity):
        """
        Update workshop capacity allocated to this project.
        
        Args:
            capacity (int): New workshop capacity allocation
        """
        self.workshop_capacity = capacity
        if self.status == 'active':
            self.estimated_completion = self._calculate_completion_date()

    def change_quantity(self, new_quantity):
        """
        Change the quantity of items to build in this project.
        
        Args:
            new_quantity (int): New quantity to build
            
        Returns:
            bool: True if change was successful, False if invalid
        """
        if new_quantity <= 0:
            return False
            
        if new_quantity < self.items_completed:
            # Cannot reduce below already completed items
            return False
            
        # Update quantity and recalculate total time
        self.quantity = new_quantity
        self.total_time = self.build_time_per_item * new_quantity
        
        # Recalculate completion estimate
        if self.status == 'active':
            self.estimated_completion = self._calculate_completion_date()
            
        return True

    def is_active(self):
        """Check if project is actively being worked on."""
        return self.status == 'active'

    def is_completed(self):
        """Check if project is completed."""
        return self.status == 'completed'

    def __str__(self):
        return f"Project {self.entry_id}: {self.items_completed}/{self.quantity} items ({self.get_completion_percentage():.1f}%)"
