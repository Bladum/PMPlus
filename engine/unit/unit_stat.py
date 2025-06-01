class TUnitStats:
    """
    Represents a unit's stats and provides methods to manage them during the game.
    """
    def __init__(self, data=None):
        data = data or {}

        # Core stats

        self.health = data.get('health', 0)  # max health

        # strength and speed
        self.speed = data.get('speed', 0)
        self.strength = data.get('strength', 0)
        self.energy = data.get('energy', 0)

        # agility and perception
        self.aim = data.get('aim', 0)
        self.melee = data.get('melee', 0)
        self.reflex = data.get('reflex', 0)

        # mind
        self.psi = data.get('psi', 0)
        self.bravery = data.get('bravery', 0)
        self.sanity = data.get('sanity', 0)

        # detection
        self.sight = data.get('sight', (0, 0))  # (day, night)
        self.sense = data.get('sense', (0, 0))  # (day, night)
        self.cover = data.get('cover', (0, 0))  # (day, night)

        # Battle stats (only left values are tracked)

        self.morale = data.get('morale', 10)
        self.action_points = data.get('action_points', 4)

        # small or large unit

        self.size = data.get('size', 1)

        self.action_points_left = self.action_points
        self.energy_left = self.energy
        self.hurt = 0  # damage to health
        self.stun = 0  # damage to stun
        self.morale_left = self.morale

    # damage and status effects

    def receive_damage(self, dmg):
        """
        Apply hurt damage. If hurt >= health, unit dies.
        If hurt + stun >= health, unit loses consciousness.
        Returns (dead, unconscious)
        """
        self.hurt += dmg
        dead = self.hurt >= self.health
        unconscious = (self.hurt + self.stun) >= self.health
        if dead:
            self.hurt = self.health
        return dead, unconscious

    def receive_stun(self, stun):
        """
        Apply stun damage. If stun >= health, unit loses consciousness.
        If hurt + stun >= health, unit loses consciousness.
        Returns unconscious (bool)
        """
        self.stun += stun
        unconscious = (self.hurt + self.stun) >= self.health or self.stun >= self.health
        if self.stun > self.health:
            self.stun = self.health
        return unconscious

    # restoration methods

    def restore_health(self, amount):
        self.hurt = max(0, self.hurt - amount)

    def restore_stun(self, amount):
        self.stun = max(0, self.stun - amount)

    def restore_energy(self, amount):
        self.energy_left = min(self.energy, self.energy_left + amount)

    def restore_morale(self, amount):
        self.morale_left = min(self.morale, self.morale_left + amount)

    # action points management

    def use_ap(self, amount):
        self.action_points_left = max(0, self.action_points_left - amount)

    # new battle handling

    def new_game(self):
        self.morale_left = self.morale  # Reset morale to initial value
        self.action_points_left = self.action_points  # Reset action points to max
        self.hurt = 0  # Reset hurt to 0
        self.stun = 0  # Reset stun to 0
        self.energy_left = self.energy

    # new turn handling

    def new_turn(self):
        # Use effective AP based on morale/sanity
        self.action_points_left = self.get_effective_ap()
        self.restore_energy(self.energy / 4)  # Reset energy by 25% of base
        self.restore_stun(1)  # Reset hurt to max health

    def action_rest(self):
        # this action should cost 2 AP
        self.restore_energy(1)
        self.restore_stun(0.25)
        self.restore_morale(0.5)

    def get_effective_ap(self):
        """
        Returns the effective action points for the turn, reduced by low morale or sanity.
        If morale or sanity is 3 or lower, deduct 1 AP per missing point (from 4).
        The lowest value between morale and sanity is used for deduction.
        """
        penalty = 0
        for stat in [self.morale_left, self.sanity]:
            if stat <= 3:
                penalty = max(penalty, 4 - max(0, stat))
        effective_ap = max(0, self.action_points - penalty)
        return effective_ap

    # alive checks

    def is_alive(self):
        return self.hurt < self.health

    def is_conscious(self):
        return (self.hurt + self.stun) < self.health and self.stun < self.health

    # morale and sanity checks

    def is_panicked(self):
        return self.morale_left <= 0

    def is_crazy(self):
        return self.sanity <= 0

    # sight and sense handling

    def get_sight(self, is_day=True):
        if isinstance(self.sight, tuple):
            return self.sight[0] if is_day else self.sight[1]
        return self.sight

    def get_health_left(self):
        return max(0, self.health - self.hurt)

    def get_stun_left(self):
        return max(0, self.health - self.stun)

    def __add__(self, other):
        if not isinstance(other, TUnitStats):
            return NotImplemented
        data = {
            'health': self.health + other.health,
            'speed': self.speed + other.speed,
            'strength': self.strength + other.strength,
            'energy': self.energy + other.energy,
            'aim': self.aim + other.aim,
            'melee': self.melee + other.melee,
            'reflex': self.reflex + other.reflex,
            'psi': self.psi + other.psi,
            'bravery': self.bravery + other.bravery,
            'sanity': self.sanity + other.sanity,
            'sight': tuple(a + b for a, b in zip(self.sight, other.sight)),
            'sense': tuple(a + b for a, b in zip(self.sense, other.sense)),
            'cover': tuple(a + b for a, b in zip(self.cover, other.cover)),
            'morale': self.morale + other.morale,
            'action_points': self.action_points + other.action_points,
        }
        return TUnitStats(data)

    def sum_with(self, other):
        """
        Sums this object's stats with another TUnitStats and updates self.
        """
        summed = self + other
        self.__dict__.update(summed.__dict__)
        return self

    def __repr__(self):
        return f"<TUnitStats HP:{self.get_health_left()}/{self.health} Hurt:{self.hurt} Stun:{self.stun} AP:{self.action_points_left}/{self.action_points} Morale:{self.morale_left}/{self.morale}>"


