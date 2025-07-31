#!/usr/bin/env python
"""
Script to update tests for hybrid array compatibility.
"""

import os
import re
import sys

def update_test_file(filepath):
    """Update a test file to be compatible with hybrid arrays."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    updated = False
    
    # Check if file imports Array
    if 'from arrpy import Array' in content or 'import arrpy' in content:
        # Add test_imports import if not already present
        if 'from test_imports import is_array' not in content:
            # Find the last import line
            import_lines = []
            lines = content.split('\n')
            last_import_idx = 0
            
            for i, line in enumerate(lines):
                if line.strip().startswith('import ') or line.strip().startswith('from '):
                    last_import_idx = i
            
            # Add the import after the last import
            if 'from arrpy import Array' in content:
                new_import = '\n# Import helper for type checking that works with hybrid arrays\ntry:\n    from test_imports import is_array\nexcept ImportError:\n    def is_array(obj):\n        return isinstance(obj, Array)\n'
                lines.insert(last_import_idx + 1, new_import)
                content = '\n'.join(lines)
                updated = True
        
        # Replace isinstance(x, Array) with is_array(x)
        pattern = r'isinstance\s*\(\s*([^,]+)\s*,\s*Array\s*\)'
        if re.search(pattern, content):
            content = re.sub(pattern, r'is_array(\1)', content)
            updated = True
    
    if updated:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"✓ Updated: {filepath}")
        return True
    return False

def main():
    """Update all test files."""
    test_dirs = ['tests/', 'tests/core/', 'tests/math/', 'tests/creation/', 
                 'tests/edge_cases/', 'tests/integration/', 'tests/performance/']
    
    total_updated = 0
    
    for test_dir in test_dirs:
        if not os.path.exists(test_dir):
            continue
            
        for filename in os.listdir(test_dir):
            if filename.endswith('.py') and filename.startswith('test_'):
                filepath = os.path.join(test_dir, filename)
                if update_test_file(filepath):
                    total_updated += 1
    
    print(f"\n✓ Updated {total_updated} test files for hybrid array compatibility")

if __name__ == '__main__':
    main()