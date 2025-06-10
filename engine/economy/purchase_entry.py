"""
TPurchaseEntry: Represents a single purchasable entry.
Purpose: Stores all data and requirements for a purchase option.
Last update: 2025-06-10
"""

class TPurchaseEntry:
    '''
    Represents a purchasable entry (item/unit/craft) that can be purchased.
    Attributes:
        pid (str): Purchase entry ID.
        name (str): Name of the entry.
        category (str): Category of the entry.
        supplier (str|None): Supplier name or None.
        purchase_cost (int): Cost to purchase.
        purchase_time (int): Time required to purchase.
        tech_needed (list): Technologies required to purchase.
        items_needed (dict): Items required to purchase.
        services_needed (list): Services required to purchase.
        region_needed (list): Required regions.
        country_needed (list): Required countries.
        items_buy (any): Items received on purchase.
        units_buy (any): Units received on purchase.
        crafts_buy (any): Crafts received on purchase.
    '''
    def __init__(self, pid, data=None):
        '''
        Initialize a purchase entry.
        Args:
            pid (str): Purchase entry ID.
            data (dict, optional): Data for the entry.
        '''
        data = data or {}
        self.pid = pid
        self.name = data.get('name', '')
        self.category = data.get('category', '')
        self.supplier = data.get('supplier', None)
        self.purchase_cost = data.get('purchase_cost', 0)
        self.purchase_time = data.get('purchase_time', 0)
        self.tech_needed = data.get('tech_needed', [])
        self.items_needed = data.get('items_needed', {})
        self.services_needed = data.get('services_needed', [])
        self.region_needed = data.get('region_needed', [])
        self.country_needed = data.get('country_needed', [])
        self.items_buy = data.get('items_buy', None)
        self.units_buy = data.get('units_buy', None)
        self.crafts_buy = data.get('crafts_buy', None)