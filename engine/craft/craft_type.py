"""
craft_type.py

Defines the TCraftType class, which represents the blueprint for all craft types in the XCOM game. Encapsulates all static data and configuration for a craft, including stats, capabilities, costs, and special features.

Classes:
    TCraftType: Craft type blueprint and configuration.

Last standardized: 2025-06-14
"""

class TCraftType:
    """
    Represents a type of craft used by XCOM with all relevant stats and configuration.

    Attributes:
        pid (str): Unique identifier for the craft type.
        name (str): Display name of the craft.
        description (str): Description for UI or pedia.
        pedia (str): Pedia entry or reference.
        map_block (str): Map block reference for deployment.
        purchase_tech (Any): Technology required to purchase.
        sell_cost (int): Cost to sell the craft.
        upkeep_cost (int): Monthly maintenance cost.
        score_lost (int): Score lost if the craft is destroyed.
        can_land (bool): Whether the craft can land.
        is_underwater (bool): Whether the craft can operate underwater.
        is_spaceship (bool): Whether the craft is a spaceship.
        is_underground (bool): Whether the craft can go underground.
        pilots (int): Number of pilots required.
        shield (int): Shield points.
        shield_regen (int): Shield regeneration per turn.
        health (int): Maximum health points.
        range (int): Maximum fuel/range.
        speed (int): Speed on world map.
        acceleration (int): Speed during dogfight.
        hit_bonus (int): Bonus to hit chance in combat.
        avoid_bonus (int): Bonus to evasion in combat.
        damage_bonus (int): Bonus to weapon damage.
        fuel_use (int): Fuel used per tile moved.
        fuel_cost (int): Cost to refuel.
        fuel_item (Any): Item used for refueling.
        repair_cost (int): Cost to repair per HP.
        repair_item (dict): Items used for repair.
        items (list): Cargo item capacity [small, large].
        units (int): Number of units (crew) capacity.
        large_units (int): Number of large units (2x2) capacity.
        radar_range (int): Radar detection range.
        radar_power (int): Radar detection power.
        stealth (int): Stealth rating.
    """
    def __init__(self, pid, data):
        """
        Initialize a new TCraftType instance.

        Args:
            pid (str): Unique identifier for the craft type.
            data (dict): Dictionary of all craft parameters.
        """
        self.pid = pid

        self.name = data.get('name', pid)

        self.description = data.get('description', '')
        self.pedia = data.get('pedia', '')
        self.map_block = data.get('map_block', '')

        # Purchase and maintenance
        self.purchase_tech = data.get('purchase_tech', None)
        self.sell_cost = data.get('sell_cost', 0)
        self.upkeep_cost = data.get('upkeep_cost', 0)
        self.score_lost = data.get('score_lost', 0)

        # Craft capabilities
        self.can_land = data.get('can_land', False)
        self.is_underwater = data.get('is_underwater', False)
        self.is_spaceship = data.get('is_spaceship', False)
        self.is_underground = data.get('is_underground', False)
        self.pilots = data.get('pilots', 1)

        # Combat stats
        self.shield = data.get('shield', 0)
        self.shield_regen = data.get('shield_regen', 0)
        self.health = data.get('health', 0)
        self.range = data.get('range', 0)                   # size of fuel tank
        self.speed = data.get('speed', 0)                   # number of tiles per turn
        self.acceleration = data.get('acceleration', 0)     # speed during dogfight

        # Combat bonuses
        self.hit_bonus = data.get('hit_bonus', 0)
        self.avoid_bonus = data.get('avoid_bonus', 0)
        self.damage_bonus = data.get('damage_bonus', 0)

        # Fuel system
        self.fuel_use = data.get('fuel_burn', 1)            # much fuel is used per tile of move
        self.fuel_cost = data.get('fuel_cost', 0)           # refuel per unit of fuel, part of monthly invoice
        self.fuel_item = data.get('fuel_item', 0)           # item used to refuel instead of cost

        # Maintenance rates
        self.repair_cost = data.get('repair_cost', 1)       # per 1 HP, as part of monthly invoice
        self.repair_item = data.get('rate_rearm', {})       # items used to repair instead of cost

        # Cargo capacity
        self.items = data.get('items', [0, 0] )
        self.units = data.get('units', 0)
        self.large_units = data.get('large_units', 0)       # unitx 2x2

        # Sensor capabilities
        self.radar_range = data.get('radar_range', 0)
        self.radar_power = data.get('radar_power', 0)
        self.stealth = data.get('stealth', 0)