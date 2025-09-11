"""
Cython-optimized reduction operations.
Reductions benefit from parallelization and type annotations.
"""

import cython
from libc.stdlib cimport malloc, free
from libc.math cimport sqrt
from cython.parallel import prange, parallel

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _sum_cython(data, shape, axis=None, keepdims=False):
    """
    Optimized sum without numpy overhead.
    Uses parallel reduction for large arrays.
    """
    cdef:
        Py_ssize_t n = len(data)
        Py_ssize_t i
        double* arr
        double total = 0.0
    
    # For now, only handle full sum (axis=None)
    if axis is not None:
        from ..python.reduction_ops import _sum_python
        return _sum_python(data, shape, axis, keepdims)
    
    # Allocate C array
    arr = <double*>malloc(n * sizeof(double))
    if not arr:
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy data to C array
        for i in range(n):
            arr[i] = <double>data[i]
        
        # Parallel reduction for large arrays
        if n > 1000:
            for i in prange(n, nogil=True):
                total += arr[i]
        else:
            # Serial for small arrays
            for i in range(n):
                total += arr[i]
        
        # Handle return shape based on keepdims
        if keepdims:
            result_shape = tuple(1 for _ in shape)
            return [total], result_shape
        else:
            return [total], ()
    
    finally:
        free(arr)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _mean_cython(data, shape, axis=None, keepdims=False):
    """
    Optimized mean calculation.
    Single pass algorithm.
    """
    cdef:
        Py_ssize_t n = len(data)
        Py_ssize_t i
        double* arr
        double total = 0.0
        double mean_val
    
    if axis is not None:
        from ..python.reduction_ops import _mean_python
        return _mean_python(data, shape, axis, keepdims)
    
    if n == 0:
        return [float('nan')], ()
    
    arr = <double*>malloc(n * sizeof(double))
    if not arr:
        raise MemoryError("Failed to allocate memory")
    
    try:
        for i in range(n):
            arr[i] = <double>data[i]
        
        # Parallel sum for large arrays
        if n > 1000:
            for i in prange(n, nogil=True):
                total += arr[i]
        else:
            for i in range(n):
                total += arr[i]
        
        mean_val = total / n
        
        if keepdims:
            result_shape = tuple(1 for _ in shape)
            return [mean_val], result_shape
        else:
            return [mean_val], ()
    
    finally:
        free(arr)


@cython.boundscheck(False)
@cython.wraparound(False)
def _min_cython(data, shape, axis=None, keepdims=False):
    """
    Optimized minimum finding.
    """
    cdef:
        Py_ssize_t n = len(data)
        Py_ssize_t i
        double* arr
        double min_val
    
    if axis is not None:
        from ..python.reduction_ops import _min_python
        return _min_python(data, shape, axis)
    
    if n == 0:
        raise ValueError("min() of empty array")
    
    arr = <double*>malloc(n * sizeof(double))
    if not arr:
        raise MemoryError("Failed to allocate memory")
    
    try:
        for i in range(n):
            arr[i] = <double>data[i]
        
        min_val = arr[0]
        
        # Serial min (parallel reduction for min/max requires special handling)
        for i in range(1, n):
            if arr[i] < min_val:
                min_val = arr[i]
        
        if keepdims:
            result_shape = tuple(1 for _ in shape)
            return [min_val], result_shape
        else:
            return [min_val], ()
    
    finally:
        free(arr)


@cython.boundscheck(False)
@cython.wraparound(False)
def _max_cython(data, shape, axis=None, keepdims=False):
    """
    Optimized maximum finding.
    """
    cdef:
        Py_ssize_t n = len(data)
        Py_ssize_t i
        double* arr
        double max_val
    
    if axis is not None:
        from ..python.reduction_ops import _max_python
        return _max_python(data, shape, axis)
    
    if n == 0:
        raise ValueError("max() of empty array")
    
    arr = <double*>malloc(n * sizeof(double))
    if not arr:
        raise MemoryError("Failed to allocate memory")
    
    try:
        for i in range(n):
            arr[i] = <double>data[i]
        
        max_val = arr[0]
        
        # Serial max (parallel reduction for min/max requires special handling)
        for i in range(1, n):
            if arr[i] > max_val:
                max_val = arr[i]
        
        if keepdims:
            result_shape = tuple(1 for _ in shape)
            return [max_val], result_shape
        else:
            return [max_val], ()
    
    finally:
        free(arr)


def _prod_cython(data, shape, axis=None):
    """Product not yet optimized in Cython."""
    raise NotImplementedError(
        "prod() not yet implemented in Cython backend.\n"
        "Available in: python\n"
        "Switch backends or contribute the implementation!"
    )


def _std_cython(data, shape, axis=None):
    """Standard deviation not yet optimized in Cython."""
    raise NotImplementedError(
        "std() not yet implemented in Cython backend.\n"
        "Available in: python\n"
        "Switch backends or contribute the implementation!"
    )


def _var_cython(data, shape, axis=None):
    """Variance not yet optimized in Cython."""
    raise NotImplementedError(
        "var() not yet implemented in Cython backend.\n"
        "Available in: python\n"
        "Switch backends or contribute the implementation!"
    )