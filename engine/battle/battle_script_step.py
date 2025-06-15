"""
engine/battle/battle_script_step.py

Defines the TBattleScriptStep class, representing a single step in a battle map generation script. Encapsulates the properties and logic for each script step, such as block placement, filtering, and conditions.

Classes:
    TBattleScriptStep: Represents a single step in a map generation script.

Last standardized: 2025-06-15
"""
from typing import List, Any, Optional, Union

class TBattleScriptStep:
    """
    Represents a single step in a map generation script.
    Each step defines an action to take when building the battle map.

    Attributes:
        type (str): Type of step (e.g., 'add_block', 'add_line', etc.).
        group (int|None): Group filter for map blocks.
        size (int|None): Size filter for map blocks.
        runs (int): Number of times to run this step.
        chance (float): Probability of applying this step.
        direction (str): Direction for line-based steps ('horizontal', 'vertical', 'both').
        row (int|None): Row index for placement (optional).
        col (int|None): Column index for placement (optional).
        ufo (str|None): Special block name for UFO (optional).
        craft (str|None): Special block name for craft (optional).
        label (int|None): Label for referencing this step.
        condition (list): List of conditions (labels) for executing this step.
    """
    def __init__(self, data: dict):
        """
        Initialize a script step from a dictionary of properties.

        Args:
            data (dict): Dictionary containing step properties.
        """
        # Core properties all steps have
        self.type: str = data.get('type', '')
        self.group: Optional[int] = data.get('group', None)
        self.size: Optional[int] = data.get('size', None)
        self.runs: int = data.get('runs', 1)
        self.chance: float = data.get('chance', 1.5)

        # Direction for line-based steps
        self.direction: str = data.get('direction', 'horizontal')

        # Position hints (if specified)
        self.row: Optional[int] = data.get('row', None)
        self.col: Optional[int] = data.get('col', None)

        # Special block names
        self.ufo: Optional[str] = data.get('ufo', None)
        self.craft: Optional[str] = data.get('craft', None)

        # Conditions
        self.label: Optional[int] = data.get('label', None)
        self.condition: List[int] = data.get('condition', [])
