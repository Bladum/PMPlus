"""
Game Data Management Module for XCOM Inventory System

This module contains all static game data including units, items, equipment slots, 
and base information. It provides centralized data management for the entire
inventory system with proper type safety and documentation.

Key Features:
- Base management with 12 configurable bases
- Unit categorization and information storage
- Item management with rarity and type systems
- Equipment slot configuration and positioning
- Dynamic base switching and state management
- Comprehensive data initialization and validation

Classes:
- ItemType: Enumeration for different item categories
- UnitCategory: Enumeration for unit types
- BaseInfo: Data class for base information storage
- GameData: Main static class containing all game data and operations
"""

import json
from enums import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Union

class ItemType(Enum):
    """
    Enumeration for different types of equipment items.
    
    Used for categorizing items and determining valid equipment slots.
    """
    ARMOUR = "armour"
    WEAPON = "weapon"
    EQUIPMENT = "equipment"
    OTHER = "other"

class UnitCategory(Enum):
    """
    Enumeration for different unit types in the game.
    
    Used for filtering, organization, and applying category-specific logic.
    """
    SOLDIER = "soldier"
    TANK = "tank"
    DOG = "dog"
    ALIEN = "alien"

@dataclass
class BaseInfo:
    """
    Data class representing information for a single base.
    
    Attributes:
        name: Human-readable base name (e.g., "OMEGA", "ALPHA")
        is_built: Whether the base has been constructed
        is_active: Whether this is the currently active base
        units: List of unit tuples (name, icon_path, info_dict)
        items: List of item tuples (name, icon_path, info_dict, count)
        
    Note:
        Only one base can be active at a time. Built bases can be
        switched between, while unbuilt bases are disabled.
    """
    name: str
    is_built: bool
    is_active: bool
    units: List[Tuple[str, str, Dict[str, Any]]] = field(default_factory=list)
    items: List[Tuple[str, str, Dict[str, Any], int]] = field(default_factory=list)

