"""
Purchase System Demo and Test Script
Purpose: Demonstrates the complete purchase system functionality
Last update: 2025-06-12
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from engine.economy.purchase import TPurchase
from engine.economy.ttransfer import TransferManager
from engine.engine.game import TGame

def load_test_purchase_data():
    """Load test purchase configuration data."""
    return {
        'purchasing': {
            'laser_rifle': {
                'name': 'Laser Rifle',
                'category': 'weapon',
                'cost': 50000,
                'delivery_time': 3,
                'monthly_limit': 10,
                'black_market': False,
                'required_technologies': ['laser_weapons'],
                'required_services': ['workshop'],
                'required_items': {},
                'delivery_contents': {
                    'items': {'laser_rifle': 1},
                    'units': {},
                    'crafts': {}
                }
            },
            'medical_supplies': {
                'name': 'Medical Supplies',
                'category': 'item',
                'cost': 2000,
                'delivery_time': 1,
                'monthly_limit': 50,
                'black_market': False,
                'required_technologies': [],
                'required_services': [],
                'required_items': {},
                'delivery_contents': {
                    'items': {'medikit': 3, 'stimpack': 5},
                    'units': {},
                    'crafts': {}
                }
            },
            'rookie_soldier': {
                'name': 'Rookie Soldier',
                'category': 'unit',
                'cost': 15000,
                'delivery_time': 7,
                'monthly_limit': 20,
                'black_market': False,
                'required_technologies': [],
                'required_services': ['barracks'],
                'required_items': {},
                'delivery_contents': {
                    'items': {'combat_armor': 1, 'rifle': 1},
                    'units': {'rookie': 1},
                    'crafts': {}
                }
            }
        },
        'black_market': {
            'reputation_threshold': 10,
            'reputation_decay': 0.1,
            'price_variance': 0.3,
            'reliability_bonus': 0.05,
            'suppliers': {
                'arms_dealer': {
                    'name': 'Underground Arms Dealer',
                    'discover_requirements': [],
                    'base_reliability': 0.9,
                    'stock_refresh_days': 3,
                    'available_items': [
                        'heavy_cannon',
                        'auto_cannon', 
                        'rocket_launcher'
                    ]
                }
            }
        }
    }

def demo_purchase_system():
    """Demonstrate purchase system functionality."""
    print("=== Purchase System Demo ===\n")
    
    # Initialize purchase system
    purchase_data = load_test_purchase_data()
    purchase_system = TPurchase(purchase_data)
    
    print(f"Purchase system initialized with {len(purchase_system.entries)} entries")
    
    # Demo available purchases
    print("\n--- Available Purchases ---")
    available_tech = ['laser_weapons']  # Player has laser weapons research
    available_services = ['workshop', 'barracks']  # Base has workshop and barracks
    available_money = 100000  # Player has $100,000
    
    available = purchase_system.get_available_purchases(
        'base_001', available_tech, available_services, available_money
    )
    
    for entry in available:
        print(f"- {entry.name}: ${entry.cost:,} (delivery: {entry.delivery_time} days)")
    
    # Demo purchase validation
    print("\n--- Purchase Validation ---")
    can_buy, issues = purchase_system.validate_purchase(
        'laser_rifle', 'base_001', 2, available_tech, available_services, available_money
    )
    print(f"Can buy 2x Laser Rifle: {can_buy}")
    if issues:
        for issue in issues:
            print(f"  Issue: {issue}")
    
    # Demo placing an order
    print("\n--- Placing Order ---")
    success, order_id, issues = purchase_system.place_order(
        'medical_supplies', 'base_001', 5, available_tech, available_services, available_money
    )
    
    if success:
        print(f"Order placed successfully! Order ID: {order_id}")
        
        # Check order status
        status = purchase_system.get_order_status(order_id)
        if status:
            print(f"Order status: {status['status']}")
            print(f"Delivery date: {status['estimated_delivery']}")
    else:
        print("Order failed:")
        for issue in issues:
            print(f"  - {issue}")
    
    # Demo active orders
    print("\n--- Active Orders ---")
    active_orders = purchase_system.get_active_orders('base_001')
    for base_id, orders in active_orders.items():
        print(f"Base {base_id} has {len(orders)} active orders")
        for order in orders:
            print(f"  Order {order.id}: {order.entry_id} x{order.quantity} - {order.status}")
    
    # Demo daily processing with transfer system
    print("\n--- Daily Processing Demo ---")
    transfer_manager = TransferManager()
    
    # Simulate some daily ticks
    for day in range(1, 5):
        print(f"\nDay {day}:")
        orders_in_transit = purchase_system.process_daily_purchases(transfer_manager)
        
        if orders_in_transit:
            for base_id, order_ids in orders_in_transit.items():
                print(f"  {len(order_ids)} orders sent to transit for base {base_id}")
        
        # Process transfers
        transfer_manager.tick_all(lambda base_id, obj_type, obj_id, qty: 
                                 print(f"    Delivered: {qty}x {obj_id} ({obj_type}) to {base_id}"))
    
    # Demo monthly reset
    print("\n--- Monthly Reset ---")
    purchase_system.process_monthly_reset()
    print("Monthly reset completed")
    
    # Demo black market
    print("\n--- Black Market ---")
    bm_purchases = purchase_system.get_black_market_purchases('base_001', 50000, reputation=5)
    if bm_purchases:
        for item in bm_purchases:
            print(f"- {item['name']}: ${item['price']:,} (reliability: {item['reliability']:.1%})")
    else:
        print("No black market items available")
    
    # Demo save/load
    print("\n--- Save/Load System ---")
    save_data = purchase_system.save_data()
    print(f"Save data contains {len(save_data)} sections")
    
    # Create new system and load data
    new_system = TPurchase()
    new_system.load_data(save_data)
    print("Data loaded into new purchase system instance")
    
    print("\n=== Demo Complete ===")

def test_integration_with_game():
    """Test integration with the game system."""
    print("\n=== Game Integration Test ===")
    
    # Initialize game
    game = TGame()
    
    # Initialize purchase system
    purchase_data = load_test_purchase_data()
    game.initialize_purchase_system(purchase_data)
    
    print("Purchase system integrated with game")
    
    # Test daily processing
    print("Testing daily processing...")
    game.process_daily_transfers_and_purchases()
    print("Daily processing completed")
    
    # Test calendar integration setup
    if hasattr(game, 'setup_calendar_integration'):
        game.setup_calendar_integration()
        print("Calendar integration setup completed")
    
    print("=== Integration Test Complete ===")

if __name__ == "__main__":
    # Run the demo
    demo_purchase_system()
    
    # Test game integration
    test_integration_with_game()
    
    print("\nAll tests completed successfully!")
