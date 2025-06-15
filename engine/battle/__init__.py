"""
Battle module initialization.
Imports all main classes for battle map generation, objectives, and deployment.

Last standardized: 2025-06-14
"""

from .battle_generator import TBattleGenerator
from .battle_script import TBattleScript
from .battle_script_step import TBattleScriptStep
from .deployment import TDeployment
from .deployment_group import TDeploymentGroup
from .objective import TBattleObjective
# ...add more as other files are standardized...
