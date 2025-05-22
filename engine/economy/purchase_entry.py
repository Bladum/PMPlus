
class TPurchaseEntry:
    """
    Represents a purchasable entry, what can be purchased
    """
    def __init__(self, pid, data = {} ):
        self.pid = pid

        self.name = data.get('name', '')
        self.category = data.get('category', '')
        self.supplier = data.get('supplier', None)

        # cost
        self.purchase_cost = data.get('purchase_cost', 0)
        self.purchase_time = data.get('purchase_time', 0)

        # Requirements
        self.tech_needed = data.get('tech_needed', [])
        self.items_needed = data.get('items_needed', {})
        self.services_needed = data.get('services_needed', [])
        self.region_needed = data.get('region_needed', [])
        self.country_needed = data.get('country_needed', [])

        # Results
        self.items_buy = data.get('items_buy', None)
        self.units_buy = data.get('units_buy', None)
        self.crafts_buy = data.get('crafts_buy', None)