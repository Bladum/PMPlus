# BIS Coding Agent Instructions & Best Practices

## Purpose
This file is a step-by-step checklist for all contributors (AI or human) working with Python code in this project. 
Follow these instructions for every Python file or class you create or modify to ensure consistency, maintainability, and quality.

## How to Use
For each Python file or class you work on, complete the following steps in order. If a required file (e.g., test file, README) does not exist, create it as described.


---

# Task List

0. **Analyze Entire File or Class**
   - Review the full Python file or class to understand its structure, logic, and dependencies.
1. **Optimize Python Code**
   - Refactor code for clarity and maintainability: create sub-methods, split large code blocks into logical steps, and add comments to explain each step.
   - Add or improve error handling and logging as needed.
   - Apply best practices from Section 1 (General Coding Principles), Section 3 (Data Handling), and Section 4 (What to Avoid).
2. **Improve Documentation and Comments**
   - Follow Section 2 (Documentation Requirements) for file, class, constructor, and method docstrings.
   - Ensure all code is well-commented and documentation is up to date.
   - Check if API.yml exists in the wiki/ or docs/ folder and is up to date with the class constructor parameters.
   - Ensure that API.yml is properly formatted and contains all necessary information about the class and its parameters.
3. **Summarize Class and Update Local README**
   - Extract structure and format from the provided readme.md example.
   - Summarize the class, its purpose, and core functionalities (see template below).
   - Update or create a readme.md in the same folder, following a consistent format for all files/classes.
   - See Section 5 (Synchronization with BIS API Documentation and Local README).
   - *Example class summary:*
     ```markdown
     ## MyClass
     MyClass is responsible for ... It provides methods to ...
     - **Attributes:** attr1, attr2
     - **Methods:** method1(), method2()
     ```
4. **Validate and Update API.yml**
   - Check if all arguments passed to the class constructor (and any derived attributes) are documented in BIS API.yml (located in the wiki/ or docs/ folder).
   - If any are missing or outdated, update BIS API.yml accordingly. Create the file if it does not exist.
   - See Section 5 (Synchronization with BIS API Documentation and Local README).
5. **Check or Create Test File**
   - Analyze files named test_* in the test subfolder for the file/class. If not present, create a test file that covers all methods and attributes.
   - Follow best practices and avoid common pitfalls as described in Section 1 and Section 4.
   - See details below for how to structure and implement tests.
   - *Example test file location:*
     - For src/my_module.py, create or update src/test/test_my_module.py

