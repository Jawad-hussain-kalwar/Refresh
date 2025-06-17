# tools/scope/tree.py

"""
This tool is used to generate a tree of the source codebase. 

args:
    - path: str
        description: The path to the source codebase.
    - exclude_dirs: list[str]
    - exclude_files: list[str]
    - exclude_extensions: list[str]
    - prefix: str
        description: The prefix to the tree.
returns:
    - tree: str
        description: The tree of the source codebase.
"""

import os
import sys

def generate_tree(directory, exclude_dirs=None, exclude_files=None, prefix=""):
    if exclude_dirs is None:
        exclude_dirs = []
    if exclude_files is None:
        exclude_files = []
    
    # List all items in the directory
    items = os.listdir(directory)
    items = [item for item in items if item not in exclude_dirs and item not in exclude_files]
    
    # Sort directories first, then files
    items.sort(key=lambda x: (not os.path.isdir(os.path.join(directory, x)), x))
    
    for i, item in enumerate(items):
        path = os.path.join(directory, item)
        is_last = i == len(items) - 1
        
        # Print the current item
        if is_last:
            print(f"{prefix}└── {item}")
            new_prefix = prefix + "    "
        else:
            print(f"{prefix}├── {item}")
            new_prefix = prefix + "│   "
        
        # Recursively print subdirectories
        if os.path.isdir(path) and item not in exclude_dirs:
            generate_tree(path, exclude_dirs, exclude_files, new_prefix)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tree.py <directory_path>")
        sys.exit(1)
    
    target_dir = sys.argv[1]
    
    # Customize exclusions here (e.g., [".venv", ".git", "__pycache__", "*.txt"])
    exclude_dirs = [".venv", ".git", "__pycache__", "cache", "Library", "Logs", "Temp", ".next", "node_modules"]
    exclude_files = [".DS_Store", "*.txt"]
    
    print(target_dir)
    generate_tree(target_dir, exclude_dirs, exclude_files)





