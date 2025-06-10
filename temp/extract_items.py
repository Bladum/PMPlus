#!/usr/bin/env python3
"""
Script to extract all unique item names from game_data.py and create PNG files
"""

import os
import shutil
import re

# Import after setting up the path
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_data import GameData

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

def extract_unique_items():
    """Extract all unique item names from all bases"""
    unique_items = set()
    
    # Go through all bases and collect item names
    for base in GameData.BASES:
        for item_name, icon_path, info_dict, count in base.items:
            unique_items.add(item_name)
    
    return sorted(list(unique_items))

def create_item_pngs(items):
    """Create PNG files for each item using the baseline item.png"""
    source_file = "other/item.png"
    items_dir = "items"
    
    if not os.path.exists(source_file):
        print(f"Error: Source file {source_file} not found!")
        return False
    
    created_files = []
    
    for item_name in items:
        camel_name = to_camel_case(item_name)
        target_file = f"{items_dir}/{camel_name}.png"
        
        try:
            shutil.copy2(source_file, target_file)
            created_files.append((item_name, target_file))
            print(f"Created: {item_name} -> {target_file}")
        except Exception as e:
            print(f"Error creating {target_file}: {e}")
            return False
    
    return created_files

def main():
    print("Extracting unique items from game data...")
    
    # Extract unique item names
    unique_items = extract_unique_items()
    print(f"Found {len(unique_items)} unique items:")
    for item in unique_items:
        print(f"  - {item}")
    
    print(f"\nCreating PNG files...")
    created_files = create_item_pngs(unique_items)
    
    if created_files:
        print(f"\nSuccessfully created {len(created_files)} PNG files:")
        for item_name, file_path in created_files:
            camel_name = to_camel_case(item_name)
            print(f"  {item_name} -> items/{camel_name}.png")
    else:
        print("Failed to create PNG files!")

if __name__ == "__main__":
    main()
