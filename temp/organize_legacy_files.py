#!/usr/bin/env python
"""
XCOM Inventory System - Legacy File Organization Script

This script organizes the legacy/deprecated files from the old inventory system
into a 'legacy' folder to keep the workspace clean while preserving the old code
for reference if needed.

Usage:
    python organize_legacy_files.py
"""

import os
import shutil
import sys

# List of files that are now replaced by the new system
LEGACY_FILES = [
    "xcom_inventory_main.py",
    "main_interface.py",
    "inventory_system.py",
    "game_data.py",
    "custom_widgets.py",
    "theme_styles.py",
    "item_path_lookup.py",
    "extract_items.py",
    "update_game_data.py"
]

def main():
    """Main function to organize legacy files"""
    print("XCOM Inventory System - Legacy File Organization")
    print("=" * 50)
    
    # Create legacy directory if it doesn't exist
    legacy_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "legacy")
    if not os.path.exists(legacy_dir):
        os.makedirs(legacy_dir)
        print(f"Created legacy directory: {legacy_dir}")
    
    # Move each legacy file to the legacy directory
    for file_name in LEGACY_FILES:
        source_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
        if os.path.exists(source_path):
            dest_path = os.path.join(legacy_dir, file_name)
            shutil.copy2(source_path, dest_path)
            print(f"Copied {file_name} to legacy directory")
        else:
            print(f"Warning: {file_name} not found, skipping")
    
    print("\nLegacy files have been copied to the 'legacy' directory.")
    print("You can safely delete the original files at the root level if desired.")
    print("To delete the original files, run:")
    print("\npython organize_legacy_files.py --delete\n")
    
    # If --delete flag is provided, delete the original files
    if len(sys.argv) > 1 and sys.argv[1] == "--delete":
        for file_name in LEGACY_FILES:
            source_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
            if os.path.exists(source_path):
                os.remove(source_path)
                print(f"Deleted original file: {file_name}")

if __name__ == "__main__":
    main()
