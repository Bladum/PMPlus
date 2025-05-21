import random
from typing import Dict, List, Any

class TDeploymentGroup:
    """
    Represents a group of similar units in a deployment, loaded from TOML.
    Supports weights for each unit, min/max qty, and inside/outside UFO chance.
    """
    def __init__(self, data):
        self.qty_low = data.get('qty_low', 0)
        self.qty_high = data.get('qty_high', 0)
        self.unit_weights = {}
        units_data = data.get('units', {})
        if isinstance(units_data, dict):
            self.unit_weights = dict(units_data)
        elif isinstance(units_data, list):
            self.unit_weights = {u: 1 for u in units_data}
        self.outside_ufo = float(data.get('outside_ufo', 0.0))
        self.inside_ufo = float(data.get('inside_ufo', 1.0 - self.outside_ufo))
        self.leader = data.get('leader', False)
        self.patrol = data.get('patrol', False)
        self.guard = data.get('guard', False)

    def pick_units(self) -> List[str]:
        count = random.randint(self.qty_low, self.qty_high)
        if not self.unit_weights or count == 0:
            return []
        units = random.choices(
            population=list(self.unit_weights.keys()),
            weights=list(self.unit_weights.values()),
            k=count
        )
        return units

