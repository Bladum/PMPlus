"""
__init__.py

Base module package initialization.

Imports all classes for handling base management, including facilities, inventory, and XCOM/alien base logic. Import this package to access all base-related classes for facility, inventory, and battle map management.

Last standardized: 2025-06-14
"""
from .abase import TBaseAlien
from .base_generator import TBaseXComBattleGenerator
from .base_inv_manager import TBaseInventory
from .facility import TFacility
from .facility_type import TFacilityType
from .xbase import TBaseXCom

__all__ = [
    "TBaseAlien",
    "TBaseXComBattleGenerator",
    "TBaseInventory",
    "TFacility",
    "TFacilityType",
    "TBaseXCom",
]
