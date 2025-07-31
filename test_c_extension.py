#!/usr/bin/env python
"""
Test script to verify C extension functionality and performance.
"""

import time
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test with pure Python first
os.environ['ARRPY_FORCE_PYTHON'] = '1'
os.environ['ARRPY_WARN_NO_C_EXT'] = '0'  # Suppress warning
import arrpy as arrpy_python

# Clear the module to reload with C extensions
del sys.modules['arrpy']
del sys.modules['arrpy.core']
del sys.modules['arrpy.core.hybrid_array']
del os.environ['ARRPY_FORCE_PYTHON']

# Try to import with C extensions
import arrpy as arrpy_c

print("=" * 60)
print("ArrPy C Extension Test")
print("=" * 60)

# Check if C extensions are available
print(f"\nC Extensions Available: {arrpy_c.core.HAS_C_EXTENSION}")

if not arrpy_c.core.HAS_C_EXTENSION:
    print("\n⚠️  C extensions not built. To build them, run:")
    print("   ./build_c_ext.sh")
    print("\nContinuing with pure Python implementation only...")
else:
    print("✓ C extensions loaded successfully!")

print("\n" + "-" * 60)
print("Basic Functionality Test")
print("-" * 60)

# Test array creation
print("\n1. Array Creation:")
arr = arrpy_c.Array([1, 2, 3, 4, 5])
print(f"   Created array: {arr}")
print(f"   Shape: {arr.shape}")
print(f"   Size: {arr.size}")

# Test indexing
print("\n2. Indexing:")
print(f"   arr[0] = {arr[0]}")
print(f"   arr[2] = {arr[2]}")
arr[1] = 10
print(f"   After arr[1] = 10: {arr}")

# Test arithmetic
print("\n3. Arithmetic Operations:")
arr2 = arrpy_c.Array([5, 4, 3, 2, 1])
print(f"   arr + 10 = {arr + 10}")
print(f"   arr + arr2 = {arr + arr2}")

# Test aggregations
print("\n4. Aggregations:")
print(f"   Sum: {arr.sum()}")
print(f"   Mean: {arr.mean()}")

if arrpy_c.core.HAS_C_EXTENSION:
    print("\n" + "-" * 60)
    print("Performance Comparison")
    print("-" * 60)
    
    sizes = [100, 1000, 10000]
    
    for size in sizes:
        print(f"\nArray size: {size}")
        
        # Test array creation
        start = time.perf_counter()
        for _ in range(100):
            py_arr = arrpy_python.zeros(size)
        py_time = time.perf_counter() - start
        
        start = time.perf_counter()
        for _ in range(100):
            c_arr = arrpy_c.zeros(size)
        c_time = time.perf_counter() - start
        
        speedup = py_time / c_time if c_time > 0 else 0
        print(f"   zeros() speedup: {speedup:.2f}x")
        
        # Test addition
        arr1 = arrpy_python.Array(list(range(size)))
        arr2 = arrpy_c.Array(list(range(size)))
        
        start = time.perf_counter()
        for _ in range(100):
            result = arr1 + 5
        py_time = time.perf_counter() - start
        
        start = time.perf_counter()
        for _ in range(100):
            result = arr2 + 5
        c_time = time.perf_counter() - start
        
        speedup = py_time / c_time if c_time > 0 else 0
        print(f"   Addition speedup: {speedup:.2f}x")
        
        # Test sum
        start = time.perf_counter()
        for _ in range(100):
            s = arr1.sum()
        py_time = time.perf_counter() - start
        
        start = time.perf_counter()
        for _ in range(100):
            s = arr2.sum()
        c_time = time.perf_counter() - start
        
        speedup = py_time / c_time if c_time > 0 else 0
        print(f"   Sum speedup: {speedup:.2f}x")

print("\n" + "=" * 60)
print("Test completed!")
print("=" * 60)