"""
Represents a specific firing/usage mode for weapons.

This class defines different operational modes for weapons (like snap shot,
aimed shot, auto fire) with distinct modifiers for accuracy, damage, etc.
Each mode provides a different balance of action point cost, accuracy,
and damage potential.

Interactions:
- Used by TItemWeapon to calculate effective weapon parameters for each mode
- Referenced by TItemType to define available modes for weapon types
- Combat systems use these parameters to calculate hit chances and damage
- UI systems display these modes as options for players during combat

Key Features:
- Modifiers for accuracy, damage, range and AP cost
- Shot count per action (for burst fire modes)
- Application of modifiers to base weapon parameters
"""

class TWeaponMode:

    def __init__(self, pid, data):
        self.pid = pid

        self.name = data.get('name', pid)
        self.key = data.get('key', '')
        self.ap_cost_modifier = data.get('ap_cost_modifier', 1.0)
        self.range_modifier = data.get('range_modifier', 1.0)
        self.accuracy_modifier = data.get('accuracy_modifier', 1.0)
        self.shots = data.get('shots', 1)
        self.damage_modifier = data.get('damage_modifier', 1.0)

    def apply(self, base_params):
        """
        base_params: dict with keys 'ap_cost', 'range', 'accuracy', 'shots', 'damage'
        Returns a dict with modified values.
        """
        return {
            'ap_cost': base_params.get('ap_cost', 1) * self.ap_cost_modifier,
            'range': base_params.get('range', 1) * self.range_modifier,
            'accuracy': base_params.get('accuracy', 1) * self.accuracy_modifier,
            'shots': base_params.get('shots', 1) * self.shots,
            'damage': base_params.get('damage', 1) * self.damage_modifier
        }

