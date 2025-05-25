from item.item_armour import TItemArmour
from item.item_weapon import TItemWeapon
from traits.trait import TTrait
from unit.race import TRace
from unit.side import TSide
from unit.unit_stat import TUnitStats
from unit.unit_type import TUnitType


class TUnit:

    def __init__(self, unit_type : TUnitType, player : TSide):
        """
        Unit represent a single entity of unit in game.
        It has type only for reference, and all parameters

        """

        from engine.engine.game import TGame
        self.game = TGame()

        self.unit_type = unit_type
        self.player = player

        # for player units

        self.name = ''
        self.nationality = ''
        self.face = ''
        self.female = False

        # core units

        self.stats : TUnitStats = None
        self.race : TRace = None
        self.traits : list[TTrait] = None

        # equipment

        self.armour : TItemArmour = None
        self.primary_weapon : TItemWeapon = None
        self.secondary_weapon : list[TItemWeapon] = None

        # position and direction

        self.position = None  # (x, y) coordinates on the map
        self.direction = None

        # status flags

        self.alive = True                # is the unit alive?
        self.dead = False                # unit is dead
        self.mind_controlled = False     # is the unit mind controlled?
        self.panicked = False            # is the unit panicked?
        self.crazy = False               # is the unit crazy?
        self.stunned = False             # is the unit stunned?
        self.kneeling = False            # is the unit kneeling?
        self.running = False             # is the unit running?