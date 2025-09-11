#!/usr/bin/env python3
"""
Benchmark SIMD operations in C++ backend.
"""

import time
import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import arrpy
from arrpy import Backend, set_backend

def benchmark_reductions():
    """Benchmark SIMD reduction operations."""
    print("=" * 60)
    print("SIMD Reduction Operations Benchmark")
    print("=" * 60)
    
    try:
        from arrpy.backends.c import reduction_ops_cpp
        print(f"\nSIMD Type: {reduction_ops_cpp.simd_type}")
    except ImportError:
        print("\nC++ reduction operations not available")
        return
    
    sizes = [1000, 10000, 100000, 1000000]
    
    print("\nComparing Python vs C++ SIMD reductions:")
    print("-" * 60)
    print(f"{'Size':<10} {'Operation':<15} {'Python (ms)':<15} {'C++ SIMD (ms)':<15} {'Speedup':<10}")
    print("-" * 60)
    
    for size in sizes:
        data = list(np.random.randn(size))
        
        # Test sum
        set_backend('python')
        a = arrpy.array(data)
        start = time.perf_counter()
        for _ in range(100):
            result_py = a.sum()
        py_time = (time.perf_counter() - start) * 10  # ms per operation
        
        # C++ SIMD sum
        start = time.perf_counter()
        for _ in range(100):
            result_cpp = reduction_ops_cpp.sum(data)
        cpp_time = (time.perf_counter() - start) * 10
        
        speedup = py_time / cpp_time if cpp_time > 0 else 0
        print(f"{size:<10} {'sum':<15} {py_time:<15.3f} {cpp_time:<15.3f} {speedup:<10.2f}x")
        
        # Test min
        start = time.perf_counter()
        for _ in range(100):
            result_py = a.min()
        py_time = (time.perf_counter() - start) * 10
        
        start = time.perf_counter()
        for _ in range(100):
            result_cpp = reduction_ops_cpp.min(data)
        cpp_time = (time.perf_counter() - start) * 10
        
        speedup = py_time / cpp_time if cpp_time > 0 else 0
        print(f"{'':<10} {'min':<15} {py_time:<15.3f} {cpp_time:<15.3f} {speedup:<10.2f}x")
        
        # Test max
        start = time.perf_counter()
        for _ in range(100):
            result_py = a.max()
        py_time = (time.perf_counter() - start) * 10
        
        start = time.perf_counter()
        for _ in range(100):
            result_cpp = reduction_ops_cpp.max(data)
        cpp_time = (time.perf_counter() - start) * 10
        
        speedup = py_time / cpp_time if cpp_time > 0 else 0
        print(f"{'':<10} {'max':<15} {py_time:<15.3f} {cpp_time:<15.3f} {speedup:<10.2f}x")
        
        if size < 1000000:  # Separator between sizes
            print()

