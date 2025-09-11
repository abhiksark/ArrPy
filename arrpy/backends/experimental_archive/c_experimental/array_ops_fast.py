"""
Fast C backend array operations with zero-copy numpy arrays.
Uses optimized C++ implementations with SIMD.
"""

import numpy as np

def _add_c(data1, data2, shape1, shape2):
    """C++ backend addition with SIMD optimization and zero-copy"""
    try:
        from . import array_ops_fast_cpp
        
        # Convert to numpy arrays if needed (views, not copies)
        arr1 = np.asarray(data1, dtype=np.float64)
        arr2 = np.asarray(data2, dtype=np.float64)
        
        # Ensure C-contiguous for optimal SIMD access
        if not arr1.flags['C_CONTIGUOUS']:
            arr1 = np.ascontiguousarray(arr1)
        if not arr2.flags['C_CONTIGUOUS']:
            arr2 = np.ascontiguousarray(arr2)
        
        # Flatten for 1D processing (view, not copy)
        arr1_flat = arr1.ravel()
        arr2_flat = arr2.ravel()
        
        # Call optimized C++ function (zero-copy)
        result = array_ops_fast_cpp.add(arr1_flat, arr2_flat)
        
        # Convert back to list for compatibility with current interface
        return result.tolist(), shape1
        
    except ImportError:
        raise NotImplementedError(
            "Fast C++ backend not compiled. Run: python setup_cpp_fast.py build_ext --inplace\n"
            "Available in: python, cython"
        )


def _multiply_c(data1, data2, shape1, shape2):
    """C++ backend multiplication with SIMD and zero-copy"""
    try:
        from . import array_ops_fast_cpp
        
        # Check if scalar multiplication
        if not isinstance(data2, (list, np.ndarray)):
            arr1 = np.asarray(data1, dtype=np.float64)
            if not arr1.flags['C_CONTIGUOUS']:
                arr1 = np.ascontiguousarray(arr1)
            arr1_flat = arr1.ravel()
            
            result = array_ops_fast_cpp.multiply_scalar(arr1_flat, float(data2))
            return result.tolist(), shape1
        else:
            # Element-wise multiplication
            arr1 = np.asarray(data1, dtype=np.float64)
            arr2 = np.asarray(data2, dtype=np.float64)
            
            if not arr1.flags['C_CONTIGUOUS']:
                arr1 = np.ascontiguousarray(arr1)
            if not arr2.flags['C_CONTIGUOUS']:
                arr2 = np.ascontiguousarray(arr2)
            
            arr1_flat = arr1.ravel()
            arr2_flat = arr2.ravel()
            
            result = array_ops_fast_cpp.multiply(arr1_flat, arr2_flat)
            return result.tolist(), shape1
            
    except ImportError:
        raise NotImplementedError(
            "Fast C++ backend not compiled. Run: python setup_cpp_fast.py build_ext --inplace\n"
            "Available in: python, cython"
        )


def _subtract_c(data1, data2, shape1, shape2):
    """C++ backend subtraction with SIMD and zero-copy"""
    try:
        from . import array_ops_fast_cpp
        
        arr1 = np.asarray(data1, dtype=np.float64)
        arr2 = np.asarray(data2, dtype=np.float64)
        
        if not arr1.flags['C_CONTIGUOUS']:
            arr1 = np.ascontiguousarray(arr1)
        if not arr2.flags['C_CONTIGUOUS']:
            arr2 = np.ascontiguousarray(arr2)
        
        arr1_flat = arr1.ravel()
        arr2_flat = arr2.ravel()
        
        result = array_ops_fast_cpp.subtract(arr1_flat, arr2_flat)
        return result.tolist(), shape1
        
    except ImportError:
        raise NotImplementedError(
            "Fast C++ backend not compiled. Run: python setup_cpp_fast.py build_ext --inplace\n"
            "Available in: python, cython"
        )


def _divide_c(data1, data2, shape1, shape2):
    """C++ backend division with SIMD and zero-copy"""
    try:
        from . import array_ops_fast_cpp
        
        arr1 = np.asarray(data1, dtype=np.float64)
        arr2 = np.asarray(data2, dtype=np.float64)
        
        if not arr1.flags['C_CONTIGUOUS']:
            arr1 = np.ascontiguousarray(arr1)
        if not arr2.flags['C_CONTIGUOUS']:
            arr2 = np.ascontiguousarray(arr2)
        
        arr1_flat = arr1.ravel()
        arr2_flat = arr2.ravel()
        
        result = array_ops_fast_cpp.divide(arr1_flat, arr2_flat)
        return result.tolist(), shape1
        
    except ImportError:
        raise NotImplementedError(
            "Fast C++ backend not compiled. Run: python setup_cpp_fast.py build_ext --inplace\n"
            "Available in: python, cython"
        )