"""
Type-specific optimized operations for different data types.
Provides specialized implementations for int32, int64, float32, float64.
"""

import cython
from libc.stdlib cimport malloc, free
from libc.math cimport isnan, isinf

# Type-specific addition functions
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _add_float64(double[:] data1, double[:] data2):
    """Optimized addition for float64 arrays using memoryviews."""
    cdef:
        Py_ssize_t n = data1.shape[0]
        Py_ssize_t i
        double[:] result = cython.view.array(shape=(n,), itemsize=sizeof(double), format='d')
    
    for i in range(n):
        result[i] = data1[i] + data2[i]
    
    return result


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _add_float32(float[:] data1, float[:] data2):
    """Optimized addition for float32 arrays."""
    cdef:
        Py_ssize_t n = data1.shape[0]
        Py_ssize_t i
        float[:] result = cython.view.array(shape=(n,), itemsize=sizeof(float), format='f')
    
    for i in range(n):
        result[i] = data1[i] + data2[i]
    
    return result


@cython.boundscheck(False)
@cython.wraparound(False)
def _add_int64(long[:] data1, long[:] data2):
    """Optimized addition for int64 arrays."""
    cdef:
        Py_ssize_t n = data1.shape[0]
        Py_ssize_t i
        long[:] result = cython.view.array(shape=(n,), itemsize=sizeof(long), format='l')
    
    for i in range(n):
        result[i] = data1[i] + data2[i]
    
    return result


@cython.boundscheck(False)
@cython.wraparound(False)
def _add_int32(int[:] data1, int[:] data2):
    """Optimized addition for int32 arrays."""
    cdef:
        Py_ssize_t n = data1.shape[0]
        Py_ssize_t i
        int[:] result = cython.view.array(shape=(n,), itemsize=sizeof(int), format='i')
    
    for i in range(n):
        result[i] = data1[i] + data2[i]
    
    return result


# Type-specific multiplication functions
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _multiply_float64(double[:] data1, double[:] data2):
    """Optimized multiplication for float64 arrays."""
    cdef:
        Py_ssize_t n = data1.shape[0]
        Py_ssize_t i
        double[:] result = cython.view.array(shape=(n,), itemsize=sizeof(double), format='d')
    
    for i in range(n):
        result[i] = data1[i] * data2[i]
    
    return result


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _multiply_float64_scalar(double[:] data, double scalar):
    """Optimized scalar multiplication for float64 arrays."""
    cdef:
        Py_ssize_t n = data.shape[0]
        Py_ssize_t i
        double[:] result = cython.view.array(shape=(n,), itemsize=sizeof(double), format='d')
    
    for i in range(n):
        result[i] = data[i] * scalar
    
    return result


# Type-specific subtraction functions
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _subtract_float64(double[:] data1, double[:] data2):
    """Optimized subtraction for float64 arrays."""
    cdef:
        Py_ssize_t n = data1.shape[0]
        Py_ssize_t i
        double[:] result = cython.view.array(shape=(n,), itemsize=sizeof(double), format='d')
    
    for i in range(n):
        result[i] = data1[i] - data2[i]
    
    return result


# Type-specific division functions
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _divide_float64(double[:] data1, double[:] data2):
    """Optimized division for float64 arrays with zero handling."""
    cdef:
        Py_ssize_t n = data1.shape[0]
        Py_ssize_t i
        double[:] result = cython.view.array(shape=(n,), itemsize=sizeof(double), format='d')
    
    for i in range(n):
        if data2[i] == 0:
            if data1[i] > 0:
                result[i] = float('inf')
            elif data1[i] < 0:
                result[i] = float('-inf')
            else:
                result[i] = float('nan')
        else:
            result[i] = data1[i] / data2[i]
    
    return result


# Vectorized operations using SIMD hints
@cython.boundscheck(False)
@cython.wraparound(False)
def _add_float64_vectorized(double[:] data1, double[:] data2):
    """
    Vectorized addition with loop unrolling for better performance.
    Compiler can auto-vectorize this with SIMD instructions.
    """
    cdef:
        Py_ssize_t n = data1.shape[0]
        Py_ssize_t i
        Py_ssize_t n_chunks = n // 4
        Py_ssize_t remainder = n % 4
        double[:] result = cython.view.array(shape=(n,), itemsize=sizeof(double), format='d')
    
    # Process 4 elements at a time (loop unrolling)
    for i in range(0, n_chunks * 4, 4):
        result[i] = data1[i] + data2[i]
        result[i+1] = data1[i+1] + data2[i+1]
        result[i+2] = data1[i+2] + data2[i+2]
        result[i+3] = data1[i+3] + data2[i+3]
    
    # Process remaining elements
    for i in range(n_chunks * 4, n):
        result[i] = data1[i] + data2[i]
    
    return result


# Fused types for generic implementations
ctypedef fused numeric:
    int
    long
    float
    double


@cython.boundscheck(False)
@cython.wraparound(False)
def _generic_add(numeric[:] data1, numeric[:] data2):
    """Generic addition that works with any numeric type."""
    cdef:
        Py_ssize_t n = data1.shape[0]
        Py_ssize_t i
        numeric[:] result = cython.view.array(
            shape=(n,), 
            itemsize=sizeof(numeric), 
            format='d' if numeric is double else 'f' if numeric is float else 'l' if numeric is long else 'i'
        )
    
    for i in range(n):
        result[i] = data1[i] + data2[i]
    
    return result