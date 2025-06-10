"""
Unified Craft Inventory Management System

This module merges and extends the features of TCraftInventoryManager to match the structure of TUnitInventoryManager.
It provides a comprehensive inventory management system for crafts, including:
- Hardpoint management (weapons, equipment, engine, etc.)
- Dynamic hardpoint availability based on craft type/size
- Performance modification from mounted components
- Equipment template save/load (with named templates)
- Weight and cargo calculation
- Component validation and compatibility checking
- Synchronization with the craft's components and cargo
- Auto-mount functionality
"""

from typing import Optional, Dict, List, Any, Tuple, Set
from item.item import TItem
from item.item_type import TItemType
from craft.craft import TCraft
from engine.enums import ECraftItemCategory



class CraftInventoryTemplate:
    """
    Container for saved craft loadout configurations.
    Templates allow players to save and quickly restore component/cargo setups
    for different scenarios or craft types. They store a mapping of hardpoint names to item data dictionaries.
    """
    def __init__(self, name: str, hardpoint_data: Dict[str, Optional[Dict[str, Any]]], cargo_data: Dict[str, Any]) -> None:
        self.name = name
        self.hardpoint_data = hardpoint_data
        self.cargo_data = cargo_data

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'hardpoint_data': self.hardpoint_data,
            'cargo_data': self.cargo_data
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CraftInventoryTemplate':
        return cls(
            name=data['name'],
            hardpoint_data=data['hardpoint_data'],
            cargo_data=data['cargo_data']
        )

