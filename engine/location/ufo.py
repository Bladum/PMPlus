from globe.location import TLocation


class TUfo(TLocation):
    """
    Represents a UFO on the world map as location
    Its temporary, but has assigned a ufo script to manage its movement
    It has deployment to control what units are during battle
    ufo must be first shot down by interception
    """
    def __init__(self, ufo_id, data):
        super().__init__(ufo_id, data)

        from engine.engine.game import TGame
        self.game : TGame = TGame()  # Reference to the game instance

        self.ufo_id = ufo_id
        self.position = data.get('position')  # Tile or coordinates on world map

        ufo_type = data.get('ufo_type')  # Reference to TUfoType instance or id
        ufo_script = data.get('ufo_script')  # Reference to TUfoScript instance or id

        self.ufo_type = self.game.mod.ufo_types.get(ufo_type)
        self.ufo_script = self.game.mod.ufo_scripts.get(ufo_script)

        self.script_step = 0
        self.speed = 0
        self.speed_max = self.ufo_type.speed
        self.health = self.ufo_type.health

    def advance_script(self, turns=1):
        """
        Advance the UFO's script by the given number of turns.
        Handles step progress, movement, and post-step delays.
        """
        if not self.ufo_script:
            return
        if not hasattr(self, '_step_state'):
            self._step_state = {
                'progress': 0,        # Progress for current step (e.g., movement progress)
                'delay': 0,           # Delay after step is completed
                'target': None,       # Target position for movement steps
                'completed': False    # Whether the current step is completed
            }
        for _ in range(turns):
            while True:
                step = self.ufo_script.get_step(self.script_step)
                if not step:
                    return  # No more steps
                duration = step.get('duration', 1)  # How long the step takes (for movement, may be dynamic)
                delay = step.get('delay', 0)        # How long to wait after step is completed
                step_type = step.get('type')
                # If step is not completed, process it
                if not self._step_state['completed']:
                    # Handle movement steps that may take multiple turns
                    if step_type in [
                        self.ufo_script.STEP_MOVE_RANDOM,
                        self.ufo_script.STEP_MOVE_CITY,
                        self.ufo_script.STEP_MOVE_CRAFT,
                        self.ufo_script.STEP_MOVE_ABASE,
                        self.ufo_script.STEP_MOVE_XBASE,
                        self.ufo_script.STEP_MOVE_REGION,
                        self.ufo_script.STEP_MOVE_COUNTRY,
                        self.ufo_script.STEP_MOVE_LAND,
                        self.ufo_script.STEP_MOVE_SEA,
                        self.ufo_script.STEP_MOVE_REMOTE
                    ]:
                        # If no target, pick one
                        if self._step_state['target'] is None:
                            # Use script logic to pick a target
                            prev_pos = getattr(self, 'position', None)
                            self.ufo_script.process_current_step(self, self.game, self.script_step, pick_target_only=True)
                            # After this, self._step_state['target'] should be set
                            if self._step_state['target'] is None:
                                # Fallback: treat as completed if no target
                                self._step_state['completed'] = True
                                continue
                        # Move towards target
                        tx, ty = self._step_state['target']
                        cx, cy = self.position if hasattr(self, 'position') else (self.x, self.y)
                        speed = max(1, self.speed_max)
                        # Simple straight-line movement (can be replaced with pathfinding)
                        dx = tx - cx
                        dy = ty - cy
                        dist = abs(dx) + abs(dy)
                        if dist == 0:
                            self._step_state['completed'] = True
                        else:
                            # Move up to speed tiles towards target
                            move_x = min(speed, abs(dx)) * (1 if dx > 0 else -1 if dx < 0 else 0)
                            move_y = min(speed - abs(move_x), abs(dy)) * (1 if dy > 0 else -1 if dy < 0 else 0)
                            new_x = cx + move_x
                            new_y = cy + move_y
                            self.set_position(new_x, new_y)
                            # If reached target, mark as completed
                            if (new_x, new_y) == (tx, ty):
                                self._step_state['completed'] = True
                        break  # Only move once per turn
                    else:
                        # Non-movement steps: process and mark as completed
                        self.ufo_script.process_current_step(self, self.game, self.script_step)
                        self._step_state['completed'] = True
                        break
                else:
                    # Step is completed, handle delay
                    if self._step_state['delay'] < delay:
                        self._step_state['delay'] += 1
                        break  # Wait for delay
                    # Step and delay finished, go to next step
                    self.script_step += 1
                    self._step_state = {'progress': 0, 'delay': 0, 'target': None, 'completed': False}

    def move_to(self, new_position):
        """
        Move the UFO to a new position (tile or coordinates).
        """
        self.position = new_position

    def set_position(self, x, y):
        """
        Set the UFO's position on the world map.
        """
        self.position = (x, y)
        self.x = x
        self.y = y

    def get_position(self):
        """
        Returns the (x, y) position of the UFO as a tuple.
        """
        if hasattr(self, 'position') and isinstance(self.position, (list, tuple)) and len(self.position) == 2:
            return tuple(self.position)
        elif hasattr(self, 'x') and hasattr(self, 'y'):
            return (self.x, self.y)
        return (0, 0)

    def distance_to(self, other):
        """
        Returns the Euclidean distance to another location or (x, y) tuple.
        """
        if hasattr(other, 'get_position'):
            ox, oy = other.get_position()
        elif isinstance(other, (list, tuple)) and len(other) == 2:
            ox, oy = other
        else:
            raise ValueError("Invalid target for distance calculation")
        x, y = self.get_position()
        import math
        return math.hypot(ox - x, oy - y)

    def take_damage(self, amount):
        """
        Apply damage to the UFO. Returns True if UFO is destroyed.
        If health drops below 50% of base, each turn there is a chance to crash.
        """
        self.health -= amount
        if self.health < 0:
            self.health = 0
        return self.is_destroyed()

    def is_destroyed(self):
        """
        Check if the UFO is destroyed (health <= 0).
        """
        return self.health <= 0

    def is_crashed(self):
        """
        Check if the damaged UFO has crashed based on current health.
        Crash chance: 0% above 50% health, then +10% for each 10% below 50%.
        """
        if not self.is_destroyed() and self.health > 0:
            base_health = self.ufo_type.health if self.ufo_type else 1
            health_ratio = self.health / base_health
            if health_ratio >= 0.5:
                return False
            # For each 10% below 50%, add 10% crash chance
            crash_chance = int((0.5 - health_ratio) * 10) * 0.1
            import random
            return random.random() < crash_chance
        # If destroyed, always crashed
        return self.is_destroyed()


