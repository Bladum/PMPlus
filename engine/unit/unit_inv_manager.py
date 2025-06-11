"""
TUnitInventoryManager: Unified inventory management for units.
Purpose: Handles equipment slots, stat modifications, templates, and auto-equip logic for unit inventories.
Last update: 2025-06-10
"""

from typing import Optional, Dict, List, Any, Tuple, Set
from engine.item.item import TItem
from engine.enums import EUnitItemCategory
from item.item_type import TItemType
from unit.unit import TUnit


class InventoryTemplate:
    """
    Container for saved equipment configurations.
    Templates allow players to save and quickly restore equipment setups
    for different scenarios or unit types. They store a mapping of equipment
    slot names to item data dictionaries.
    """
    def __init__(self, name: str, equipment_data: Dict[str, Optional[Dict[str, Any]]]) -> None:
        """
        Initialize an InventoryTemplate.
        Args:
            name (str): Template name.
            equipment_data (dict): Mapping of slot names to item data dicts.
        """
        self.name = name
        self.equipment_data = equipment_data

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'equipment_data': self.equipment_data
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InventoryTemplate':
        return cls(
            name=data['name'],
            equipment_data=data['equipment_data']
        )

class TUnitInventoryManager:
    """
    Unified inventory manager for a single unit.
    Handles slot logic, stat modification, template save/load, dynamic slot availability, and auto-equip.
    """
    def __init__(self, unit: Optional[TUnit] = None):
        """
        Initialize a TUnitInventoryManager.
        Args:
            unit (TUnit, optional): The unit this manager is attached to.
        Attributes:
            unit (TUnit): The unit instance.
            equipment_slots (dict): Mapping of slot names to equipped items.
            slot_types (dict): Mapping of slot names to item categories.
            available_slots (set): Set of currently available slot names.
            stat_modifiers (dict): Stat modifiers per slot.
            _template (dict): Last saved template.
            _named_templates (dict): Named templates for quick load/save.
        """
        self.unit = unit
        self.equipment_slots: Dict[str, Optional[TItem]] = {
            'Armor': None,
            'Weapon': None,
            'Equipment 1': None,
            'Equipment 2': None,
            'Equipment 3': None,
            'Equipment 4': None
        }
        self.slot_types: Dict[str, EUnitItemCategory] = {
            'Armor': EUnitItemCategory.ARMOR,
            'Weapon': EUnitItemCategory.WEAPON,
            'Equipment 1': EUnitItemCategory.EQUIPMENT,
            'Equipment 2': EUnitItemCategory.EQUIPMENT,
            'Equipment 3': EUnitItemCategory.EQUIPMENT,
            'Equipment 4': EUnitItemCategory.EQUIPMENT
        }
        self.available_slots: Set[str] = set(self.equipment_slots.keys())
        self.stat_modifiers: Dict[str, Dict[str, int]] = {k: {} for k in self.equipment_slots}
        self._template: Optional[Dict[str, Any]] = None
        self._named_templates: Dict[str, InventoryTemplate] = {}
        self._update_available_slots()

    def _update_available_slots(self):
        """Update available slots based on armor properties."""
        armor_item = self.equipment_slots.get('Armor')
        # Default: 2 equipment slots if no armor or not specified
        slots = 2
        if armor_item and hasattr(armor_item, 'properties'):
            slots = armor_item.properties.get('equipment_slots', 2)
            slots = max(1, min(4, slots))
        # Enable only the allowed number of equipment slots
        self.available_slots = {'Armor', 'Weapon'}
        for i in range(1, slots+1):
            self.available_slots.add(f'Equipment {i}')
        # Remove items from disabled slots
        for i in range(slots+1, 5):
            slot = f'Equipment {i}'
            if self.equipment_slots[slot] is not None:
                self.equipment_slots[slot] = None

    def can_accept_item(self, item: TItem, slot_name: str) -> bool:
        """Check if an item can be placed in the specified slot."""
        if slot_name not in self.slot_types:
            return False
        slot_type = self.slot_types[slot_name]
        item_type = getattr(item, 'item_type', EUnitItemCategory.WEAPON)
        item_type_str = str(item_type).lower() if hasattr(item_type, '__str__') else ""
        if slot_type == EUnitItemCategory.ARMOR:
            return 'armor' in item_type_str or 'armour' in item_type_str
        elif slot_type == EUnitItemCategory.WEAPON:
            return 'weapon' in item_type_str
        elif slot_type == EUnitItemCategory.EQUIPMENT:
            return 'equipment' in item_type_str
        return False

    def equip_item(self, slot_name: str, item: TItem) -> bool:
        """Equip an item to a specified slot."""
        if slot_name not in self.equipment_slots or slot_name not in self.available_slots:
            return False
        if not self.can_accept_item(item, slot_name):
            return False
        self.unequip_item(slot_name)
        self.equipment_slots[slot_name] = item
        if hasattr(item, 'stat_modifiers'):
            self.stat_modifiers[slot_name] = item.stat_modifiers
            self._apply_stat_modifiers(slot_name, item.stat_modifiers)
        if slot_name == 'Armor':
            self._update_available_slots()
        self._sync_to_unit_inventory()
        return True

    def unequip_item(self, slot_name: str) -> Optional[TItem]:
        if slot_name not in self.equipment_slots:
            return None
        item = self.equipment_slots[slot_name]
        if not item:
            return None
        if self.stat_modifiers.get(slot_name):
            self._remove_stat_modifiers(slot_name, self.stat_modifiers[slot_name])
            self.stat_modifiers[slot_name] = {}
        self.equipment_slots[slot_name] = None
        if slot_name == 'Armor':
            self._update_available_slots()
        self._sync_to_unit_inventory()
        return item

    def get_total_weight(self) -> int:
        total = 0
        for slot in self.available_slots:
            item = self.equipment_slots.get(slot)
            if item:
                total += getattr(item, 'weight', 1)
        return total

    def get_available_slots(self) -> List[str]:
        return list(self.available_slots)

    def save_template(self) -> Dict[str, Any]:
        template = {}
        for slot_name, item in self.equipment_slots.items():
            template[slot_name] = item.to_dict() if item else None
        self._template = template
        return template

    def load_template(self, template: Dict[str, Any]):
        for slot_name in self.equipment_slots:
            self.unequip_item(slot_name)
        for slot_name, item_data in template.items():
            if item_data and slot_name in self.equipment_slots:
                item = TItem.from_dict(item_data)
                self.equip_item(slot_name, item)
        self._template = template

    def save_named_template(self, name: str):
        data = {slot: item.to_dict() if item else None for slot, item in self.equipment_slots.items()}
        self._named_templates[name] = InventoryTemplate(name, data)

    def load_named_template(self, name: str):
        if name in self._named_templates:
            self.load_template(self._named_templates[name].equipment_data)

    def list_templates(self) -> List[str]:
        return list(self._named_templates.keys())

    def clear_all(self):
        for slot_name in self.equipment_slots:
            self.unequip_item(slot_name)
        self._update_available_slots()

    def get_all_items(self) -> List[TItem]:
        items = []
        for slot in self.available_slots:
            item = self.equipment_slots.get(slot)
            if item:
                items.append(item)
        return items

    def to_dict(self) -> Dict[str, Any]:
        result = {
            'slots': {},
            'available_slots': list(self.available_slots)
        }
        for slot, item in self.equipment_slots.items():
            result['slots'][slot] = item.to_dict() if item else None
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any], item_factory) -> 'TUnitInventoryManager':
        inv = cls()
        inv.available_slots = set(data.get('available_slots', []))
        for slot, item_data in data.get('slots', {}).items():
            if item_data:
                inv.equipment_slots[slot] = item_factory(item_data)
        return inv

    def _apply_stat_modifiers(self, slot_name: str, modifiers: Dict[str, int]):
        if not self.unit:
            return
        for stat_name, modifier in modifiers.items():
            if hasattr(self.unit, stat_name):
                current_value = getattr(self.unit, stat_name)
                setattr(self.unit, stat_name, current_value + modifier)

    def _remove_stat_modifiers(self, slot_name: str, modifiers: Dict[str, int]):
        if not self.unit:
            return
        for stat_name, modifier in modifiers.items():
            if hasattr(self.unit, stat_name):
                current_value = getattr(self.unit, stat_name)
                setattr(self.unit, stat_name, current_value - modifier)

    def _sync_to_unit_inventory(self):
        if not self.unit:
            return
        if not hasattr(self.unit, 'inventory'):
            self.unit.inventory = []
        self.unit.inventory = []
        for slot_name, item in self.equipment_slots.items():
            if item:
                if hasattr(item, 'equipment_slot'):
                    item.equipment_slot = slot_name
                else:
                    setattr(item, 'equipment_slot', slot_name)
                self.unit.inventory.append(item)

    def auto_equip(self, item: TItem) -> Tuple[bool, str]:
        """
        Automatically equip an item in the first available slot of appropriate type.
        Returns (success, slot_name)
        """
        item_type = getattr(item, 'item_type', EUnitItemCategory.EQUIPMENT)
        item_type_str = str(item_type).lower() if hasattr(item_type, '__str__') else ""
        if 'armor' in item_type_str or 'armour' in item_type_str:
            if self.can_accept_item(item, 'Armor') and self.equipment_slots['Armor'] is None:
                return self.equip_item('Armor', item), 'Armor'
        elif 'weapon' in item_type_str:
            if self.can_accept_item(item, 'Weapon') and self.equipment_slots['Weapon'] is None:
                return self.equip_item('Weapon', item), 'Weapon'
        elif 'equipment' in item_type_str:
            for i in range(1, 5):
                slot = f'Equipment {i}'
                if slot in self.available_slots and self.equipment_slots[slot] is None:
                    return self.equip_item(slot, item), slot
        return False, ''
