#!/usr/bin/env python3
"""
Script to update game_data.py to use the new item PNG file paths
"""

import os
import re

def to_camel_case(text):
    """Convert text to camelCase format for filenames"""
    # Remove special characters and split on spaces
    words = re.sub(r'[^\w\s]', '', text).split()
    if not words:
        return text.lower()
    
    # First word lowercase, rest title case
    result = words[0].lower()
    for word in words[1:]:
        result += word.capitalize()
    
    return result

def update_game_data():
    """Update game_data.py to use new item file paths"""
    
    # Read the current game_data.py
    with open('game_data.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Track changes
    changes_made = []
    
    # Find all item entries and update their icon paths
    # Pattern: ("Item Name", "old/path.png", {...}, count)
    pattern = r'(\("([^"]+)",\s*)"(other/item2?\.png)"(\s*,\s*\{[^}]+\}\s*,\s*\d+\))'
    
    def replace_path(match):
        item_name = match.group(2)
        old_path = match.group(3)
        camel_name = to_camel_case(item_name)
        new_path = f"items/{camel_name}.png"
        
        changes_made.append(f"{item_name}: {old_path} -> {new_path}")
        
        return f'{match.group(1)}"{new_path}"{match.group(4)}'
    
    # Apply the replacements
    updated_content = re.sub(pattern, replace_path, content)
    
    # Write the updated content back
    with open('game_data.py', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    return changes_made

def main():
    print("Updating game_data.py to use new item file paths...")
    
    changes = update_game_data()
    
    if changes:
        print(f"\nSuccessfully updated {len(changes)} item references:")
        for change in changes:
            print(f"  - {change}")
        print(f"\nAll item data now references files in the items/ directory!")
    else:
        print("No changes were made. This might indicate the file was already updated or there was an issue.")

if __name__ == "__main__":
    main()
