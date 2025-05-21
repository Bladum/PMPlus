import random
from engine.craft.craft import TCraft
from engine.craft.craft_type import TCraftType
from engine.craft.craft_item import TCraftItem

class TInterception:
    """
    Handles the interception combat mechanics
    Manages dogfighting between XCOM craft and UFOs
    Calculates hit chances, damage, and evasion
    """
    def __init__(self, craft1, craft2, distance=100):
        self.crafts = [craft1, craft2]  # [XCOM, UFO]
        self.distance = distance  # in km
        self.turn = 0
        self.ap = [4, 4]  # action points for each craft per turn
        self.log = []
        self.crashed = [False, False]

    def get_state(self):
        return {
            'distance': self.distance,
            'crafts': [self._craft_state(c) for c in self.crafts],
            'ap': self.ap[:],
            'turn': self.turn,
            'crashed': self.crashed[:],
        }

    def _craft_state(self, craft):
        return {
            'id': craft.id,
            'health': craft.health,
            'max_health': craft.type.health,
            'weapons': [w.id for w in craft.weapons],
            'status': getattr(craft, 'status', 'active'),
        }

    def spend_ap(self, craft_idx, action, **kwargs):
        """
        Spend AP for a craft. action: 'move_towards', 'move_away', 'fire', etc.
        """
        if self.crashed[craft_idx]:
            self.log.append(f"Craft {craft_idx} is crashed and cannot act.")
            return False
        if self.ap[craft_idx] <= 0:
            self.log.append(f"Craft {craft_idx} has no AP left.")
            return False

        if action == 'move_towards':
            accel = getattr(self.crafts[craft_idx].type, 'acceleration', 3)
            self.distance = max(0, self.distance - accel)
            self.ap[craft_idx] -= 1
            self.log.append(f"Craft {craft_idx} moves towards enemy by {accel} km. Distance: {self.distance}")

        elif action == 'move_away':
            accel = getattr(self.crafts[craft_idx].type, 'acceleration', 3)
            self.distance += accel
            self.ap[craft_idx] -= 1
            self.log.append(f"Craft {craft_idx} moves away from enemy by {accel} km. Distance: {self.distance}")

        elif action == 'fire':
            weapon_idx = kwargs.get('weapon_idx', 0)
            target_idx = 1 - craft_idx
            if weapon_idx >= len(self.crafts[craft_idx].weapons):
                self.log.append(f"Craft {craft_idx} tried to fire invalid weapon.")
                return False
            weapon = self.crafts[craft_idx].weapons[weapon_idx]
            # Check range
            if self.distance > weapon.range * 10:  # weapon.range is in 10km units
                self.log.append(f"Weapon out of range.")
                return False
            # Check ammo
            if getattr(weapon, 'ammo', 1) <= 0:
                self.log.append(f"Weapon has no ammo.")
                return False
            # Roll to hit
            hit_chance = getattr(weapon, 'accuracy', 0.5) + getattr(self.crafts[craft_idx].type, 'hit_bonus', 0)
            hit_roll = random.random()
            if hit_roll < hit_chance:
                damage = getattr(weapon, 'damage', 1) + getattr(self.crafts[craft_idx].type, 'damage_bonus', 0)
                self.crafts[target_idx].health -= damage
                self.log.append(f"Craft {craft_idx} hits craft {target_idx} for {damage} damage!")

                # Check for crash
                if self.crafts[target_idx].health <= self.crafts[target_idx].type.health * 0.5:
                    over = self.crafts[target_idx].type.health * 0.5 - self.crafts[target_idx].health
                    crash_chance = min(1.0, max(0.1, over / (self.crafts[target_idx].type.health * 0.5)))
                    if random.random() < crash_chance:
                        self.crashed[target_idx] = True
                        self.log.append(f"Craft {target_idx} has crashed!")
            else:
                self.log.append(f"Craft {craft_idx} missed.")
            # Spend AP and ammo
            self.ap[craft_idx] -= 1
            if hasattr(weapon, 'ammo'):
                weapon.ammo -= 1
        else:
            self.log.append(f"Unknown action: {action}")
            return False
        return True

    def next_turn(self):
        self.turn += 1
        self.ap = [4, 4]
        self.log.append(f"--- Turn {self.turn} ---")
        # End if distance > 100km for 3 turns or both crafts crashed
        # (Add more logic as needed)

    def is_over(self):
        # End if both crafts crashed or distance > 100km for 3 turns
        if all(self.crashed):
            return True
        if self.distance > 100:
            return True
        return False

    def get_log(self):
        return self.log

    def calculate_rearm_costs(self):
        """
        Calculate the cost to rearm all crafts after interception.
        Returns a list of dicts per craft: {craft_id, weapons: [{weapon_id, ammo_needed, rearm_cost}]}
        """
        rearm_summary = []
        for craft in self.crafts:
            craft_info = {'craft_id': getattr(craft, 'id', None), 'weapons': []}
            for weapon in getattr(craft, 'weapons', []):
                ammo_needed = weapon.ammo_needed() if hasattr(weapon, 'ammo_needed') else 0
                cost = weapon.rearm_cost() if hasattr(weapon, 'rearm_cost') else 0
                craft_info['weapons'].append({
                    'weapon_id': getattr(weapon, 'id', None),
                    'ammo_needed': ammo_needed,
                    'rearm_cost': cost
                })
            rearm_summary.append(craft_info)
        return rearm_summary

    def rearm_crafts(self):
        """
        Actually refill all craft weapons to max ammo (should be called after player pays cost).
        """
        for craft in self.crafts:
            for weapon in getattr(craft, 'weapons', []):
                if hasattr(weapon, 'max_ammo'):
                    weapon.ammo = weapon.max_ammo
