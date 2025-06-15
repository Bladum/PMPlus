# Task 4: Python Code Optimization and Refactoring

**Purpose:**
Refactor and optimize Python code for clarity, maintainability, and scalability, following project conventions.

## Steps & Examples

1. **Separation of Concerns**  
   Each module, class, or component should have a single responsibility.
   
   *Example:*
   ```python
   # BAD: Mixing data access and business logic
   def process_and_save(data):
       # process data
       # save to database
       pass
   # GOOD: Separate functions
   def process(data):
       # process data
       pass
   def save_to_db(processed_data):
       # save to database
       pass
   ```

2. **DRY Principle**  
   Avoid duplicating code by creating reusable functions or classes.

3. **Keep It Simple**  
   Write code that is easy to read and understand, avoiding unnecessary complexity.
   
   *Example:*
   ```python
   # BAD: Overly complex
   def f(x): return (lambda y: y+1)(x)
   # GOOD: Simple and clear
   def increment(x): return x + 1
   ```

4. **Early Returns to Avoid Deep Nesting**  
   *Example:*
   ```python
   # BAD: Deep nesting
   if a:
       if b:
           if c:
               do_something()
   # GOOD: Early returns
   if not a or not b or not c:
       return
   do_something()
   ```

5. **Error Handling and Logging**  
   Add or improve error handling and logging as needed.

6. **Data Handling**  
   Do not use pandas or polars DataFrames for new code.
   Prefer DuckDB API, DuckDB SQL, or pure Python data structures.

7. **Remove Unused Code and Imports**  
   Remove commented-out code, unused variables, and imports.

8. **Consistent Naming and Style**  
   Follow PEP8 and project conventions.

9. **Test Driven Development (TDD)**  
   Write tests before implementing features.
