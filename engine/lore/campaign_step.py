"""
TCampaignStep: Mission generation rules for a specific game month.
Purpose: Defines how many campaigns/events are generated and their weights for a given month.
Last update: 2025-06-10
"""

import logging

class TCampaignStep:
    """
    TCampaignStep defines mission generation rules for a specific game month.
    It specifies how many campaigns/events are generated and their weights for a given month.

    Attributes:
        month (int): Month number (1-based).
        qty_min (int): Minimum number of campaigns/events to generate.
        qty_max (int): Maximum number of campaigns/events to generate.
        events (int): Total number of events in this month.
        weights (dict): Arc weights for random selection (faction or event type -> weight).
    """
    def __init__(self, month, data):
        """
        Initialize campaign step rules for a month.
        Args:
            month (int): Month number (1-based).
            data (dict): Step data with possible keys:
                - qty_min (int): Minimum number of campaigns/events.
                - qty_max (int): Maximum number of campaigns/events.
                - events (int): Total number of events in this month.
                - weights (dict): Arc weights for random selection.
        """
        self.month = month
        self.qty_min = data.get('qty_min', 0)
        self.qty_max = data.get('qty_max', 0)
        self.events = data.get('events', 0)
        # Arc weights for random selection
        self.weights = {}
        weights = data.get('weights', {})
        if isinstance(weights, dict):
            self.weights = weights
        elif weights:
            logging.warning(f"Invalid weights type for TCampaignStep month {month}: {type(weights)}. Expected dict.")
            self.weights = {}
        # Defensive: ensure all numeric fields are ints
        try:
            self.qty_min = int(self.qty_min)
        except Exception as e:
            logging.error(f"qty_min conversion error in TCampaignStep month {month}: {e}")
            self.qty_min = 0
        try:
            self.qty_max = int(self.qty_max)
        except Exception as e:
            logging.error(f"qty_max conversion error in TCampaignStep month {month}: {e}")
            self.qty_max = 0
        try:
            self.events = int(self.events)
        except Exception as e:
            logging.error(f"events conversion error in TCampaignStep month {month}: {e}")
            self.events = 0
