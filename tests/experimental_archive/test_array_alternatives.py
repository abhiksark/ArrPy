#!/usr/bin/env python3
"""
Test and benchmark alternative array storage approaches for ArrPy.
Evaluates different unified storage solutions for Python/C++ interoperability.
"""

import array
import ctypes
import mmap
import struct
import time
import sys
import numpy as np
from typing import List, Tuple
import gc

class BenchmarkResults:
    """Store and format benchmark results."""
    def __init__(self):
        self.results = {}
    
    def add(self, name, creation_time, access_time, modification_time, memory_bytes):
        self.results[name] = {
            'creation': creation_time * 1000,  # ms
            'access': access_time * 1000,
            'modification': modification_time * 1000,
            'memory': memory_bytes / (1024 * 1024)  # MB
        }
    
    def print_results(self):
        print("\n" + "="*80)
        print("Alternative Array Storage Benchmark Results")
        print("="*80)
        print(f"{'Method':<25} {'Create(ms)':<12} {'Access(ms)':<12} {'Modify(ms)':<12} {'Memory(MB)':<10}")
        print("-"*80)
        
        for name, metrics in self.results.items():
            print(f"{name:<25} {metrics['creation']:<12.3f} {metrics['access']:<12.3f} "
                  f"{metrics['modification']:<12.3f} {metrics['memory']:<10.2f}")


def benchmark_python_list(size: int) -> Tuple[float, float, float, int]:
    """Benchmark Python list (baseline)."""
    # Creation
    gc.collect()
    start = time.perf_counter()
    data = [float(i) for i in range(size)]
    creation_time = time.perf_counter() - start
    
    # Access
    start = time.perf_counter()
    total = sum(data[i] for i in range(0, size, 100))
    access_time = time.perf_counter() - start
    
    # Modification
    start = time.perf_counter()
    for i in range(0, size, 100):
        data[i] *= 2
    modification_time = time.perf_counter() - start
    
    # Memory estimate (8 bytes per float + Python object overhead ~24 bytes)
    memory = size * 32
    
    return creation_time, access_time, modification_time, memory


def benchmark_array_module(size: int) -> Tuple[float, float, float, int]:
    """Benchmark Python's built-in array module."""
    # Creation
    gc.collect()
    start = time.perf_counter()
    data = array.array('d', (float(i) for i in range(size)))
    creation_time = time.perf_counter() - start
    
    # Access via buffer protocol
    start = time.perf_counter()
    mv = memoryview(data)
    total = sum(mv[i] for i in range(0, size, 100))
    access_time = time.perf_counter() - start
    
    # Modification
    start = time.perf_counter()
    for i in range(0, size, 100):
        data[i] *= 2
    modification_time = time.perf_counter() - start
    
    # Memory (8 bytes per double)
    memory = data.buffer_info()[1] * data.itemsize
    
    return creation_time, access_time, modification_time, memory


def benchmark_memoryview(size: int) -> Tuple[float, float, float, int]:
    """Benchmark memoryview with bytearray backend."""
    # Creation
    gc.collect()
    start = time.perf_counter()
    # Create bytearray and wrap with memoryview
    raw_data = bytearray(size * 8)  # 8 bytes per double
    mv = memoryview(raw_data).cast('d')
    for i in range(size):
        mv[i] = float(i)
    creation_time = time.perf_counter() - start
    
    # Access
    start = time.perf_counter()
    total = sum(mv[i] for i in range(0, size, 100))
    access_time = time.perf_counter() - start
    
    # Modification
    start = time.perf_counter()
    for i in range(0, size, 100):
        mv[i] *= 2
    modification_time = time.perf_counter() - start
    
    # Memory
    memory = len(raw_data)
    
    return creation_time, access_time, modification_time, memory


def benchmark_ctypes_array(size: int) -> Tuple[float, float, float, int]:
    """Benchmark ctypes array for C interop."""
    # Creation
    gc.collect()
    start = time.perf_counter()
    ArrayType = ctypes.c_double * size
    data = ArrayType()
    for i in range(size):
        data[i] = float(i)
    creation_time = time.perf_counter() - start
    
    # Access (direct C-style)
    start = time.perf_counter()
    total = sum(data[i] for i in range(0, size, 100))
    access_time = time.perf_counter() - start
    
    # Modification
    start = time.perf_counter()
    for i in range(0, size, 100):
        data[i] *= 2
    modification_time = time.perf_counter() - start
    
    # Memory
    memory = ctypes.sizeof(data)
    
    return creation_time, access_time, modification_time, memory


def benchmark_mmap_array(size: int) -> Tuple[float, float, float, int]:
    """Benchmark memory-mapped array."""
    import tempfile
    import os
    
    # Create temporary file
    fd, filepath = tempfile.mkstemp()
    
    try:
        # Creation
        gc.collect()
        start = time.perf_counter()
        
        # Write initial data
        with open(filepath, 'wb') as f:
            for i in range(size):
                f.write(struct.pack('d', float(i)))
        
        # Memory map the file
        with open(filepath, 'r+b') as f:
            mm = mmap.mmap(f.fileno(), size * 8)
        
        creation_time = time.perf_counter() - start
        
        # Access
        start = time.perf_counter()
        total = 0
        for i in range(0, size, 100):
            offset = i * 8
            value = struct.unpack('d', mm[offset:offset+8])[0]
            total += value
        access_time = time.perf_counter() - start
        
        # Modification
        start = time.perf_counter()
        for i in range(0, size, 100):
            offset = i * 8
            old_value = struct.unpack('d', mm[offset:offset+8])[0]
            mm[offset:offset+8] = struct.pack('d', old_value * 2)
        modification_time = time.perf_counter() - start
        
        # Memory (file size)
        memory = size * 8
        
        mm.close()
        
    finally:
        os.close(fd)
        os.unlink(filepath)
    
    return creation_time, access_time, modification_time, memory


