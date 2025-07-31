#!/usr/bin/env python3
"""
Performance benchmark comparing Python vs Cython implementation.
"""

import time
import sys
import os

# Force import of Python version for comparison
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'arrpy', 'core'))
from array import Array as PythonArray

# Import the mixed version (will use Cython if available)
from arrpy.core import Array as OptimizedArray
from arrpy.creation import zeros
from arrpy.math import power

def time_function(func, *args, **kwargs):
    """Time a function execution."""
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    return result, end - start

def benchmark_array_creation(size=1000):
    """Benchmark array creation."""
    print(f"\n=== Array Creation Benchmark (size={size}) ===")
    
    # Python version
    data = [[i + j for j in range(size // 10)] for i in range(10)]
    _, py_time = time_function(lambda: PythonArray(data))
    
    # Optimized version
    _, opt_time = time_function(lambda: OptimizedArray(data))
    
    print(f"Python version:    {py_time:.6f}s")
    print(f"Optimized version: {opt_time:.6f}s")
    print(f"Speedup: {py_time / opt_time:.2f}x" if opt_time > 0 else "N/A")

def benchmark_arithmetic_operations(size=1000):
    """Benchmark arithmetic operations."""
    print(f"\n=== Arithmetic Operations Benchmark (size={size}) ===")
    
    # Create test arrays
    data1 = [[i + j for j in range(size // 10)] for i in range(10)]
    data2 = [[2 for j in range(size // 10)] for i in range(10)]
    
    py_arr1 = PythonArray(data1)
    py_arr2 = PythonArray(data2)
    opt_arr1 = OptimizedArray(data1)
    opt_arr2 = OptimizedArray(data2)
    
    # Addition
    _, py_add_time = time_function(lambda: py_arr1 + py_arr2)
    _, opt_add_time = time_function(lambda: opt_arr1 + opt_arr2)
    
    print(f"Addition:")
    print(f"  Python:    {py_add_time:.6f}s")
    print(f"  Optimized: {opt_add_time:.6f}s")
    print(f"  Speedup:   {py_add_time / opt_add_time:.2f}x" if opt_add_time > 0 else "  N/A")
    
    # Multiplication
    _, py_mul_time = time_function(lambda: py_arr1 * py_arr2)
    _, opt_mul_time = time_function(lambda: opt_arr1 * opt_arr2)
    
    print(f"Multiplication:")
    print(f"  Python:    {py_mul_time:.6f}s")
    print(f"  Optimized: {opt_mul_time:.6f}s")
    print(f"  Speedup:   {py_mul_time / opt_mul_time:.2f}x" if opt_mul_time > 0 else "  N/A")

def benchmark_aggregation_functions(size=5000):
    """Benchmark aggregation functions."""
    print(f"\n=== Aggregation Functions Benchmark (size={size}) ===")
    
    # Create large test array
    data = [[i + j for j in range(size // 50)] for i in range(50)]
    
    py_arr = PythonArray(data)
    opt_arr = OptimizedArray(data)
    
    # Sum operation
    _, py_sum_time = time_function(lambda: py_arr.sum())
    
    # Try Cython fast sum if available
    if hasattr(opt_arr, 'sum_fast'):
        _, opt_sum_time = time_function(lambda: opt_arr.sum_fast())
        method = "sum_fast"
    else:
        _, opt_sum_time = time_function(lambda: opt_arr.sum())
        method = "sum"
    
    print(f"Sum ({method}):")
    print(f"  Python:    {py_sum_time:.6f}s")
    print(f"  Optimized: {opt_sum_time:.6f}s")
    print(f"  Speedup:   {py_sum_time / opt_sum_time:.2f}x" if opt_sum_time > 0 else "  N/A")
    
    # Mean operation
    _, py_mean_time = time_function(lambda: py_arr.mean())
    
    if hasattr(opt_arr, 'mean_fast'):
        _, opt_mean_time = time_function(lambda: opt_arr.mean_fast())
        method = "mean_fast"
    else:
        _, opt_mean_time = time_function(lambda: opt_arr.mean())
        method = "mean"
    
    print(f"Mean ({method}):")
    print(f"  Python:    {py_mean_time:.6f}s")
    print(f"  Optimized: {opt_mean_time:.6f}s")
    print(f"  Speedup:   {py_mean_time / opt_mean_time:.2f}x" if opt_mean_time > 0 else "  N/A")

def benchmark_mathematical_functions(size=1000):
    """Benchmark mathematical functions."""
    print(f"\n=== Mathematical Functions Benchmark (size={size}) ===")
    
    # Create test array
    data = [[float(i + j + 1) for j in range(size // 10)] for i in range(10)]
    
    py_arr = PythonArray(data)
    opt_arr = OptimizedArray(data)
    
    # Square root
    _, py_sqrt_time = time_function(lambda: py_arr.sqrt())
    
    # Check if Cython fast sqrt is available
    if hasattr(opt_arr, 'sqrt_fast'):
        _, opt_sqrt_time = time_function(lambda: opt_arr.sqrt_fast())
        method = "sqrt_fast"
    else:
        _, opt_sqrt_time = time_function(lambda: opt_arr.sqrt())
        method = "sqrt"
    
    print(f"Square root ({method}):")
    print(f"  Python:    {py_sqrt_time:.6f}s")
    print(f"  Optimized: {opt_sqrt_time:.6f}s")
    print(f"  Speedup:   {py_sqrt_time / opt_sqrt_time:.2f}x" if opt_sqrt_time > 0 else "  N/A")

def detect_implementation():
    """Detect which implementation is being used."""
    print("=== Implementation Detection ===")
    
    # Create a test array
    arr = OptimizedArray([[1, 2, 3]])
    
    print(f"Array type: {type(arr)}")
    print(f"Module: {type(arr).__module__}")
    
    # Check for Cython-specific methods
    cython_methods = ['sum_fast', 'mean_fast', 'sqrt_fast', 'sin_fast', 'cos_fast']
    cython_features = [method for method in cython_methods if hasattr(arr, method)]
    
    if cython_features:
        print(f"Cython features detected: {', '.join(cython_features)}")
        print("✓ Using Cython-optimized implementation")
    else:
        print("⚠ Using pure Python implementation")
    
    return len(cython_features) > 0

def main():
    """Run all benchmarks."""
    print("ArrPy Performance Benchmark: Python vs Cython")
    print("=" * 50)
    
    is_cython = detect_implementation()
    
    if is_cython:
        print("\nRunning performance comparison...")
        benchmark_array_creation(1000)
        benchmark_arithmetic_operations(1000)
        benchmark_aggregation_functions(5000)
        benchmark_mathematical_functions(1000)
        
        print("\n" + "=" * 50)
        print("Benchmark completed!")
        print("Note: Speedup measurements show Cython vs Python performance.")
    else:
        print("\nCython implementation not available.")
        print("Run 'python setup.py build_ext --inplace' to build Cython extensions.")

if __name__ == "__main__":
    main()