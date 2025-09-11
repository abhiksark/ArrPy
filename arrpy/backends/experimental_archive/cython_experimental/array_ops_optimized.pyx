"""
Optimized Cython array operations without numpy overhead.
Uses memory views and type-specific implementations.
"""

import cython
from libc.stdlib cimport malloc, free
from libc.string cimport memcpy

@cython.boundscheck(False)
@cython.wraparound(False)
def _add_double_optimized(list data1, list data2, tuple shape1, tuple shape2):
    """
    Optimized addition for double arrays without numpy conversion.
    """
    cdef:
        size_t n = len(data1)
        size_t i
        double* arr1
        double* arr2
        double* result
        list result_list = []
    
    # Allocate C arrays
    arr1 = <double*>malloc(n * sizeof(double))
    arr2 = <double*>malloc(n * sizeof(double))
    result = <double*>malloc(n * sizeof(double))
    
    if not arr1 or not arr2 or not result:
        if arr1: free(arr1)
        if arr2: free(arr2)
        if result: free(result)
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy Python list to C array
        for i in range(n):
            arr1[i] = <double>data1[i]
            arr2[i] = <double>data2[i]
        
        # Perform addition
        for i in range(n):
            result[i] = arr1[i] + arr2[i]
        
        # Copy result back to Python list
        result_list = [result[i] for i in range(n)]
        
        return result_list, shape1
    
    finally:
        free(arr1)
        free(arr2)
        free(result)


@cython.boundscheck(False)
@cython.wraparound(False)
def _multiply_double_optimized(list data1, object data2, tuple shape1, shape2):
    """
    Optimized multiplication for double arrays.
    Handles both element-wise and scalar multiplication.
    """
    cdef:
        size_t n = len(data1)
        size_t i
        double* arr1
        double* arr2 = NULL
        double* result
        double scalar
        list result_list = []
        bint is_scalar = not isinstance(data2, list)
    
    # Allocate arrays
    arr1 = <double*>malloc(n * sizeof(double))
    result = <double*>malloc(n * sizeof(double))
    
    if not is_scalar:
        arr2 = <double*>malloc(n * sizeof(double))
    
    if not arr1 or not result or (not is_scalar and not arr2):
        if arr1: free(arr1)
        if arr2: free(arr2)
        if result: free(result)
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy data
        for i in range(n):
            arr1[i] = <double>data1[i]
        
        if is_scalar:
            # Scalar multiplication
            scalar = <double>data2
            for i in range(n):
                result[i] = arr1[i] * scalar
        else:
            # Element-wise multiplication
            for i in range(n):
                arr2[i] = <double>data2[i]
            for i in range(n):
                result[i] = arr1[i] * arr2[i]
        
        # Copy result back
        result_list = [result[i] for i in range(n)]
        
        return result_list, shape1
    
    finally:
        free(arr1)
        if arr2: free(arr2)
        free(result)


@cython.boundscheck(False)
@cython.wraparound(False)
def _subtract_double_optimized(list data1, list data2, tuple shape1, tuple shape2):
    """
    Optimized subtraction for double arrays.
    """
    cdef:
        size_t n = len(data1)
        size_t i
        double* arr1
        double* arr2
        double* result
        list result_list = []
    
    # Allocate C arrays
    arr1 = <double*>malloc(n * sizeof(double))
    arr2 = <double*>malloc(n * sizeof(double))
    result = <double*>malloc(n * sizeof(double))
    
    if not arr1 or not arr2 or not result:
        if arr1: free(arr1)
        if arr2: free(arr2)
        if result: free(result)
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy Python list to C array
        for i in range(n):
            arr1[i] = <double>data1[i]
            arr2[i] = <double>data2[i]
        
        # Perform subtraction
        for i in range(n):
            result[i] = arr1[i] - arr2[i]
        
        # Copy result back to Python list
        result_list = [result[i] for i in range(n)]
        
        return result_list, shape1
    
    finally:
        free(arr1)
        free(arr2)
        free(result)


@cython.boundscheck(False)
@cython.wraparound(False)
def _divide_double_optimized(list data1, list data2, tuple shape1, tuple shape2):
    """
    Optimized division for double arrays.
    """
    cdef:
        size_t n = len(data1)
        size_t i
        double* arr1
        double* arr2
        double* result
        list result_list = []
    
    # Allocate C arrays
    arr1 = <double*>malloc(n * sizeof(double))
    arr2 = <double*>malloc(n * sizeof(double))
    result = <double*>malloc(n * sizeof(double))
    
    if not arr1 or not arr2 or not result:
        if arr1: free(arr1)
        if arr2: free(arr2)
        if result: free(result)
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy Python list to C array
        for i in range(n):
            arr1[i] = <double>data1[i]
            arr2[i] = <double>data2[i]
        
        # Perform division (with zero check)
        for i in range(n):
            if arr2[i] != 0:
                result[i] = arr1[i] / arr2[i]
            else:
                # Handle division by zero (inf)
                result[i] = float('inf') if arr1[i] > 0 else float('-inf') if arr1[i] < 0 else float('nan')
        
        # Copy result back to Python list
        result_list = [result[i] for i in range(n)]
        
        return result_list, shape1
    
    finally:
        free(arr1)
        free(arr2)
        free(result)