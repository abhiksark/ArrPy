#!/usr/bin/env python3
"""
Tutorial 01: Understanding ArrPy's Backend System

Learn how the three-backend architecture works and why it's educational.
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import arrpy
from arrpy import Backend, set_backend


def lesson_1_backend_basics():
    """Lesson 1: What are backends?"""
    print("\n" + "="*60)
    print("LESSON 1: Understanding Backends")
    print("="*60)
    
    print("""
ArrPy implements the same operations in three different ways:

1. PYTHON Backend:
   - Pure Python implementation
   - Easy to read and understand
   - Shows the algorithms clearly
   - Slowest performance

2. CYTHON Backend:
   - Python-like syntax with C types
   - Compiled to C for speed
   - Removes Python overhead
   - 5-20x faster than Python

3. C++ Backend:
   - Native C++ with SIMD vectorization
   - Maximum performance
   - Uses AVX2/NEON instructions
   - 50-1000x faster than Python
    """)
    
    # Demonstrate switching
    print("Current backend:", arrpy.get_backend())
    
    set_backend('python')
    print("Switched to:", arrpy.get_backend())
    
    set_backend('cython')
    print("Switched to:", arrpy.get_backend())


def lesson_2_compare_implementations():
    """Lesson 2: Compare the same operation across backends."""
    print("\n" + "="*60)
    print("LESSON 2: Comparing Implementations")
    print("="*60)
    
    print("""
Let's see how the same operation (array addition) is implemented
in each backend. The API is identical, but the implementation differs.
    """)
    
    # Create test arrays
    data1 = list(range(1000))
    data2 = list(range(1000, 2000))
    
    results = {}
    
    # Python backend
    print("\n1. PYTHON BACKEND:")
    print("   Implementation: Pure Python loops")
    print("   Code snippet:")
    print("""
   def _add_python(data1, data2, shape1, shape2):
       result = []
       for i in range(len(data1)):
           result.append(data1[i] + data2[i])
       return result, shape1
    """)
    
    set_backend('python')
    a = arrpy.array(data1)
    b = arrpy.array(data2)
    
    start = time.perf_counter()
    c = a + b
    py_time = (time.perf_counter() - start) * 1000
    results['python'] = py_time
    print(f"   Time: {py_time:.3f} ms")
    print(f"   Result sum: {c.sum()}")
    
    # Cython backend
    print("\n2. CYTHON BACKEND:")
    print("   Implementation: Typed memoryviews, compiled C")
    print("   Code snippet:")
    print("""
   @cython.boundscheck(False)
   def _add_cython(double[:] data1, double[:] data2):
       cdef int i
       cdef double[:] result = np.empty(len(data1))
       for i in range(len(data1)):
           result[i] = data1[i] + data2[i]
       return np.asarray(result)
    """)
    
    try:
        set_backend('cython')
        a = arrpy.array(data1)
        b = arrpy.array(data2)
        
        start = time.perf_counter()
        c = a + b
        cy_time = (time.perf_counter() - start) * 1000
        results['cython'] = cy_time
        print(f"   Time: {cy_time:.3f} ms")
        print(f"   Speedup: {py_time/cy_time:.1f}x")
    except:
        print("   Cython backend not available")
    
    # C++ backend
    print("\n3. C++ BACKEND:")
    print("   Implementation: SIMD vectorization")
    print("   Code snippet:")
    print("""
   // AVX2 SIMD addition (4 doubles at once)
   __m256d vec1 = _mm256_loadu_pd(&data1[i]);
   __m256d vec2 = _mm256_loadu_pd(&data2[i]);
   __m256d sum = _mm256_add_pd(vec1, vec2);
   _mm256_storeu_pd(&result[i], sum);
    """)
    
    try:
        set_backend('c')
        a = arrpy.array(data1)
        b = arrpy.array(data2)
        
        start = time.perf_counter()
        c = a + b
        cpp_time = (time.perf_counter() - start) * 1000
        results['c'] = cpp_time
        print(f"   Time: {cpp_time:.3f} ms")
        print(f"   Speedup: {py_time/cpp_time:.1f}x")
    except:
        print("   C++ backend not available")


def lesson_3_when_to_use_each():
    """Lesson 3: When to use each backend."""
    print("\n" + "="*60)
    print("LESSON 3: Choosing the Right Backend")
    print("="*60)
    
    print("""
WHEN TO USE EACH BACKEND:

Python Backend:
✓ Learning and understanding algorithms
✓ Debugging your code
✓ Small arrays where performance doesn't matter
✓ When you need all operations available

Cython Backend:
✓ General numerical computation
✓ Medium-sized arrays (1000-100000 elements)
✓ Good balance of speed and availability
✓ When you need Python compatibility

C++ Backend:
✓ Performance-critical code
✓ Large arrays (>100000 elements)
✓ Real-time applications
✓ When you need maximum speed

