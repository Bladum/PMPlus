# Task: Validate and Document API Usage from YAML to Python

## Goal
Automatically validate and update documentation for Python classes that are configured via YAML files. Ensure that all parameters defined in YAML configuration files (in `mods/xcom/rules/`) have corresponding attributes in the relevant Python class constructors, and that documentation is kept in sync. The output should be a comprehensive `API.md` file containing tables for each class, making it easy for modders to understand and use the API.

## Output
- **API.md**: A markdown file containing, for each relevant class, a table with:
  - **API Name**: The parameter/attribute name.
  - **Example Value**: A sample value from the YAML configuration.
  - **Description**: A human-readable description (from class docstrings or inferred from context).
- Each class should have its own section and table in `API.md`.

## Steps

1. **Locate YAML and Python Files**
   - Identify YAML files in `mods/xcom/rules/` that define configuration for game entities.
   - Identify Python classes that represent these entities (e.g., in `engine/economy/`).

2. **Extract Parameters from YAML**
   - For each entity in the YAML, collect all parameter names and their example values.
   - Aggregate all unique parameter names used across all entities in the YAML file.

3. **Extract Constructor Parameters from Python**
   - For each relevant Python class, extract the parameters set as attributes in the `__init__` method.
   - Gather descriptions from class docstrings or comments if available.

4. **Match YAML Parameters to Python Attributes**
   - Compare YAML parameters to Python class attributes.
   - Identify parameters present in YAML but missing in Python, and vice versa.

5. **Generate API.md Documentation**
   - For each class, create a markdown table with columns: API Name, Example Value, Description.
   - Populate the table with data from YAML and Python sources.
   - Add a section for each class, including a brief class description.

6. **Validate and Update Documentation**
   - Update the class docstring to reflect all possible parameters, noting which are required, optional, or missing.
   - Optionally, generate a report or table showing the mapping and any mismatches.

7. **(Optional) Suggest Code or YAML Updates**
   - Suggest adding missing parameters to Python or removing unused ones from YAML.

## Extended Instructions: Generating API.md in OpenXcom Ruleset Style

To ensure your API documentation is clear and modder-friendly, follow the OpenXcom ruleset reference style:

- **For each relevant Python class**, create a section in `API.md` with a table listing all configurable parameters.
- **Table columns:**
  - **API Name**: The parameter/attribute name as used in YAML and Python.
  - **Example Value**: A sample or default value from the YAML configuration.
  - **Description**: A concise, human-readable explanation (from class docstrings, YAML comments, or inferred from context).
- **Documentation style:**
  - Use concise, tabular format for clarity.
  - Highlight OXCE-specific or extended parameters as needed.
  - Include YAML snippets for complex features (anchors, inheritance, !add/!remove tags) if relevant.
  - Add a brief class description before each table, based on the class docstring or YAML section comment.
- **See `API.md` for an example of the required format.**

---

## Example Table (see API.md for more)

| API Name | Example Value | Description |
|----------|---------------|-------------|
| id       | "STR_LASER_RIFLE" | Unique string identifier for the item. |
| type     | "weapon"      | The category/type of the item. |
| costBuy  | 30000         | Purchase cost in in-game currency. |

---

*This approach ensures your documentation is as clear and useful as the OpenXcom ruleset reference, making it easy for modders to understand and use your API.*

## Notes
- This task can be automated as a script or tool.
- Keep this document updated as the process evolves.
- The `API.md` file should be clear and comprehensive for modders.
