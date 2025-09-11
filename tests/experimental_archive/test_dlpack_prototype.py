#!/usr/bin/env python3
"""
DLPack-style buffer protocol implementation prototype for ArrPy.
DLPack is an open standard for tensor data structure to share tensors among frameworks.
"""

import ctypes
import array
import struct
from enum import IntEnum
from typing import Optional, Tuple

class DLDataTypeCode(IntEnum):
    """DLPack data type codes."""
    kDLInt = 0
    kDLUInt = 1
    kDLFloat = 2
    kDLBfloat = 3
    kDLComplex = 4

class DLDeviceType(IntEnum):
    """DLPack device type codes."""
    kDLCPU = 1
    kDLCUDA = 2
    kDLCUDAHost = 3
    kDLOpenCL = 4
    kDLVulkan = 7
    kDLMetal = 8
    kDLVPI = 9
    kDLROCM = 10

class DLDataType(ctypes.Structure):
    """DLPack data type descriptor."""
    _fields_ = [
        ("code", ctypes.c_uint8),      # Type code
        ("bits", ctypes.c_uint8),      # Number of bits
        ("lanes", ctypes.c_uint16)     # Number of lanes (for SIMD)
    ]

class DLDevice(ctypes.Structure):
    """DLPack device descriptor."""
    _fields_ = [
        ("device_type", ctypes.c_int32),  # Device type
        ("device_id", ctypes.c_int32)     # Device id
    ]

class DLTensor(ctypes.Structure):
    """DLPack tensor structure - compatible with C/C++."""
    _fields_ = [
        ("data", ctypes.c_void_p),              # Data pointer
        ("device", DLDevice),                    # Device info
        ("ndim", ctypes.c_int32),               # Number of dimensions
        ("dtype", DLDataType),                   # Data type
        ("shape", ctypes.POINTER(ctypes.c_int64)),    # Shape
        ("strides", ctypes.POINTER(ctypes.c_int64)),  # Strides
        ("byte_offset", ctypes.c_uint64)        # Byte offset
    ]

class DLManagedTensor(ctypes.Structure):
    """Managed DLTensor with deleter for memory management."""
    _fields_ = [
        ("dl_tensor", DLTensor),
        ("manager_ctx", ctypes.c_void_p),
        ("deleter", ctypes.CFUNCTYPE(None, ctypes.c_void_p))
    ]

