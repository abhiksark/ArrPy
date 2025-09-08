# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: nonecheck=False
# cython: cdivision=True

"""
Pooled memory versions of array operations.
Uses memory pool to reduce allocation overhead.
"""

import cython
from libc.stdlib cimport malloc, free
from libc.math cimport sin, cos, exp, log, sqrt, pow

# Import memory pool
from .memory_pool cimport MemoryPool, get_global_pool

@cython.boundscheck(False)
@cython.wraparound(False)
def _add_pooled(data1, data2, shape1, shape2):
    """Optimized addition using pooled memory."""
    cdef int i
    cdef int n = len(data1)
    cdef MemoryPool pool = get_global_pool()
    cdef double* arr1 = pool.get_memory(n)
    cdef double* arr2 = pool.get_memory(n)
    cdef double* result_arr = pool.get_memory(n)
    
    if not arr1 or not arr2 or not result_arr:
        # Fallback to regular allocation if pool fails
        if arr1:
            pool.return_memory(arr1)
        if arr2:
            pool.return_memory(arr2)
        if result_arr:
            pool.return_memory(result_arr)
        
        # Use regular malloc
        arr1 = <double*>malloc(n * sizeof(double))
        arr2 = <double*>malloc(n * sizeof(double))
        result_arr = <double*>malloc(n * sizeof(double))
        
        if not arr1 or not arr2 or not result_arr:
            if arr1:
                free(arr1)
            if arr2:
                free(arr2)
            if result_arr:
                free(result_arr)
            raise MemoryError("Failed to allocate memory")
        
        try:
            # Copy input data
            for i in range(n):
                arr1[i] = float(data1[i])
                arr2[i] = float(data2[i])
            
            # Perform addition
            for i in range(n):
                result_arr[i] = arr1[i] + arr2[i]
            
            # Convert to Python list
            result = []
            for i in range(n):
                result.append(result_arr[i])
            
            return result, shape1
        
        finally:
            free(arr1)
            free(arr2)
            free(result_arr)
    
    try:
        # Copy input data
        for i in range(n):
            arr1[i] = float(data1[i])
            arr2[i] = float(data2[i])
        
        # Perform addition
        for i in range(n):
            result_arr[i] = arr1[i] + arr2[i]
        
        # Convert to Python list
        result = []
        for i in range(n):
            result.append(result_arr[i])
        
        return result, shape1
    
    finally:
        pool.return_memory(arr1)
        pool.return_memory(arr2)
        pool.return_memory(result_arr)

@cython.boundscheck(False)
@cython.wraparound(False)
def _subtract_pooled(data1, data2, shape1, shape2):
    """Optimized subtraction using pooled memory."""
    cdef int i
    cdef int n = len(data1)
    cdef MemoryPool pool = get_global_pool()
    cdef double* arr1 = pool.get_memory(n)
    cdef double* arr2 = pool.get_memory(n)
    cdef double* result_arr = pool.get_memory(n)
    
    if not arr1 or not arr2 or not result_arr:
        if arr1:
            pool.return_memory(arr1)
        if arr2:
            pool.return_memory(arr2)
        if result_arr:
            pool.return_memory(result_arr)
        raise MemoryError("Failed to allocate memory from pool")
    
    try:
        # Copy input data
        for i in range(n):
            arr1[i] = float(data1[i])
            arr2[i] = float(data2[i])
        
        # Perform subtraction
        for i in range(n):
            result_arr[i] = arr1[i] - arr2[i]
        
        # Convert to Python list
        result = []
        for i in range(n):
            result.append(result_arr[i])
        
        return result, shape1
    
    finally:
        pool.return_memory(arr1)
        pool.return_memory(arr2)
        pool.return_memory(result_arr)

@cython.boundscheck(False)
@cython.wraparound(False)
def _multiply_pooled(data1, data2, shape1, shape2):
    """Optimized multiplication using pooled memory."""
    cdef int i
    cdef int n = len(data1)
    cdef MemoryPool pool = get_global_pool()
    cdef double* arr1 = pool.get_memory(n)
    cdef double* arr2 = pool.get_memory(n)
    cdef double* result_arr = pool.get_memory(n)
    
    if not arr1 or not arr2 or not result_arr:
        if arr1:
            pool.return_memory(arr1)
        if arr2:
            pool.return_memory(arr2)
        if result_arr:
            pool.return_memory(result_arr)
        raise MemoryError("Failed to allocate memory from pool")
    
    try:
        # Copy input data
        for i in range(n):
            arr1[i] = float(data1[i])
            arr2[i] = float(data2[i])
        
        # Perform multiplication
        for i in range(n):
            result_arr[i] = arr1[i] * arr2[i]
        
        # Convert to Python list
        result = []
        for i in range(n):
            result.append(result_arr[i])
        
        return result, shape1
    
    finally:
        pool.return_memory(arr1)
        pool.return_memory(arr2)
        pool.return_memory(result_arr)

