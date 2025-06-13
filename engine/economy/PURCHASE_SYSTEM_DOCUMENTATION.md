# Purchase System Comprehensive Documentation

## Overview

The Purchase System is a comprehensive solution for acquiring items, units, and crafts in the XCOM-style game. It provides functionality for standard purchases, black market transactions, monthly limits, and delivery tracking through integration with the existing transfer system.

## Architecture

```
TPurchase (Main Interface)
├── PurchaseManager (Order Orchestration)
│   ├── PurchaseOrder (Individual Orders)
│   └── Monthly Limit Tracking
├── TPurchaseEntry (Purchase Templates)
└── BlackMarket (Special Suppliers)
    ├── BlackMarketSupplier (Individual Suppliers)
    └── Reputation System

TGame (Integration Layer)
├── Daily Processing (via Calendar)
├── Transfer System Integration
└── Base Inventory Integration
```

## Core Components

### 1. TPurchase (Main Interface)
**Purpose**: Primary purchasing system interface managing all purchase operations.

```python
class TPurchase:
    """Primary purchasing system interface."""
    
    # Core Operations
    def get_available_purchases(base_id, technologies, services, money)
    def place_order(entry_id, base_id, quantity, technologies, services, money)
    def validate_purchase(entry_id, base_id, quantity, technologies, services, money)
    
    # Black Market
    def get_black_market_purchases(base_id, money, reputation)
    def place_black_market_order(supplier_id, item_id, base_id, quantity, money)
    
    # Order Management
    def get_order_status(order_id)
    def get_active_orders(base_id)
    def cancel_order(order_id)
    
    # System Processing
    def process_daily_purchases(transfer_manager)
    def process_monthly_reset()
```

### 2. TPurchaseEntry (Purchase Templates)
**Purpose**: Defines what can be purchased and under what conditions.

```python
class TPurchaseEntry:
    """Represents a purchasable entry."""
    
    # Basic Properties
    id: str                          # Unique identifier
    name: str                        # Display name
    category: str                    # Item category
    cost: int                        # Purchase cost
    delivery_time: int               # Days for delivery
    
    # Restrictions
    monthly_limit: int               # Monthly purchase limit (0 = unlimited)
    required_technologies: List[str] # Required research
    required_services: List[str]     # Required base facilities
    required_items: Dict[str, int]   # Required items for purchase
    
    # Black Market
    black_market: bool               # Available on black market
    supplier: Optional[str]          # Specific supplier requirement
    
    # Delivery Contents
    delivery_contents: Dict[str, Dict[str, int]]  # What gets delivered
    # Structure: {
    #   'items': {'item_id': quantity},
    #   'units': {'unit_id': quantity}, 
    #   'crafts': {'craft_id': quantity}
    # }
```

### 3. PurchaseOrder (Order Tracking)
**Purpose**: Tracks individual purchase orders from placement to delivery.

```python
class PurchaseOrder:
    """Represents a purchase order."""
    
    # Order Identity
    id: str                          # Unique order ID
    base_id: str                     # Destination base
    entry_id: str                    # Purchase entry reference
    quantity: int                    # Quantity ordered
    
    # Status Tracking
    status: str                      # 'ordered', 'in_transit', 'delivered', 'cancelled'
    order_date: datetime             # When order was placed
    estimated_delivery: datetime     # Expected delivery date
    
    # Delivery Integration
    delivery_contents: Dict          # What will be delivered
    transfer_ids: List[str]          # Associated transfer IDs
```

### 4. BlackMarket (Special Suppliers)
**Purpose**: Manages special suppliers with unique items and mechanics.

```python
class BlackMarket:
    """Manages black market suppliers and transactions."""
    
    # Supplier Management
    suppliers: Dict[str, BlackMarketSupplier]
    reputation: int                  # Player reputation
    
    # Core Operations
    def discover_supplier(supplier_id, requirements)
    def get_available_purchases(money, reputation)
    def place_order(supplier_id, item_id, base_id, quantity, money)
    def monthly_refresh()
```

