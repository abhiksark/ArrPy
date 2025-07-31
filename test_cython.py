#!/usr/bin/env python3
"""
Quick test script to verify Cython implementation works correctly.
"""

from arrpy.core import Array
from arrpy.creation import zeros, ones
from arrpy.math import power, absolute

def test_cython_array():
    """Test basic Array functionality with Cython."""
    print("Testing Cython Array implementation...")
    
    # Test array creation
    arr = Array([[1, 2, 3], [4, 5, 6]])
    print(f"Created array: {arr}")
    print(f"Shape: {arr.shape}")
    print(f"Size: {arr.size}")
    
    # Test indexing
    print(f"Element at [0, 1]: {arr[0, 1]}")
    print(f"First row: {arr[0]}")
    
    # Test arithmetic
    arr2 = Array([[2, 2, 2], [2, 2, 2]])
    result = arr + arr2
    print(f"Addition result: {result}")
    
    # Test fast methods if available (Cython-specific)
    if hasattr(arr, 'sum_fast'):
        print(f"Fast sum: {arr.sum_fast()}")
        print(f"Fast mean: {arr.mean_fast()}")
    else:
        print(f"Regular sum: {arr.sum()}")
        print(f"Regular mean: {arr.mean()}")

def test_cython_creation():
    """Test creation functions with Cython."""
    print("\nTesting Cython creation functions...")
    
    # Test zeros
    z = zeros((2, 3))
    print(f"Zeros: {z}")
    
    # Test ones
    o = ones(3)
    print(f"Ones: {o}")

def test_cython_math():
    """Test math functions with Cython."""
    print("\nTesting Cython math functions...")
    
    arr = Array([1, 4, 9, 16])
    
    # Test power
    squared = power(arr, 2)
    print(f"Squared: {squared}")
    
    # Test absolute
    neg_arr = Array([-1, -2, 3, -4])
    abs_result = absolute(neg_arr)
    print(f"Absolute: {abs_result}")

def benchmark_comparison():
    """Simple benchmark comparing operations."""
    import time
    
    print("\nSimple performance comparison...")
    
    # Create a larger array
    size = 1000
    data = [[i + j for j in range(size)] for i in range(10)]
    arr = Array(data)
    
    # Test sum performance
    start = time.time()
    if hasattr(arr, 'sum_fast'):
        result = arr.sum_fast()
        method = "Cython fast"
    else:
        result = arr.sum()
        method = "Python"
    end = time.time()
    
    print(f"Sum using {method}: {result} (Time: {end - start:.6f}s)")

if __name__ == "__main__":
    test_cython_array()
    test_cython_creation()
    test_cython_math()
    benchmark_comparison()
    print("\nAll tests completed successfully!")