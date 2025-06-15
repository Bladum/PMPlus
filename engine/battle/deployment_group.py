"""
engine/battle/deployment_group.py

Defines the TDeploymentGroup class, representing a group of similar units in a deployment, supporting weighted selection, min/max quantity, and special roles.

Classes:
    TDeploymentGroup: Represents a group of similar units in a deployment, loaded from TOML.

Last standardized: 2025-06-15
"""
import random
from typing import Dict, List, Any

class TDeploymentGroup:
    """
    Represents a group of similar units in a deployment, loaded from TOML.
    Supports weights for each unit, min/max qty, and inside/outside UFO chance.

    Attributes:
        qty_low (int): Minimum number of units in the group.
        qty_high (int): Maximum number of units in the group.
        unit_weights (dict): Dictionary of unit types and their weights.
        outside_ufo (float): Chance unit is outside UFO (0.0-1.0).
        inside_ufo (float): Chance unit is inside UFO (0.0-1.0).
        leader (bool): Is this group a leader group?
        patrol (bool): Is this group a patrol group?
        guard (bool): Is this group a guard group?
    """
    def __init__(self, data):
        """
        Initialize a TDeploymentGroup instance with the given properties.

        Args:
            data (dict): Dictionary containing group properties (qty_low, qty_high, units, outside_ufo, inside_ufo, leader, patrol, guard).
        """
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
        """
        Randomly pick units for this group based on weights and quantity.
        Returns:
            list[str]: List of unit type identifiers.
        """
        count = random.randint(self.qty_low, self.qty_high)
        if not self.unit_weights or count == 0:
            return []
        units = random.choices(
            population=list(self.unit_weights.keys()),
            weights=list(self.unit_weights.values()),
            k=count
        )
        return units
