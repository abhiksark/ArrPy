#!/usr/bin/env python3
"""
Test the new optimized subtract and divide operations.
"""

import time
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import arrpy
from arrpy import Backend, set_backend

def benchmark_operation(op_name, op_func, sizes=[100, 1000, 10000]):
    """Benchmark an operation across backends."""
    print(f"\n{op_name} Benchmark")
    print("=" * 40)
    
    for size in sizes:
        print(f"\nSize: {size}")
        data1 = list(range(1, size + 1))  # Start from 1 to avoid div by zero
        data2 = list(range(size, 0, -1))  # Reverse order
        
        results = {}
        
        for backend_name in ['python', 'cython']:
            try:
                set_backend(backend_name)
                a = arrpy.array(data1)
                b = arrpy.array(data2)
                
                # Warmup
                for _ in range(5):
                    _ = op_func(a, b)
                
                # Benchmark
                iterations = 100 if size <= 1000 else 10
                start = time.perf_counter()
                for _ in range(iterations):
                    result = op_func(a, b)
                elapsed = time.perf_counter() - start
                
                avg_time = (elapsed / iterations) * 1000  # Convert to ms
                results[backend_name] = avg_time
                print(f"  {backend_name:8}: {avg_time:8.3f} ms")
                
            except NotImplementedError:
                print(f"  {backend_name:8}: Not implemented")
            except Exception as e:
                print(f"  {backend_name:8}: Error - {str(e)[:30]}")
        
        # Calculate speedup
        if 'python' in results and 'cython' in results:
            speedup = results['python'] / results['cython']
            print(f"  Speedup: {speedup:.2f}x")

def main():
    print("Testing new optimized Cython operations")
    print("=" * 40)
    
    # Test subtract
    benchmark_operation("Subtraction", lambda a, b: a - b)
    
    # Test divide
    benchmark_operation("Division", lambda a, b: a / b)
    
    # Test scalar operations
    print("\n\nScalar Operations")
    print("=" * 40)
    
    benchmark_operation("Scalar Multiply", lambda a, b: a * 2)
    benchmark_operation("Scalar Divide", lambda a, b: a / 2)
    benchmark_operation("Scalar Subtract", lambda a, b: a - 1)

if __name__ == "__main__":
    main()