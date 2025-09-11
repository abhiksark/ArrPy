#!/usr/bin/env python3
"""
Benchmark memory pooling improvements.
Compares regular allocation vs pooled allocation.
"""

import time
import sys
import os
import gc

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import memory pool functions directly
from arrpy.backends.cython import memory_pool
from arrpy.backends.cython import array_ops_pooled

def benchmark_pooled_vs_regular():
    """Compare pooled operations vs regular operations."""
    print("=" * 60)
    print("Memory Pool Performance Benchmark")
    print("=" * 60)
    
    sizes = [100, 1000, 10000, 100000]
    iterations = [10000, 1000, 100, 10]
    
    print("\nComparing pooled vs regular memory allocation:")
    print("-" * 60)
    print(f"{'Size':<10} {'Iterations':<12} {'Regular (ms)':<15} {'Pooled (ms)':<15} {'Speedup':<10}")
    print("-" * 60)
    
    for size, iters in zip(sizes, iterations):
        # Create test data
        data1 = list(range(size))
        data2 = list(range(size, size * 2))
        shape = (size,)
        
        # Import regular Cython operations
        from arrpy.backends.cython.array_ops import _add_cython
        
        # Warmup
        for _ in range(10):
            _add_cython(data1, data2, shape, shape)
            array_ops_pooled._add_pooled(data1, data2, shape, shape)
        
        # Force garbage collection
        gc.collect()
        
        # Benchmark regular allocation
        start = time.perf_counter()
        for _ in range(iters):
            result, _ = _add_cython(data1, data2, shape, shape)
        regular_time = (time.perf_counter() - start) * 1000
        
        # Force garbage collection
        gc.collect()
        
        # Benchmark pooled allocation
        start = time.perf_counter()
        for _ in range(iters):
            result, _ = array_ops_pooled._add_pooled(data1, data2, shape, shape)
        pooled_time = (time.perf_counter() - start) * 1000
        
        speedup = regular_time / pooled_time if pooled_time > 0 else 0
        
        print(f"{size:<10} {iters:<12} {regular_time:<15.3f} {pooled_time:<15.3f} {speedup:<10.2f}x")
    
    # Print pool statistics
    print("\n" + "=" * 60)
    print("Memory Pool Statistics:")
    print("-" * 60)
    stats = memory_pool.get_pool_stats()
    for key, value in stats.items():
        if isinstance(value, float):
            if 'mb' in key:
                print(f"{key:<20}: {value:.2f} MB")
            elif 'rate' in key:
                print(f"{key:<20}: {value:.2%}")
            else:
                print(f"{key:<20}: {value:.2f}")
        else:
            print(f"{key:<20}: {value}")

def benchmark_multiple_operations():
    """Benchmark multiple operations to show pool efficiency."""
    print("\n" + "=" * 60)
    print("Multiple Operations Benchmark")
    print("=" * 60)
    
    size = 10000
    iterations = 100
    
    data1 = list(range(size))
    data2 = list(range(size, size * 2))
    shape = (size,)
    
    from arrpy.backends.cython.array_ops import (
        _add_cython, _subtract_cython, _multiply_cython, _divide_cython
    )
    
    print(f"\nSize: {size}, Iterations: {iterations}")
    print("-" * 60)
    
    # Regular operations (each allocates new memory)
    gc.collect()
    start = time.perf_counter()
    for _ in range(iterations):
        r1, _ = _add_cython(data1, data2, shape, shape)
        r2, _ = _subtract_cython(data1, data2, shape, shape)
        r3, _ = _multiply_cython(data1, data2, shape, shape)
        r4, _ = _divide_cython(data1, data2, shape, shape)
    regular_time = (time.perf_counter() - start) * 1000
    
    # Pooled operations (reuses memory)
    gc.collect()
    start = time.perf_counter()
    for _ in range(iterations):
        r1, _ = array_ops_pooled._add_pooled(data1, data2, shape, shape)
        r2, _ = array_ops_pooled._subtract_pooled(data1, data2, shape, shape)
        r3, _ = array_ops_pooled._multiply_pooled(data1, data2, shape, shape)
        r4, _ = array_ops_pooled._divide_pooled(data1, data2, shape, shape)
    pooled_time = (time.perf_counter() - start) * 1000
    
    print(f"Regular (4 ops): {regular_time:.3f} ms")
    print(f"Pooled (4 ops):  {pooled_time:.3f} ms")
    print(f"Speedup:         {regular_time/pooled_time:.2f}x")
    
    # Show final pool stats
    print("\nFinal Pool Statistics:")
    print("-" * 60)
    stats = memory_pool.get_pool_stats()
    print(f"Total allocations:   {stats['allocations']}")
    print(f"Pool hit rate:       {stats['hit_rate']:.2%}")
    print(f"Memory allocated:    {stats['total_allocated_mb']:.2f} MB")
    print(f"Memory in use:       {stats['total_in_use_mb']:.2f} MB")

def main():
    print("Testing Memory Pool System")
    print("=" * 60)
    
    # Reset pool for clean start
    memory_pool.reset_pool()
    
    # Run benchmarks
    benchmark_pooled_vs_regular()
    benchmark_multiple_operations()
    
    print("\n" + "=" * 60)
    print("Benchmark Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()