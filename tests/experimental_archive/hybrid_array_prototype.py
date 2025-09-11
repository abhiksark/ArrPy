#!/usr/bin/env python3
"""
Hybrid array storage prototype for ArrPy.
Combines best aspects of different approaches for optimal performance and flexibility.
"""

import array
import ctypes
import numpy as np
from enum import Enum
from typing import Union, Tuple, Optional
import time

class StorageBackend(Enum):
    """Available storage backends."""
    PYTHON_LIST = "python_list"      # Original, for compatibility
    ARRAY_MODULE = "array_module"    # Python's array module
    CTYPES_ARRAY = "ctypes_array"   # ctypes for C interop
    NUMPY_ARRAY = "numpy_array"      # NumPy for comparison
    
class HybridArray:
    """
    Hybrid array implementation that can switch storage backends.
    Provides unified interface regardless of underlying storage.
    """
    
    def __init__(self, data=None, shape=None, dtype='float64', backend=StorageBackend.ARRAY_MODULE):
        """
        Initialize hybrid array with specified backend.
        
        Parameters:
        -----------
        data : list, array-like, or None
            Initial data
        shape : tuple or None
            Shape of array (for empty initialization)
        dtype : str
            Data type ('float64', 'float32', 'int32')
        backend : StorageBackend
            Storage backend to use
        """
        self.dtype = dtype
        self.backend = backend
        
        # Determine shape and size
        if data is not None:
            self.shape = self._get_shape(data)
            self.size = self._calculate_size(self.shape)
            self._initialize_from_data(data)
        elif shape is not None:
            self.shape = shape if isinstance(shape, tuple) else (shape,)
            self.size = self._calculate_size(self.shape)
            self._initialize_empty()
        else:
            raise ValueError("Either data or shape must be provided")
        
        # Calculate strides
        self.strides = self._calculate_strides(self.shape)
        
    def _get_shape(self, data):
        """Get shape from nested data."""
        if not isinstance(data, (list, tuple)):
            return ()
        shape = []
        current = data
        while isinstance(current, (list, tuple)):
            shape.append(len(current))
            if len(current) == 0:
                break
            current = current[0]
        return tuple(shape)
    
    def _calculate_size(self, shape):
        """Calculate total number of elements."""
        size = 1
        for dim in shape:
            size *= dim
        return size
    
    def _calculate_strides(self, shape):
        """Calculate strides for row-major layout."""
        if len(shape) == 0:
            return ()
        strides = []
        stride = 1
        for dim in reversed(shape[1:]):
            strides.append(stride)
            stride *= dim
        strides.append(stride)
        return tuple(reversed(strides))
    
    def _flatten_data(self, data):
        """Flatten nested data to 1D."""
        if not isinstance(data, (list, tuple)):
            return [data]
        flat = []
        def flatten_recursive(item):
            if isinstance(item, (list, tuple)):
                for subitem in item:
                    flatten_recursive(subitem)
            else:
                flat.append(item)
        flatten_recursive(data)
        return flat
    
    def _initialize_from_data(self, data):
        """Initialize storage from provided data."""
        flat_data = self._flatten_data(data)
        
        if self.backend == StorageBackend.PYTHON_LIST:
            self._storage = flat_data
            
        elif self.backend == StorageBackend.ARRAY_MODULE:
            if self.dtype == 'float64':
                self._storage = array.array('d', flat_data)
            elif self.dtype == 'float32':
                self._storage = array.array('f', flat_data)
            elif self.dtype == 'int32':
                self._storage = array.array('i', flat_data)
                
        elif self.backend == StorageBackend.CTYPES_ARRAY:
            if self.dtype == 'float64':
                ArrayType = ctypes.c_double * self.size
            elif self.dtype == 'float32':
                ArrayType = ctypes.c_float * self.size
            elif self.dtype == 'int32':
                ArrayType = ctypes.c_int32 * self.size
            self._storage = ArrayType(*flat_data)
            
        elif self.backend == StorageBackend.NUMPY_ARRAY:
            self._storage = np.array(data, dtype=self.dtype).ravel()
    
    def _initialize_empty(self):
        """Initialize empty storage."""
        if self.backend == StorageBackend.PYTHON_LIST:
            self._storage = [0] * self.size
            
        elif self.backend == StorageBackend.ARRAY_MODULE:
            if self.dtype == 'float64':
                self._storage = array.array('d', [0.0] * self.size)
            elif self.dtype == 'float32':
                self._storage = array.array('f', [0.0] * self.size)
            elif self.dtype == 'int32':
                self._storage = array.array('i', [0] * self.size)
                
        elif self.backend == StorageBackend.CTYPES_ARRAY:
            if self.dtype == 'float64':
                ArrayType = ctypes.c_double * self.size
            elif self.dtype == 'float32':
                ArrayType = ctypes.c_float * self.size
            elif self.dtype == 'int32':
                ArrayType = ctypes.c_int32 * self.size
            self._storage = ArrayType()
            
        elif self.backend == StorageBackend.NUMPY_ARRAY:
            self._storage = np.zeros(self.size, dtype=self.dtype)
    
    def get_c_pointer(self) -> Optional[int]:
        """Get C pointer to underlying data (if available)."""
        if self.backend == StorageBackend.ARRAY_MODULE:
            return self._storage.buffer_info()[0]
        elif self.backend == StorageBackend.CTYPES_ARRAY:
            return ctypes.addressof(self._storage)
        elif self.backend == StorageBackend.NUMPY_ARRAY:
            return self._storage.__array_interface__['data'][0]
        else:
            return None
    
    def to_memoryview(self):
        """Get memoryview of data (for buffer protocol)."""
        if self.backend == StorageBackend.ARRAY_MODULE:
            return memoryview(self._storage)
        elif self.backend == StorageBackend.CTYPES_ARRAY:
            return memoryview(self._storage)
        elif self.backend == StorageBackend.NUMPY_ARRAY:
            return memoryview(self._storage)
        else:
            raise NotImplementedError(f"memoryview not available for {self.backend}")
    
    def __getitem__(self, idx):
        """Get item by index."""
        if isinstance(idx, int):
            return self._storage[idx]
        elif isinstance(idx, tuple):
            flat_idx = 0
            for i, index in enumerate(idx):
                flat_idx += index * self.strides[i]
            return self._storage[flat_idx]
    
    def __setitem__(self, idx, value):
        """Set item by index."""
        if isinstance(idx, int):
            self._storage[idx] = value
        elif isinstance(idx, tuple):
            flat_idx = 0
            for i, index in enumerate(idx):
                flat_idx += index * self.strides[i]
            self._storage[flat_idx] = value
    
    def convert_backend(self, new_backend: StorageBackend):
        """Convert array to different storage backend."""
        if new_backend == self.backend:
            return self
        
        # Get current data as list
        if self.backend == StorageBackend.PYTHON_LIST:
            data = self._storage
        elif self.backend == StorageBackend.NUMPY_ARRAY:
            data = self._storage.tolist()
        else:
            data = list(self._storage)
        
        # Create new array with different backend - preserve original shape
        new_arr = HybridArray(shape=self.shape, dtype=self.dtype, backend=new_backend)
        for i, val in enumerate(data):
            new_arr._storage[i] = val
        return new_arr
    
    def __repr__(self):
        return f"HybridArray(shape={self.shape}, dtype={self.dtype}, backend={self.backend.value})"


