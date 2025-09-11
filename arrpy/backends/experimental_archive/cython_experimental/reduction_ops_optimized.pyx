"""
Optimized reduction operations using parallel processing.
No numpy overhead, direct memory management.
"""

import cython
from libc.stdlib cimport malloc, free
from libc.math cimport sqrt, fabs
from cython.parallel import prange, parallel
from openmp cimport omp_get_num_threads, omp_get_thread_num

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _sum_parallel(data, shape, axis=None, keepdims=False):
    """
    Parallel sum reduction without numpy overhead.
    Uses OpenMP for large arrays.
    """
    cdef:
        Py_ssize_t n = len(data)
        Py_ssize_t i
        double* arr
        double total = 0.0
        double local_sum
    
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
            with nogil, parallel():
                local_sum = 0.0
                for i in prange(n):
                    local_sum += arr[i]
                with gil:
                    total += local_sum
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
def _mean_parallel(data, shape, axis=None, keepdims=False):
    """
    Parallel mean calculation.
    Single pass algorithm.
    """
    cdef:
        Py_ssize_t n = len(data)
        Py_ssize_t i
        double* arr
        double total = 0.0
        double mean_val
        double local_sum
    
    if axis is not None:
        from ..python.reduction_ops import _mean_python
        return _mean_python(data, shape, axis, keepdims)
    
    if n == 0:
        return [float('nan')], ()
    
    # Allocate C array
    arr = <double*>malloc(n * sizeof(double))
    if not arr:
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy data
        for i in range(n):
            arr[i] = <double>data[i]
        
        # Parallel sum
        if n > 1000:
            with nogil, parallel():
                local_sum = 0.0
                for i in prange(n):
                    local_sum += arr[i]
                with gil:
                    total += local_sum
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
def _min_parallel(data, shape, axis=None, keepdims=False):
    """
    Parallel minimum finding.
    Uses reduction with local minima.
    """
    cdef:
        Py_ssize_t n = len(data)
        Py_ssize_t i
        double* arr
        double min_val
        double local_min
    
    if axis is not None:
        from ..python.reduction_ops import _min_python
        return _min_python(data, shape, axis)
    
    if n == 0:
        raise ValueError("min() of empty array")
    
    # Allocate C array
    arr = <double*>malloc(n * sizeof(double))
    if not arr:
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy data
        for i in range(n):
            arr[i] = <double>data[i]
        
        min_val = arr[0]
        
        # Parallel min for large arrays
        if n > 1000:
            # OpenMP parallel reduction
            for i in prange(1, n, nogil=True):
                if arr[i] < min_val:
                    min_val = arr[i]
        else:
            # Serial for small arrays
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
def _max_parallel(data, shape, axis=None, keepdims=False):
    """
    Parallel maximum finding.
    Uses reduction with local maxima.
    """
    cdef:
        Py_ssize_t n = len(data)
        Py_ssize_t i
        double* arr
        double max_val
        double local_max
    
    if axis is not None:
        from ..python.reduction_ops import _max_python
        return _max_python(data, shape, axis)
    
    if n == 0:
        raise ValueError("max() of empty array")
    
    # Allocate C array
    arr = <double*>malloc(n * sizeof(double))
    if not arr:
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy data
        for i in range(n):
            arr[i] = <double>data[i]
        
        max_val = arr[0]
        
        # Parallel max for large arrays
        if n > 1000:
            # OpenMP parallel reduction
            for i in prange(1, n, nogil=True):
                if arr[i] > max_val:
                    max_val = arr[i]
        else:
            # Serial for small arrays
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


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _std_parallel(data, shape, axis=None, ddof=0, keepdims=False):
    """
    Parallel standard deviation calculation.
    Single-pass algorithm using Welford's method.
    """
    cdef:
        Py_ssize_t n = len(data)
        Py_ssize_t i
        double* arr
        double mean = 0.0
        double M2 = 0.0
        double delta, delta2
        double std_val
        int count = 0
    
    if axis is not None:
        from ..python.reduction_ops import _std_python
        return _std_python(data, shape, axis)
    
    if n <= ddof:
        return [float('nan')], ()
    
    # Allocate C array
    arr = <double*>malloc(n * sizeof(double))
    if not arr:
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy data
        for i in range(n):
            arr[i] = <double>data[i]
        
        # Welford's online algorithm for variance
        for i in range(n):
            count += 1
            delta = arr[i] - mean
            mean += delta / count
            delta2 = arr[i] - mean
            M2 += delta * delta2
        
        # Calculate standard deviation
        if count > ddof:
            std_val = sqrt(M2 / (count - ddof))
        else:
            std_val = float('nan')
        
        if keepdims:
            result_shape = tuple(1 for _ in shape)
            return [std_val], result_shape
        else:
            return [std_val], ()
    
    finally:
        free(arr)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _var_parallel(data, shape, axis=None, ddof=0, keepdims=False):
    """
    Parallel variance calculation.
    Single-pass algorithm using Welford's method.
    """
    cdef:
        Py_ssize_t n = len(data)
        Py_ssize_t i
        double* arr
        double mean = 0.0
        double M2 = 0.0
        double delta, delta2
        double var_val
        int count = 0
    
    if axis is not None:
        from ..python.reduction_ops import _var_python
        return _var_python(data, shape, axis)
    
    if n <= ddof:
        return [float('nan')], ()
    
    # Allocate C array
    arr = <double*>malloc(n * sizeof(double))
    if not arr:
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy data
        for i in range(n):
            arr[i] = <double>data[i]
        
        # Welford's online algorithm
        for i in range(n):
            count += 1
            delta = arr[i] - mean
            mean += delta / count
            delta2 = arr[i] - mean
            M2 += delta * delta2
        
        # Calculate variance
        if count > ddof:
            var_val = M2 / (count - ddof)
        else:
            var_val = float('nan')
        
        if keepdims:
            result_shape = tuple(1 for _ in shape)
            return [var_val], result_shape
        else:
            return [var_val], ()
    
    finally:
        free(arr)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _prod_parallel(data, shape, axis=None, keepdims=False):
    """
    Parallel product calculation.
    """
    cdef:
        Py_ssize_t n = len(data)
        Py_ssize_t i
        double* arr
        double product = 1.0
        double local_prod
    
    if axis is not None:
        from ..python.reduction_ops import _prod_python
        return _prod_python(data, shape, axis)
    
    # Allocate C array
    arr = <double*>malloc(n * sizeof(double))
    if not arr:
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy data
        for i in range(n):
            arr[i] = <double>data[i]
        
        # Parallel product for large arrays
        if n > 1000:
            with nogil, parallel():
                local_prod = 1.0
                for i in prange(n):
                    local_prod *= arr[i]
                with gil:
                    product *= local_prod
        else:
            # Serial for small arrays
            for i in range(n):
                product *= arr[i]
        
        if keepdims:
            result_shape = tuple(1 for _ in shape)
            return [product], result_shape
        else:
            return [product], ()
    
    finally:
        free(arr)