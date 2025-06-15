# Task 3: Test Case Creation and Best Practices

**Purpose:**
Ensure every file and class is covered by robust, maintainable tests in a `test` subfolder.

## Steps & Examples

1. **Test File Naming and Location**  
   Test files should be named `test_<module>.py` and placed in a `test` subfolder next to the module being tested.

2. **Test Structure**  
   Each test file should:
   - Import the class/module to be tested.
   - Use `pytest` or `unittest` for fixtures and mocking dependencies.
   - Cover all public methods and attributes.
   - Test both typical and edge cases, including error handling.
   - Use descriptive test method names (e.g., `test_methodname_scenario`).
   - Assert expected outcomes and side effects.

3. **Example Test File**
   ```python
   import unittest
   from engine.economy.ttransfer import TTransfer, TransferManager

   class TestTTransfer(unittest.TestCase):
       def test_init_and_tick(self):
           t = TTransfer('id1', 'base1', 'item', 'medkit', 5, 2)
           self.assertEqual(t.id, 'id1')
           # ... more assertions ...
           t.tick()
           # ... more assertions ...

       def test_cancel(self):
           t = TTransfer('id2', 'base2', 'craft', 'skyranger', 1, 3)
           t.cancel()
           self.assertEqual(t.status, 'cancelled')

   class TestTransferManager(unittest.TestCase):
       def test_add_and_tick_all(self):
           tm = TransferManager()
           delivered = []
           def base_storage_lookup(base_id, object_type, object_id, quantity):
               delivered.append((base_id, object_type, object_id, quantity))
           t1 = TTransfer('id3', 'base3', 'unit', 'soldier', 2, 1)
           tm.add_transit(t1)
           tm.tick_all(base_storage_lookup)
           self.assertEqual(len(delivered), 1)
           # ... more assertions ...
   ```

4. **Best Practices**
   - Use fixtures for setup/teardown.
   - Mock external dependencies.
   - Avoid testing private methods directly.
   - Ensure tests are independent and repeatable.
