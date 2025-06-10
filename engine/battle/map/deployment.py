from typing import List, Any
from .deployment_group import TDeploymentGroup
import random

class TDeployment:
    """
    Represents a deployment for a battle, loaded from TOML.
    Contains a list of TDeploymentGroup and civilian info.

    Attributes:
        pid (str): Deployment identifier.
        effect (str|None): Special effect for this deployment (e.g., 'smoke').
        civilians (int): Number of civilians to deploy.
        groups (list[TDeploymentGroup]): List of deployment groups.
        civilian_types (list): List of civilian unit types for the terrain.
    """
    def __init__(self, pid, data = {}, terrain_civilian_types=None):
        self.pid = pid

        self.effect = data.get('effect', None)
        self.civilians = int(data.get('civilians', 0))
        self.groups = []
        self.civilian_types = terrain_civilian_types or []
        units_data = data.get('units', [])
        for group_data in units_data:
            self.groups.append(TDeploymentGroup(group_data))

    def generate_unit_list(self) -> List[str]:
        """
        Returns a flat list of all units (including civilians) for this deployment.
        """
        all_units = []
        for group in self.groups:
            all_units.extend(group.pick_units())
        # Add civilians if types are available
        for _ in range(self.civilians):
            if self.civilian_types:
                all_units.append(random.choice(self.civilian_types))
        return all_units
