"""
TWeaponMode: Represents a specific firing/usage mode for weapons.
Purpose: Defines operational modes (snap, aimed, auto, etc.) with modifiers for accuracy, damage, AP cost, and shot count.
Last update: 2025-06-10
"""

class TWeaponMode:
    """
    Represents a specific firing/usage mode for weapons.

    Attributes:
        pid (str): Mode identifier.
        name (str): Human-readable name for the mode.
        key (str): UI key or shortcut for the mode.
        ap_cost_modifier (float): Modifier for action point cost.
        range_modifier (float): Modifier for range.
        accuracy_modifier (float): Modifier for accuracy.
        shots (int): Number of shots per action.
        damage_modifier (float): Modifier for damage.
    """

    def __init__(self, pid: str, data: dict):
        """
        Initialize a weapon mode.

        Args:
            pid (str): Mode identifier.
            data (dict): Dictionary with mode properties (name, key, ap_cost_modifier, range_modifier, accuracy_modifier, shots, damage_modifier).
        """
        self.pid = pid

        self.name = data.get('name', pid)
        self.key = data.get('key', '')
        self.ap_cost_modifier = data.get('ap_cost_modifier', 1.0)
        self.range_modifier = data.get('range_modifier', 1.0)
        self.accuracy_modifier = data.get('accuracy_modifier', 1.0)
        self.shots = data.get('shots', 1)
        self.damage_modifier = data.get('damage_modifier', 1.0)

    def apply(self, base_params: dict) -> dict:
        """
        Apply mode modifiers to base weapon parameters.

        Args:
            base_params (dict): Dictionary with keys 'ap_cost', 'range', 'accuracy', 'shots', 'damage'.

        Returns:
            dict: Modified parameters with mode effects applied.
        """
        return {
            'ap_cost': base_params.get('ap_cost', 1) * self.ap_cost_modifier,
            'range': base_params.get('range', 1) * self.range_modifier,
            'accuracy': base_params.get('accuracy', 1) * self.accuracy_modifier,
            'shots': base_params.get('shots', 1) * self.shots,
            'damage': base_params.get('damage', 1) * self.damage_modifier
        }