class DLPackArray:
    """
    ArrPy array implementation using DLPack-compatible storage.
    This allows zero-copy data exchange with C++ and other frameworks.
    """
    
    def __init__(self, shape: Tuple[int, ...], dtype='float64'):
        """Initialize DLPack-compatible array."""
        self.shape = shape
        self.dtype = dtype
        self.ndim = len(shape)
        
        # Calculate size
        self.size = 1
        for dim in shape:
            self.size *= dim
        
        # Create underlying storage based on dtype
        if dtype == 'float64':
            self._array = array.array('d', [0.0] * self.size)
            self._itemsize = 8
            self._typecode = DLDataTypeCode.kDLFloat
            self._bits = 64
        elif dtype == 'float32':
            self._array = array.array('f', [0.0] * self.size)
            self._itemsize = 4
            self._typecode = DLDataTypeCode.kDLFloat
            self._bits = 32
        elif dtype == 'int32':
            self._array = array.array('i', [0] * self.size)
            self._itemsize = 4
            self._typecode = DLDataTypeCode.kDLInt
            self._bits = 32
        else:
            raise ValueError(f"Unsupported dtype: {dtype}")
        
        # Calculate strides (in number of elements, not bytes)
        self.strides = self._calculate_strides(shape)
        
        # Create DLPack tensor
        self._create_dl_tensor()
    
    def _calculate_strides(self, shape):
        """Calculate strides for row-major (C-order) layout."""
        strides = []
        stride = 1
        for dim in reversed(shape):
            strides.append(stride)
            stride *= dim
        return tuple(reversed(strides))
    
    def _create_dl_tensor(self):
        """Create DLPack tensor structure."""
        # Get buffer info
        buffer_info = self._array.buffer_info()
        
        # Create shape array
        self._shape_arr = (ctypes.c_int64 * self.ndim)(*self.shape)
        
        # Create strides array (in bytes)
        strides_bytes = [s * self._itemsize for s in self.strides]
        self._strides_arr = (ctypes.c_int64 * self.ndim)(*strides_bytes)
        
        # Create DLDataType
        self._dl_dtype = DLDataType(
            code=self._typecode,
            bits=self._bits,
            lanes=1  # Not using SIMD lanes at Python level
        )
        
        # Create DLDevice (CPU)
        self._dl_device = DLDevice(
            device_type=DLDeviceType.kDLCPU,
            device_id=0
        )
        
        # Create DLTensor
        self.dl_tensor = DLTensor(
            data=buffer_info[0],  # Pointer to data
            device=self._dl_device,
            ndim=self.ndim,
            dtype=self._dl_dtype,
            shape=self._shape_arr,
            strides=self._strides_arr,
            byte_offset=0
        )
    
    def __getitem__(self, idx):
        """Get item using index."""
        if isinstance(idx, int):
            # 1D indexing
            return self._array[idx]
        elif isinstance(idx, tuple):
            # Multi-dimensional indexing
            flat_idx = 0
            for i, index in enumerate(idx):
                flat_idx += index * self.strides[i]
            return self._array[flat_idx]
    
    def __setitem__(self, idx, value):
        """Set item using index."""
        if isinstance(idx, int):
            self._array[idx] = value
        elif isinstance(idx, tuple):
            flat_idx = 0
            for i, index in enumerate(idx):
                flat_idx += index * self.strides[i]
            self._array[flat_idx] = value
    
    def to_dlpack(self):
        """Export as DLPack capsule (for framework interop)."""
        # In real implementation, would return PyCapsule
        # For now, return the DLTensor structure
        return self.dl_tensor
    
    @classmethod
    def from_dlpack(cls, dl_tensor):
        """Create array from DLPack tensor."""
        # Extract info from DLTensor
        ndim = dl_tensor.ndim
        shape = tuple(dl_tensor.shape[i] for i in range(ndim))
        
        # Determine dtype
        if dl_tensor.dtype.code == DLDataTypeCode.kDLFloat:
            if dl_tensor.dtype.bits == 64:
                dtype = 'float64'
            elif dl_tensor.dtype.bits == 32:
                dtype = 'float32'
        elif dl_tensor.dtype.code == DLDataTypeCode.kDLInt:
            if dl_tensor.dtype.bits == 32:
                dtype = 'int32'
        
        # Create new array
        arr = cls(shape, dtype)
        
        # Copy data (in real implementation, could share memory)
        # This is simplified - would need proper memory management
        return arr
    
    def get_c_pointer(self):
        """Get raw C pointer for direct C++ access."""
        return self.dl_tensor.data
    
    def __repr__(self):
        return f"DLPackArray(shape={self.shape}, dtype={self.dtype})"


def test_dlpack_array():
    """Test DLPack array implementation."""
    print("Testing DLPack Array Implementation")
    print("="*60)
    
    # Create 2D array
    arr = DLPackArray((3, 4), dtype='float64')
    
    # Set some values
    for i in range(3):
        for j in range(4):
            arr[i, j] = i * 4 + j
    
    # Test access
    print(f"Array: {arr}")
    print(f"Shape: {arr.shape}")
    print(f"Strides: {arr.strides}")
    print(f"Size: {arr.size}")
    
    # Test indexing
    print(f"\nArray[1, 2] = {arr[1, 2]}")
    print(f"Array[2, 3] = {arr[2, 3]}")
    
    # Get DLPack tensor
    dl_tensor = arr.to_dlpack()
    print(f"\nDLTensor:")
    print(f"  Data pointer: 0x{dl_tensor.data:x}")
    print(f"  Device: CPU (type={dl_tensor.device.device_type})")
    print(f"  Dtype: code={dl_tensor.dtype.code}, bits={dl_tensor.dtype.bits}")
    print(f"  Ndim: {dl_tensor.ndim}")
    
    # Get C pointer
    c_ptr = arr.get_c_pointer()
    print(f"\nC pointer: 0x{c_ptr:x}")
    
    # Show memory layout
    print(f"\nMemory layout (row-major):")
    for i in range(arr.size):
        print(f"  [{i}]: {arr._array[i]:.1f}", end="")
        if (i + 1) % 4 == 0:
            print()  # New row


