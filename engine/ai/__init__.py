"""
__init__.py

AI module package initialization.

Imports all classes for handling AI logic, including tactical battle AI and grand strategy AI for alien forces. Import this package to access all AI-related classes for tactical and strategic decision-making.

Last standardized: 2025-06-14
"""
from .battle import TBattleAI
from .strategy import TAlienStrategy

__all__ = [
    "TBattleAI",
    "TAlienStrategy",
]
