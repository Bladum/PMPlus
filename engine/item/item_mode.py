class TWeaponMode:
    def __init__(self, pid, data):
        self.pid = pid

        self.name = data.get('name', pid)
        self.key = data.get('key', '')
        self.ap_cost_modifier = data.get('ap_cost_modifier', 1.0)
        self.range_modifier = data.get('range_modifier', 1.0)
        self.accuracy_modifier = data.get('accuracy_modifier', 1.0)
        self.shots = data.get('shots', 1)
        self.damage_modifier = data.get('damage_modifier', 1.0)

    def apply(self, base_params):
        """
        base_params: dict with keys 'ap_cost', 'range', 'accuracy', 'shots', 'damage'
        Returns a dict with modified values.
        """
        return {
            'ap_cost': base_params.get('ap_cost', 1) * self.ap_cost_modifier,
            'range': base_params.get('range', 1) * self.range_modifier,
            'accuracy': base_params.get('accuracy', 1) * self.accuracy_modifier,
            'shots': base_params.get('shots', 1) * self.shots,
            'damage': base_params.get('damage', 1) * self.damage_modifier
        }

