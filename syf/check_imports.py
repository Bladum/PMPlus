#!/usr/bin/env python
"""
XCOM Inventory System - Import Checker

This script checks for any import issues in the codebase to ensure
everything is properly integrated.

Usage:
    python check_imports.py
"""

import os
import importlib.util
import sys
from importlib.abc import Loader

def check_file_import(file_path):
    """Check if a file can be imported without errors"""
    try:
        # Extract module name from file path
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        
        # Create a spec for the module
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        
        # Skip if spec is None (not a Python file, etc.)
        if spec is None or not isinstance(spec.loader, Loader):
            return False, f"Not a valid Python module: {file_path}"
        
        # Create the module
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        
        # Execute the module
        try:
            spec.loader.exec_module(module)
            return True, f"Successfully imported {file_path}"
        except ImportError as e:
            # Print more detailed import error
            import traceback
            tb = traceback.format_exc()
            return False, f"Import error in {file_path}: {str(e)}\n{tb}"
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            return False, f"Error in {file_path}: {str(e)}\n{tb}"
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        return False, f"Error importing {file_path}: {str(e)}\n{tb}"

def find_python_files(directory):
    """Find all Python files in a directory (recursive)"""
    python_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    
    return python_files

def check_barracks_imports():
    """Check imports of the barracks UI and related files"""
    critical_files = [        "engine/gui/base/gui_barracks.py",
        "engine/base/geo/xbase.py",
        "engine/unit/unit.py",
        "engine/unit/unit_type.py", 
        "engine/item/item_weapon.py",
        "engine/item/item_armour.py"
    ]
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    all_success = True
    
    for file in critical_files:
        full_path = os.path.join(base_dir, file)
        
        if not os.path.exists(full_path):
            print(f"✗ File not found: {file}")
            all_success = False
            continue
        
        success, message = check_file_import(full_path)
        
        if success:
            print(f"✓ {file} - OK")
        else:
            print(f"✗ {file} - {message}")
            all_success = False
    
    return all_success

def main():
    """Main function"""
    print("=== XCOM Inventory System Import Checker ===\n")
    
    print("Checking critical files...")
    if check_barracks_imports():
        print("\nAll critical files imported successfully!")
    else:
        print("\nThere were import errors in critical files.")
        print("Please fix these errors before running the tests.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