def benchmark_dlpack_vs_alternatives():
    """Compare DLPack approach with other alternatives."""
    import time
    import numpy as np
    
    print("\n" + "="*60)
    print("DLPack vs Other Approaches - Performance Comparison")
    print("="*60)
    
    size = 100000
    iterations = 100
    
    # DLPack array
    print("\n1. DLPack Array:")
    start = time.perf_counter()
    dlpack_arr = DLPackArray((size,), dtype='float64')
    for i in range(0, size, 100):
        dlpack_arr[i] = float(i)
    creation_time = time.perf_counter() - start
    
    start = time.perf_counter()
    for _ in range(iterations):
        total = sum(dlpack_arr[i] for i in range(0, size, 1000))
    access_time = (time.perf_counter() - start) / iterations
    
    print(f"   Creation: {creation_time*1000:.3f} ms")
    print(f"   Access: {access_time*1000:.3f} ms")
    print(f"   C pointer: 0x{dlpack_arr.get_c_pointer():x}")
    
    # Python array.array
    print("\n2. Python array.array:")
    start = time.perf_counter()
    py_arr = array.array('d', [0.0] * size)
    for i in range(0, size, 100):
        py_arr[i] = float(i)
    creation_time = time.perf_counter() - start
    
    start = time.perf_counter()
    for _ in range(iterations):
        total = sum(py_arr[i] for i in range(0, size, 1000))
    access_time = (time.perf_counter() - start) / iterations
    
    buffer_info = py_arr.buffer_info()
    print(f"   Creation: {creation_time*1000:.3f} ms")
    print(f"   Access: {access_time*1000:.3f} ms")
    print(f"   C pointer: 0x{buffer_info[0]:x}")
    
    # NumPy array
    print("\n3. NumPy array:")
    start = time.perf_counter()
    np_arr = np.zeros(size, dtype=np.float64)
    np_arr[::100] = np.arange(0, size, 100)
    creation_time = time.perf_counter() - start
    
    start = time.perf_counter()
    for _ in range(iterations):
        total = np_arr[::1000].sum()
    access_time = (time.perf_counter() - start) / iterations
    
    print(f"   Creation: {creation_time*1000:.3f} ms")
    print(f"   Access: {access_time*1000:.3f} ms")
    print(f"   C pointer: 0x{np_arr.__array_interface__['data'][0]:x}")


def show_dlpack_advantages():
    """Demonstrate advantages of DLPack approach."""
    print("\n" + "="*60)
    print("DLPack Advantages for ArrPy")
    print("="*60)
    
    print("""
1. **Framework Interoperability**
   - Standard protocol used by PyTorch, TensorFlow, JAX, MXNet
   - Zero-copy tensor exchange between frameworks
   - Future-proof as industry adopts DLPack

2. **C++ Integration**
   - Direct struct layout matching C/C++ 
   - No Python/C API needed for basic operations
   - SIMD-friendly memory layout

3. **Memory Efficiency**
   - Minimal overhead (just metadata)
   - Supports external memory (GPU, shared memory)
   - Explicit device management

4. **Educational Value**
   - Shows real-world tensor implementation
   - Demonstrates zero-copy principles
   - Compatible with ML frameworks

5. **Implementation Simplicity**
   - Clear separation of data and metadata
   - Standard structure across languages
   - Well-documented protocol
    """)
    
    # Show example C++ code that would work with this
    print("\nExample C++ code that works with DLPack:")
    print("-"*60)
    print("""
// C++ side - can directly use DLTensor structure
struct DLTensor {
    void* data;
    DLDevice device;
    int32_t ndim;
    DLDataType dtype;
    int64_t* shape;
    int64_t* strides;
    uint64_t byte_offset;
};

// SIMD operation using DLPack tensor
void add_simd(DLTensor* a, DLTensor* b, DLTensor* result) {
    double* data_a = (double*)a->data;
    double* data_b = (double*)b->data;
    double* data_r = (double*)result->data;
    
    int64_t size = 1;
    for (int i = 0; i < a->ndim; i++) {
        size *= a->shape[i];
    }
    
    // AVX2 SIMD processing
    for (int64_t i = 0; i < size; i += 4) {
        __m256d va = _mm256_load_pd(&data_a[i]);
        __m256d vb = _mm256_load_pd(&data_b[i]);
        __m256d vr = _mm256_add_pd(va, vb);
        _mm256_store_pd(&data_r[i], vr);
    }
}
    """)


if __name__ == "__main__":
    test_dlpack_array()
    benchmark_dlpack_vs_alternatives()
    show_dlpack_advantages()
    
    print("\n" + "="*60)
    print("RECOMMENDATION: Hybrid Approach")
    print("="*60)
    print("""
For ArrPy, recommend a HYBRID approach:

1. **Default Storage**: Python array.array
   - Simple, built-in, low overhead
   - Good for educational purposes
   - Buffer protocol support

2. **Performance Path**: DLPack-compatible wrapper
   - When C++ backend is selected
   - Wrap array.array with DLPack metadata
   - Zero-copy to C++ via DLTensor

3. **Future Extension**: Full DLPack
   - When GPU support is added
   - For framework interoperability
   - Industry-standard approach

This gives the best of all worlds:
- Simple Python implementation
- High-performance C++ path  
- Future-proof architecture
- Educational value
    """)