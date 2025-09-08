#!/usr/bin/env python3
"""
Test C++ backend functionality and performance.
"""

import sys
import time
import numpy as np

# Add current directory to path
import arrpy
from arrpy import Backend, set_backend

def test_cpp_availability():
    """Check if C++ backend is available and working."""
    print("Testing C++ Backend Availability")
    print("=" * 50)
    
    try:
        # Try to import the C++ modules directly
        from arrpy.backends.c import array_ops_cpp, linalg_ops_cpp
        
        print(f"✓ C++ array operations module loaded")
        print(f"  - SIMD type: {array_ops_cpp.simd_type}")
        print(f"  - Platform: {array_ops_cpp.platform}")
        print(f"  - Has AVX2: {array_ops_cpp.has_avx2}")
        print(f"  - Has NEON: {array_ops_cpp.has_neon}")
        
        print(f"\n✓ C++ linear algebra module loaded")
        print(f"  - SIMD type: {linalg_ops_cpp.simd_type}")
        print(f"  - Platform: {linalg_ops_cpp.platform}")
        
        return True
    except ImportError as e:
        print(f"✗ C++ backend not available: {e}")
        return False

def test_basic_operations():
    """Test basic arithmetic operations."""
    print("\nTesting Basic Operations")
    print("=" * 50)
    
    # Test data
    data1 = list(range(1000))
    data2 = list(range(1000, 2000))
    
    # Test with each backend
    for backend_name in ['python', 'cython', 'c']:
        print(f"\n{backend_name.upper()} Backend:")
        
        try:
            set_backend(backend_name)
            
            # Create arrays
            a = arrpy.array(data1)
            b = arrpy.array(data2)
            
            # Test operations
            start = time.perf_counter()
            
            # Addition
            c = a + b
            assert len(c._data) == 1000
            assert c._data[0] == 1000  # 0 + 1000
            assert c._data[-1] == 2998  # 999 + 1999
            print(f"  ✓ Addition works")
            
            # Subtraction
            c = b - a
            assert c._data[0] == 1000  # 1000 - 0
            assert c._data[-1] == 1000  # 1999 - 999
            print(f"  ✓ Subtraction works")
            
            # Multiplication
            c = a * 2
            assert c._data[0] == 0
            assert c._data[-1] == 1998
            print(f"  ✓ Scalar multiplication works")
            
            # Division
            c = b / 2
            assert abs(c._data[0] - 500) < 1e-10
            assert abs(c._data[-1] - 999.5) < 1e-10
            print(f"  ✓ Division works")
            
            elapsed = time.perf_counter() - start
            print(f"  Time: {elapsed*1000:.3f} ms")
            
        except NotImplementedError as e:
            print(f"  Some operations not implemented: {str(e)[:50]}...")
        except Exception as e:
            print(f"  Error: {e}")

def test_linear_algebra():
    """Test linear algebra operations."""
    print("\nTesting Linear Algebra")
    print("=" * 50)
    
    # Create test matrices
    m, n, p = 50, 60, 40
    mat1 = np.random.randn(m, n)
    mat2 = np.random.randn(n, p)
    
    for backend_name in ['python', 'cython', 'c']:
        print(f"\n{backend_name.upper()} Backend:")
        
        try:
            set_backend(backend_name)
            
            # Create arrays
            a = arrpy.array(mat1.flatten().tolist()).reshape((m, n))
            b = arrpy.array(mat2.flatten().tolist()).reshape((n, p))
            
            # Matrix multiplication
            start = time.perf_counter()
            c = arrpy.linalg.matmul(a, b)
            matmul_time = time.perf_counter() - start
            
            assert c._shape == (m, p)
            print(f"  ✓ Matrix multiply ({m}×{n})@({n}×{p}): {matmul_time*1000:.3f} ms")
            
            # Dot product
            vec1 = list(range(1000))
            vec2 = list(range(1000, 2000))
            
            v1 = arrpy.array(vec1)
            v2 = arrpy.array(vec2)
            
            start = time.perf_counter()
            dot_result = arrpy.linalg.dot(v1, v2)
            dot_time = time.perf_counter() - start
            
            # Verify result
            expected = sum(a * b for a, b in zip(vec1, vec2))
            actual = dot_result if isinstance(dot_result, (int, float)) else dot_result._data[0]
            assert abs(actual - expected) < 1e-6
            
            print(f"  ✓ Dot product (1000 elements): {dot_time*1000:.3f} ms")
            
        except Exception as e:
            print(f"  Error: {e}")

def benchmark_performance():
    """Benchmark C++ backend against others."""
    print("\nPerformance Comparison")
    print("=" * 50)
    
    sizes = [100, 1000, 10000, 100000]
    
    print("\nAddition operation (times in ms):")
    print(f"{'Size':<10} {'Python':<10} {'Cython':<10} {'C++':<10} {'Speedup':<10}")
    print("-" * 50)
    
    for size in sizes:
        data1 = list(range(size))
        data2 = list(range(size, size * 2))
        times = {}
        
        for backend_name in ['python', 'cython', 'c']:
            try:
                set_backend(backend_name)
                a = arrpy.array(data1)
                b = arrpy.array(data2)
                
                # Warmup
                for _ in range(5):
                    _ = a + b
                
                # Benchmark
                iterations = 1000 if size <= 1000 else 100 if size <= 10000 else 10
                start = time.perf_counter()
                for _ in range(iterations):
                    c = a + b
                elapsed = time.perf_counter() - start
                
                times[backend_name] = (elapsed / iterations) * 1000
            except:
                times[backend_name] = float('inf')
        
        speedup = times['python'] / times['c'] if times['c'] != float('inf') else 0
        
        print(f"{size:<10} {times['python']:<10.3f} {times['cython']:<10.3f} {times['c']:<10.3f} {speedup:<10.2f}x")

def test_simd_detection():
    """Test SIMD capability detection."""
    print("\nSIMD Capability Detection")
    print("=" * 50)
    
    try:
        from arrpy.backends.c import array_ops_cpp
        
        print(f"Platform: {array_ops_cpp.platform}")
        print(f"SIMD Type: {array_ops_cpp.simd_type}")
        
        # Test SIMD performance
        size = 10000
        data1 = list(range(size))
        data2 = list(range(size, size * 2))
        
        # Direct C++ call
        start = time.perf_counter()
        for _ in range(100):
            result, shape = array_ops_cpp.add(
                data1, data2,
                (size, 1), (size, 1)
            )
        simd_time = time.perf_counter() - start
        
        print(f"\nDirect SIMD performance (10000 elements, 100 iterations):")
        print(f"  Time: {simd_time*1000:.3f} ms")
        print(f"  Throughput: {(size * 100) / simd_time / 1e6:.1f} M elements/sec")
        
        # Verify correctness
        expected_first = 0 + size  # 0 + 10000 = 10000
        expected_last = (size - 1) + (2 * size - 1)  # 9999 + 19999 = 29998
        
        assert result[0] == expected_first, f"First element: {result[0]} != {expected_first}"
        assert result[-1] == expected_last, f"Last element: {result[-1]} != {expected_last}"
        print(f"  ✓ Results correct")
        
    except ImportError:
        print("C++ backend not available")

def main():
    print("=" * 60)
    print("ArrPy C++ Backend Test Suite")
    print("=" * 60)
    
    # Check availability
    if not test_cpp_availability():
        print("\nC++ backend not available. Please run: make build-cpp")
        return
    
    # Run tests
    test_basic_operations()
    test_linear_algebra()
    test_simd_detection()
    benchmark_performance()
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()