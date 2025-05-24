"""
TOML to YAML Converter Script

This script converts all TOML files in a directory structure to YAML format,
preserving comments and maintaining the same directory structure in the output.
"""

import os
import sys
import shutil
import yaml
import re
from pathlib import Path

# Source and destination directories
SOURCE_DIR = os.path.join('mods', 'xcom', 'rules')
DEST_DIR = os.path.join('mods', 'xcom', 'rules2')

# Configure custom YAML representation
class CustomYAML(yaml.Dumper):
    """Custom YAML Dumper that preserves quotes for values but not for keys."""
    pass

def quoted_scalar_representer(dumper, data):
    """Force strings to be represented with quotes."""
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style="'")

# Register the string representer
yaml.add_representer(str, quoted_scalar_representer, Dumper=CustomYAML)

def ensure_dir(directory):
    """Ensure that a directory exists, creating it if necessary."""
    os.makedirs(directory, exist_ok=True)

def parse_toml_with_comments(toml_file):
    """
    Parse TOML content preserving comments.
    Returns a dictionary with the parsed data and comments.
    """
    with open(toml_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Process the file line by line
    result = []
    current_section = ""
    section_data = {}
    section_comments = {}

    for line in lines:
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            result.append({"type": "empty"})
            continue

        # Handle comments
        if stripped.startswith('#'):
            result.append({"type": "comment", "content": stripped})
            continue

        # Handle inline comments
        comment_part = ""
        if '#' in stripped:
            parts = stripped.split('#', 1)
            stripped = parts[0].strip()
            if stripped:  # If there's content before the comment
                comment_part = '#' + parts[1]

        # Handle section headers [section]
        if stripped.startswith('[') and stripped.endswith(']'):
            current_section = stripped[1:-1].strip()
            result.append({"type": "section", "name": current_section, "comment": comment_part})
            continue

        # Handle key-value pairs
        if '=' in stripped:
            key, value = stripped.split('=', 1)
            key = key.strip()
            value = value.strip()
            result.append({"type": "key_value", "key": key, "value": value, "comment": comment_part})
            continue

        # Handle any other line
        result.append({"type": "other", "content": stripped})

    return result

def parse_value(value_str):
    """
    Parse a TOML value string into its appropriate Python type.
    Handles strings, numbers, booleans, arrays and inline tables.
    """
    value_str = value_str.strip()

    # Handle empty value
    if not value_str:
        return ""

    # Handle boolean
    if value_str.lower() == "true":
        return True
    if value_str.lower() == "false":
        return False

    # Handle arrays/lists
    if value_str.startswith('[') and value_str.endswith(']'):
        array_content = value_str[1:-1].strip()
        if not array_content:
            return []
        values = []
        current_item = ""
        in_string = False
        quote_char = None
        in_curlies = 0
        in_brackets = 0
        for char in array_content:
            if char == '"' or char == "'":
                if not in_string:
                    in_string = True
                    quote_char = char
                elif char == quote_char and (len(current_item) == 0 or current_item[-1] != '\\'):
                    in_string = False
                    quote_char = None
                current_item += char
            elif char == '{':
                in_curlies += 1
                current_item += char
            elif char == '}':
                in_curlies -= 1
                current_item += char
            elif char == '[':
                in_brackets += 1
                current_item += char
            elif char == ']':
                in_brackets -= 1
                current_item += char
            elif char == ',' and not in_string and in_curlies == 0 and in_brackets == 0:
                values.append(parse_value(current_item))
                current_item = ""
            else:
                current_item += char
        if current_item:
            values.append(parse_value(current_item))
        return values

    # Handle inline tables
    if value_str.startswith('{') and value_str.endswith('}'):
        table_content = value_str[1:-1].strip()
        if not table_content:
            return {}
        items = []
        current_item = ""
        in_string = False
        quote_char = None
        in_curlies = 0
        in_brackets = 0
        for char in table_content:
            if char == '"' or char == "'":
                if not in_string:
                    in_string = True
                    quote_char = char
                elif char == quote_char and (len(current_item) == 0 or current_item[-1] != '\\'):
                    in_string = False
                    quote_char = None
                current_item += char
            elif char == '{':
                in_curlies += 1
                current_item += char
            elif char == '}':
                in_curlies -= 1
                current_item += char
            elif char == '[':
                in_brackets += 1
                current_item += char
            elif char == ']':
                in_brackets -= 1
                current_item += char
            elif char == ',' and not in_string and in_curlies == 0 and in_brackets == 0:
                items.append(current_item)
                current_item = ""
            else:
                current_item += char
        if current_item:
            items.append(current_item)
        table_dict = {}
        for item in items:
            if '=' in item:
                k, v = item.split('=', 1)
                table_dict[k.strip()] = parse_value(v)
        return table_dict

    # Handle strings (quoted)
    if (value_str.startswith('"') and value_str.endswith('"')) or (value_str.startswith("'") and value_str.endswith("'")):
        string_value = value_str[1:-1]
        return string_value.strip()

    # Handle numbers
    try:
        if '.' in value_str:
            return float(value_str)
        else:
            return int(value_str)
    except ValueError:
        return value_str.strip()

def toml_to_yaml_structure(toml_parsed):
    """Convert the parsed TOML structure to a YAML-compatible data structure."""
    yaml_data = {}
    current_section = yaml_data
    sections_stack = []

    for item in toml_parsed:
        if item["type"] == "section":
            section_path = item["name"].split('.')
            current_section = yaml_data

            # Navigate to the correct nested section
            for section in section_path:
                if section not in current_section:
                    current_section[section] = {}
                current_section = current_section[section]

        elif item["type"] == "key_value":
            # Use the improved parser for values
            current_section[item["key"]] = parse_value(item["value"])

    return yaml_data

def format_yaml_with_comments(toml_parsed, yaml_data):
    """Format YAML content with preserved comments, matching TOML line positions."""
    yaml_content = yaml.dump(
        yaml_data,
        default_flow_style=False,
        sort_keys=False,
        indent=4,
        width=120,
        Dumper=CustomYAML
    )
    # Remove all types of quotes from keys (single, double, triple)
    yaml_content = re.sub(r"(['\"]{1,3})([^'\"]+?)\1(?=:)", r"\2", yaml_content)
    yaml_lines = yaml_content.splitlines()

    # Build a list of YAML lines to insert TOML comments/empty lines at the same TOML line positions
    result_lines = []
    yaml_idx = 0
    for item in toml_parsed:
        if item["type"] == "comment":
            result_lines.append(item["content"])
        elif item["type"] == "empty":
            result_lines.append("")
        else:
            # For section/key_value/other, insert the next YAML line
            if yaml_idx < len(yaml_lines):
                result_lines.append(yaml_lines[yaml_idx])
                # Add inline comment if present and this is a key_value
                if item["type"] == "key_value" and item.get("comment"):
                    if result_lines[-1].strip():
                        result_lines[-1] = f"{result_lines[-1]} {item['comment']}"
                yaml_idx += 1
    # Add any remaining YAML lines
    while yaml_idx < len(yaml_lines):
        result_lines.append(yaml_lines[yaml_idx])
        yaml_idx += 1
    return '\n'.join(result_lines)

def convert_toml_to_yaml(toml_file, yaml_file):
    """Convert a TOML file to YAML format, preserving comments."""
    try:
        # Parse TOML with comments
        toml_structure = parse_toml_with_comments(toml_file)

        # Convert to YAML data structure
        yaml_data = toml_to_yaml_structure(toml_structure)

        # Format YAML with comments
        yaml_content = format_yaml_with_comments(toml_structure, yaml_data)

        # Write the result to file
        with open(yaml_file, 'w', encoding='utf-8') as f:
            f.write(yaml_content)

        return True
    except Exception as e:
        print(f"Error converting {toml_file} to YAML: {e}")
        return False

def process_directory(source_dir, dest_dir):
    """Process all TOML files in the source directory and subdirectories."""
    # Create destination directory if it doesn't exist
    ensure_dir(dest_dir)

    # Walk through source directory
    for root, dirs, files in os.walk(source_dir):
        # Create corresponding subdirectories in destination
        rel_path = os.path.relpath(root, source_dir)
        current_dest_dir = os.path.join(dest_dir, rel_path) if rel_path != '.' else dest_dir
        ensure_dir(current_dest_dir)

        # Process each file
        for file in files:
            if file.lower().endswith('.toml'):
                source_file = os.path.join(root, file)
                dest_file = os.path.join(current_dest_dir, file.replace('.toml', '.yaml'))

                print(f"Converting {source_file} to {dest_file}...")
                success = convert_toml_to_yaml(source_file, dest_file)
                if success:
                    print(f"Successfully converted {source_file} to {dest_file}")
                else:
                    print(f"Failed to convert {source_file}")
            else:
                # Copy non-TOML files as-is (optional)
                # source_file = os.path.join(root, file)
                # dest_file = os.path.join(current_dest_dir, file)
                # shutil.copy2(source_file, dest_file)
                pass

def main():
    print(f"Converting TOML files from {SOURCE_DIR} to YAML format in {DEST_DIR}")

    # Get absolute paths
    base_dir = os.path.abspath(os.getcwd())
    absolute_source = os.path.join(base_dir, SOURCE_DIR)
    absolute_dest = os.path.join(base_dir, DEST_DIR)

    # Verify source exists
    if not os.path.exists(absolute_source):
        print(f"Error: Source directory {absolute_source} does not exist.")
        return

    # Process files
    process_directory(absolute_source, absolute_dest)
    print("Conversion completed!")

if __name__ == "__main__":
    main()
