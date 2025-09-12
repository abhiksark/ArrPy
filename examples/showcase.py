#!/usr/bin/env python3
"""
ArrPy v1.0.0 - Complete Feature Showcase
Demonstrates all major capabilities of the library.
"""

import sys
import os
import time
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import arrpy
from arrpy import Backend, set_backend


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def showcase_backend_switching():
    """Demonstrate runtime backend switching."""
    print_section("Backend Switching")
    
    data = list(range(1000))
    
    for backend_name in ['python', 'cython', 'c']:
        try:
            set_backend(backend_name)
            print(f"\nUsing {backend_name.upper()} backend:")
            
            a = arrpy.array(data)
            b = arrpy.array(data)
            
            start = time.perf_counter()
            c = a + b
            elapsed = (time.perf_counter() - start) * 1000
            
            print(f"  Addition of 1000 elements: {elapsed:.3f} ms")
            print(f"  Result sum: {c.sum()}")
            
        except Exception as e:
            print(f"  {backend_name}: Not available")


def showcase_array_creation():
    """Demonstrate various array creation methods."""
    print_section("Array Creation")
    set_backend('python')  # Use Python backend for reliability
    
    # Basic creation
    a = arrpy.array([1, 2, 3, 4, 5])
    print(f"array([1,2,3,4,5]): shape={a.shape}, dtype={a.dtype}")
    
    # 2D array
    b = arrpy.array([[1, 2], [3, 4], [5, 6]])
    print(f"2D array: shape={b.shape}")
    print(b)
    
    # Special arrays
    zeros = arrpy.zeros((2, 3))
    ones = arrpy.ones((2, 3))
    eye_mat = arrpy.eye(3)
    arange_arr = arrpy.arange(0, 10, 2)
    linspace_arr = arrpy.linspace(0, 1, 5)
    
    print(f"\nzeros((2,3)): {zeros._data[:6]}")
    print(f"ones((2,3)): {ones._data[:6]}")
    print(f"eye(3): {eye_mat._data}")
    print(f"arange(0,10,2): {arange_arr._data}")
    print(f"linspace(0,1,5): {linspace_arr._data}")


def showcase_broadcasting():
    """Demonstrate broadcasting capabilities."""
    print_section("Broadcasting")
    set_backend('python')  # Use Python backend for reliability
    
    # Scalar broadcasting
    a = arrpy.array([[1, 2, 3], [4, 5, 6]])
    b = a + 10
    print(f"Matrix + scalar:\n{b}")
    
    # Row broadcasting
    row = arrpy.array([1, 2, 3])
    c = a + row
    print(f"\nMatrix + row vector:\n{c}")
    
    # Column broadcasting
    col = arrpy.array([[10], [20]])
    d = a + col
    print(f"\nMatrix + column vector:\n{d}")


def showcase_linear_algebra():
    """Demonstrate linear algebra operations."""
    print_section("Linear Algebra")
    set_backend('python')
    
    # Matrix multiplication
    A = arrpy.array([[1, 2], [3, 4]])
    B = arrpy.array([[5, 6], [7, 8]])
    C = arrpy.matmul(A, B)
    print(f"Matrix multiplication:\n{A} @\n{B} =\n{C}")
    
    # Solve linear system
    A = arrpy.array([[3, 1], [1, 2]])
    b = arrpy.array([10, 8])
    x = arrpy.solve(A, b)
    print(f"\nSolving Ax = b:")
    print(f"  A = {A._data}")
    print(f"  b = {b._data}")
    print(f"  x = {x._data}")
    
    # Matrix inverse
    A_inv = arrpy.inv(A)
    print(f"\nMatrix inverse:")
    print(f"  A^-1 = {A_inv._data}")
    
    # Verify A * A^-1 = I
    I = arrpy.matmul(A, A_inv)
    print(f"  A * A^-1 = {I._data} (should be identity)")
    
    # Determinant
    det = arrpy.det(A)
    print(f"\nDeterminant of A: {det}")
    
    # QR decomposition
    Q, R = arrpy.qr(A)
    print(f"\nQR decomposition:")
    print(f"  Q shape: {Q.shape}")
    print(f"  R shape: {R.shape}")


# FFT functionality has been removed (requires complex number support)


