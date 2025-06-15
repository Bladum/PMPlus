# Task 1: Documentation and Commenting for Python Files

**Purpose:**
Standardize and automate the process of documenting every Python file, class, and method for clarity, maintainability, and onboarding.

## Steps & Examples

1. **File-Level Docstring**  
   Add a docstring at the top of each file summarizing its purpose and main contents.
   
   *Example:*
   ```python
   """
   engine/economy/ttransfer.py

   Defines the TTransfer and TransferManager classes, which manage item, craft, and unit transits between bases, including delivery, status, and daily updates.

   Classes:
       TTransfer: Represents a single delivery in transit.
       TransferManager: Manages all active deliveries and their progress.

   Last standardized: 2025-06-15
   """
   ```

2. **Class-Level Docstring**  
   Every class must have a docstring describing its purpose, listing all attributes and methods.
   
   *Example:*
   ```python
   class TTransfer:
       """
       Represents a single transit for one item, craft, or unit.
       Contains info about what, where, when, and quantity.

       Attributes:
           id (str): Transit ID.
           base_id (str): Base receiving the delivery.
           object_type (str): 'item', 'craft', or 'unit'.
           object_id (str): ID of the object being transferred.
           quantity (int): Quantity being transferred.
           days_left (int): Days remaining for delivery.
           status (str): 'in_transit', 'delivered', or 'cancelled'.

       Methods:
           tick(): Progress the transit by one day.
           is_delivered(): Check if the transit is delivered.
           cancel(): Cancel the transit if still in transit.
       """
   ```

3. **Constructor and Method Docstrings**  
   Document all parameters and their types in the constructor docstring.
   
   *Example:*
   ```python
       def __init__(self, transit_id, base_id, object_type, object_id, quantity, days_required):
           """
           Initialize a new transit.

           Args:
               transit_id (str): Unique ID for the transit.
               base_id (str): Receiving base.
               object_type (str): 'item', 'craft', or 'unit'.
               object_id (str): ID of the object.
               quantity (int): Number of objects.
               days_required (int): Days for delivery.
           """
           # ...
   ```

   Every method/function must have a concise docstring describing its purpose, arguments, return value, and exceptions.
   
   *Example:*
   ```python
       def tick(self):
           """
           Progress the transit by one day. Updates status if delivered.
           """
           # ...
   ```

4. **In-Method Comments**  
   For longer methods, add inline comments to explain major steps or code blocks.

5. **Import All Python Files in `__init__.py`**  
   In every `__init__.py`, import all Python files from the same folder.

6. **Replace Old Documentation**  
   Always replace existing documentation and comments with the standardized format. Do not append or mix with old comments.
