#!/usr/bin/env python3
"""Check which ArrPy backends are available."""

import sys
sys.path.insert(0, '.')

# ANSI color codes
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[0;33m'
RESET = '\033[0m'

def check_backends():
    """Check availability of each backend."""
    import arrpy
    
    # Python backend (always available)
    print(f"{GREEN}✓ Python backend: Available{RESET}")
    
    # Cython backend
    try:
        arrpy.set_backend('cython')
        # Test if it actually works
        a = arrpy.ones(10)
        b = a + a
        print(f"{GREEN}✓ Cython backend: Available{RESET}")
    except Exception:
        print(f"{RED}✗ Cython backend: Not built{RESET}")
        print(f"  {YELLOW}→ Build with: make build-cython{RESET}")
    
    # C++ backend
    try:
        arrpy.set_backend('c')
        # Test if it actually works
        a = arrpy.ones(10)
        b = a + a
        print(f"{GREEN}✓ C++ backend: Available{RESET}")
    except Exception:
        print(f"{RED}✗ C++ backend: Not built{RESET}")
        print(f"  {YELLOW}→ Build with: make build-cpp{RESET}")
    
    # Reset to Python backend
    arrpy.set_backend('python')

if __name__ == "__main__":
    check_backends()