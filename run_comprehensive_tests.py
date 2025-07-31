#!/usr/bin/env python3
"""
Comprehensive test runner for ArrPy Cython implementation.

This script runs all test suites and provides a summary of the testing coverage
for the Cython-optimized ArrPy library.
"""

import subprocess
import sys
import time
from pathlib import Path


def run_command(cmd, description):
    """Run a command and return success status and output."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print('='*60)
    
    start_time = time.time()
    
    try:
        result = subprocess.run(cmd, 
                              capture_output=True, 
                              text=True, 
                              timeout=120)
        
        duration = time.time() - start_time
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        success = result.returncode == 0
        print(f"\n{'✅ PASSED' if success else '❌ FAILED'} in {duration:.2f}s")
        
        return success, result.stdout, result.stderr
    
    except subprocess.TimeoutExpired:
        print("❌ TIMEOUT after 120 seconds")
        return False, "", "Timeout"
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False, "", str(e)


def main():
    """Run comprehensive test suite."""
    print("ArrPy Cython Implementation - Comprehensive Test Suite")
    print("=" * 60)
    
    # Change to project directory
    project_dir = Path(__file__).parent
    import os
    os.chdir(project_dir)
    
    # Test categories with their descriptions
    test_suites = [
        # Core functionality tests
        (
            ["python", "-m", "pytest", "tests/test_array.py", "-q", "--tb=line"],
            "Core Array Functionality Tests (All existing tests)"
        ),
        
        # Cython-specific tests
        (
            ["python", "-m", "pytest", "tests/test_cython_implementation.py", "-v"],
            "Cython Implementation Tests"
        ),
        
        # Build system tests
        (
            ["python", "-m", "pytest", "tests/test_build_system.py", "-q"],
            "Build System Tests"
        ),
        
        # Performance tests (non-slow)
        (
            ["python", "-m", "pytest", "tests/test_performance_regression.py", 
             "-m", "not slow", "-q"],
            "Performance Regression Tests (Fast)"
        ),
        
        # Cython feature verification
        (
            ["python", "-c", """
from arrpy.core import Array
arr = Array([1, 2, 3, 4, 5])
print(f'Array type: {type(arr)}')
print(f'Module: {type(arr).__module__}')
print(f'Sum: {arr.sum()}')
if hasattr(arr, 'sum_fast'):
    print(f'Fast sum: {arr.sum_fast()}')
    print('✅ Cython fast methods available')
else:
    print('⚠ Using Python fallback')
            """],
            "Cython Feature Verification"
        ),
        
        # Import verification
        (
            ["python", "-c", """
try:
    from arrpy.core import Array
    from arrpy.creation import zeros, ones, full, eye
    from arrpy.math import power, absolute
    from arrpy.manipulation.joining import concatenate
    print('✅ All imports successful')
    
    # Quick functionality test
    arr = Array([[1, 2], [3, 4]])
    z = zeros((2, 2))
    result = arr + z
    print(f'✅ Basic operations working: {result._data}')
    
except Exception as e:
    print(f'❌ Import error: {e}')
    exit(1)
            """],
            "Import and Basic Functionality Test"
        ),
        
        # Build verification
        (
            ["python", "setup.py", "build_ext", "--inplace", "--quiet"],
            "Cython Extension Build Test"
        ),
    ]
    
    # Run all test suites
    results = []
    total_start = time.time()
    
    for cmd, description in test_suites:
        success, stdout, stderr = run_command(cmd, description)
        results.append((description, success, stdout, stderr))
    
    total_duration = time.time() - total_start
    
    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for _, success, _, _ in results if success)
    total = len(results)
    
    for description, success, stdout, stderr in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status:<10} {description}")
    
    print(f"\nOverall: {passed}/{total} test suites passed")
    print(f"Total time: {total_duration:.2f} seconds")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! ArrPy Cython implementation is working correctly.")
        
        # Show performance comparison if available
        print("\n" + "="*60)
        print("PERFORMANCE VERIFICATION")
        print("="*60)
        
        try:
            result = subprocess.run([
                "python", "benchmark_cython.py"
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                # Extract key performance metrics
                for line in lines:
                    if 'Speedup:' in line or 'Using Cython' in line or 'Array type:' in line:
                        print(line)
            else:
                print("⚠ Performance benchmark encountered issues")
                
        except Exception as e:
            print(f"⚠ Could not run performance benchmark: {e}")
    
    else:
        print(f"\n⚠ {total - passed} test suite(s) failed. Check output above for details.")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)