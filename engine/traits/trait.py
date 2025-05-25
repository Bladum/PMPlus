

class TTrait:

    """
    Represents a traits of unit, which adds some stats to unit
    This is virtual class, it is used to create other classes
    """

    # Class type constants
    TRAIT_PROMOTION = 0     # XCOM soldier promotion
    TRAIT_ENEMY = 1         # Enemy only class
    TRAIT_ORIGIN = 2        # Random career path when soldier is hired
    TRAIT_TRANSFORMATION = 3  # Soldier transformation during gameplay
    TRAIT_MEDAL = 4         # Special awards/medals
    TRAIT_WOUND = 5         # Permanent wounds from battle/events
    TRAIT_EFFECT = 6        # Temporary effects on battle like auras

    def __init__(self, pid, data):
        self.id = pid

        self.name = data.get('name', pid)
        self.icon = data.get('icon', '')
        self.description = data.get('description', '')
        self.type = data.get('type', 0)  # Default to promotion type

        # Stats modifications
        self.stats = data.get('stats', {})
        self.cost = data.get('cost', 0)

        # Requirements to get it
        self.races = data.get('races', [])
        self.min_level = data.get('min_level', 0)
        self.max_level = data.get('max_level', 99)
        self.services_needed = data.get('services_needed', [])
        self.tech_needed = data.get('tech_needed', [])

        # Transformation specific
        self.recovery_time = data.get('recovery_time', 0)       # days
        self.transfer_time = data.get('transfer_time', 0)       # days

        # battle specific
        self.battle_duration = data.get('battle_duration', 0)
        self.battle_effect = data.get('battle_effect', None)
        self.battle_chance_complete = data.get('battle_chance_complete', 0)
        self.battle_only = data.get('battle_only', False)
