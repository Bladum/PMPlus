"""
BattleLoot: Handles post-battle report generation, including loot, score, captures, experience, sanity, ammo, medals, and more.

Provides static methods to generate a summary report after a battle, aggregating all relevant statistics and rewards for the player.

Classes:
    BattleLoot: Main class for post-battle report and loot calculation.

Last standardized: 2025-06-14
"""

class BattleLoot:
    """
    Handles post-battle report, loot, score, captures, experience, sanity, ammo, medals, etc.
    Usage: BattleLoot.generate(battle) -> dict
    """
    @staticmethod
    def generate(battle):
        """
        Generate a post-battle report summarizing score, loot, captures, experience, sanity, ammo, and medals.
        Args:
            battle: Battle object containing all relevant data.
        Returns:
            dict: Report with keys 'score', 'loot', 'captures', 'experience', 'sanity', 'ammo', 'medals'.
        """
        report = {}
        report['score'] = BattleLoot._calculate_score(battle)
        report['loot'] = BattleLoot._collect_loot(battle)
        report['captures'] = BattleLoot._collect_captures(battle)
        report['experience'] = BattleLoot._calculate_experience(battle, side=battle.SIDE_PLAYER)
        report['sanity'] = BattleLoot._calculate_sanity(battle, side=battle.SIDE_PLAYER)
        report['ammo'] = BattleLoot._calculate_ammo(battle, side=battle.SIDE_PLAYER)
        report['medals'] = BattleLoot._calculate_medals(battle, side=battle.SIDE_PLAYER)
        return report

    @staticmethod
    def _calculate_score(battle):
        """
        Calculate the total score for the battle based on objectives, unit status, and other factors.
        Args:
            battle: Battle object.
        Returns:
            int: Total score value.
        """
        score = 0
        for obj in battle.objectives:
            obj_score = obj.params.get('score', 0)
            obj_penalty = obj.params.get('penalty', 0)
            if obj.status == 'complete':
                score += obj_score
            elif obj.status == 'failed':
                score -= obj_penalty
        for unit in battle.find_units(side=battle.SIDE_ENEMY, alive=False):
            score += getattr(unit, 'score_kill', 0)
        for unit in battle.find_units(side=battle.SIDE_ENEMY, alive=True):
            if getattr(unit, 'is_stunned', False) or getattr(unit, 'is_surrendered', False):
                score += getattr(unit, 'score_capture', 0)
        for obj in battle.find_objects():
            score += getattr(obj, 'score_loot', 0)
        for unit in battle.find_units(side=battle.SIDE_PLAYER, alive=False):
            score -= getattr(unit, 'score_loss', 0)
        for side in [battle.SIDE_ALLY, battle.SIDE_NEUTRAL]:
            for unit in battle.find_units(side=side, alive=False):
                score -= getattr(unit, 'score_loss', 0)
        for y, row in enumerate(battle.tiles):
            for x, tile in enumerate(row):
                if tile.wall and getattr(tile.wall, 'is_destroyed', False):
                    score -= getattr(tile.wall, 'score_loss', 0)
        return score

    @staticmethod
    def _collect_loot(battle):
        """
        Collect all loot obtained during the battle.
        Args:
            battle: Battle object.
        Returns:
            list: List of loot items.
        """
        loot = {}
        for obj in battle.find_objects():
            obj_id = getattr(obj, 'id', None)
            if obj_id:
                loot[obj_id] = loot.get(obj_id, 0) + 1
        return loot

    @staticmethod
    def _collect_captures(battle):
        """
        Collect all captured units or objects during the battle.
        Args:
            battle: Battle object.
        Returns:
            list: List of captured entities.
        """
        captures = {}
        for unit in battle.find_units(side=battle.SIDE_ENEMY, alive=True):
            if getattr(unit, 'is_stunned', False) or getattr(unit, 'is_surrendered', False):
                unit_id = getattr(unit, 'id', None)
                if unit_id:
                    captures[unit_id] = captures.get(unit_id, 0) + 1
        return captures

    @staticmethod
    def _calculate_experience(battle, side):
        """
        Calculate experience gained by a given side during the battle.
        Args:
            battle: Battle object.
            side: Side identifier (e.g., player, enemy).
        Returns:
            int: Total experience gained.
        """
        exp = {}
        for unit in battle.find_units(side=side):
            exp[getattr(unit, 'id', None)] = getattr(unit, 'experience_gained', 0)
        return exp

    @staticmethod
    def _calculate_sanity(battle, side):
        """
        Calculate sanity changes for a given side during the battle.
        Args:
            battle: Battle object.
            side: Side identifier.
        Returns:
            int: Sanity value or change.
        """
        sanity = {}
        for unit in battle.find_units(side=side):
            sanity[getattr(unit, 'id', None)] = getattr(unit, 'sanity_lost', 0)
        return sanity

    @staticmethod
    def _calculate_ammo(battle, side):
        """
        Calculate remaining or used ammo for a given side during the battle.
        Args:
            battle: Battle object.
            side: Side identifier.
        Returns:
            int: Ammo value or change.
        """
        ammo = {}
        for unit in battle.find_units(side=side):
            for item in getattr(unit, 'inventory', []):
                if hasattr(item, 'ammo_used'):
                    ammo[item.id] = ammo.get(item.id, 0) + item.ammo_used
        return ammo

    @staticmethod
    def _calculate_medals(battle, side):
        """
        Calculate medals or awards earned by a given side during the battle.
        Args:
            battle: Battle object.
            side: Side identifier.
        Returns:
            list: List of medals or awards.
        """
        medals = {}
        for unit in battle.find_units(side=side):
            medals[getattr(unit, 'id', None)] = getattr(unit, 'medals_earned', [])
        return medals
