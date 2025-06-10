"""
TBattleEffect: Special effect for battle map tiles/units (e.g. smoke, fire, panic, sanity).
Last update: 2025-06-10
"""

class TBattleEffect:
    """
    Special effect that is used on battle map for all tiles/units (e.g. smoke, fire, panic, sanity).
    Attributes:
        pid (str): Effect identifier.
        name (str): Name of the effect.
        description (str): Description of the effect.
        icon (str): Icon path or identifier.
    """

    def __init__(self, pid, data):
        """
        Initialize a battle effect.
        Args:
            pid (str): Effect identifier.
            data (dict): Dictionary with effect properties (name, description, icon).
        """
        self.pid = pid
        self.name = data.get('name', pid)
        self.description = data.get('description', '')
        self.icon = data.get('icon', '')

        # Requirements to get (to be implemented)