## Features and Capabilities

### 1. Standard Purchasing
```python
# Get available purchases for a base
available = purchase_system.get_available_purchases(
    base_id='base_001',
    available_technologies=['laser_weapons', 'alien_alloys'],
    available_services=['workshop', 'barracks'],
    available_money=100000
)

# Place an order
success, order_id, issues = purchase_system.place_order(
    entry_id='laser_rifle',
    base_id='base_001', 
    quantity=5,
    available_technologies=['laser_weapons'],
    available_services=['workshop'],
    available_money=250000
)
```

### 2. Monthly Limits
- Each purchase entry can have a monthly limit
- Limits reset automatically at month start
- System tracks purchases per base per month
- Validation prevents exceeding limits

### 3. Black Market System
```python
# Get black market items
black_market_items = purchase_system.get_black_market_purchases(
    base_id='base_001',
    available_money=50000,
    reputation=15
)

# Purchase from black market
success, order_id, issues = purchase_system.place_black_market_order(
    supplier_id='shadow_broker',
    item_id='plasma_rifle',
    base_id='base_001',
    quantity=1,
    available_money=75000
)
```

### 4. Delivery System Integration
- Orders create transfers in the existing transfer system
- Daily processing moves ready orders to transit
- Transfer system handles final delivery to base inventory
- Supports items, units, and crafts

### 5. Order Management
```python
# Check order status
status = purchase_system.get_order_status(order_id)
print(f"Status: {status['status']}, ETA: {status['estimated_delivery']}")

# Get all active orders
orders = purchase_system.get_active_orders(base_id='base_001')

# Cancel an order (if not yet in transit)
cancelled = purchase_system.cancel_order(order_id)
```

## Configuration Format

### Purchase Entries (TOML)
```toml
[purchasing.laser_rifle]
name = "Laser Rifle"
category = "weapon"
cost = 50000
delivery_time = 3
monthly_limit = 10
black_market = false
required_technologies = ["laser_weapons"]
required_services = ["workshop"]
required_items = {}

[purchasing.laser_rifle.delivery_contents]
items = { "laser_rifle" = 1 }
units = {}
crafts = {}
```

### Black Market Configuration
```toml
[black_market]
reputation_threshold = 10
reputation_decay = 0.1
price_variance = 0.3
reliability_bonus = 0.05

[black_market.suppliers.shadow_broker]
name = "Shadow Broker"
discover_requirements = ["black_market_contacts"]
base_reliability = 0.8
stock_refresh_days = 7
available_items = ["plasma_rifle", "alien_alloys", "psi_amp"]
```

## Game Integration

### 1. Daily Processing
```python
class TGame:
    def on_daily_tick(self):
        """Called every day by calendar system."""
        # Process transfers and purchases
        self.process_daily_transfers_and_purchases()
        
    def process_daily_transfers_and_purchases(self):
        """Process daily deliveries."""
        # Transfer system processes deliveries
        self.transfer_manager.tick_all(self._add_delivered_items_to_base)
        
        # Purchase system processes new orders ready for delivery
        if self.purchase_system:
            self.purchase_system.process_daily_purchases(self.transfer_manager)
```

### 2. Monthly Processing
```python
def on_monthly_tick(self):
    """Called every month by calendar system."""
    if self.purchase_system:
        # Reset monthly purchase limits
        self.purchase_system.process_monthly_reset()
```

### 3. Base Inventory Integration
```python
def _add_delivered_items_to_base(self, base_id: str, object_type: str, 
                                 object_id: str, quantity: int):
    """Callback for transfer system to add delivered items."""
    if base_id in self.bases:
        base = self.bases[base_id]
        
        if object_type == 'item':
            base.add_item(object_id, quantity)
        elif object_type == 'unit':
            # Create and add unit instances
            pass
        elif object_type == 'craft':
            # Create and add craft instances
            pass
```

## Purchase Flow

