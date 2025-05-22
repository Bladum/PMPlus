from .item_mode import TWeaponMode

class TItemType:
    """
    Basic type of item used by soldiers
    """

    ITEM_GENERAL = 0
    ITEM_CRAFT_ITEM = 1
    ITEM_UNIT_ITEM = 2
    ITEM_UNIT_EQUIPMENT = 3
    ITEM_UNIT_ARMOUR = 4
    ITEM_UNIT_CAPTURE = 5

    def __init__(self, pid, data, mode_defs=None):
        self.pid = pid
        self.name = data.get('name', pid)
        self.category = data.get('category', '')
        self.description = data.get('description', '')

        # Basic stats
        self.weight = data.get('weight', 0)         # for soldier inventory
        self.size = data.get('size', 0)             # for base capacity

        self.pedia = data.get('pedia', '')
        self.sprite = data.get('sprite', '')
        self.sound = data.get('sound', '')

        # tech required to use it on battlefield / interception
        self.tech_needed = data.get('tech_needed', [])

        # Combat stats
        self.unit_damage = data.get('unit_damage', 0)
        self.unit_damage_type = data.get('unit_damage_type', '')
        self.unit_accuracy = data.get('unit_accuracy', 0)
        self.unit_range = data.get('unit_range', 0)
        self.unit_ammo = data.get('unit_ammo', 0)
        self.unit_action_point = data.get('unit_action_point', 2)
        # Ammo/reload details after battle / when move to base
        self.unit_rearm_cost = data.get('unit_rearm_cost', 0)       # after battle, as monthly report
        self.unit_rearm_item = data.get('unit_rearm_item', None)    # after battle

        # Armor stats
        self.armour_defense = data.get('armour_defense', 0)
        self.armour_resistance = data.get('armour_resistance', {})
        self.armour_shield = data.get('armour_shield', 0)
        self.armour_shield_regen = data.get('armour_shield_regen', 0)

        self.armour_cover = data.get('armour_cover', [0, 0])
        self.armour_sight = data.get('armour_sight', [0, 0])
        self.armour_sense = data.get('armour_sense', [0, 0])

        # Combat stats for craft
        self.craft_damage = data.get('craft_damage', 0)
        self.craft_accuracy = data.get('craft_accuracy', 0.0)
        self.craft_range = data.get('craft_range', 0)
        self.craft_ammo = data.get('craft_ammo', 0)
        self.craft_size = data.get('craft_size', 1)     # small or large
        self.craft_action_point = data.get('craft_action_point', 1)
        self.craft_rearm_time = data.get('craft_rearm_time', 1)           # time to reload craft
        self.craft_rearm_cost = data.get('craft_rearm_cost', 0)           # time to reload craft
        self.craft_reload_time = data.get('craft_reload_time', 0)           # time to reload weapon during battle

        # Manufacturing info
        self.manufacture_tech = data.get('manufacture_tech', [])

        # Purchase info
        self.purchase_tech = data.get('purchase_tech', [])
        self.sell_cost = data.get('sell_cost', 0)

        # Special properties
        self.effects = data.get('effects', {})
        self.bonus = data.get('bonus', {})
        self.requirements = data.get('requirements', {})

        self.is_underwater = data.get('is_underwater', False)

        # Item modes
        self.modes = {}
        mode_names = data.get('modes', ['snap'])
        if mode_defs is None:
            mode_defs = {}
        for mode_name in mode_names:
            mode_data = mode_defs.get(mode_name, {})
            self.modes[mode_name] = TWeaponMode(mode_name, mode_data)

    def get_mode_parameters(self, mode_name):
        """
        Returns the effective parameters for the given mode.
        """
        base_params = {
            'ap_cost': self.unit_action_point,
            'range': self.unit_range,
            'accuracy': self.unit_accuracy,
            'shots': 1,
            'damage': self.unit_damage
        }
        mode = self.modes.get(mode_name, self.modes.get('snap'))
        return mode.apply(base_params)

