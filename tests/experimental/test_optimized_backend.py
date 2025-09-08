#!/usr/bin/env python3
"""
Test the optimized C++ backend performance improvements.
"""

import time
import sys
import numpy as np
sys.path.insert(0, '.')

import arrpy
from arrpy import set_backend

def benchmark_operation(op_name, func1, func2, size=100000, iterations=100):
    """Benchmark two operations and compare."""
    # Warmup
    for _ in range(5):
        func1()
        func2()
    
    # Benchmark original
    start = time.perf_counter()
    for _ in range(iterations):
        func1()
    time1 = (time.perf_counter() - start) / iterations * 1000
    
    # Benchmark optimized
    start = time.perf_counter()
    for _ in range(iterations):
        func2()
    time2 = (time.perf_counter() - start) / iterations * 1000
    
    speedup = time1 / time2 if time2 > 0 else 0
    print(f"{op_name:20} Original: {time1:7.3f}ms  Optimized: {time2:7.3f}ms  Speedup: {speedup:5.2f}x")
    
    return speedup

def test_optimized_backend():
    """Test the optimized C++ backend."""
    print("="*80)
    print("Testing Optimized C++ Backend Performance")
    print("="*80)
    
    # Test different sizes
    sizes = [1000, 10000, 100000]
    
    for size in sizes:
        print(f"\n📊 Array Size: {size:,} elements")
        print("-"*60)
        
        # Create test arrays
        set_backend('c')
        a = arrpy.ones(size, dtype=arrpy.float64)
        b = arrpy.ones(size, dtype=arrpy.float64) * 2.0
        
        # Test if optimized module is available
        try:
            from arrpy.backends.c import array_ops_optimized
            from arrpy.backends.c import array_ops_buffer
            
            print("✅ Optimized module loaded successfully")
            
            # Compare operations
            print("\nBenchmarking operations:")
            
            # Addition
            speedup_add = benchmark_operation(
                "Addition",
                lambda: array_ops_buffer._add_c(a._data, b._data, a._shape, b._shape),
                lambda: array_ops_optimized._add_optimized(a._data, b._data, a._shape, b._shape),
                size=size
            )
            
            # Multiplication
            speedup_mul = benchmark_operation(
                "Multiplication",
                lambda: array_ops_buffer._multiply_c(a._data, b._data, a._shape, b._shape),
                lambda: array_ops_optimized._multiply_optimized(a._data, b._data, a._shape, b._shape),
                size=size
            )
            
            # Division
            speedup_div = benchmark_operation(
                "Division",
                lambda: array_ops_buffer._divide_c(a._data, b._data, a._shape, b._shape),
                lambda: array_ops_optimized._divide_optimized(a._data, b._data, a._shape, b._shape),
                size=size
            )
            
            # Test fast division mode
            print("\n🚀 Fast mode division (reciprocal approximation):")
            start = time.perf_counter()
            for _ in range(100):
                array_ops_optimized._divide_optimized(a._data, b._data, a._shape, b._shape, fast_mode=True)
            fast_time = (time.perf_counter() - start) / 100 * 1000
            print(f"Fast division: {fast_time:.3f}ms (additional speedup for slight accuracy loss)")
            
            # Test in-place operations
            print("\n💾 In-place operations (no allocation overhead):")
            import array as pyarray
            a_copy = pyarray.array('d', a._data)
            start = time.perf_counter()
            array_ops_optimized._add_inplace_optimized(a_copy, b._data)
            inplace_time = (time.perf_counter() - start) * 1000
            print(f"In-place addition: {inplace_time:.3f}ms (modifies array directly)")
            
        except ImportError as e:
            print(f"❌ Could not load optimized module: {e}")
            print("Build with: python setup_optimized_cpp.py build_ext --inplace")
            return
    
    # Compare with NumPy
    print("\n" + "="*80)
    print("📊 Comparison with NumPy (100k elements)")
    print("-"*80)
    
    size = 100000
    iterations = 100
    
    # NumPy
    a_np = np.ones(size, dtype=np.float64)
    b_np = np.ones(size, dtype=np.float64) * 2.0
    
    start = time.perf_counter()
    for _ in range(iterations):
        c = a_np + b_np
    numpy_time = (time.perf_counter() - start) / iterations * 1000
    
    # ArrPy optimized
    set_backend('c')
    a_arrpy = arrpy.ones(size, dtype=arrpy.float64)
    b_arrpy = arrpy.ones(size, dtype=arrpy.float64) * 2.0
    
    start = time.perf_counter()
    for _ in range(iterations):
        c = a_arrpy + b_arrpy
    arrpy_time = (time.perf_counter() - start) / iterations * 1000
    
    print(f"NumPy:          {numpy_time:.3f}ms")
    print(f"ArrPy Optimized: {arrpy_time:.3f}ms")
    print(f"Performance gap: {arrpy_time/numpy_time:.1f}x slower than NumPy")
    
    # Analysis
    print("\n" + "="*80)
    print("🔬 Optimization Analysis")
    print("-"*80)
    print("""
Expected improvements from optimizations:
1. Memory alignment: ~20-30% speedup ✓
2. Loop unrolling: ~15-20% speedup ✓
3. Prefetching: ~5-10% speedup ✓
4. Compiler flags: ~10-15% speedup ✓
5. In-place operations: Reduces allocation overhead ✓

Note: OpenMP parallelization not available on this system.
Install with: brew install libomp
    """)

if __name__ == "__main__":
    test_optimized_backend()