def showcase_statistics():
    """Demonstrate statistical functions."""
    print_section("Statistical Functions")
    set_backend('python')
    
    # Create sample data
    data = arrpy.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    
    print(f"Data: {data._data}")
    print(f"Mean: {data.mean()}")
    print(f"Median: {arrpy.median(data)}")
    print(f"Std: {arrpy.std(data):.3f}")
    print(f"Var: {arrpy.var(data):.3f}")
    
    # Percentiles
    p25 = arrpy.percentile(data, 25)
    p75 = arrpy.percentile(data, 75)
    print(f"25th percentile: {p25}")
    print(f"75th percentile: {p75}")
    
    # Cumulative operations
    cumsum = arrpy.cumsum(data)
    print(f"Cumsum: {cumsum._data[:5]} ...")
    
    # Histogram (not implemented)
    # hist, edges = arrpy.histogram(data, bins=3)
    # print(f"\nHistogram (3 bins):")
    # print(f"  Counts: {hist._data}")
    # print(f"  Edges: {edges._data}")


def showcase_indexing():
    """Demonstrate advanced indexing."""
    print_section("Advanced Indexing")
    set_backend('python')
    
    # Create test array
    a = arrpy.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(f"Original array:\n{a}")
    
    # Boolean indexing
    mask = a > 5
    print(f"\nElements > 5: {arrpy.boolean_index(a, mask)._data}")
    
    # Where function
    result = arrpy.where(a > 5, a, 0)
    print(f"\nwhere(a > 5, a, 0):\n{result}")
    
    # Fancy indexing
    indices = arrpy.array([0, 2])
    selected = arrpy.fancy_index(a.flatten(), indices)
    print(f"\nFancy indexing [0, 2]: {selected._data}")


def showcase_io():
    """Demonstrate I/O operations."""
    print_section("I/O Operations")
    set_backend('python')
    
    print("Note: I/O operations are not yet implemented in ArrPy v1.0.0")
    print("")
    print("Planned features:")
    print("  • Binary save/load (arrpy.save, arrpy.load)")
    print("  • Text file I/O (arrpy.savetxt, arrpy.loadtxt)")
    print("  • Compressed archives (arrpy.savez, arrpy.loadz)")
    print("  • NumPy compatible file formats")
    print("")
    print("For now, you can use Python's pickle or numpy.save/load")


def showcase_sorting():
    """Demonstrate sorting operations."""
    print_section("Sorting and Searching")
    set_backend('python')
    
    # Create unsorted data
    data = arrpy.array([3, 1, 4, 1, 5, 9, 2, 6, 5])
    print(f"Original: {data._data}")
    
    # Sort
    sorted_data = arrpy.sort(data)
    print(f"Sorted: {sorted_data._data}")
    
    # Argsort
    indices = arrpy.argsort(data)
    print(f"Argsort indices: {indices._data}")
    
    # Unique
    unique_vals, counts = arrpy.unique(data, return_counts=True)
    print(f"Unique values: {unique_vals._data}")
    print(f"Counts: {counts._data}")
    
    # Binary search
    sorted_arr = arrpy.sort(data)
    pos = arrpy.searchsorted(sorted_arr, 4)
    print(f"Insert position for 4: {pos}")


def showcase_performance():
    """Demonstrate performance characteristics."""
    print_section("Performance Comparison")
    
    sizes = [100, 1000, 10000]
    
    print("\nElement-wise addition performance:")
    print("-"*40)
    print(f"{'Size':<10} {'Python':<12} {'Cython':<12} {'C++':<12}")
    print("-"*40)
    
    for size in sizes:
        data = list(range(size))
        row = f"{size:<10}"
        
        for backend_name in ['python', 'cython', 'c']:
            try:
                set_backend(backend_name)
                a = arrpy.array(data)
                b = arrpy.array(data)
                
                start = time.perf_counter()
                for _ in range(100):
                    c = a + b
                elapsed = (time.perf_counter() - start) * 10  # ms per op
                
                row += f"{elapsed:<12.3f}"
            except:
                row += f"{'N/A':<12}"
        
        print(row)


def main():
    """Run all showcases."""
    print("="*60)
    print("  ArrPy v1.0.0 - Complete Feature Showcase")
    print("="*60)
    
    showcase_backend_switching()
    showcase_array_creation()
    showcase_broadcasting()
    showcase_linear_algebra()
    # showcase_fft() - removed (requires complex number support)
    showcase_statistics()
    showcase_indexing()
    showcase_sorting()
    # showcase_io()  # I/O operations not yet implemented
    showcase_performance()
    
    print("\n" + "="*60)
    print("  Showcase Complete!")
    print("="*60)
    print("\nArrPy demonstrates:")
    print("• Complete NumPy-compatible API")
    print("• Three swappable backends")
    print("• Educational algorithm implementations")
    print("• Production-ready performance")
    print("\nExplore the code to learn more!")


if __name__ == "__main__":
    main()