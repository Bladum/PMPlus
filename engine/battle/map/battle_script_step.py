"""
Battle script step module for defining individual steps in a battle map generation script.
"""
from typing import List, Any, Optional, Union

class TBattleScriptStep:
    """
    Represents a single step in a map generation script.
    Each step defines an action to take when building the battle map.
    """
    def __init__(self, data: dict):
        """
        Initialize a script step from a dictionary of properties.

        Args:
            data: Dictionary containing step properties
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

