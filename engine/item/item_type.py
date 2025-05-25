from typing import Any, Dict, List, Optional
from .item_mode import TWeaponMode

class TItemType:
    """
    Basic type of item used by soldiers
    """

    ITEM_GENERAL: int = 0
    ITEM_CRAFT_ITEM: int = 1
    ITEM_UNIT_ITEM: int = 2
    ITEM_UNIT_EQUIPMENT: int = 3
    ITEM_UNIT_ARMOUR: int = 4
    ITEM_UNIT_CAPTURE: int = 5

    def __init__(self, pid: str, data: Dict[str, Any], mode_defs: Optional[Dict[str, Any]] = None):
        self.pid: str = pid
        self.name: str = data.get('name', pid)
        self.category: int = data.get('category', 0)
        self.description: str = data.get('description', '')

        # Basic stats
        self.weight: int = data.get('weight', 0)         # for soldier inventory
        self.size: int = data.get('size', 0)             # for base capacity

        self.pedia: str = data.get('pedia', '')
        self.sprite: str = data.get('sprite', '')
        self.sound: str = data.get('sound', '')

        # tech required to use it on battlefield / interception
        self.tech_needed: List[str] = data.get('tech_needed', [])

        # Combat stats
        self.unit_damage: int = data.get('unit_damage', 0)
        self.unit_damage_type: str = data.get('unit_damage_type', '')
        self.unit_accuracy: int = data.get('unit_accuracy', 0)
        self.unit_range: int = data.get('unit_range', 0)
        self.unit_ammo: int = data.get('unit_ammo', 0)
        self.unit_action_point: int = data.get('unit_action_point', 2)

        # Ammo/reload details after battle / when move to base
        self.unit_rearm_cost: int = data.get('unit_rearm_cost', 0)       # after battle, as monthly report
        self.unit_rearm_item: Optional[str] = data.get('unit_rearm_item', None)    # after battle

        # Armor stats
        self.armour_defense: int = data.get('armour', 0)
        # Load resistance as a dict of float, from 'resistance' in YAML
        resistance_raw = data.get('resistance', {})
        self.armour_resistance: Dict[str, float] = {k: float(v) for k, v in resistance_raw.items()}
        self.armour_shield: int = data.get('shield', 0)
        self.armour_shield_regen: int = data.get('shield_regen', 0)

        self.armour_cover: List[int] = data.get('armour_cover', [0, 0])
        self.armour_sight: List[int] = data.get('armour_sight', [0, 0])
        self.armour_sense: List[int] = data.get('armour_sense', [0, 0])

        # Add slots for armour
        self.primary_slots: int = data.get('primary_slots', 1) if self.category == self.ITEM_UNIT_ARMOUR else 0
        self.secondary_slots: int = data.get('secondary_slots', 2) if self.category == self.ITEM_UNIT_ARMOUR else 0

        # Combat stats for craft
        self.craft_damage: int = data.get('craft_damage', 0)
        self.craft_accuracy: float = data.get('craft_accuracy', 0.0)
        self.craft_range: int = data.get('craft_range', 0)
        self.craft_ammo: int = data.get('craft_ammo', 0)
        self.craft_size: int = data.get('craft_size', 1)     # small or large
        self.craft_action_point: int = data.get('craft_action_point', 1)
        self.craft_rearm_time: int = data.get('craft_rearm_time', 1)           # time to reload craft
        self.craft_rearm_cost: int = data.get('craft_rearm_cost', 0)           # time to reload craft
        self.craft_reload_time: int = data.get('craft_reload_time', 0)           # time to reload weapon during battle

        # Manufacturing info
        self.manufacture_tech: List[str] = data.get('manufacture_tech', [])

        # Purchase info
        self.purchase_tech: List[str] = data.get('purchase_tech', [])
        self.sell_cost: int = data.get('sell_cost', 0)

        # Special properties
        self.effects: Dict[str, Any] = data.get('effects', {})
        self.bonus: Dict[str, Any] = data.get('bonus', {})
        self.requirements: Dict[str, Any] = data.get('requirements', {})

        self.is_underwater: bool = data.get('is_underwater', False)

        # Item modes
        self.modes: Dict[str, TWeaponMode] = {}
        mode_names: List[str] = data.get('modes', ['snap'])
        if mode_defs is None:
            mode_defs = {}
        for mode_name in mode_names:
            mode_data: Dict[str, Any] = mode_defs.get(mode_name, {})
            self.modes[mode_name] = TWeaponMode(mode_name, mode_data)

    def get_mode_parameters(self, mode_name: str) -> Dict[str, Any]:
        """
        Returns the effective parameters for the given mode.
        """
        base_params: Dict[str, Any] = {
            'ap_cost': self.unit_action_point,
            'range': self.unit_range,
            'accuracy': self.unit_accuracy,
            'shots': 1,
            'damage': self.unit_damage
        }
        mode: TWeaponMode = self.modes.get(mode_name, self.modes.get('snap'))
        return mode.apply(base_params)

