import pytest
from engine.economy.purchase import PurchaseOrder

class TestPurchaseOrder:
    def test_init_and_is_empty(self):
        po = PurchaseOrder('order1', 'base1')
        assert po.id == 'order1'
        assert po.base_id == 'base1'
        assert po.is_empty()
        po2 = PurchaseOrder('order2', 'base2', items={'item1': 2})
        assert not po2.is_empty()

    def test_mark_processed_and_cancelled(self):
        po = PurchaseOrder('order1', 'base1')
        po.mark_processed()
        assert po.status == 'processed'
        po.mark_cancelled()
        assert po.status == 'cancelled'

    def test_calculate_total_cost(self):
        po = PurchaseOrder('order1', 'base1', items={'item1': 2}, units={'unit1': 1}, crafts={'craft1': 3})
        def item_cost_lookup(item_id):
            return {'item1': 10}.get(item_id, 0)
        def unit_cost_lookup(unit_id):
            return {'unit1': 100}.get(unit_id, 0)
        def craft_cost_lookup(craft_id):
            return {'craft1': 1000}.get(craft_id, 0)
        total = po.calculate_total_cost(item_cost_lookup, unit_cost_lookup, craft_cost_lookup)
        assert total == 10*2 + 100*1 + 1000*3

