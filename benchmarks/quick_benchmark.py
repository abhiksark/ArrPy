#!/usr/bin/env python3
"""
Quick benchmark suite for ArrPy v1.0.0
Tests key operations across available backends
"""

import time
import sys
import numpy as np
sys.path.insert(0, '.')

import arrpy
from arrpy import Backend, set_backend

def time_operation(func, *args, iterations=10):
    """Time an operation over multiple iterations."""
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        result = func(*args)
        end = time.perf_counter()
        times.append(end - start)
    return min(times) * 1000  # Return best time in ms

def benchmark_backend(backend_name):
    """Run benchmarks for a specific backend."""
    try:
        set_backend(backend_name)
    except:
        return None
    
    results = {}
    
    # Test sizes
    small_size = 1000
    medium_size = 10000
    large_size = 100000
    matrix_size = 100
    
    # 1. Array creation
    start = time.perf_counter()
    a = arrpy.zeros((medium_size,))
    results['zeros'] = (time.perf_counter() - start) * 1000
    
    # 2. Element-wise addition
    try:
        a = arrpy.array([float(i) for i in range(medium_size)])
        b = arrpy.array([float(i) for i in range(medium_size)])
        results['add'] = time_operation(lambda: a + b, iterations=10)
        
        # 3. Element-wise multiplication
        results['multiply'] = time_operation(lambda: a * b, iterations=10)
    except NotImplementedError:
        pass  # Skip if not implemented
    
    # 4. Sum reduction
    try:
        a = arrpy.array([float(i) for i in range(large_size)])
        results['sum'] = time_operation(lambda: a.sum(), iterations=10)
    except NotImplementedError:
        pass  # Skip if not implemented
    
    # 5. Matrix multiplication
    try:
        mat_a = arrpy.array([[float(i+j) for j in range(matrix_size)] for i in range(matrix_size)])
        mat_b = arrpy.array([[float(i-j) for j in range(matrix_size)] for i in range(matrix_size)])
        results['matmul'] = time_operation(lambda: arrpy.matmul(mat_a, mat_b), iterations=5)
    except NotImplementedError:
        pass  # Skip if not implemented
    
    # 6. Trigonometric functions
    try:
        angles = arrpy.array([float(i) * 0.01 for i in range(small_size)])
        results['sin'] = time_operation(lambda: arrpy.sin(angles), iterations=10)
    except NotImplementedError:
        pass  # Skip if not implemented
    
    # 7. Square root
    try:
        nums = arrpy.array([float(i) for i in range(1, small_size + 1)])
        results['sqrt'] = time_operation(lambda: arrpy.sqrt(nums), iterations=10)
    except NotImplementedError:
        pass  # Skip if not implemented
    
    return results

def benchmark_numpy_reference():
    """Run the same benchmarks with NumPy for comparison."""
    results = {}
    
    small_size = 1000
    medium_size = 10000
    large_size = 100000
    matrix_size = 100
    
    # 1. Array creation
    start = time.perf_counter()
    a = np.zeros(medium_size)
    results['zeros'] = (time.perf_counter() - start) * 1000
    
    # 2. Element-wise addition
    a = np.arange(medium_size, dtype=np.float64)
    b = np.arange(medium_size, dtype=np.float64)
    results['add'] = time_operation(lambda: a + b, iterations=10)
    
    # 3. Element-wise multiplication
    results['multiply'] = time_operation(lambda: a * b, iterations=10)
    
    # 4. Sum reduction
    a = np.arange(large_size, dtype=np.float64)
    results['sum'] = time_operation(lambda: a.sum(), iterations=10)
    
    # 5. Matrix multiplication
    mat_a = np.random.randn(matrix_size, matrix_size)
    mat_b = np.random.randn(matrix_size, matrix_size)
    results['matmul'] = time_operation(lambda: np.matmul(mat_a, mat_b), iterations=5)
    
    # 6. Trigonometric functions
    angles = np.arange(small_size, dtype=np.float64) * 0.01
    results['sin'] = time_operation(lambda: np.sin(angles), iterations=10)
    
    # 7. Square root
    nums = np.arange(1, small_size + 1, dtype=np.float64)
    results['sqrt'] = time_operation(lambda: np.sqrt(nums), iterations=10)
    
    return results