class TCraftInventoryManager:
    """
    Unified inventory manager for a single craft.
    Handles hardpoint logic, performance modification, template save/load, dynamic hardpoint availability, and auto-mount.
    """
    def __init__(self, craft: Optional[TCraft] = None):
        self.craft = craft
        self.hardpoints: Dict[str, Optional[TItem]] = {}
        self.hardpoint_types: Dict[str, ECraftItemCategory] = {}
        self.available_hardpoints: Set[str] = set()
        self.cargo: Dict[str, Tuple[TItem, int]] = {}
        self.performance_modifiers: Dict[str, Dict[str, int]] = {k: {} for k in self.hardpoints}
        self._template: Optional[Dict[str, Any]] = None
        self._named_templates: Dict[str, CraftInventoryTemplate] = {}
        self.MAX_WEAPON_SLOTS = 3
        self.MAX_EQUIPMENT_SLOTS = 3
        self._init_default_hardpoints()
        self._update_available_hardpoints()

    def _init_default_hardpoints(self):
        # Only 3 weapons and 3 equipment slots, plus cargo
        for i in range(1, 4):
            self.add_hardpoint(f"Weapon {i}", ECraftItemCategory.WEAPON)
            self.add_hardpoint(f"Equipment {i}", ECraftItemCategory.EQUIPMENT)
        self.add_hardpoint("Cargo", ECraftItemCategory.CARGO)

    def _update_available_hardpoints(self):
        if not self.craft:
            return
        self.available_hardpoints = set()
        # Always allow 3 weapons, 3 equipment, and cargo
        for i in range(1, 4):
            self.available_hardpoints.add(f"Weapon {i}")
            self.available_hardpoints.add(f"Equipment {i}")
        self.available_hardpoints.add("Cargo")

    def add_hardpoint(self, hardpoint_name: str, hardpoint_type: ECraftItemCategory):
        self.hardpoints[hardpoint_name] = None
        self.hardpoint_types[hardpoint_name] = hardpoint_type
        self.available_hardpoints.add(hardpoint_name)
        self.performance_modifiers[hardpoint_name] = {}

    def can_accept_component(self, component: TItem, hardpoint_name: str) -> bool:
        if hardpoint_name.startswith("Weapon"):
            component_type = getattr(component, 'item_type', ECraftItemCategory.WEAPON)
            component_type_str = str(component_type).lower() if hasattr(component_type, '__str__') else ""
            return "weapon" in component_type_str or "craft_weapon" in component_type_str
        elif hardpoint_name.startswith("Equipment"):
            component_type = getattr(component, 'item_type', ECraftItemCategory.EQUIPMENT)
            component_type_str = str(component_type).lower() if hasattr(component_type, '__str__') else ""
            return "equipment" in component_type_str or "craft_equipment" in component_type_str
        elif hardpoint_name == "Cargo":
            component_type = getattr(component, 'item_type', ECraftItemCategory.CARGO)
            component_type_str = str(component_type).lower() if hasattr(component_type, '__str__') else ""
            return "cargo" in component_type_str
        return False

    def mount_component(self, hardpoint_name: str, component: TItem) -> bool:
        if hardpoint_name not in self.hardpoints or hardpoint_name not in self.available_hardpoints:
            return False
        if not self.can_accept_component(component, hardpoint_name):
            return False
        self.unmount_component(hardpoint_name)
        self.hardpoints[hardpoint_name] = component
        if hasattr(component, 'performance_modifiers'):
            self.performance_modifiers[hardpoint_name] = component.performance_modifiers
            self._apply_performance_modifiers(hardpoint_name, component.performance_modifiers)
        self._sync_to_craft_components()
        return True

    def unmount_component(self, hardpoint_name: str) -> Optional[TItem]:
        if hardpoint_name not in self.hardpoints:
            return None
        component = self.hardpoints[hardpoint_name]
        if not component:
            return None
        if self.performance_modifiers.get(hardpoint_name):
            self._remove_performance_modifiers(hardpoint_name, self.performance_modifiers[hardpoint_name])
            self.performance_modifiers[hardpoint_name] = {}
        self.hardpoints[hardpoint_name] = None
        self._sync_to_craft_components()
        return component

    def get_total_weight(self) -> int:
        total = 0
        for hardpoint in self.available_hardpoints:
            component = self.hardpoints.get(hardpoint)
            if component:
                total += getattr(component, 'weight', 1)
        for item_name, (item, quantity) in self.cargo.items():
            total += getattr(item, 'weight', 1) * quantity
        return total

    def get_available_hardpoints(self) -> List[str]:
        return list(self.available_hardpoints)

    def save_template(self) -> Dict[str, Any]:
        template = {
            'hardpoints': {k: v.to_dict() if v else None for k, v in self.hardpoints.items()},
            'cargo': {k: {'item': item.to_dict(), 'quantity': qty} for k, (item, qty) in self.cargo.items()}
        }
        self._template = template
        return template

    def load_template(self, template: Dict[str, Any]):
        for hardpoint_name in self.hardpoints:
            self.unmount_component(hardpoint_name)
        self.cargo = {}
        for hardpoint_name, component_data in template.get('hardpoints', {}).items():
            if component_data and hardpoint_name in self.hardpoints:
                component = TItem.from_dict(component_data)
                self.mount_component(hardpoint_name, component)
        for item_name, cargo_data in template.get('cargo', {}).items():
            if cargo_data and 'item' in cargo_data:
                item = TItem.from_dict(cargo_data['item'])
                quantity = cargo_data.get('quantity', 1)
                self.add_cargo(item, quantity)
        self._template = template

    def save_named_template(self, name: str):
        hardpoint_data = {k: v.to_dict() if v else None for k, v in self.hardpoints.items()}
        cargo_data = {k: {'item': item.to_dict(), 'quantity': qty} for k, (item, qty) in self.cargo.items()}
        self._named_templates[name] = CraftInventoryTemplate(name, hardpoint_data, cargo_data)

    def load_named_template(self, name: str):
        if name in self._named_templates:
            tpl = self._named_templates[name]
            self.load_template({'hardpoints': tpl.hardpoint_data, 'cargo': tpl.cargo_data})

    def list_templates(self) -> List[str]:
        return list(self._named_templates.keys())

    def clear_all(self):
        for hardpoint_name in self.hardpoints:
            self.unmount_component(hardpoint_name)
        self.cargo = {}
        self._update_available_hardpoints()

    def get_all_items(self) -> List[TItem]:
        items = []
        for hardpoint in self.available_hardpoints:
            component = self.hardpoints.get(hardpoint)
            if component:
                items.append(component)
        for item_name, (item, quantity) in self.cargo.items():
            items.extend([item] * quantity)
        return items

    def to_dict(self) -> Dict[str, Any]:
        result = {
            'hardpoints': {},
            'available_hardpoints': list(self.available_hardpoints),
            'cargo': {}
        }
        for hardpoint, component in self.hardpoints.items():
            result['hardpoints'][hardpoint] = component.to_dict() if component else None
        for item_name, (item, quantity) in self.cargo.items():
            result['cargo'][item_name] = {'item': item.to_dict(), 'quantity': quantity}
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any], item_factory) -> 'TCraftInventoryManager':
        inv = cls()
        inv.available_hardpoints = set(data.get('available_hardpoints', []))
        for hardpoint, component_data in data.get('hardpoints', {}).items():
            if component_data:
                inv.hardpoints[hardpoint] = item_factory(component_data)
        for item_name, cargo_data in data.get('cargo', {}).items():
            if cargo_data and 'item' in cargo_data:
                item = item_factory(cargo_data['item'])
                quantity = cargo_data.get('quantity', 1)
                inv.cargo[item_name] = (item, quantity)
        return inv

    def _apply_performance_modifiers(self, hardpoint_name: str, modifiers: Dict[str, int]):
        if not self.craft:
            return
        for stat_name, modifier in modifiers.items():
            if hasattr(self.craft, stat_name):
                current_value = getattr(self.craft, stat_name)
                setattr(self.craft, stat_name, current_value + modifier)

    def _remove_performance_modifiers(self, hardpoint_name: str, modifiers: Dict[str, int]):
        if not self.craft:
            return
        for stat_name, modifier in modifiers.items():
            if hasattr(self.craft, stat_name):
                current_value = getattr(self.craft, stat_name)
                setattr(self.craft, stat_name, current_value - modifier)

    def _sync_to_craft_components(self):
        if not self.craft:
            return
        if not hasattr(self.craft, 'components'):
            self.craft.components = []
        self.craft.components = []
        for hardpoint_name, component in self.hardpoints.items():
            if component:
                if hasattr(component, 'hardpoint'):
                    component.hardpoint = hardpoint_name
                else:
                    setattr(component, 'hardpoint', hardpoint_name)
                self.craft.components.append(component)

    def _sync_to_craft_cargo(self):
        if not self.craft:
            return
        if not hasattr(self.craft, 'cargo'):
            self.craft.cargo = {}
        self.craft.cargo = {}
        for item_name, (item, quantity) in self.cargo.items():
            self.craft.cargo[item_name] = {
                'item': item,
                'quantity': quantity
            }

    def add_cargo(self, item: TItem, quantity: int = 1) -> bool:
        if not item:
            return False
        item_name = item.name
        cargo_capacity = self._get_cargo_capacity()
        current_cargo_weight = self._get_current_cargo_weight()
        item_weight = getattr(item, 'weight', 1) * quantity
        if current_cargo_weight + item_weight > cargo_capacity:
            return False
        if item_name in self.cargo:
            _, current_quantity = self.cargo[item_name]
            self.cargo[item_name] = (item, current_quantity + quantity)
        else:
            self.cargo[item_name] = (item, quantity)
        self._sync_to_craft_cargo()
        return True

    def remove_cargo(self, item_name: str, quantity: int = 1) -> Optional[Tuple[TItem, int]]:
        if item_name not in self.cargo:
            return None
        item, current_quantity = self.cargo[item_name]
        quantity_to_remove = min(quantity, current_quantity)
        remaining = current_quantity - quantity_to_remove
        if remaining <= 0:
            removed_item = self.cargo.pop(item_name)
        else:
            self.cargo[item_name] = (item, remaining)
            removed_item = (item, quantity_to_remove)
        self._sync_to_craft_cargo()
        return removed_item

    def _get_cargo_capacity(self) -> int:
        base_capacity = 10
        if self.craft:
            craft_size = getattr(self.craft, 'size', 1)
            base_capacity = 10 * craft_size
            cargo_bay = self.hardpoints.get("Cargo Bay")
            if cargo_bay and hasattr(cargo_bay, 'cargo_capacity'):
                base_capacity += cargo_bay.cargo_capacity
        return base_capacity

    def _get_current_cargo_weight(self) -> int:
        total = 0
        for item_name, (item, quantity) in self.cargo.items():
            total += getattr(item, 'weight', 1) * quantity
        return total

    def auto_mount(self, component: TItem) -> Tuple[bool, str]:
        component_type = getattr(component, 'item_type', ECraftItemCategory.WEAPON)
        component_type_str = str(component_type).lower() if hasattr(component_type, '__str__') else ""
        if "weapon" in component_type_str or "craft_weapon" in component_type_str:
            for slot in self.get_weapon_slots():
                if self.can_accept_component(component, slot) and self.hardpoints[slot] is None:
                    return self.mount_component(slot, component), slot
        elif "equipment" in component_type_str or "craft_equipment" in component_type_str:
            for slot in self.get_equipment_slots():
                if self.can_accept_component(component, slot) and self.hardpoints[slot] is None:
                    return self.mount_component(slot, component), slot
        elif "cargo" in component_type_str:
            if self.can_accept_component(component, "Cargo") and self.hardpoints["Cargo"] is None:
                return self.mount_component("Cargo", component), "Cargo"
        return False, ''

    def get_weapon_slots(self) -> List[str]:
        return [f"Weapon {i}" for i in range(1, 4)]

    def get_equipment_slots(self) -> List[str]:
        return [f"Equipment {i}" for i in range(1, 4)]

    def get_weapon_count(self) -> int:
        weapon_slots = self.get_weapon_slots()
        return sum(1 for slot in weapon_slots if self.hardpoints.get(slot) is not None)

    def get_equipment_count(self) -> int:
        equipment_slots = self.get_equipment_slots()
        return sum(1 for slot in equipment_slots if self.hardpoints.get(slot) is not None)

    def is_weapon_compatible(self, weapon: TItem) -> bool:
        weapon_slots = self.get_weapon_slots()
        if not weapon_slots:
            return False
        return self.can_accept_component(weapon, weapon_slots[0])

    def is_equipment_compatible(self, equipment: TItem) -> bool:
        equipment_slots = self.get_equipment_slots()
        if not equipment_slots:
            return False
        return self.can_accept_component(equipment, equipment_slots[0])