6. **OXC references**
   - ALienFall is clone of Open XCOM and its repository (https://github.com/OpenXcom/OpenXcom/)
   - You can use OXC code as a reference for how to implement classes, methods, and documentation.
   - Update any relevant OXC documentation or comments in the code.

---

## 1. General Coding Principles

### 1.1 Clean Code
1. **Separation of Concerns**
   - Each module, class, or component should have a single responsibility, making it easier to understand, maintain, and test.
   - *Example:*
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
2. **Document Your Code**
   - Use clear and concise comments and docstrings to explain the purpose of functions, classes, and complex logic.
   - *Example:*
     ```python
     def calculate_area(radius):
         """Calculate the area of a circle given its radius."""
         return 3.1415 * radius ** 2
     ```
3. **Don't Repeat Yourself (DRY)**
   - Avoid duplicating code by creating reusable functions or classes.
   - *Example:*
     ```python
     # BAD: Copy-pasted logic
     def add_user(name):
         # validate name
         # add user
         pass
     def add_admin(name):
         # validate name
         # add admin
         pass
     # GOOD: Reuse logic
     def add_person(name, role):
         # validate name
         # add person with role
         pass
     ```
4. **Keep It Simple**
   - Write code that is easy to read and understand, avoiding unnecessary complexity.
   - *Example:*
     ```python
     # BAD: Overly complex
     def f(x): return (lambda y: y+1)(x)
     # GOOD: Simple and clear
     def increment(x): return x + 1
     ```
5. **Test Driven Development (TDD)**
   - Write tests before implementing features to ensure code correctness and maintainability.
   - *Example:*
     ```python
     # Write test first
     def test_increment():
         assert increment(2) == 3
     # Then implement increment()
     ```
6. **You Aren't Gonna Need It (YAGNI)**
   - Only implement features that are currently needed, avoiding over-engineering.
   - *Example:*
     ```python
     # BAD: Adding unused parameters or features
     def process(data, unused_option=None):
         pass
     # GOOD: Only what is needed
     def process(data):
         pass
     ```

### 1.2 Python Code Design
- Prioritize readability, error handling, and scalability in all changes.
- Use descriptive variable and function names.
- Avoid deeply nested logic; refactor into smaller functions if needed.
- Design with scalability in mind: make it easy to extend or modify code in the future.
- Use blank lines to separate methods and logical steps within methods for readability.
- *Example:*
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


### 1.3 Data Handling

- **Do not use pandas or polars DataFrames** for new code.
- Prefer using DuckDB API, DuckDB SQL, or pure Python data structures for all data processing and querying.
- Only use DataFrames if absolutely necessary for compatibility.
- *Example:*
  ```python
  # GOOD: DuckDB
  import duckdb
  con = duckdb.connect()
  con.execute('SELECT * FROM my_table')
  # GOOD: Pure Python
  data = [dict(id=1, value='a'), dict(id=2, value='b')]
  ```

### 1.4 What to Avoid

- Missing or outdated docstrings at file, class, __init__, or method level.
- Magic numbers or strings: use named constants instead.
- Commented-out code: remove unused code from the codebase.
- Large functions/classes: break into smaller, focused units.
- Inconsistent naming or style: follow PEP8 and project conventions.
- Deeply nested logic: refactor for clarity.
- Duplicated code: refactor to use reusable functions/classes.
- Unused imports or variables: remove them.
- Using pandas or polars DataFrames for new code (unless required for compatibility).
- Overly complex or clever code: prefer clarity and simplicity.


---

## 2. Documentation Requirements

### 2.1 File-level docstring
Every Python file must start with a docstring summarizing its purpose and main contents.
```python
"""
TExcelColumn: Column widget for Excel report generation.
Purpose: Handles formatting, rules, hyperlinks, and writing column data to worksheet.
Last update: 2025-06-08
"""
```

### 2.2 Class-level docstring
Every class must have a docstring describing its purpose and usage.
```python
class TExcelColumn(TExcelWidget):
    '''
    Column formatter without header.
    Attributes:
        col_reference (Optional[Dict]): Reference to other columns.
        column_format_per_cell (Optional[Any]): Per-cell formatting.
        column_formatting (Optional[Dict]): Formatting dictionary.
        compare: Compare rules for conditional formatting.
        df_reference (Optional[pd.DataFrame]): Reference DataFrame.
        df_serie (pd.Series): Column data.
    '''
    # ...
```

### 2.3 __init__ docstring
Document all parameters and their types in the constructor docstring.
```python
    def __init__(
        self,
        worksheet: xlsxwriter.workbook.Worksheet,
        series: pd.Series,
        label: str = "Label",
        label_translate: str = '',
        sheet_name: Optional[str] = None,
        row_height: Optional[int] = None,
    ):
        """
        Initialize the Excel column widget.
        Args:
            worksheet: Worksheet to write to.
            series: Data for the column.
            label: Column label.
            label_translate: Translated label or tuple.
            sheet_name: Name of the worksheet.
            row_height: Row height for the column.
        """
        # ...
```

### 2.4 Method/function docstring

Every method/function must have a concise docstring describing its purpose, arguments, and return value.
```python
    def write_excel(self):
        """
        Write the column data, formatting, hyperlinks, and apply rules to the worksheet.
        Steps:
            1. Calculate and set column width.
            2. Write hyperlinks if present.
            3. Apply cell formats and write data.
            4. Apply conditional formatting rules.
            5. Highlight rows if specified.
        Exception handling and logging are included for robustness.
        """
        # ...
```

---


## 3 Update Local README.md

- For every Python file, update (or create if missing) a `readme.md` file in the same folder as the Python file.
- The `readme.md` should contain a short description of what the file/class does, its purpose, and any important usage notes.
- Ensure the local `readme.md` in the same folder as the Python file describes what the file and its main class are doing.
- Keep the README, code docstrings, and `API.yml` in sync and up to date.

---

## 4 Parameter Documentation in API.yml

- For every parameter in each class constructor, check that it is properly documented in the `API.yml` file.
- If a parameter is missing or its description is outdated, update `API.yml` to match the code and docstrings.
- Ensure the documentation in `API.yml` is clear, complete, and uses the same naming and types as in the code.
- For every class, verify that all parameters present in the class constructor are documented in `API.yml`.
- If any parameter exists in the class but is missing or not properly described in `API.yml`, update the documentation accordingly.
- Do not add any python code to API.yml, it should only contain documentation in YAML format with comments how to use it.
- API.yml should be in sync with corresponding Python class and its constructor parameters.
- API.yml should be in sync with mod data in mods folder (e.g. mods/xcom/rules/*.yaml).

---

## 5. Test File Requirements and Best Practices

- Test files should be named `test_<module>.py` and placed in a `test` subfolder next to the module being tested.
- Each test file should:
  - Import the class/module to be tested.
  - Use pytest and unittest.mock for fixtures and mocking dependencies.
  - Cover all public methods and attributes of the class.
  - Test both typical and edge cases, including error handling.
  - Use descriptive test method names (e.g., `test_methodname_scenario`).
  - Assert expected outcomes and side effects (e.g., logger calls, file outputs).
- Example structure:
  ```python
  import pytest
  from <module> import <Class>
  from unittest.mock import MagicMock

  class Test<Class>:
      def test_init(self):
          ...
      def test_method(self):
          ...
  ```
- See provided test files for more detailed examples.

---

## Agent Workflow Summary
- Apply the documentation formatting rules to all files.
- Refactor code to follow the general Python code design and clean code rules above.
- For every class constructor, check and update parameter documentation in  `API.yml`.
- For every parameter in every class, ensure it is documented in `API.yml` and descriptions are up to date.
- For every Python file, update the local `readme.md` in the same folder to describe the file/class and keep it in sync with the code and API documentation.
- Ensure the local `readme.md` describes what the file and its main class are doing.
- Avoid using pandas/polars DataFrames; use DuckDB or pure Python instead.
- Ensure all methods are documented and code is well-spaced and organized.
- Prioritize readability, error handling, and scalability in all changes.
- Just follow instructions.md for all files, dont ask me every time, i will see results and accept or reject.
---

By following these instructions, you will help maintain a high-quality, maintainable, and consistent codebase, with synchronized code, API documentation, and local usage notes.
