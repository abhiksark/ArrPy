#!/usr/bin/env python3
"""
Benchmark optimized reduction operations.
"""

import time
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import arrpy
from arrpy import Backend, set_backend

def benchmark_reduction(op_name, op_func, sizes=[100, 1000, 10000, 100000]):
    """Benchmark a reduction operation across backends."""
    print(f"\n{op_name} Benchmark")
    print("=" * 50)
    
    for size in sizes:
        print(f"\nSize: {size:,}")
        data = list(range(size))
        
        results = {}
        
        for backend_name in ['python', 'cython']:
            try:
                set_backend(backend_name)
                a = arrpy.array(data)
                
                # Warmup
                for _ in range(5):
                    _ = op_func(a)
                
                # Benchmark
                iterations = 1000 if size <= 1000 else 100 if size <= 10000 else 10
                start = time.perf_counter()
                for _ in range(iterations):
                    result = op_func(a)
                elapsed = time.perf_counter() - start
                
                avg_time = (elapsed / iterations) * 1000  # Convert to ms
                results[backend_name] = avg_time
                print(f"  {backend_name:8}: {avg_time:8.4f} ms")
                
            except NotImplementedError:
                print(f"  {backend_name:8}: Not implemented")
            except Exception as e:
                print(f"  {backend_name:8}: Error - {str(e)[:30]}")
        
        # Calculate speedup
        if 'python' in results and 'cython' in results:
            speedup = results['python'] / results['cython']
            print(f"  Speedup: {speedup:.2f}x")

def test_correctness():
    """Verify that optimized operations produce correct results."""
    print("\nCorrectness Tests")
    print("=" * 50)
    
    import numpy as np
    
    test_data = [
        [1, 2, 3, 4, 5],
        [1.5, 2.5, 3.5, 4.5, 5.5],
        list(range(1000)),
        [-5, -3, 0, 3, 5],
    ]
    
    for data in test_data:
        print(f"\nTesting with {len(data)} elements...")
        
        # Test sum
        set_backend('python')
        a_py = arrpy.array(data)
        sum_py = a_py.sum()
        
        set_backend('cython')
        a_cy = arrpy.array(data)
        sum_cy = a_cy.sum()
        
        np_arr = np.array(data)
        sum_np = np_arr.sum()
        
        # Sum returns a scalar value
        sum_py_val = sum_py if isinstance(sum_py, (int, float)) else sum_py._data[0]
        sum_cy_val = sum_cy if isinstance(sum_cy, (int, float)) else sum_cy._data[0]
        
        assert abs(sum_py_val - sum_np) < 1e-10, f"Python sum mismatch"
        assert abs(sum_cy_val - sum_np) < 1e-10, f"Cython sum mismatch"
        print(f"  Sum: Python={sum_py_val:.2f}, Cython={sum_cy_val:.2f}, NumPy={sum_np:.2f} ✓")
        
        # Test mean
        try:
            mean_py = a_py.mean()
            mean_cy = a_cy.mean()
            mean_np = np_arr.mean()
            
            mean_py_val = mean_py if isinstance(mean_py, (int, float)) else mean_py._data[0]
            mean_cy_val = mean_cy if isinstance(mean_cy, (int, float)) else mean_cy._data[0]
            
            assert abs(mean_py_val - mean_np) < 1e-10, f"Python mean mismatch"
            assert abs(mean_cy_val - mean_np) < 1e-10, f"Cython mean mismatch"
            print(f"  Mean: Python={mean_py_val:.2f}, Cython={mean_cy_val:.2f}, NumPy={mean_np:.2f} ✓")
        except NotImplementedError:
            print(f"  Mean: Cython not implemented")
        
        # Test min/max
        try:
            min_py = a_py.min()
            min_cy = a_cy.min()
            min_np = np_arr.min()
            
            max_py = a_py.max()
            max_cy = a_cy.max()
            max_np = np_arr.max()
            
            min_py_val = min_py if isinstance(min_py, (int, float)) else min_py._data[0]
            min_cy_val = min_cy if isinstance(min_cy, (int, float)) else min_cy._data[0]
            max_py_val = max_py if isinstance(max_py, (int, float)) else max_py._data[0]
            max_cy_val = max_cy if isinstance(max_cy, (int, float)) else max_cy._data[0]
            
            assert abs(min_py_val - min_np) < 1e-10, f"Min mismatch"
            assert abs(min_cy_val - min_np) < 1e-10, f"Min mismatch"
            assert abs(max_py_val - max_np) < 1e-10, f"Max mismatch"
            assert abs(max_cy_val - max_np) < 1e-10, f"Max mismatch"
            
            print(f"  Min: Python={min_py_val:.2f}, Cython={min_cy_val:.2f}, NumPy={min_np:.2f} ✓")
            print(f"  Max: Python={max_py_val:.2f}, Cython={max_cy_val:.2f}, NumPy={max_np:.2f} ✓")
        except NotImplementedError:
            print(f"  Min/Max: Cython not implemented")

def main():
    print("Testing Optimized Reduction Operations")
    print("=" * 50)
    
    # First verify correctness
    test_correctness()
    
    print("\n" + "="*50)
    print("Performance Benchmarks")
    print("=" * 50)
    
    # Benchmark each reduction operation
    benchmark_reduction("Sum", lambda a: a.sum())
    benchmark_reduction("Mean", lambda a: a.mean())
    benchmark_reduction("Min", lambda a: a.min())
    benchmark_reduction("Max", lambda a: a.max())
    
    # Test parallel performance scaling
    print("\n" + "="*50)
    print("Parallel Scaling Analysis")
    print("=" * 50)
    
    sizes = [100, 1000, 10000, 100000, 1000000]
    print("\nSum operation scaling:")
    
    for size in sizes:
        data = list(range(size))
        set_backend('cython')
        a = arrpy.array(data)
        
        # Time the operation
        start = time.perf_counter()
        for _ in range(10):
            _ = a.sum()
        elapsed = time.perf_counter() - start
        
        ops_per_sec = 10 / elapsed
        elements_per_sec = size * ops_per_sec
        
        print(f"  Size {size:>8,}: {elapsed/10*1000:6.3f}ms, {elements_per_sec/1e6:6.1f}M elements/sec")

if __name__ == "__main__":
    main()