def print_results(results_dict):
    """Pretty print benchmark results."""
    print("\n" + "="*80)
    print("ArrPy v1.0.0 Benchmark Results")
    print("="*80)
    
    # Collect all operations
    all_ops = set()
    for backend_results in results_dict.values():
        if backend_results:
            all_ops.update(backend_results.keys())
    all_ops = sorted(all_ops)
    
    # Print header
    backends = list(results_dict.keys())
    header = "Operation".ljust(15) + "".join(b.ljust(15) for b in backends)
    print("\n" + header)
    print("-" * len(header))
    
    # Print results for each operation
    for op in all_ops:
        row = op.ljust(15)
        for backend in backends:
            if results_dict[backend] and op in results_dict[backend]:
                time_ms = results_dict[backend][op]
                row += f"{time_ms:.3f} ms".ljust(15)
            else:
                row += "N/A".ljust(15)
        print(row)
    
    # Calculate speedups
    if 'Python' in results_dict and results_dict['Python']:
        print("\n" + "="*80)
        print("Speedup vs Python Backend")
        print("-"*80)
        
        python_results = results_dict['Python']
        for backend in backends:
            if backend != 'Python' and results_dict[backend]:
                print(f"\n{backend} Speedups:")
                for op in all_ops:
                    if op in python_results and op in results_dict[backend]:
                        speedup = python_results[op] / results_dict[backend][op]
                        print(f"  {op}: {speedup:.2f}x")
    
    # Compare with NumPy
    if 'NumPy' in results_dict and results_dict['NumPy']:
        print("\n" + "="*80)
        print("Performance vs NumPy")
        print("-"*80)
        
        numpy_results = results_dict['NumPy']
        for backend in backends:
            if backend != 'NumPy' and results_dict[backend]:
                print(f"\n{backend} vs NumPy:")
                for op in all_ops:
                    if op in numpy_results and op in results_dict[backend]:
                        ratio = results_dict[backend][op] / numpy_results[op]
                        if ratio < 1:
                            print(f"  {op}: {1/ratio:.2f}x faster")
                        else:
                            print(f"  {op}: {ratio:.2f}x slower")

def main():
    """Run all benchmarks."""
    print("Starting ArrPy v1.0.0 Benchmarks...")
    print("Test sizes:")
    print("  - Small: 1,000 elements")
    print("  - Medium: 10,000 elements")
    print("  - Large: 100,000 elements")
    print("  - Matrix: 100x100")
    
    results = {}
    
    # Benchmark each backend
    print("\nBenchmarking Python backend...")
    results['Python'] = benchmark_backend('python')
    
    print("Benchmarking Cython backend...")
    cython_results = benchmark_backend('cython')
    if cython_results:
        results['Cython'] = cython_results
    else:
        print("  Cython backend not available")
    
    print("Benchmarking C++ backend...")
    c_results = benchmark_backend('c')
    if c_results:
        results['C++'] = c_results
    else:
        print("  C++ backend not available")
    
    # Benchmark NumPy for reference
    print("Benchmarking NumPy (reference)...")
    results['NumPy'] = benchmark_numpy_reference()
    
    # Print results
    print_results(results)
    
    # Summary
    print("\n" + "="*80)
    print("Summary")
    print("-"*80)
    print("✅ Python backend: Complete implementation (baseline)")
    if 'Cython' in results:
        print("✅ Cython backend: Optimized operations available")
    else:
        print("❌ Cython backend: Not built (run 'python setup.py build_ext --inplace')")
    if 'C++' in results:
        print("✅ C++ backend: SIMD operations available")
    else:
        print("❌ C++ backend: Not built (Linux only, run 'python setup_cpp.py build_ext --inplace')")
    print("\n📊 Benchmark complete!")

if __name__ == "__main__":
    main()