def benchmark_ufuncs():
    """Benchmark SIMD ufunc operations."""
    print("\n" + "=" * 60)
    print("SIMD Universal Functions Benchmark")
    print("=" * 60)
    
    try:
        from arrpy.backends.c import ufuncs_ops_cpp
        print(f"\nSIMD Type: {ufuncs_ops_cpp.simd_type}")
        print(f"Has native sqrt: {ufuncs_ops_cpp.has_native_sqrt}")
    except ImportError:
        print("\nC++ ufunc operations not available")
        return
    
    sizes = [1000, 10000, 100000]
    
    print("\nComparing Cython vs C++ SIMD ufuncs:")
    print("-" * 60)
    print(f"{'Size':<10} {'Operation':<15} {'Cython (ms)':<15} {'C++ SIMD (ms)':<15} {'Speedup':<10}")
    print("-" * 60)
    
    for size in sizes:
        # Use values in reasonable range for trig functions
        data = [float(x) for x in np.random.randn(size)]
        shape = (size, 1)  # Need 2D shape for C++ functions
        
        # Test sqrt
        positive_data = [float(x) for x in np.abs(np.random.randn(size))]
        
        set_backend('cython')
        a = arrpy.array(positive_data)
        start = time.perf_counter()
        for _ in range(100):
            result_cy = arrpy.sqrt(a)
        cy_time = (time.perf_counter() - start) * 10
        
        start = time.perf_counter()
        for _ in range(100):
            result_cpp, _ = ufuncs_ops_cpp.sqrt(positive_data, shape)
        cpp_time = (time.perf_counter() - start) * 10
        
        speedup = cy_time / cpp_time if cpp_time > 0 else 0
        print(f"{size:<10} {'sqrt':<15} {cy_time:<15.3f} {cpp_time:<15.3f} {speedup:<10.2f}x")
        
        # Test sin
        a = arrpy.array(data)
        start = time.perf_counter()
        for _ in range(100):
            result_cy = arrpy.sin(a)
        cy_time = (time.perf_counter() - start) * 10
        
        start = time.perf_counter()
        for _ in range(100):
            result_cpp, _ = ufuncs_ops_cpp.sin(data, shape)
        cpp_time = (time.perf_counter() - start) * 10
        
        speedup = cy_time / cpp_time if cpp_time > 0 else 0
        print(f"{'':<10} {'sin':<15} {cy_time:<15.3f} {cpp_time:<15.3f} {speedup:<10.2f}x")
        
        # Test exp
        small_data = [x * 0.1 for x in data]  # Scale down to avoid overflow
        a = arrpy.array(small_data)
        start = time.perf_counter()
        for _ in range(100):
            result_cy = arrpy.exp(a)
        cy_time = (time.perf_counter() - start) * 10
        
        start = time.perf_counter()
        for _ in range(100):
            result_cpp, _ = ufuncs_ops_cpp.exp(small_data, shape)
        cpp_time = (time.perf_counter() - start) * 10
        
        speedup = cy_time / cpp_time if cpp_time > 0 else 0
        print(f"{'':<10} {'exp':<15} {cy_time:<15.3f} {cpp_time:<15.3f} {speedup:<10.2f}x")
        
        if size < 100000:
            print()

def benchmark_simd_arithmetic():
    """Benchmark basic SIMD arithmetic operations."""
    print("\n" + "=" * 60)
    print("SIMD Arithmetic Operations Benchmark")
    print("=" * 60)
    
    try:
        from arrpy.backends.c import array_ops_cpp
        print(f"\nSIMD Type: {array_ops_cpp.simd_type}")
        print(f"Platform: {array_ops_cpp.platform}")
    except ImportError:
        print("\nC++ array operations not available")
        return
    
    sizes = [1000, 10000, 100000, 1000000]
    
    print("\nArithmetic operations performance:")
    print("-" * 60)
    print(f"{'Size':<10} {'Operation':<15} {'Time (ms)':<15} {'Throughput (M/s)':<20}")
    print("-" * 60)
    
    for size in sizes:
        data1 = list(range(size))
        data2 = list(range(size, size * 2))
        shape = (size, 1)
        
        # Test addition
        iterations = 1000 if size <= 10000 else 100 if size <= 100000 else 10
        start = time.perf_counter()
        for _ in range(iterations):
            result, _ = array_ops_cpp.add(data1, data2, shape, shape)
        elapsed = time.perf_counter() - start
        
        time_ms = (elapsed / iterations) * 1000
        throughput = (size * iterations) / elapsed / 1e6
        
        print(f"{size:<10} {'add':<15} {time_ms:<15.3f} {throughput:<20.1f}")
        
        # Test multiplication
        start = time.perf_counter()
        for _ in range(iterations):
            result, _ = array_ops_cpp.multiply(data1, data2, shape, shape)
        elapsed = time.perf_counter() - start
        
        time_ms = (elapsed / iterations) * 1000
        throughput = (size * iterations) / elapsed / 1e6
        
        print(f"{'':<10} {'multiply':<15} {time_ms:<15.3f} {throughput:<20.1f}")
        
        if size < 1000000:
            print()

def main():
    print("=" * 60)
    print("ArrPy SIMD Operations Benchmark")
    print("=" * 60)
    
    benchmark_reductions()
    benchmark_ufuncs()
    benchmark_simd_arithmetic()
    
    print("\n" + "=" * 60)
    print("Benchmark Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()