class GameData:
    """
    Main static class containing all game data and management operations.
    
    This class serves as the central repository for all game-related data
    including bases, units, items, and equipment configurations. It provides
    methods for accessing and manipulating game state while maintaining
    data integrity and consistency.
    
    Features:
    - Base management with built/unbuilt states
    - Dynamic base switching with proper state updates
    - Unit and item organization by base
    - Equipment slot configuration with positioning
    - Category filtering for UI organization
    - Summary statistics generation
    """
    
    # Base management data - 12 bases total, 3 initially built
    BASES: List[BaseInfo] = [
        BaseInfo("OMEGA", True, True),      # Base 1 - built and active
        BaseInfo("ALPHA", True, False),     # Base 2 - built but not active
        BaseInfo("BETA", True, False),      # Base 3 - built but not active  
        BaseInfo("GAMMA", False, False),    # Base 4 - not built yet
        BaseInfo("DELTA", False, False),    # Base 5 - not built yet
        BaseInfo("EPSILON", False, False),  # Base 6 - not built yet
        BaseInfo("ZETA", False, False),     # Base 7 - not built yet
        BaseInfo("ETA", False, False),      # Base 8 - not built yet
        BaseInfo("THETA", False, False),    # Base 9 - not built yet
        BaseInfo("IOTA", False, False),     # Base 10 - not built yet
        BaseInfo("KAPPA", False, False),    # Base 11 - not built yet
        BaseInfo("LAMBDA", False, False),   # Base 12 - not built yet
    ]

    @staticmethod
    def initialize_base_data() -> None:
        """
        Initialize each base with predefined units and items.
        
        Populates the built bases with their starting rosters of units
        and inventory items. This method is called automatically when
        the module is imported to ensure data is available.
        
        The data includes diverse unit types (soldiers, tanks, dogs, aliens)
        and various item categories (weapons, armor, equipment, misc items)
        with different rarity levels and characteristics.
        """
        base_units = [
            # Base 1 - OMEGA
            [
                ("Tom Bladko", "units/soldier1.png", {"type": "Soldier", "class": "Sniper", "level": 5, "desc": "Veteran marksman.", "category": "soldier"}),
                ("Jak Kowalski", "units/soldier2.png", {"type": "Soldier", "class": "Heavy", "level": 3, "desc": "Explosives expert.", "category": "soldier"}),
                ("M1 Abrams", "units/tank1.png", {"type": "Tank", "class": "Heavy", "level": 3, "desc": "Main battle tank.", "category": "tank"}),
                ("Rex", "units/dog1.png", {"type": "Dog", "class": "Scout", "level": 2, "desc": "Detection specialist.", "category": "dog"}),
                ("Sectoid", "units/alien1.png", {"type": "Alien", "class": "Psi", "level": 4, "desc": "Psychic abilities.", "category": "alien"}),
            ],
            # Base 2 - ALPHA
            [
                ("Megan Fox", "units/soldier3.png", {"type": "Soldier", "class": "Scout", "level": 2, "desc": "Fast and agile.", "category": "soldier"}),
                ("John Smith", "units/soldier4.png", {"type": "Soldier", "class": "Medic", "level": 4, "desc": "Field medic.", "category": "soldier"}),
                ("Bradley IFV", "units/tank2.png", {"type": "Tank", "class": "Support", "level": 2, "desc": "Infantry fighting vehicle.", "category": "tank"}),
                ("Max", "units/dog2.png", {"type": "Dog", "class": "Attack", "level": 3, "desc": "Combat trained.", "category": "dog"}),
            ],
            # Base 3 - BETA
            [
                ("Sarah Connor", "units/soldier5.png", {"type": "Soldier", "class": "Leader", "level": 6, "desc": "Squad commander.", "category": "soldier"}),
                ("Muton", "units/alien2.png", {"type": "Alien", "class": "Warrior", "level": 5, "desc": "Heavy assault unit.", "category": "alien"}),
            ],
        ]

        base_items = [
            # Base 1 - OMEGA
            [
                ("Laser Rifle", "items/laserRifle.png", {"type": "Weapon", "class": "Rifle", "level": 3, "desc": "High-energy laser weapon.", "item_type": "weapon", "rarity": "rare", "weight": 4}, 3),
                ("Plasma Cannon", "items/plasmaCannon.png", {"type": "Weapon", "class": "Heavy", "level": 4, "desc": "Heavy plasma weapon.", "item_type": "weapon", "rarity": "epic", "weight": 6}, 2),
                ("Auto Pistol", "items/autoPistol.png", {"type": "Weapon", "class": "Pistol", "level": 1, "desc": "Standard sidearm.", "item_type": "weapon", "rarity": "common", "weight": 1}, 5),
                ("Light Armour", "items/lightArmour.png", {"type": "Armour", "class": "Light", "level": 2, "desc": "Basic protection armor.", "item_type": "armour", "rarity": "common", "weight": 5, "equipment_slots": 2}, 4),
                ("Combat Vest", "items/combatVest.png", {"type": "Armour", "class": "Basic", "level": 1, "desc": "Basic combat protection.", "item_type": "armour", "rarity": "common", "weight": 3, "equipment_slots": 1}, 6),
                ("Grenade", "items/grenade.png", {"type": "Equipment", "class": "Explosive", "level": 1, "desc": "Standard frag grenade.", "item_type": "equipment", "rarity": "common", "weight": 1}, 15),
                ("Smoke Grenade", "items/smokeGrenade.png", {"type": "Equipment", "class": "Tactical", "level": 1, "desc": "Provides concealment.", "item_type": "equipment", "rarity": "common", "weight": 1}, 10),
                ("Medikit", "items/medikit.png", {"type": "Equipment", "class": "Medical", "level": 1, "desc": "Heals wounds in battle.", "item_type": "equipment", "rarity": "common", "weight": 2}, 12),
                ("Stim Pack", "items/stimPack.png", {"type": "Equipment", "class": "Medical", "level": 2, "desc": "Advanced healing compound.", "item_type": "equipment", "rarity": "uncommon", "weight": 1}, 8),
                ("Motion Scanner", "items/motionScanner.png", {"type": "Equipment", "class": "Tech", "level": 2, "desc": "Detects movement.", "item_type": "equipment", "rarity": "uncommon", "weight": 2}, 4),
                ("Data Chip", "items/dataChip.png", {"type": "Other", "class": "Data", "level": 1, "desc": "Contains encrypted data.", "item_type": "other", "rarity": "common", "weight": 1}, 25),
                ("Alien Alloy", "items/alienAlloy.png", {"type": "Other", "class": "Material", "level": 3, "desc": "Exotic alien material.", "item_type": "other", "rarity": "rare", "weight": 2}, 8),
            ],
            # Base 2 - ALPHA  
            [
                ("Plasma Pistol", "items/plasmaPistol.png", {"type": "Weapon", "class": "Pistol", "level": 2, "desc": "Compact plasma sidearm.", "item_type": "weapon", "rarity": "uncommon", "weight": 2}, 6),
                ("Sniper Rifle", "items/sniperRifle.png", {"type": "Weapon", "class": "Rifle", "level": 3, "desc": "Long-range precision weapon.", "item_type": "weapon", "rarity": "rare", "weight": 5}, 3),
                ("Shotgun", "items/shotgun.png", {"type": "Weapon", "class": "Shotgun", "level": 2, "desc": "Close-range devastation.", "item_type": "weapon", "rarity": "uncommon", "weight": 4}, 4),
                ("Nano Armour", "items/nanoArmour.png", {"type": "Armour", "class": "Nano", "level": 4, "desc": "Lightweight, strong armor.", "item_type": "armour", "rarity": "epic", "weight": 3, "equipment_slots": 4}, 2),
                ("Tactical Armour", "items/tacticalArmour.png", {"type": "Armour", "class": "Tactical", "level": 3, "desc": "Military-grade protection.", "item_type": "armour", "rarity": "rare", "weight": 6, "equipment_slots": 3}, 3),
                ("Scanner", "items/scanner.png", {"type": "Equipment", "class": "Tech", "level": 2, "desc": "Motion detection device.", "item_type": "equipment", "rarity": "uncommon", "weight": 1}, 8),
                ("EMP Grenade", "items/empGrenade.png", {"type": "Equipment", "class": "Electronic", "level": 3, "desc": "Disables electronics.", "item_type": "equipment", "rarity": "rare", "weight": 1}, 6),
                ("Laser Sight", "items/laserSight.png", {"type": "Equipment", "class": "Upgrade", "level": 2, "desc": "Improves accuracy.", "item_type": "equipment", "rarity": "uncommon", "weight": 1}, 5),
                ("Night Vision", "items/nightVision.png", {"type": "Equipment", "class": "Tech", "level": 2, "desc": "See in darkness.", "item_type": "equipment", "rarity": "uncommon", "weight": 1}, 4),
                ("Alien Artifact", "items/alienArtifact.png", {"type": "Other", "class": "Misc", "level": 1, "desc": "Unknown alien technology.", "item_type": "other", "rarity": "rare", "weight": 3}, 5),
                ("Energy Cell", "items/energyCell.png", {"type": "Other", "class": "Power", "level": 2, "desc": "High-capacity power source.", "item_type": "other", "rarity": "uncommon", "weight": 1}, 12),
            ],
            # Base 3 - BETA
            [
                ("Heavy Cannon", "items/heavyCannon.png", {"type": "Weapon", "class": "Heavy", "level": 4, "desc": "Devastating heavy weapon.", "item_type": "weapon", "rarity": "epic", "weight": 8}, 2),
                ("Fusion Lance", "items/fusionLance.png", {"type": "Weapon", "class": "Energy", "level": 5, "desc": "Experimental fusion weapon.", "item_type": "weapon", "rarity": "legendary", "weight": 7}, 1),
                ("Assault Rifle", "items/assaultRifle.png", {"type": "Weapon", "class": "Rifle", "level": 2, "desc": "Reliable automatic weapon.", "item_type": "weapon", "rarity": "common", "weight": 3}, 4),
                ("Power Armour", "items/powerArmour.png", {"type": "Armour", "class": "Power", "level": 5, "desc": "Heavy powered armor.", "item_type": "armour", "rarity": "legendary", "weight": 10, "equipment_slots": 3}, 1),
                ("Stealth Suit", "items/stealthSuit.png", {"type": "Armour", "class": "Stealth", "level": 3, "desc": "Cloaking technology armor.", "item_type": "armour", "rarity": "rare", "weight": 4, "equipment_slots": 1}, 2),
                ("Heavy Armour", "items/heavyArmour.png", {"type": "Armour", "class": "Heavy", "level": 4, "desc": "Maximum protection armor.", "item_type": "armour", "rarity": "epic", "weight": 8, "equipment_slots": 2}, 2),
                ("Shield Generator", "items/shieldGenerator.png", {"type": "Equipment", "class": "Defensive", "level": 5, "desc": "Projects a protective shield.", "item_type": "equipment", "rarity": "legendary", "weight": 6}, 3),
                ("Plasma Grenade", "items/plasmaGrenade.png", {"type": "Equipment", "class": "Explosive", "level": 4, "desc": "High-energy explosive.", "item_type": "equipment", "rarity": "epic", "weight": 2}, 4),
                ("Psi Amp", "items/psiAmp.png", {"type": "Equipment", "class": "Psionic", "level": 4, "desc": "Enhances psychic abilities.", "item_type": "equipment", "rarity": "epic", "weight": 2}, 2),
                ("Combat Stim", "items/combatStim.png", {"type": "Equipment", "class": "Medical", "level": 3, "desc": "Battle enhancement drug.", "item_type": "equipment", "rarity": "rare", "weight": 1}, 6),
                ("Alien Core", "items/alienCore.png", {"type": "Other", "class": "Technology", "level": 5, "desc": "Alien power core.", "item_type": "other", "rarity": "legendary", "weight": 4}, 2),
                ("Elerium", "items/elerium.png", {"type": "Other", "class": "Material", "level": 4, "desc": "Rare alien element.", "item_type": "other", "rarity": "epic", "weight": 1}, 6),
            ],
        ]

        # Assign units and items to bases
        for i, base in enumerate(GameData.BASES):
            if base.is_built and i < len(base_units):
                base.units = base_units[i]
            if base.is_built and i < len(base_items):
                base.items = base_items[i]

    @staticmethod
    def get_unit_categories() -> List[Dict[str, str]]:
        """
        Get list of unit categories for filtering UI.
        
        Returns:
            List of dictionaries containing category names and icon paths
            
        Used by UI components to populate filter dropdowns and organize
        unit displays by type.
        """
        return [
            {"name": "All", "icon": "units/icon_a.png"},
            {"name": "Soldier", "icon": "units/icon_a.png"},
            {"name": "Tank", "icon": "units/icon_b.png"},
            {"name": "Dog", "icon": "units/icon_c.png"},
            {"name": "Alien", "icon": "units/icon_d.png"},
        ]

    @staticmethod
    def get_item_categories() -> List[Dict[str, str]]:
        """
        Get list of item categories for filtering UI.
        
        Returns:
            List of dictionaries containing category names and icon paths
            
        Used by UI components to populate filter dropdowns and organize
        item displays by type.
        """
        return [
            {"name": "All", "icon": "other/item2.png"},
            {"name": "Armour", "icon": "other/item2.png"},
            {"name": "Weapon", "icon": "other/item2.png"},
            {"name": "Equipment", "icon": "other/item.png"},
            {"name": "Other", "icon": "other/item.png"},
        ]

    @staticmethod
    def get_current_base_units() -> List[Tuple[str, str, Dict[str, Any]]]:
        """
        Get units for the currently active base.
        
        Returns:
            List of unit tuples: (name, icon_path, info_dict)
            
        Returns empty list if no active base or no units available.
        """
        active_base = GameData.get_active_base()
        return active_base.units if active_base else []

    @staticmethod
    def get_current_base_items() -> List[Tuple[str, str, Dict[str, Any], int]]:
        """
        Get items for the currently active base.
        
        Returns:
            List of item tuples: (name, icon_path, info_dict, count)
            
        Returns empty list if no active base or no items available.
        """
        active_base = GameData.get_active_base()
        return active_base.items if active_base else []

    @staticmethod
    def get_base_summary() -> Dict[str, int]:
        """
        Get summary statistics for the current active base.
        
        Returns:
            Dictionary containing unit counts by category and base capacity
            
        Keys include: 'soldiers', 'tanks', 'dogs', 'aliens', 'capacity'
        Returns zeros for all categories if no active base.
        """
        active_base = GameData.get_active_base()
        if not active_base or not active_base.units:
            return {"soldiers": 0, "tanks": 0, "dogs": 0, "aliens": 0, "capacity": 50}
        
        counts = {"soldiers": 0, "tanks": 0, "dogs": 0, "aliens": 0}
        for unit_name, icon_path, info in active_base.units:
            category = info.get('category', 'soldier')
            if category == 'soldier':
                counts['soldiers'] += 1
            elif category == 'tank':
                counts['tanks'] += 1
            elif category == 'dog':
                counts['dogs'] += 1
            elif category == 'alien':
                counts['aliens'] += 1
        
        counts['capacity'] = 50  # Fixed capacity for now
        return counts

    @staticmethod
    def get_units() -> List[Tuple[str, str, Dict[str, Any]]]:
        """
        Legacy method - returns current base units.
        
        Returns:
            List of unit tuples for the active base
            
        Note: This method is maintained for backward compatibility.
        New code should use get_current_base_units() directly.
        """
        return GameData.get_current_base_units()

    @staticmethod
    def get_items() -> List[Tuple[str, str, Dict[str, Any], int]]:
        """
        Legacy method - returns current base items.
        
        Returns:
            List of item tuples for the active base
            
        Note: This method is maintained for backward compatibility.
        New code should use get_current_base_items() directly.
        """
        return GameData.get_current_base_items()

    @staticmethod
    def get_equipment_slots() -> List[Dict[str, Any]]:
        """
        Get equipment slot configuration data.
        
        Returns:
            List of slot dictionaries containing position, type, and styling info
            
        Each slot dictionary contains:
        - name: Display name for the slot
        - type: ItemType enum value for slot validation
        - position: (x, y) grid coordinates for UI positioning
        - color_adjust: (r, g, b) color adjustment values for visual variety
        """
        return [
            {"name": "Armour", "type": ItemType.ARMOUR, "position": (20, 7), "color_adjust": (0, 0, 0.05)},  # Blue tint
            {"name": "Weapon", "type": ItemType.WEAPON, "position": (28, 7), "color_adjust": (0.05, 0, 0)},  # Red tint
            {"name": "Equipment 1", "type": ItemType.EQUIPMENT, "position": (21, 13), "color_adjust": (0, 0.05, 0)},  # Green tint
            {"name": "Equipment 2", "type": ItemType.EQUIPMENT, "position": (21, 18), "color_adjust": (0, 0.05, 0)},  # Green tint
            {"name": "Equipment 3", "type": ItemType.EQUIPMENT, "position": (27, 13), "color_adjust": (0, 0.05, 0)},  # Green tint
            {"name": "Equipment 4", "type": ItemType.EQUIPMENT, "position": (27, 18), "color_adjust": (0, 0.05, 0)},  # Green tint
        ]

    @staticmethod
    def get_active_base() -> Optional[BaseInfo]:
        """
        Get the currently active base.
        
        Returns:
            BaseInfo object for the active base, or first base as fallback
            
        Searches through all bases to find the one marked as active.
        If no active base is found, returns the first base as a safe default.
        """
        for base in GameData.BASES:
            if base.is_active:
                return base
        return GameData.BASES[0]  # Default to first base

    @staticmethod
    def set_active_base(index: int) -> bool:
        """
        Set a base as the active base.
        
        Args:
            index: Zero-based index of the base to activate
            
        Returns:
            True if base was successfully activated, False otherwise
            
        Only built bases can be activated. Deactivates all other bases
        before activating the selected one to ensure single active base.
        """
        if 0 <= index < len(GameData.BASES) and GameData.BASES[index].is_built:
            # Deactivate all bases
            for base in GameData.BASES:
                base.is_active = False
            # Activate selected base
            GameData.BASES[index].is_active = True
            return True
        return False

    @staticmethod
    def get_base_status(index: int) -> str:
        """
        Get the status of a base by index.
        
        Args:
            index: Zero-based index of the base to check
            
        Returns:
            String status: 'disabled', 'available', or 'active'
            
        Status meanings:
        - 'disabled': Base is not built yet (cannot be selected)
        - 'available': Base is built but not currently active
        - 'active': Base is built and currently active
        """
        if 0 <= index < len(GameData.BASES):
            base = GameData.BASES[index]
            if not base.is_built:
                return 'disabled'
            elif base.is_active:
                return 'active'
            else:
                return 'available'
        return 'disabled'

# Initialize base data when module is loaded
GameData.initialize_base_data()