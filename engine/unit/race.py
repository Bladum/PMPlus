"""
TRace: Represents a race/type of unit and its basic stats.
Purpose: Stores race-specific attributes, stats, abilities, and AI behavior for units.
Last update: 2025-06-10
"""

from unit.unit_stat import TUnitStats


class TRace:
    """
    Represents a race (type of unit) and its basic stats, abilities, and AI behavior.
    Used as a template for unit creation and stat calculation.
    """

    def __init__(self, pid, data):
        """
        Initialize a TRace instance.
        Args:
            pid (str): Unique identifier for the race.
            data (dict): Dictionary containing race attributes and stats.
        Attributes:
            pid (str): Race ID.
            name (str): Display name.
            description (str): Description of the race.
            sprite (str): Sprite or image reference.
            is_big (bool): Whether the unit is large-sized.
            is_mechanical (bool): Whether the unit is mechanical.
            gain_experience (bool): Whether the unit gains experience.
            health_regen (int): Health regeneration per turn.
            sound_death (str|None): Sound played on death.
            corpse_image (str|None): Image for the corpse.
            stats (TUnitStats): Base stats for the race.
            aggression (float): AI aggression level.
            intelligence (float): AI intelligence level.
            immune_panic (bool): Immunity to panic.
            immune_pain (bool): Immunity to pain.
            immune_bleed (bool): Immunity to bleeding.
            can_run (bool): Can the unit run?
            can_kneel (bool): Can the unit kneel?
            can_sneak (bool): Can the unit sneak?
            can_surrender (bool): Can the unit surrender?
            can_capture (bool): Can the unit be captured?
            spawn_on_death (str|None): Unit spawned on death.
            avoids_fire (bool): Avoids fire tiles.
            spotter (int): Spotter role value.
            sniper (int): Sniper role value.
            sell_cost (int): Sell cost for the unit.
            female_frequency (float): Frequency of female units.
            level_max (int): Maximum level.
            level_train (int): Training level.
            level_start (int): Starting level.
        """
        self.pid = pid

        self.name = data.get('name', pid)
        self.description = data.get('description', '')
        self.sprite = data.get('sprite', '')

        self.is_big = data.get('is_big', False)
        self.is_mechanical = data.get('is_mechanical', False)
        self.gain_experience = data.get('gain_experience', True)
        self.health_regen = data.get('health_regen', 0)
        self.sound_death = data.get('sound_death', None)
        self.corpse_image = data.get('corpse_image', None)

        # Stats
        self.stats = TUnitStats(data)

        # AI behavior
        self.aggression = data.get('aggression', 0.0)
        self.intelligence = data.get('intelligence', 0.0)

        # Abilities and immunities
        self.immune_panic = data.get('immune_panic', False)
        self.immune_pain = data.get('immune_pain', False)
        self.immune_bleed = data.get('immune_bleed', False)
        self.can_run = data.get('can_run', True)
        self.can_kneel = data.get('can_kneel', True)
        self.can_sneak = data.get('can_sneak', True)
        self.can_surrender = data.get('can_surrender', False)
        self.can_capture = data.get('can_capture', False)
        self.spawn_on_death = data.get('spawn_on_death', None)
        self.avoids_fire = data.get('avoids_fire', False)

        # Combat roles
        self.spotter = data.get('spotter', 0)
        self.sniper = data.get('sniper', 0)

        # Purchase info
        self.sell_cost = data.get('sell_cost', 0)
        self.female_frequency = data.get('female_frequency', 0.0)
        self.level_max = data.get('level_max', 0)
        self.level_train = data.get('level_train', 0)
        self.level_start = data.get('level_start', 0)
