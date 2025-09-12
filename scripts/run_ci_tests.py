#!/usr/bin/env python3
"""
Simple CI test runner for ArrPy.
Runs basic tests to verify the package works.
"""

import sys
import subprocess

def run_command(cmd, description):
    """Run a command and report results."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {cmd}")
    print('='*60)
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    
    if result.returncode != 0:
        print(f"❌ FAILED: {description}")
        if result.stderr:
            print(f"Error: {result.stderr}")
        return False
    else:
        print(f"✅ PASSED: {description}")
        return True

def main():
    """Run CI tests."""
    all_passed = True
    
    # Test 1: Import test
    all_passed &= run_command(
        "python -c \"import arrpy; print(f'ArrPy imported successfully')\"",
        "Import Test"
    )
    
    # Test 2: Basic array operations
    all_passed &= run_command(
        """python -c "import arrpy; a = arrpy.array([1,2,3]); b = arrpy.array([4,5,6]); c = a + b; print(f'Addition works: {c._data}')" """,
        "Basic Operations Test"
    )
    
    # Test 3: Backend switching
    all_passed &= run_command(
        """python -c "import arrpy; arrpy.set_backend('python'); a = arrpy.ones(5); print(f'Python backend: {a.sum()}'); arrpy.set_backend('cython'); b = arrpy.ones(5); print(f'Cython backend: {b.sum()}')" """,
        "Backend Switching Test"
    )
    
    # Test 4: Run pytest on core tests (not experimental)
    all_passed &= run_command(
        "python -m pytest tests/ --ignore=tests/experimental --ignore=tests/experimental_archive -q --tb=no",
        "Core Test Suite"
    )
    
    # Test 5: Feature matrix generation
    all_passed &= run_command(
        "python scripts/check_features.py --backend python --json > /dev/null && echo 'Feature matrix works'",
        "Feature Matrix Test"
    )
    
    # Report final status
    print("\n" + "="*60)
    if all_passed:
        print("✅ ALL CI TESTS PASSED")
        return 0
    else:
        print("❌ SOME CI TESTS FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())