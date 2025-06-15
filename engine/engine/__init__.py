"""
engine/engine/__init__.py

Imports all core engine classes for unified access.

Last standardized: 2025-06-15
"""

from .animation import TAnimation
from .difficulty import TDifficulty
from .game import TGame
from .mod import TMod
from .modloader import TModLoader
from .savegame import TSaveGame
from .sounds import TSoundManager
from .stats import TStatistics

__all__ = [
    "TAnimation",
    "TDifficulty",
    "TGame",
    "TMod",
    "TModLoader",
    "TSaveGame",
    "TSoundManager",
    "TStatistics",
]
