from unit.unit_stat import TUnitStats


class TTrait:

    """
    Represents a traits of unit, which adds some stats to unit
    This is virtual class, it is used to create other classes
    """

    # Class type constants
    TRAIT_PROMOTION = 0       # XCOM soldier promotion
    TRAIT_ENEMY_RANK = 1      # Enemy only ranks
    TRAIT_ORIGIN = 2          # Random career path when soldier is hired
    TRAIT_TRANSFORMATION = 3  # Soldier transformation during gameplay
    TRAIT_MEDAL = 4           # Special awards/medals
    TRAIT_WOUND = 5           # Permanent wounds from battle/events
    TRAIT_EFFECT = 6          # Temporary effects on battle like auras
    TRAIT_PERK = 7            # special one time added perk to unit on specific level

    def __init__(self, pid, data):
        self.id = pid

        self.name = data.get('name', pid)
        self.sprite = data.get('sprite', '')
        self.description = data.get('description', '')
        self.type = data.get('type', 0)  # Default to promotion type

        # Stats modifications
        stats = data.get('stats', {})
        self.stats: TUnitStats = TUnitStats(stats)

        # cost to get it
        self.cost = data.get('cost', 0)
        self.items_needed = data.get('items_needed', [])

        # Requirements to get it
        self.races = data.get('races', [])
        self.min_level = data.get('min_level', 0)
        self.max_level = data.get('max_level', 99)
        self.services_needed = data.get('services_needed', [])
        self.tech_needed = data.get('tech_needed', [])

        # Transformation specific
        self.recovery_time = data.get('recovery_time', 0)       # days in hospital
        self.transfer_time = data.get('transfer_time', 0)       # days in transit

        # TODO add wounds specific

        # battle specific
        self.battle_duration = data.get('battle_duration', 0)
        self.battle_effect = data.get('battle_effect', None)
        self.battle_chance_complete = data.get('battle_chance_complete', 0)
        self.battle_only = data.get('battle_only', False)

    def get_stat_modifiers(self):
        """
        Returns a dictionary of stat modifiers provided by this trait.
        Override in subclasses or extend to provide modifiers.
        """
        # If self.stats is set, return its __dict__ (shallow copy)
        if self.stats:
            return self.stats.__dict__.copy()
        return {}

    # TODO create method to check if unit may get this trait

    # TODO get a list of origins traits when new unit is created

    # TODO get a list of promotions traits when unit is promoted, and which one is available

    # TODO get list of transformation traits when unit is transformed, which one are available