@cython.boundscheck(False)
@cython.wraparound(False)
def _divide_pooled(data1, data2, shape1, shape2):
    """Optimized division using pooled memory."""
    cdef int i
    cdef int n = len(data1)
    cdef MemoryPool pool = get_global_pool()
    cdef double* arr1 = pool.get_memory(n)
    cdef double* arr2 = pool.get_memory(n)
    cdef double* result_arr = pool.get_memory(n)
    
    if not arr1 or not arr2 or not result_arr:
        if arr1:
            pool.return_memory(arr1)
        if arr2:
            pool.return_memory(arr2)
        if result_arr:
            pool.return_memory(result_arr)
        raise MemoryError("Failed to allocate memory from pool")
    
    try:
        # Copy input data
        for i in range(n):
            arr1[i] = float(data1[i])
            arr2[i] = float(data2[i])
        
        # Perform division with zero check
        for i in range(n):
            if arr2[i] == 0:
                result_arr[i] = float('inf') if arr1[i] > 0 else float('-inf') if arr1[i] < 0 else float('nan')
            else:
                result_arr[i] = arr1[i] / arr2[i]
        
        # Convert to Python list
        result = []
        for i in range(n):
            result.append(result_arr[i])
        
        return result, shape1
    
    finally:
        pool.return_memory(arr1)
        pool.return_memory(arr2)
        pool.return_memory(result_arr)

# Ufuncs with pooled memory
@cython.boundscheck(False)
@cython.wraparound(False)
def _sin_pooled(data, shape):
    """Optimized sine using pooled memory."""
    cdef int i
    cdef int n = len(data)
    cdef MemoryPool pool = get_global_pool()
    cdef double* arr = pool.get_memory(n)
    cdef double* result_arr = pool.get_memory(n)
    
    if not arr or not result_arr:
        if arr:
            pool.return_memory(arr)
        if result_arr:
            pool.return_memory(result_arr)
        raise MemoryError("Failed to allocate memory from pool")
    
    try:
        # Copy input data
        for i in range(n):
            arr[i] = float(data[i])
        
        # Apply sine
        for i in range(n):
            result_arr[i] = sin(arr[i])
        
        # Convert to Python list
        result = []
        for i in range(n):
            result.append(result_arr[i])
        
        return result, shape
    
    finally:
        pool.return_memory(arr)
        pool.return_memory(result_arr)

@cython.boundscheck(False)
@cython.wraparound(False)
def _exp_pooled(data, shape):
    """Optimized exponential using pooled memory."""
    cdef int i
    cdef int n = len(data)
    cdef MemoryPool pool = get_global_pool()
    cdef double* arr = pool.get_memory(n)
    cdef double* result_arr = pool.get_memory(n)
    
    if not arr or not result_arr:
        if arr:
            pool.return_memory(arr)
        if result_arr:
            pool.return_memory(result_arr)
        raise MemoryError("Failed to allocate memory from pool")
    
    try:
        # Copy input data
        for i in range(n):
            arr[i] = float(data[i])
        
        # Apply exponential
        for i in range(n):
            result_arr[i] = exp(arr[i])
        
        # Convert to Python list
        result = []
        for i in range(n):
            result.append(result_arr[i])
        
        return result, shape
    
    finally:
        pool.return_memory(arr)
        pool.return_memory(result_arr)

@cython.boundscheck(False)
@cython.wraparound(False)
def _sqrt_pooled(data, shape):
    """Optimized square root using pooled memory."""
    cdef int i
    cdef int n = len(data)
    cdef MemoryPool pool = get_global_pool()
    cdef double* arr = pool.get_memory(n)
    cdef double* result_arr = pool.get_memory(n)
    
    if not arr or not result_arr:
        if arr:
            pool.return_memory(arr)
        if result_arr:
            pool.return_memory(result_arr)
        raise MemoryError("Failed to allocate memory from pool")
    
    try:
        # Copy input data
        for i in range(n):
            arr[i] = float(data[i])
        
        # Apply square root
        for i in range(n):
            result_arr[i] = sqrt(arr[i])
        
        # Convert to Python list
        result = []
        for i in range(n):
            result.append(result_arr[i])
        
        return result, shape
    
    finally:
        pool.return_memory(arr)
        pool.return_memory(result_arr)