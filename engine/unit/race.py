from unit.unit_stat import TUnitStats


class TRace:
    """
    Represents race = type of unit and its basic stats
    """

    def __init__(self, pid, data):
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