def benchmark_hybrid_backends():
    """Benchmark different storage backends in hybrid array."""
    print("Hybrid Array Backend Benchmarks")
    print("="*80)
    
    sizes = [1000, 10000, 100000]
    operations = ['creation', 'sequential_access', 'random_access', 'modification']
    
    for size in sizes:
        print(f"\nSize: {size:,} elements")
        print("-"*60)
        
        results = {}
        test_data = list(range(size))
        
        for backend in StorageBackend:
            results[backend] = {}
            
            # Creation
            start = time.perf_counter()
            arr = HybridArray(data=test_data, backend=backend)
            results[backend]['creation'] = (time.perf_counter() - start) * 1000
            
            # Sequential access
            start = time.perf_counter()
            total = sum(arr[i] for i in range(0, min(1000, size)))
            results[backend]['sequential'] = (time.perf_counter() - start) * 1000
            
            # Random access
            import random
            indices = [random.randint(0, size-1) for _ in range(100)]
            start = time.perf_counter()
            total = sum(arr[i] for i in indices)
            results[backend]['random'] = (time.perf_counter() - start) * 1000
            
            # Modification
            start = time.perf_counter()
            for i in range(0, min(100, size)):
                arr[i] = arr[i] * 2
            results[backend]['modification'] = (time.perf_counter() - start) * 1000
            
            # C pointer availability
            c_ptr = arr.get_c_pointer()
            results[backend]['c_pointer'] = c_ptr is not None
        
        # Print results
        print(f"{'Backend':<20} {'Create(ms)':<12} {'Seq(ms)':<12} {'Rand(ms)':<12} {'Mod(ms)':<12} {'C Ptr':<8}")
        for backend in StorageBackend:
            r = results[backend]
            c_ptr_str = "Yes" if r['c_pointer'] else "No"
            print(f"{backend.value:<20} {r['creation']:<12.3f} {r['sequential']:<12.3f} "
                  f"{r['random']:<12.3f} {r['modification']:<12.3f} {c_ptr_str:<8}")


