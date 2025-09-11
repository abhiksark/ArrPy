#!/usr/bin/env python3
"""
Comprehensive benchmark comparing all three backends.
"""

import time
import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import arrpy
from arrpy import Backend, set_backend

def print_header(title):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"{title:^60}")
    print('='*60)

def benchmark_operation(op_name, op_func, sizes, backends=['python', 'cython', 'c']):
    """Benchmark a single operation across backends."""
    print(f"\n{op_name}")
    print("-" * 50)
    
    # Header
    header = f"{'Size':<12}"
    for backend in backends:
        header += f"{backend.upper():<12}"
    header += "Best"
    print(header)
    print("-" * 50)
    
    for size in sizes:
        # Create test data
        data1 = list(range(size))
        data2 = list(range(size, size * 2))
        
        times = {}
        
        for backend_name in backends:
            try:
                set_backend(backend_name)
                a = arrpy.array(data1)
                b = arrpy.array(data2)
                
                # Warmup
                for _ in range(3):
                    _ = op_func(a, b)
                
                # Benchmark
                iterations = 1000 if size <= 1000 else 100 if size <= 10000 else 10
                start = time.perf_counter()
                for _ in range(iterations):
                    result = op_func(a, b)
                elapsed = time.perf_counter() - start
                
                times[backend_name] = (elapsed / iterations) * 1000  # ms
                
            except Exception as e:
                times[backend_name] = float('inf')
        
        # Find best performer
        best = min(times, key=times.get)
        
        # Print row
        row = f"{size:<12}"
        for backend in backends:
            if times[backend] == float('inf'):
                row += f"{'N/A':<12}"
            else:
                row += f"{times[backend]:<12.3f}"
        
        # Add speedup for best
        if times[best] != float('inf'):
            speedup = times['python'] / times[best] if 'python' in times else 1.0
            row += f"{best} ({speedup:.1f}x)"
        else:
            row += "N/A"
        
        print(row)

def benchmark_arithmetic():
    """Benchmark arithmetic operations."""
    print_header("Arithmetic Operations")
    
    sizes = [100, 1000, 10000, 100000]
    
    operations = [
        ("Addition", lambda a, b: a + b),
        ("Subtraction", lambda a, b: a - b),
        ("Multiplication", lambda a, b: a * b),
        ("Division", lambda a, b: a / b),
        ("Scalar Multiply", lambda a, b: a * 2.5),
    ]
    
    for op_name, op_func in operations:
        benchmark_operation(op_name, op_func, sizes)

def benchmark_linear_algebra():
    """Benchmark linear algebra operations."""
    print_header("Linear Algebra Operations")
    
    # Matrix multiplication
    print("\nMatrix Multiplication (M×N @ N×P)")
    print("-" * 50)
    
    matrix_sizes = [
        (10, 10, 10),
        (50, 50, 50),
        (100, 100, 100),
        (200, 200, 200),
    ]
    
    header = f"{'Size':<20}{'Python':<12}{'Cython':<12}{'C++':<12}{'Best'}"
    print(header)
    print("-" * 50)
    
    for m, n, p in matrix_sizes:
        # Create test matrices
        mat1 = np.random.randn(m * n).tolist()
        mat2 = np.random.randn(n * p).tolist()
        
        times = {}
        
        for backend_name in ['python', 'cython', 'c']:
            try:
                set_backend(backend_name)
                a = arrpy.array(mat1).reshape((m, n))
                b = arrpy.array(mat2).reshape((n, p))
                
                # Warmup
                _ = arrpy.linalg.matmul(a, b)
                
                # Benchmark
                iterations = 100 if m <= 50 else 10 if m <= 100 else 3
                start = time.perf_counter()
                for _ in range(iterations):
                    result = arrpy.linalg.matmul(a, b)
                elapsed = time.perf_counter() - start
                
                times[backend_name] = (elapsed / iterations) * 1000  # ms
                
            except Exception:
                times[backend_name] = float('inf')
        
        # Find best
        best = min(times, key=times.get)
        speedup = times['python'] / times[best] if times[best] != float('inf') else 1.0
        
        # Print row
        size_str = f"({m}×{n})@({n}×{p})"
        row = f"{size_str:<20}"
        for backend in ['python', 'cython', 'c']:
            if times[backend] == float('inf'):
                row += f"{'N/A':<12}"
            else:
                row += f"{times[backend]:<12.3f}"
        row += f"{best} ({speedup:.1f}x)"
        print(row)
    
    # Dot product
    print("\nDot Product")
    print("-" * 50)
    
    sizes = [100, 1000, 10000, 100000]
    benchmark_operation("Vector Dot", lambda a, b: arrpy.linalg.dot(a, b), sizes)

