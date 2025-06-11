import pytest
from unit.unit_stat import TUnitStats

class TestTUnitStats:
    def test_init_defaults(self):
        stats = TUnitStats()
        assert stats.health == 0
        assert stats.speed == 0
        assert stats.strength == 0
        assert stats.energy == 0
        assert stats.aim == 0
        assert stats.melee == 0
        assert stats.reflex == 0
        assert stats.psi == 0
        assert stats.bravery == 0
        assert stats.sanity == 0
        assert stats.sight == (0, 0)
        assert stats.sense == (0, 0)
        assert stats.cover == (0, 0)
        assert stats.morale == 10
        assert stats.action_points == 4
        assert stats.size == 1
        assert stats.action_points_left == 4
        assert stats.energy_left == 0
        assert stats.hurt == 0
        assert stats.stun == 0
        assert stats.morale_left == 10

    def test_receive_damage_and_stun(self):
        stats = TUnitStats({'health': 10})
        dead, unconscious = stats.receive_damage(5)
        assert not dead
        assert not unconscious
        dead, unconscious = stats.receive_damage(6)
        assert dead
        assert unconscious
        stats = TUnitStats({'health': 10})
        unconscious = stats.receive_stun(11)
        assert unconscious

    def test_restore_and_use(self):
        stats = TUnitStats({'health': 10, 'energy': 8, 'morale': 5, 'action_points': 4})
        stats.hurt = 5
        stats.stun = 3
        stats.energy_left = 2
        stats.morale_left = 2
        stats.restore_health(2)
        assert stats.hurt == 3
        stats.restore_stun(1)
        assert stats.stun == 2
        stats.restore_energy(3)
        assert stats.energy_left == 5
        stats.restore_morale(2)
        assert stats.morale_left == 4
        stats.use_ap(2)
        assert stats.action_points_left == 2

    def test_alive_and_status(self):
        stats = TUnitStats({'health': 10, 'sanity': 2, 'morale': 2})
        stats.hurt = 9
        assert stats.is_alive()
        stats.hurt = 10
        assert not stats.is_alive()
        stats = TUnitStats({'health': 10})
        stats.hurt = 5
        stats.stun = 5
        assert not stats.is_conscious()
        stats = TUnitStats({'morale': 2, 'sanity': 2})
        stats.morale_left = 0
        assert stats.is_panicked()
        stats.sanity = 0
        assert stats.is_crazy()

    def test_add_and_sum_with(self):
        a = TUnitStats({'health': 5, 'speed': 2, 'sight': (1, 2)})
        b = TUnitStats({'health': 3, 'speed': 1, 'sight': (2, 3)})
        c = a + b
        assert c.health == 8
        assert c.speed == 3
        assert c.sight == (3, 5)
        a.sum_with(b)
        assert a.health == 8
        assert a.sight == (3, 5)

    def test_repr(self):
        stats = TUnitStats({'health': 10})
        assert "TUnitStats" in repr(stats)

