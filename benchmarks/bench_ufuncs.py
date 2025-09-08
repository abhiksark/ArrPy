#!/usr/bin/env python3
"""
Benchmark universal functions (ufuncs) across backends.
"""

import time
import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import arrpy
from arrpy import Backend, set_backend

def benchmark_ufunc(name, func, data, backends=['python', 'cython']):
    """Benchmark a single ufunc across backends."""
    print(f"\n{name}")
    print("-" * 40)
    
    times = {}
    
    for backend_name in backends:
        try:
            set_backend(backend_name)
            a = arrpy.array(data)
            
            # Warmup
            for _ in range(5):
                _ = func(a)
            
            # Benchmark
            iterations = 100
            start = time.perf_counter()
            for _ in range(iterations):
                result = func(a)
            elapsed = time.perf_counter() - start
            
            times[backend_name] = (elapsed / iterations) * 1000  # ms
            print(f"  {backend_name:<10}: {times[backend_name]:.3f} ms")
            
        except Exception as e:
            print(f"  {backend_name:<10}: Error - {str(e)[:50]}")
            times[backend_name] = float('inf')
    
    # Calculate speedup
    if 'python' in times and 'cython' in times and times['cython'] != float('inf'):
        speedup = times['python'] / times['cython']
        print(f"  Speedup: {speedup:.2f}x")

def main():
    print("=" * 50)
    print("ArrPy Universal Functions Benchmark")
    print("=" * 50)
    
    # Test data
    sizes = [100, 1000, 10000]
    
    for size in sizes:
        print(f"\n{'='*50}")
        print(f"Array size: {size}")
        print(f"{'='*50}")
        
        # Create test data (values between 0 and 1 for trig functions)
        data = [i / size for i in range(size)]
        
        # Trigonometric functions
        print("\nTrigonometric Functions:")
        benchmark_ufunc("sin", lambda a: arrpy.sin(a), data)
        benchmark_ufunc("cos", lambda a: arrpy.cos(a), data)
        benchmark_ufunc("tan", lambda a: arrpy.tan(a), data)
        
        # Exponential and logarithmic
        print("\nExponential and Logarithmic:")
        # Use smaller values for exp to avoid overflow
        exp_data = [i / (size * 10) for i in range(size)]
        benchmark_ufunc("exp", lambda a: arrpy.exp(a), exp_data)
        
        # Use positive values for log
        log_data = [i + 1 for i in range(size)]
        benchmark_ufunc("log", lambda a: arrpy.log(a), log_data)
        benchmark_ufunc("log10", lambda a: arrpy.log10(a), log_data)
        
        # Other functions
        print("\nOther Functions:")
        positive_data = [i + 1 for i in range(size)]
        benchmark_ufunc("sqrt", lambda a: arrpy.sqrt(a), positive_data)
        
        # Test absolute with negative values
        mixed_data = [i - size/2 for i in range(size)]
        benchmark_ufunc("absolute", lambda a: arrpy.absolute(a), mixed_data)
    
    print("\n" + "=" * 50)
    print("Benchmark Complete!")
    print("=" * 50)

if __name__ == "__main__":
    main()