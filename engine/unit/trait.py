"""
TTrait: Represents a trait of a unit, modifying stats and abilities.
Purpose: Base class for all unit traits (promotions, wounds, effects, etc.).
Last update: 2025-06-10
"""

from unit.unit_stat import TUnitStats


class TTrait:
    """
    Represents a trait of a unit, which modifies stats or abilities.
    This is a virtual base class for all specific trait types.
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
        """
        Initialize a TTrait instance.
        Args:
            pid (str): Unique identifier for the trait.
            data (dict): Dictionary containing trait attributes and stat modifications.
        Attributes:
            id (str): Trait ID.
            name (str): Display name.
            sprite (str): Sprite or image reference.
            description (str): Description of the trait.
            type (int): Trait type/category.
            stats (TUnitStats): Stat modifications provided by the trait.
            cost (int): Cost to acquire the trait.
            items_needed (list): Items required to acquire the trait.
            races (list): Races eligible for the trait.
            min_level (int): Minimum level required.
            max_level (int): Maximum level allowed.
            services_needed (list): Required services for the trait.
            tech_needed (list): Technologies required to unlock.
            recovery_time (int): Recovery time (for transformations).
            transfer_time (int): Transfer time (for transformations).
            battle_duration (int): Duration of battle effect.
            battle_effect (Any): Effect applied in battle.
            battle_chance_complete (int): Chance to complete effect in battle.
            battle_only (bool): Whether the trait is battle-only.
        """
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