### Standard Purchase Flow
1. **Discovery**: Player views available purchases filtered by requirements
2. **Validation**: System checks technology, service, money, and limit requirements
3. **Order Placement**: Order created with estimated delivery date
4. **Daily Processing**: System checks if orders are ready for delivery
5. **Transfer Creation**: Ready orders become transfer objects
6. **Delivery**: Transfer system delivers items to base inventory

### Black Market Flow
1. **Supplier Discovery**: Meet requirements to unlock suppliers
2. **Stock Check**: View available items with price variance
3. **Reputation Check**: Ensure sufficient reputation for access
4. **Order Placement**: Place order with reliability consideration
5. **Processing**: Same as standard flow but with failure chance

## Error Handling

### Validation Errors
- Insufficient funds
- Missing technology requirements
- Missing service requirements
- Monthly limit exceeded
- Unknown purchase entry

### Order Errors
- Order not found
- Cannot cancel (already in transit)
- Invalid order status

### Black Market Errors
- Insufficient reputation
- Supplier not discovered
- Item not available
- Transaction failed (reliability check)

## Testing and Validation

### Unit Tests
```python
def test_purchase_validation():
    """Test purchase requirement validation."""
    purchase_system = TPurchase(test_data)
    
    can_buy, issues = purchase_system.validate_purchase(
        'laser_rifle', 'base_001', 1,
        ['laser_weapons'], ['workshop'], 50000
    )
    
    assert can_buy == True
    assert len(issues) == 0

def test_monthly_limits():
    """Test monthly purchase limits."""
    # Place orders up to limit
    # Verify limit enforcement
    # Test monthly reset
```

### Integration Tests
```python
def test_daily_processing():
    """Test daily order processing."""
    # Create orders
    # Advance days
    # Verify transfers created
    # Verify delivery to base

def test_transfer_integration():
    """Test integration with transfer system."""
    # Create purchase order
    # Process daily
    # Verify transfer creation
    # Process transfer delivery
```

## Performance Considerations

### Optimization Strategies
- Lazy loading of purchase entries
- Cached requirement validation
- Efficient monthly limit tracking
- Minimal transfer object creation

### Memory Management
- Orders cleaned up after delivery
- Historical data archival
- Supplier state management

## Future Enhancements

### Planned Features
1. **Dynamic Pricing**: Market-based price fluctuation
2. **Bulk Discounts**: Volume-based pricing
3. **Expedited Delivery**: Pay more for faster delivery
4. **Contract System**: Long-term supply agreements
5. **Quality Variants**: Different quality levels for items

### UI Improvements
1. **Advanced Filtering**: Search and sort capabilities
2. **Order History**: Complete purchase history view
3. **Supplier Management**: Black market supplier interface
4. **Budget Planning**: Purchase planning tools

## API Reference

### TPurchase Class Methods

#### Core Purchase Operations
- `get_available_purchases(base_id, technologies, services, money) -> List[TPurchaseEntry]`
- `validate_purchase(entry_id, base_id, quantity, technologies, services, money) -> Tuple[bool, List[str]]`
- `place_order(entry_id, base_id, quantity, technologies, services, money) -> Tuple[bool, Optional[str], List[str]]`

#### Black Market Operations
- `get_black_market_purchases(base_id, money, reputation) -> List[Dict[str, Any]]`
- `place_black_market_order(supplier_id, item_id, base_id, quantity, money) -> Tuple[bool, Optional[str], List[str]]`

#### Order Management
- `get_order_status(order_id) -> Optional[Dict[str, Any]]`
- `get_active_orders(base_id) -> Dict[str, List[Any]]`
- `cancel_order(order_id) -> bool`

#### System Processing
- `process_daily_purchases(transfer_manager) -> Dict[str, List[str]]`
- `process_monthly_reset() -> None`

#### Data Management
- `save_data() -> Dict[str, Any]`
- `load_data(data) -> None`

---

This comprehensive purchase system provides all the functionality needed for an XCOM-style purchasing and procurement system with full integration into the existing game architecture.