Example: Choosing backend by array size
    """)
    
    def smart_backend_selection(size):
        if size < 100:
            return 'python'  # Small arrays, overhead dominates
        elif size < 100000:
            return 'cython'  # Medium arrays, good balance
        else:
            return 'c'       # Large arrays, need max performance
    
    sizes = [50, 5000, 500000]
    
    for size in sizes:
        backend = smart_backend_selection(size)
        print(f"\nArray size {size}: Use {backend.upper()} backend")
        
        try:
            set_backend(backend)
            data = list(range(size))
            a = arrpy.array(data)
            
            start = time.perf_counter()
            result = a.sum()
            elapsed = (time.perf_counter() - start) * 1000
            
            print(f"  Sum operation: {elapsed:.3f} ms")
        except:
            print(f"  {backend} backend not available")


def lesson_4_backend_fallbacks():
    """Lesson 4: Understanding backend limitations."""
    print("\n" + "="*60)
    print("LESSON 4: Backend Limitations")
    print("="*60)
    
    print("""
Not all operations are implemented in all backends:

• Python: 100% coverage (reference implementation)
• Cython: ~30% coverage (optimized hot paths)
• C++: ~10% coverage (critical performance paths)

ArrPy doesn't use automatic fallbacks - this is intentional!
You explicitly choose performance vs. functionality.
    """)
    
    # Show which operations are available
    operations_to_test = [
        ('Addition', lambda a, b: a + b),
        ('Matrix multiply', lambda a, b: arrpy.matmul(a, b)),
        ('FFT', lambda a, b: arrpy.fft_func(a)),
        ('Solve', lambda a, b: arrpy.solve(a, b))
    ]
    
    print("\nOperation availability:")
    print("-"*40)
    
    for backend_name in ['python', 'cython', 'c']:
        print(f"\n{backend_name.upper()} Backend:")
        set_backend(backend_name)
        
        for op_name, op_func in operations_to_test:
            try:
                # Create appropriate test data
                if op_name in ['Matrix multiply', 'Solve']:
                    a = arrpy.eye(2)
                    b = arrpy.ones((2, 2)) if op_name == 'Matrix multiply' else arrpy.ones(2)
                else:
                    a = arrpy.array([1, 2, 3, 4])
                    b = arrpy.array([1, 2, 3, 4])
                
                op_func(a, b)
                print(f"  ✓ {op_name}")
            except NotImplementedError:
                print(f"  ✗ {op_name} (not implemented)")
            except Exception as e:
                print(f"  ✗ {op_name} (error)")


def lesson_5_educational_value():
    """Lesson 5: Learning from the implementations."""
    print("\n" + "="*60)
    print("LESSON 5: Educational Value")
    print("="*60)
    
    print("""
ArrPy is designed for LEARNING. Here's what you can learn:

1. ALGORITHM UNDERSTANDING (Python Backend):
   - See exactly how operations work
   - No hidden complexity
   - Step through with debugger
   - Modify and experiment

2. OPTIMIZATION TECHNIQUES (Cython Backend):
   - Type annotations for speed
   - Memory views vs Python lists
   - Bounds checking elimination
   - Parallel processing with OpenMP

3. LOW-LEVEL PERFORMANCE (C++ Backend):
   - SIMD vectorization
   - Cache optimization
   - Memory alignment
   - CPU architecture utilization

Example: Matrix Multiplication Evolution
    """)
    
    print("\nPython (O(n³) naive):")
    print("""
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i,j] += A[i,k] * B[k,j]
    """)
    
    print("\nCython (optimized loops):")
    print("""
    @cython.boundscheck(False)
    cdef double sum_val
    for i in range(m):
        for j in range(n):
            sum_val = 0
            for k in range(p):
                sum_val += A[i,k] * B[k,j]
            C[i,j] = sum_val
    """)
    
    print("\nC++ (cache blocking + SIMD):")
    print("""
    // Process in cache-friendly blocks
    for (ii = 0; ii < m; ii += BLOCK) {
        for (jj = 0; jj < n; jj += BLOCK) {
            for (kk = 0; kk < p; kk += BLOCK) {
                // SIMD operations on blocks
                __m256d sum = _mm256_setzero_pd();
                // ... vectorized computation
            }
        }
    }
    """)


def main():
    """Run all lessons."""
    print("="*60)
    print("  ArrPy Tutorial: Understanding the Backend System")
    print("="*60)
    
    lesson_1_backend_basics()
    lesson_2_compare_implementations()
    lesson_3_when_to_use_each()
    lesson_4_backend_fallbacks()
    lesson_5_educational_value()
    
    print("\n" + "="*60)
    print("  Tutorial Complete!")
    print("="*60)
    print("""
KEY TAKEAWAYS:
• ArrPy has 3 backends with different performance characteristics
• You explicitly choose between clarity and speed
• Study the implementations to learn optimization techniques
• No hidden magic - everything is transparent

Next: Run tutorial 02 to learn about broadcasting and vectorization!
    """)


if __name__ == "__main__":
    main()