def test_backend_conversion():
    """Test conversion between different backends."""
    print("\nBackend Conversion Test")
    print("="*80)
    
    # Create initial array
    data = [[1, 2, 3], [4, 5, 6]]
    arr_list = HybridArray(data=data, backend=StorageBackend.PYTHON_LIST)
    print(f"Original: {arr_list}")
    
    # Convert to different backends
    arr_array = arr_list.convert_backend(StorageBackend.ARRAY_MODULE)
    print(f"To array.array: {arr_array}")
    
    arr_ctypes = arr_list.convert_backend(StorageBackend.CTYPES_ARRAY)
    print(f"To ctypes: {arr_ctypes}")
    
    # Verify data integrity
    print("\nData integrity check:")
    for i in range(2):
        for j in range(3):
            idx = (i, j)
            val_list = arr_list[idx]
            val_array = arr_array[idx]
            val_ctypes = arr_ctypes[idx]
            print(f"  [{i},{j}]: list={val_list}, array={val_array}, ctypes={val_ctypes}")
            assert val_list == val_array == val_ctypes


def demonstrate_c_integration():
    """Demonstrate C/C++ integration capabilities."""
    print("\nC/C++ Integration Demonstration")
    print("="*80)
    
    size = 1000
    
    for backend in [StorageBackend.ARRAY_MODULE, StorageBackend.CTYPES_ARRAY]:
        arr = HybridArray(shape=(size,), dtype='float64', backend=backend)
        
        # Fill with test data
        for i in range(size):
            arr[i] = float(i)
        
        c_ptr = arr.get_c_pointer()
        if c_ptr:
            print(f"\n{backend.value}:")
            print(f"  C pointer: 0x{c_ptr:x}")
            print(f"  Can pass to C function: Yes")
            
            # Show example C function signature
            print(f"  Example C function:")
            print(f"    void process_array(double* data, int size) {{")
            print(f"        // Direct SIMD operations on data")
            print(f"    }}")
            
            # Could call actual C function here if compiled
            # result = c_lib.process_array(c_ptr, size)


def propose_final_architecture():
    """Propose final architecture for ArrPy."""
    print("\n" + "="*80)
    print("PROPOSED HYBRID ARCHITECTURE FOR ARRPY")
    print("="*80)
    
    print("""
## Core Design

1. **Primary Storage**: Python's array.array
   - Built-in, no external dependencies
   - Low memory overhead (8 bytes per float64)
   - Buffer protocol support
   - Direct C pointer access via buffer_info()

2. **Backend-Specific Optimization**:
   
   a) Python Backend:
      - Use array.array directly
      - Pure Python operations for clarity
   
   b) Cython Backend:
      - Use memoryview on array.array
      - Zero-copy access with typed memoryviews
      - Parallel operations with OpenMP
   
   c) C++ Backend:
      - Direct pointer from array.array.buffer_info()
      - Zero-copy SIMD operations
      - Optional DLPack wrapper for framework interop

3. **Migration Path**:
   
   Phase 1: Replace Python list with array.array
   - Minimal code changes
   - Immediate memory savings
   - C pointer availability
   
   Phase 2: Update backends for zero-copy
   - Cython: Use memoryviews
   - C++: Use direct pointers
   
   Phase 3: Add DLPack support (optional)
   - For ML framework integration
   - GPU support preparation

## Implementation Example:

```python
class ArrPy:
    def __init__(self, data, dtype=None):
        # Use array.array as primary storage
        if dtype == float64:
            self._data = array.array('d', self._flatten_data(data))
        else:
            self._data = array.array('f', self._flatten_data(data))
        
        self._shape = self._get_shape(data)
        self._dtype = dtype or float64
    
    def __add__(self, other):
        backend = get_backend()
        
        if backend == Backend.PYTHON:
            # Pure Python with array.array
            result = array.array('d')
            for i in range(len(self._data)):
                result.append(self._data[i] + other._data[i])
            return ArrPy._from_array(result, self._shape)
        
        elif backend == Backend.CYTHON:
            # Zero-copy with memoryview
            from .backends.cython import ops
            mv_self = memoryview(self._data)
            mv_other = memoryview(other._data)
            result = ops.add_memoryview(mv_self, mv_other)
            return ArrPy._from_array(result, self._shape)
        
        elif backend == Backend.C:
            # Direct pointer access
            from .backends.c import ops
            ptr_self = self._data.buffer_info()[0]
            ptr_other = other._data.buffer_info()[0]
            size = len(self._data)
            result_ptr = ops.add_simd(ptr_self, ptr_other, size)
            # Wrap result back in array.array
            return ArrPy._from_pointer(result_ptr, size, self._shape)
```

## Benefits:

1. **Simplicity**: One storage type, clear semantics
2. **Performance**: Zero-copy to C++, 10-100x speedup achievable
3. **Memory**: 4x less memory than Python lists
4. **Compatibility**: Works with existing Python ecosystem
5. **Educational**: Clear progression from simple to optimized
    """)


if __name__ == "__main__":
    benchmark_hybrid_backends()
    test_backend_conversion()
    demonstrate_c_integration()
    propose_final_architecture()