#!/usr/bin/env python3
"""
Test and benchmark the fast C++ backend against the original.
"""

import time
import sys
import numpy as np
sys.path.insert(0, '.')

import arrpy
from arrpy import Backend, set_backend

# Import both implementations
from arrpy.backends.c import array_ops as old_cpp
from arrpy.backends.c import array_ops_fast as new_cpp

def benchmark_operation(name, func, data1, data2, shape, iterations=100):
    """Benchmark a single operation."""
    # Warmup
    for _ in range(5):
        func(data1, data2, shape, shape)
    
    # Benchmark
    start = time.perf_counter()
    for _ in range(iterations):
        result = func(data1, data2, shape, shape)
    elapsed = time.perf_counter() - start
    
    return elapsed / iterations * 1000  # ms

def main():
    print("="*60)
    print("C++ Backend Performance Comparison")
    print("Testing old (list-based) vs new (numpy zero-copy)")
    print("="*60)
    
    sizes = [1000, 10000, 100000, 1000000]
    
    for size in sizes:
        print(f"\nArray size: {size:,} elements")
        print("-"*40)
        
        # Create test data
        data1 = list(np.random.randn(size))
        data2 = list(np.random.randn(size))
        shape = (size,)
        
        # Adjust iterations based on size
        iterations = 1000 if size <= 10000 else 100 if size <= 100000 else 10
        
        operations = [
            ("Addition", "_add_c"),
            ("Multiplication", "_multiply_c"),
            ("Subtraction", "_subtract_c"),
            ("Division", "_divide_c"),
        ]
        
        for op_name, func_name in operations:
            try:
                # Test old implementation
                old_func = getattr(old_cpp, func_name)
                old_time = benchmark_operation(op_name + " (old)", old_func, 
                                              data1, data2, shape, iterations)
                
                # Test new implementation
                new_func = getattr(new_cpp, func_name)
                new_time = benchmark_operation(op_name + " (new)", new_func,
                                              data1, data2, shape, iterations)
                
                # Calculate speedup
                speedup = old_time / new_time
                
                print(f"{op_name:15} Old: {old_time:8.3f} ms  New: {new_time:8.3f} ms  "
                      f"Speedup: {speedup:6.2f}x")
                      
            except Exception as e:
                print(f"{op_name:15} Error: {e}")
    
    # Now test against Python and Cython backends
    print("\n" + "="*60)
    print("Full Backend Comparison (size=100,000)")
    print("="*60)
    
    size = 100000
    data1 = list(np.random.randn(size))
    data2 = list(np.random.randn(size))
    shape = (size,)
    iterations = 50
    
    for op_name in ["Addition", "Multiplication"]:
        print(f"\n{op_name}:")
        results = {}
        
        # Python backend
        set_backend('python')
        a = arrpy.array(data1)
        b = arrpy.array(data2)
        start = time.perf_counter()
        for _ in range(iterations):
            if op_name == "Addition":
                c = a + b
            else:
                c = a * b
        python_time = (time.perf_counter() - start) / iterations * 1000
        results['Python'] = python_time
        
        # Cython backend
        try:
            set_backend('cython')
            a = arrpy.array(data1)
            b = arrpy.array(data2)
            start = time.perf_counter()
            for _ in range(iterations):
                if op_name == "Addition":
                    c = a + b
                else:
                    c = a * b
            cython_time = (time.perf_counter() - start) / iterations * 1000
            results['Cython'] = cython_time
        except:
            results['Cython'] = None
        
        # Old C++ backend
        set_backend('c')
        a = arrpy.array(data1)
        b = arrpy.array(data2)
        start = time.perf_counter()
        for _ in range(iterations):
            if op_name == "Addition":
                c = a + b
            else:
                c = a * b
        old_cpp_time = (time.perf_counter() - start) / iterations * 1000
        results['C++ (old)'] = old_cpp_time
        
        # Print results
        for backend, time_ms in results.items():
            if time_ms is not None:
                speedup = results['Python'] / time_ms if 'Python' in results else 1
                print(f"  {backend:12} {time_ms:8.3f} ms  (Speedup: {speedup:6.2f}x)")

if __name__ == "__main__":
    main()