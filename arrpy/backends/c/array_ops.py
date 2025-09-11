"""
C backend array operations.
Uses PyBind11 for high-performance C++ implementations with SIMD.
Now with buffer protocol support for zero-copy operations.
"""

import array

def _add_c(data1, data2, shape1, shape2):
    """C++ backend addition with SIMD optimization"""
    # Try buffer protocol path first for array.array
    if isinstance(data1, array.array) and isinstance(data2, array.array):
        from . import array_ops_buffer
        return array_ops_buffer._add_c(data1, data2, shape1, shape2)
    
    # Fall back to original implementation
    try:
        from . import array_ops_cpp
        result, shape = array_ops_cpp.add(
            list(data1), list(data2), 
            (shape1[0] if shape1 else 1, shape1[1] if len(shape1) > 1 else 1),
            (shape2[0] if shape2 else 1, shape2[1] if len(shape2) > 1 else 1)
        )
        return result, shape1
    except ImportError:
        raise NotImplementedError(
            "C++ backend not compiled. Run: make build-cpp\n"
            "Available in: python, cython"
        )


def _multiply_c(data1, data2, shape1, shape2):
    """C++ backend multiplication with SIMD"""
    # Try buffer protocol path first for array.array
    if isinstance(data1, array.array):
        from . import array_ops_buffer
        return array_ops_buffer._multiply_c(data1, data2, shape1, shape2)
    
    # Fall back to original implementation
    try:
        from . import array_ops_cpp
        
        # Check if scalar multiplication
        if not isinstance(data2, list):
            result, shape = array_ops_cpp.multiply_scalar(
                list(data1), float(data2),
                (shape1[0] if shape1 else 1, shape1[1] if len(shape1) > 1 else 1)
            )
        else:
            result, shape = array_ops_cpp.multiply(
                list(data1), list(data2),
                (shape1[0] if shape1 else 1, shape1[1] if len(shape1) > 1 else 1),
                (shape2[0] if shape2 else 1, shape2[1] if len(shape2) > 1 else 1)
            )
        return result, shape1
    except ImportError:
        raise NotImplementedError(
            "C++ backend not compiled. Run: make build-cpp\n"
            "Available in: python, cython"
        )


def _subtract_c(data1, data2, shape1, shape2):
    """C++ backend subtraction with SIMD"""
    # Try buffer protocol path first for array.array
    if isinstance(data1, array.array) and isinstance(data2, array.array):
        from . import array_ops_buffer
        return array_ops_buffer._subtract_c(data1, data2, shape1, shape2)
    
    # Fall back to original implementation
    try:
        from . import array_ops_cpp
        result, shape = array_ops_cpp.subtract(
            list(data1), list(data2),
            (shape1[0] if shape1 else 1, shape1[1] if len(shape1) > 1 else 1),
            (shape2[0] if shape2 else 1, shape2[1] if len(shape2) > 1 else 1)
        )
        return result, shape1
    except ImportError:
        raise NotImplementedError(
            "C++ backend not compiled. Run: make build-cpp\n"
            "Available in: python, cython"
        )


def _divide_c(data1, data2, shape1, shape2):
    """C++ backend division with SIMD"""
    # Try buffer protocol path first for array.array
    if isinstance(data1, array.array) and isinstance(data2, array.array):
        from . import array_ops_buffer
        return array_ops_buffer._divide_c(data1, data2, shape1, shape2)
    
    # Fall back to original implementation
    try:
        from . import array_ops_cpp
        result, shape = array_ops_cpp.divide(
            list(data1), list(data2),
            (shape1[0] if shape1 else 1, shape1[1] if len(shape1) > 1 else 1),
            (shape2[0] if shape2 else 1, shape2[1] if len(shape2) > 1 else 1)
        )
        return result, shape1
    except ImportError:
        raise NotImplementedError(
            "C++ backend not compiled. Run: make build-cpp\n"
            "Available in: python, cython"
        )