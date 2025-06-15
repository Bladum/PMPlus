"""
TItemType: Base item type definition that stores static parameters for all types of items.

Acts as the central reference for all item characteristics and parameters. Defines the static/unchanging properties of items that individual instances refer to, acting as a template for creating actual game items.

Classes:
    TItemType: Main class for item type definitions.

Last standardized: 2025-06-14
"""

from typing import Any, Dict, List, Optional
from enums import EUnitItemCategory
from unit.unit_stat import TUnitStats
from .item_mode import TWeaponMode

class TItemType:
    """
    Base item type definition for all types of items.

    Stores static parameters and acts as a template for item instances.

    Attributes:
        pid (str): Unique identifier for the item type.
        name (str): Human-readable name.
        category (int): Item category.
        description (str): Description text.
        weight (int): Item weight for inventory.
        size (int): Item size for base capacity.
        pedia (str): Pedia entry or reference.
        sprite (str): Path to sprite/icon.
        sound (str): Path to sound effect.
        tech_needed (List[str]): Technologies required to use.
        unit_damage (int): Damage value for unit use.
        unit_damage_type (str): Damage type for unit use.
        unit_accuracy (int): Accuracy value for unit use.
        unit_range (int): Range value for unit use.
        unit_ammo (int): Ammo capacity for unit use.
        unit_shots (int): Shots per action for unit use.
        unit_action_point (int): Action point cost for unit use.
        unit_stats (TUnitStats): Stat modifiers for units.
        unit_modes (Dict[str, TWeaponMode]): Available weapon modes.
        unit_rearm_cost (int): Rearm cost after battle.
        armour_defense (int): Armor defense value.
        armour_resistance (Dict[str, float]): Resistance by damage type.
        armour_shield (int): Shield value.
        armour_shield_regen (int): Shield regeneration per turn.
        armour_cover (List[int]): Cover values.
        armour_sight (List[int]): Sight modifiers.
        armour_sense (List[int]): Sense modifiers.
        primary_slots (int): Number of primary slots (if weapon).
        secondary_slots (int): Number of secondary slots (if equipment).
        craft_damage (int): Craft damage value.
        craft_accuracy (float): Craft accuracy value.
        craft_range (int): Craft range value.
        craft_ammo (int): Craft ammo capacity.
        craft_size (int): Craft size.
        craft_action_point (int): Craft action point cost.
        craft_rearm_time (int): Time to rearm craft.
        craft_rearm_cost (int): Cost to rearm craft.
        craft_reload_time (int): Time to reload craft weapon.
        manufacture_tech (List[str]): Techs required for manufacturing.
        purchase_tech (List[str]): Techs required for purchase.
        sell_cost (int): Sell cost.
        effects (Dict[str, Any]): Special effects.
        bonus (Dict[str, Any]): Bonus properties.
        requirements (Dict[str, Any]): Requirements for use.
        is_underwater (bool): Whether item is usable underwater.
        modes (Dict[str, TWeaponMode]): Weapon modes.
    """
    def __init__(self, pid: str, data: Dict[str, Any], mode_defs: Optional[Dict[str, Any]] = None):
        """
        Initialize a new item type definition.

        Args:
            pid (str): Unique identifier for the item type.
            data (dict): Dictionary of item type properties.
            mode_defs (Optional[dict]): Optional dictionary of weapon mode definitions.
        """
        from engine.engine.game import TGame
        self.game = TGame()

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
        self.unit_shots: int = data.get('unit_shots', 1)  # number of shots per action
        self.unit_action_point: int = data.get('unit_action_point', 2)

        # unit stats modifiers
        self.unit_stats: TUnitStats = TUnitStats( data.get('unit_stats', {}) )

        # available item modes
        unit_modes: List[str] = data.get('unit_modes', ['snap'])
        self.unit_modes: Dict[str, TWeaponMode] = {}
        for unit_mode in unit_modes:
            self.unit_modes[unit_mode] = self.game.mod.weapon_modes.get(unit_mode)

        # Ammo/reload details after battle / when move to base
        self.unit_rearm_cost: int = data.get('unit_rearm_cost', 0)       # after battle, as monthly report

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
        self.primary_slots: int = data.get('primary_slots', 1) if self.category == EUnitItemCategory.WEAPON else 0
        self.secondary_slots: int = data.get('secondary_slots', 2) if self.category == EUnitItemCategory.EQUIPMENT else 0

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

        Args:
            mode_name (str): Name of the mode to retrieve parameters for.
        Returns:
            dict: Effective parameters for the mode (ap_cost, range, accuracy, shots, damage).
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