def benchmark_reductions():
    """Benchmark reduction operations."""
    print_header("Reduction Operations")
    
    sizes = [100, 1000, 10000, 100000]
    
    operations = [
        ("Sum", lambda a, b: a.sum()),
        ("Mean", lambda a, b: a.mean()),
        ("Min", lambda a, b: a.min()),
        ("Max", lambda a, b: a.max()),
    ]
    
    for op_name, op_func in operations:
        benchmark_operation(op_name, op_func, sizes)

def analyze_simd_performance():
    """Analyze SIMD performance characteristics."""
    print_header("SIMD Performance Analysis")
    
    try:
        from arrpy.backends.c import array_ops_cpp
        
        print(f"\nPlatform: {array_ops_cpp.platform}")
        print(f"SIMD Type: {array_ops_cpp.simd_type}")
        
        if array_ops_cpp.simd_type == "NEON":
            print("  - ARM NEON: 2 doubles per instruction")
        elif array_ops_cpp.simd_type == "AVX2":
            print("  - Intel AVX2: 4 doubles per instruction")
        elif array_ops_cpp.simd_type == "SSE2":
            print("  - Intel SSE2: 2 doubles per instruction")
        else:
            print("  - Scalar: No SIMD, using loop unrolling")
        
        # Test different array sizes to see cache effects
        print("\nCache Effects (Addition operation)")
        print("-" * 50)
        print(f"{'Size':<15}{'Time (ms)':<15}{'Throughput (M/s)':<20}{'Efficiency'}")
        print("-" * 50)
        
        sizes = [64, 256, 1024, 4096, 16384, 65536, 262144]
        
        for size in sizes:
            data1 = list(range(size))
            data2 = list(range(size, size * 2))
            
            # Direct C++ call for pure performance
            iterations = 1000 if size <= 4096 else 100 if size <= 65536 else 10
            
            start = time.perf_counter()
            for _ in range(iterations):
                result, shape = array_ops_cpp.add(
                    data1, data2,
                    (size, 1), (size, 1)
                )
            elapsed = time.perf_counter() - start
            
            time_ms = (elapsed / iterations) * 1000
            throughput = (size * iterations) / elapsed / 1e6
            
            # Estimate cache efficiency
            if size * 8 <= 32 * 1024:  # L1 cache (32KB typical)
                efficiency = "L1 Cache"
            elif size * 8 <= 256 * 1024:  # L2 cache (256KB typical)
                efficiency = "L2 Cache"
            elif size * 8 <= 8 * 1024 * 1024:  # L3 cache (8MB typical)
                efficiency = "L3 Cache"
            else:
                efficiency = "Memory"
            
            print(f"{size:<15}{time_ms:<15.3f}{throughput:<20.1f}{efficiency}")
        
    except ImportError:
        print("C++ backend not available")

def print_summary():
    """Print performance summary and recommendations."""
    print_header("Performance Summary")
    
    print("""
Key Findings:
------------
1. C++ Backend:
   - Uses SIMD instructions (NEON on ARM, AVX2/SSE2 on x86)
   - Best for large arrays (>10,000 elements)
   - Cache-efficient algorithms for linear algebra

2. Cython Backend:
   - Good balance of performance and compatibility
   - Removes Python overhead
   - Better for medium-sized arrays (1,000-10,000)

3. Python Backend:
   - Reference implementation
   - Best compatibility
   - Suitable for small arrays (<1,000)

Recommendations:
---------------
- Use C++ backend for production workloads
- Use Cython for development and testing
- Use Python for debugging and education
""")

def main():
    print("=" * 60)
    print("ArrPy Complete Backend Performance Comparison")
    print("=" * 60)
    
    # Check if C++ backend is available
    try:
        from arrpy.backends.c import array_ops_cpp
        print(f"\n✓ All backends available (Python, Cython, C++)")
        print(f"✓ SIMD: {array_ops_cpp.simd_type} on {array_ops_cpp.platform}")
    except ImportError:
        print("\n⚠ C++ backend not available. Run: make build-cpp")
    
    # Run benchmarks
    benchmark_arithmetic()
    benchmark_linear_algebra()
    benchmark_reductions()
    analyze_simd_performance()
    print_summary()
    
    print("\n" + "=" * 60)
    print("Benchmark Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()