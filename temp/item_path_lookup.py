#!/usr/bin/env python3
"""
Helper script to find canonical item paths from game_data.py
"""

from game_data import GameData

def build_item_path_lookup():
    """Build a lookup dictionary mapping item names to their canonical paths"""
    item_paths = {}
    
    # Process each base's items
    for base in GameData.BASES:
        for item_name, icon_path, properties, count in base.items:
            if item_name not in item_paths:
                item_paths[item_name] = icon_path
    
    return item_paths

if __name__ == "__main__":
    # Test the lookup
    paths = build_item_path_lookup()
    print(f"Found {len(paths)} items with canonical paths:")
    for name, path in sorted(paths.items()):
        print(f"{name}: {path}")
        
# Create a function to get a canonical path for an item
def get_canonical_path(item_name):
    """
    Get the canonical path for an item based on its name.
    Returns the path from game_data if found, otherwise returns a default.
    """
    paths = build_item_path_lookup()
    return paths.get(item_name, 'items/item.png')  # Default if not found