def benchmark_numpy_array(size: int) -> Tuple[float, float, float, int]:
    """Benchmark NumPy array (reference)."""
    # Creation
    gc.collect()
    start = time.perf_counter()
    data = np.arange(size, dtype=np.float64)
    creation_time = time.perf_counter() - start
    
    # Access
    start = time.perf_counter()
    total = data[::100].sum()
    access_time = time.perf_counter() - start
    
    # Modification
    start = time.perf_counter()
    data[::100] *= 2
    modification_time = time.perf_counter() - start
    
    # Memory
    memory = data.nbytes
    
    return creation_time, access_time, modification_time, memory


def test_buffer_protocol_compatibility():
    """Test buffer protocol support for each approach."""
    print("\n" + "="*80)
    print("Buffer Protocol Compatibility Test")
    print("="*80)
    
    size = 1000
    
    # Python array module
    arr = array.array('d', range(size))
    print(f"array.array:     Supports buffer protocol: {hasattr(arr, '__buffer__')}")
    print(f"                 Can create memoryview: {memoryview(arr) is not None}")
    
    # Bytearray with memoryview
    ba = bytearray(size * 8)
    mv = memoryview(ba).cast('d')
    print(f"memoryview:      Supports buffer protocol: {hasattr(mv, '__buffer__')}")
    print(f"                 C-contiguous: {mv.c_contiguous}")
    
    # ctypes array
    CArray = ctypes.c_double * size
    ct_arr = CArray()
    print(f"ctypes array:    Supports buffer protocol: {hasattr(ct_arr, '__buffer__')}")
    try:
        mv_ct = memoryview(ct_arr)
        print(f"                 Can create memoryview: True")
    except:
        print(f"                 Can create memoryview: False")
    
    # NumPy array
    np_arr = np.arange(size, dtype=np.float64)
    print(f"numpy.ndarray:   Supports buffer protocol: {hasattr(np_arr, '__buffer__')}")
    print(f"                 Can create memoryview: {memoryview(np_arr) is not None}")


def test_c_interop():
    """Test C/C++ interoperability for each approach."""
    print("\n" + "="*80)
    print("C/C++ Interoperability Test")
    print("="*80)
    
    size = 1000
    
    # Python array module
    arr = array.array('d', range(size))
    info = arr.buffer_info()
    print(f"array.array:     Direct pointer access: address={hex(info[0])}, size={info[1]}")
    
    # ctypes array
    CArray = ctypes.c_double * size
    ct_arr = CArray()
    ptr = ctypes.cast(ct_arr, ctypes.POINTER(ctypes.c_double))
    print(f"ctypes array:    Direct pointer access: address={hex(ctypes.addressof(ct_arr))}")
    
    # Memoryview
    ba = bytearray(size * 8)
    mv = memoryview(ba).cast('d')
    # Can't get direct pointer from memoryview easily
    print(f"memoryview:      Buffer protocol access only (no direct pointer)")
    
    # NumPy array
    np_arr = np.arange(size, dtype=np.float64)
    ptr_value = np_arr.__array_interface__['data'][0]
    print(f"numpy.ndarray:   Direct pointer access: address={hex(ptr_value)}")


def main():
    """Run all benchmarks and tests."""
    print("Testing Alternative Array Storage Approaches for ArrPy")
    print("="*80)
    
    # Test different sizes
    sizes = [1000, 10000, 100000]
    
    for size in sizes:
        print(f"\nBenchmarking with {size:,} elements...")
        
        results = BenchmarkResults()
        
        # Run benchmarks
        print("  Testing Python list...")
        results.add("Python list (baseline)", *benchmark_python_list(size))
        
        print("  Testing array.array...")
        results.add("array.array", *benchmark_array_module(size))
        
        print("  Testing memoryview...")
        results.add("memoryview + bytearray", *benchmark_memoryview(size))
        
        print("  Testing ctypes array...")
        results.add("ctypes.c_double array", *benchmark_ctypes_array(size))
        
        if size <= 10000:  # mmap is slow for large sizes
            print("  Testing mmap...")
            results.add("mmap array", *benchmark_mmap_array(size))
        
        print("  Testing NumPy...")
        results.add("numpy.ndarray (reference)", *benchmark_numpy_array(size))
        
        results.print_results()
    
    # Additional tests
    test_buffer_protocol_compatibility()
    test_c_interop()
    
    # Print recommendations
    print("\n" + "="*80)
    print("RECOMMENDATIONS")
    print("="*80)
    print("""
1. **array.array with Buffer Protocol** (RECOMMENDED)
   - Pros: Built-in, low memory overhead, buffer protocol support
   - Cons: Limited dtype support, no direct SIMD
   - Use case: General-purpose array storage with C interop

2. **ctypes arrays** (BEST FOR C++ INTEGRATION)
   - Pros: Direct C memory layout, zero-copy to C functions
   - Cons: Slower Python access, manual memory management
   - Use case: When C++ performance is critical

3. **memoryview + bytearray** (MOST FLEXIBLE)
   - Pros: Very flexible, supports multiple dtypes, zero-copy slicing
   - Cons: More complex API, manual type casting
   - Use case: Advanced memory manipulation

4. **Custom Buffer with DLPack** (FUTURE-PROOF)
   - Pros: Industry standard, GPU support, framework interop
   - Cons: Requires implementation, external dependency
   - Use case: If planning GPU support or ML framework integration
    """)


if __name__ == "__main__":
    main()