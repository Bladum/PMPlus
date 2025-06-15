"""
TBattleEffect: Represents special effects applied to battle map tiles or units (smoke, fire, panic, sanity, etc.).

Encapsulates the properties and initialization logic for effects that can influence gameplay, visuals, or unit status on the battle map.

Classes:
    TBattleEffect: Main class for battle map and unit effects.

Last standardized: 2025-06-14
"""

class TBattleEffect:
    """
    Defines a special effect that can be applied to battle map tiles or units.
    Effects may include environmental hazards (smoke, fire), psychological states (panic, sanity), or other temporary modifiers.

    Attributes:
        pid (str): Unique effect identifier.
        name (str): Human-readable name of the effect.
        description (str): Description of the effect's impact.
        icon (str): Path or identifier for the effect's icon.
    """

    def __init__(self, pid, data):
        """
        Initialize a TBattleEffect instance with the given identifier and properties.

        Args:
            pid (str): Unique effect identifier.
            data (dict): Dictionary containing effect properties (name, description, icon).
        """
        self.pid = pid
        self.name = data.get('name', pid)
        self.description = data.get('description', '')
        self.icon = data.get('icon', '')

        # Requirements to get (to be implemented)
