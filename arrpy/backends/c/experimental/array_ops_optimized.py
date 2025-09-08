"""
Wrapper for optimized C++ array operations with buffer protocol.
Provides both regular and in-place operations for maximum performance.
"""

import array as pyarray
import numpy as np

# Try to import the optimized C++ module
try:
    from .array_ops_optimized_cpp import (
        add_optimized,
        subtract_optimized,
        multiply_optimized,
        divide_optimized,
        add_inplace_optimized,
    )
    CPP_OPTIMIZED_AVAILABLE = True
except ImportError:
    CPP_OPTIMIZED_AVAILABLE = False

# Fall back to buffer module if optimized not available
if not CPP_OPTIMIZED_AVAILABLE:
    try:
        from .array_ops_buffer_cpp import (
            add_buffer as add_optimized,
            subtract_buffer as subtract_optimized,
            multiply_buffer as multiply_optimized,
            divide_buffer as divide_optimized,
        )
        add_inplace_optimized = None  # Not available in buffer module
        CPP_OPTIMIZED_AVAILABLE = True
    except ImportError:
        pass

def _add_optimized(data1, data2, shape1, shape2):
    """Optimized element-wise addition using C++ with SIMD and OpenMP."""
    if not CPP_OPTIMIZED_AVAILABLE:
        raise NotImplementedError("Optimized C++ backend not available. Build with setup_optimized_cpp.py")
    
    # Ensure data is array.array
    if not isinstance(data1, pyarray.array):
        data1 = pyarray.array('d', data1)
    if not isinstance(data2, pyarray.array):
        if np.isscalar(data2):
            # Broadcast scalar
            data2 = pyarray.array('d', [float(data2)] * len(data1))
        else:
            data2 = pyarray.array('d', data2)
    
    # Get buffer pointers
    ptr1, size1 = data1.buffer_info()
    ptr2, size2 = data2.buffer_info()
    
    # Check sizes match
    if size1 != size2:
        raise ValueError(f"Array sizes don't match: {size1} vs {size2}")
    
    # Allocate result
    result_data = pyarray.array('d', [0.0] * size1)
    ptr_result, _ = result_data.buffer_info()
    
    # Call optimized C++ function
    add_optimized(ptr1, ptr2, ptr_result, size1)
    
    return result_data

def _subtract_optimized(data1, data2, shape1, shape2):
    """Optimized element-wise subtraction using C++ with SIMD and OpenMP."""
    if not CPP_OPTIMIZED_AVAILABLE:
        raise NotImplementedError("Optimized C++ backend not available. Build with setup_optimized_cpp.py")
    
    # Ensure data is array.array
    if not isinstance(data1, pyarray.array):
        data1 = pyarray.array('d', data1)
    if not isinstance(data2, pyarray.array):
        if np.isscalar(data2):
            # Broadcast scalar
            data2 = pyarray.array('d', [float(data2)] * len(data1))
        else:
            data2 = pyarray.array('d', data2)
    
    # Get buffer pointers
    ptr1, size1 = data1.buffer_info()
    ptr2, size2 = data2.buffer_info()
    
    # Check sizes match
    if size1 != size2:
        raise ValueError(f"Array sizes don't match: {size1} vs {size2}")
    
    # Allocate result
    result_data = pyarray.array('d', [0.0] * size1)
    ptr_result, _ = result_data.buffer_info()
    
    # Call optimized C++ function
    subtract_optimized(ptr1, ptr2, ptr_result, size1)
    
    return result_data

def _multiply_optimized(data1, data2, shape1, shape2):
    """Optimized element-wise multiplication using C++ with SIMD and OpenMP."""
    if not CPP_OPTIMIZED_AVAILABLE:
        raise NotImplementedError("Optimized C++ backend not available. Build with setup_optimized_cpp.py")
    
    # Ensure data is array.array
    if not isinstance(data1, pyarray.array):
        data1 = pyarray.array('d', data1)
    if not isinstance(data2, pyarray.array):
        if np.isscalar(data2):
            # Broadcast scalar
            data2 = pyarray.array('d', [float(data2)] * len(data1))
        else:
            data2 = pyarray.array('d', data2)
    
    # Get buffer pointers
    ptr1, size1 = data1.buffer_info()
    ptr2, size2 = data2.buffer_info()
    
    # Check sizes match
    if size1 != size2:
        raise ValueError(f"Array sizes don't match: {size1} vs {size2}")
    
    # Allocate result
    result_data = pyarray.array('d', [0.0] * size1)
    ptr_result, _ = result_data.buffer_info()
    
    # Call optimized C++ function
    multiply_optimized(ptr1, ptr2, ptr_result, size1)
    
    return result_data

def _divide_optimized(data1, data2, shape1, shape2, fast_mode=False):
    """Optimized element-wise division using C++ with SIMD and OpenMP.
    
    Args:
        fast_mode: If True, uses reciprocal approximation for faster but 
                  slightly less accurate results.
    """
    if not CPP_OPTIMIZED_AVAILABLE:
        raise NotImplementedError("Optimized C++ backend not available. Build with setup_optimized_cpp.py")
    
    # Ensure data is array.array
    if not isinstance(data1, pyarray.array):
        data1 = pyarray.array('d', data1)
    if not isinstance(data2, pyarray.array):
        if np.isscalar(data2):
            # Broadcast scalar
            data2 = pyarray.array('d', [float(data2)] * len(data1))
        else:
            data2 = pyarray.array('d', data2)
    
    # Get buffer pointers
    ptr1, size1 = data1.buffer_info()
    ptr2, size2 = data2.buffer_info()
    
    # Check sizes match
    if size1 != size2:
        raise ValueError(f"Array sizes don't match: {size1} vs {size2}")
    
    # Allocate result
    result_data = pyarray.array('d', [0.0] * size1)
    ptr_result, _ = result_data.buffer_info()
    
    # Call optimized C++ function
    divide_optimized(ptr1, ptr2, ptr_result, size1, fast_mode)
    
    return result_data

def _add_inplace_optimized(data1, data2):
    """In-place addition: data1 += data2. Modifies data1 directly."""
    if not CPP_OPTIMIZED_AVAILABLE or add_inplace_optimized is None:
        # Fallback to Python
        for i in range(len(data1)):
            data1[i] += data2[i]
        return
    
    # Ensure data is array.array
    if not isinstance(data1, pyarray.array):
        raise TypeError("In-place operations require array.array")
    if not isinstance(data2, pyarray.array):
        if np.isscalar(data2):
            # Broadcast scalar
            data2 = pyarray.array('d', [float(data2)] * len(data1))
        else:
            data2 = pyarray.array('d', data2)
    
    # Get buffer pointers
    ptr1, size1 = data1.buffer_info()
    ptr2, size2 = data2.buffer_info()
    
    # Check sizes match
    if size1 != size2:
        raise ValueError(f"Array sizes don't match: {size1} vs {size2}")
    
    # Call optimized C++ function - modifies data1 in place
    add_inplace_optimized(ptr1, ptr2, size1)

# Export the functions
__all__ = [
    '_add_optimized',
    '_subtract_optimized',
    '_multiply_optimized',
    '_divide_optimized',
    '_add_inplace_optimized',
    'CPP_OPTIMIZED_AVAILABLE',
]