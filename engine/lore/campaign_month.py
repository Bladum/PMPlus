class TCampaignMonth:
    """
    Represents mission generation rules for a specific game month
    """

    def __init__(self, month, data):
        self.month = month

        # Mission generation limits
        self.qty_min = data.get('qty_min', 0)
        self.qty_max = data.get('qty_max', 0)

        # total number of events in this month
        self.events = data.get('events', 0)

        # Arc weights for random selection
        self.weights = {}
        if 'weights' in data and isinstance(data['weights'], dict):
            self.weights = data['weights']