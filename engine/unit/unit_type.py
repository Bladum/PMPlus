import random

from item.item_armour import TItemArmour
from item.item_weapon import TItemWeapon
from unit.side import TSide


class TUnitType:
    """
    Represents a type of unit with its stats
    This is a combination of RACE, TRAITS, and ITEMS
    This is kind of a template for units, used to create actual units in the game.
    This is not used by player, only by AI units
    """

    def __init__(self, pid, data):
        self.pid = pid

        self.name = data.get('name', '')
        self.race = data.get('race', '')
        self.rank = data.get('rank', 0)
        self.traits = data.get('traits', [])

        # Handle equipment that can be either a string, list, or nan
        self.armour = data.get('armour', None)
        self.primary = data.get('primary', None)
        self.secondary = data.get('secondary', None)

        # Scoring and rewards
        self.score_dead = data.get('score_dead', 0)
        self.score_alive = data.get('score_alive', 0)
        self.items_dead = data.get('items_dead', [])
        self.items_alive = data.get('items_alive', [])

        # AI behavior
        self.ai_ignore = data.get('ai_ignore', False)
        self.vip = data.get('vip', False)

        # drop items on death
        self.drop_items = data.get('drop_items', False)
        self.drop_armour = data.get('drop_armour', False)

    @staticmethod
    def create_unit_from_template(unit_type : str, player: TSide):
        """
        Create a unit instance based on this type
        """

        from engine.engine.game import TGame
        game = TGame()

        # basic unit type
        unit_type = game.mod.units.get(unit_type)
        if unit_type is None:
            return None

        # create basic unit

        from engine.unit.unit import TUnit
        unit = TUnit( unit_type, player)

        # assign race

        unit.race = game.mod.races.get(unit)

        # assign armour

        armour_name = unit_type.armour
        armour_selected = random.choice( armour_name )
        armour = game.mod.items.get(armour_selected)
        if armour:
            unit.armour = TItemArmour(armour.name)

        # assign primary weapons

        primary_name = unit_type.primary
        primary_selected = random.choice(primary_name)
        prim_weapon = game.mod.items.get(primary_selected)
        if prim_weapon:
            unit.primary_weapon = TItemWeapon(prim_weapon.name)

        # assign secondary weapons
        # this supposed to be list of lists to choose from

        unit.secondary_weapon.clear()
        secondary_names_list = unit_type.secondary
        for secondary_name in secondary_names_list:
            secondary_selected = random.choice(secondary_name)
            second_weapon = game.mod.items.get(secondary_selected)
            if second_weapon:
                unit.secondary_weapon.append(TItemWeapon(second_weapon.name))

        # assign traits

        unit.traits.clear()  # Clear existing traits if any
        traits = unit_type.traits
        for trait_name in traits:
            trait = game.mod.traits.get(trait_name)
            if trait:
                unit.traits.append(trait)

        return unit