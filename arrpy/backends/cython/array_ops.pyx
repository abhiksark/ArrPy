"""
Cython-optimized array operations.
Uses type-specific implementations for maximum performance.
"""

import cython
from libc.stdlib cimport malloc, free
from libc.string cimport memcpy

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _add_cython(data1, data2, shape1, shape2):
    """
    Optimized addition without numpy overhead.
    Uses raw C arrays for maximum performance.
    """
    cdef:
        Py_ssize_t n = len(data1)
        Py_ssize_t i
        double* arr1
        double* arr2
        double* result_arr
        list result_list = []
    
    # Allocate C arrays
    arr1 = <double*>malloc(n * sizeof(double))
    arr2 = <double*>malloc(n * sizeof(double))
    result_arr = <double*>malloc(n * sizeof(double))
    
    if not arr1 or not arr2 or not result_arr:
        if arr1: free(arr1)
        if arr2: free(arr2)
        if result_arr: free(result_arr)
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy Python list to C arrays (optimized loop)
        for i in range(n):
            arr1[i] = <double>data1[i]
            arr2[i] = <double>data2[i]
        
        # Perform vectorized addition
        for i in range(n):
            result_arr[i] = arr1[i] + arr2[i]
        
        # Copy result back to Python list
        result_list = [result_arr[i] for i in range(n)]
        
        return result_list, shape1
    
    finally:
        free(arr1)
        free(arr2)
        free(result_arr)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _multiply_cython(data1, data2, shape1, shape2):
    """
    Optimized multiplication for both scalar and element-wise.
    """
    cdef:
        Py_ssize_t n = len(data1)
        Py_ssize_t i
        double* arr1
        double* arr2 = NULL
        double* result_arr
        double scalar
        list result_list = []
        bint is_scalar = not isinstance(data2, list)
    
    # Allocate arrays
    arr1 = <double*>malloc(n * sizeof(double))
    result_arr = <double*>malloc(n * sizeof(double))
    
    if not is_scalar:
        arr2 = <double*>malloc(n * sizeof(double))
        if not arr2:
            if arr1: free(arr1)
            if result_arr: free(result_arr)
            raise MemoryError("Failed to allocate memory")
    
    if not arr1 or not result_arr:
        if arr1: free(arr1)
        if arr2: free(arr2)
        if result_arr: free(result_arr)
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy first array
        for i in range(n):
            arr1[i] = <double>data1[i]
        
        if is_scalar:
            # Scalar multiplication
            scalar = <double>data2
            for i in range(n):
                result_arr[i] = arr1[i] * scalar
        else:
            # Element-wise multiplication
            for i in range(n):
                arr2[i] = <double>data2[i]
            for i in range(n):
                result_arr[i] = arr1[i] * arr2[i]
        
        # Copy result back
        result_list = [result_arr[i] for i in range(n)]
        
        return result_list, shape1
    
    finally:
        free(arr1)
        if arr2: free(arr2)
        free(result_arr)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _subtract_cython(data1, data2, shape1, shape2):
    """
    Optimized subtraction without numpy overhead.
    Uses raw C arrays for maximum performance.
    """
    cdef:
        Py_ssize_t n = len(data1)
        Py_ssize_t i
        double* arr1
        double* arr2 = NULL
        double* result_arr
        double scalar
        list result_list = []
        bint is_scalar = not isinstance(data2, list)
    
    # Allocate arrays
    arr1 = <double*>malloc(n * sizeof(double))
    result_arr = <double*>malloc(n * sizeof(double))
    
    if not is_scalar:
        arr2 = <double*>malloc(n * sizeof(double))
        if not arr2:
            if arr1: free(arr1)
            if result_arr: free(result_arr)
            raise MemoryError("Failed to allocate memory")
    
    if not arr1 or not result_arr:
        if arr1: free(arr1)
        if arr2: free(arr2)
        if result_arr: free(result_arr)
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy first array
        for i in range(n):
            arr1[i] = <double>data1[i]
        
        if is_scalar:
            # Scalar subtraction
            scalar = <double>data2
            for i in range(n):
                result_arr[i] = arr1[i] - scalar
        else:
            # Element-wise subtraction
            for i in range(n):
                arr2[i] = <double>data2[i]
            for i in range(n):
                result_arr[i] = arr1[i] - arr2[i]
        
        # Copy result back
        result_list = [result_arr[i] for i in range(n)]
        
        return result_list, shape1
    
    finally:
        free(arr1)
        if arr2: free(arr2)
        free(result_arr)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _divide_cython(data1, data2, shape1, shape2):
    """
    Optimized division without numpy overhead.
    Uses raw C arrays for maximum performance.
    """
    cdef:
        Py_ssize_t n = len(data1)
        Py_ssize_t i
        double* arr1
        double* arr2 = NULL
        double* result_arr
        double scalar
        list result_list = []
        bint is_scalar = not isinstance(data2, list)
    
    # Allocate arrays
    arr1 = <double*>malloc(n * sizeof(double))
    result_arr = <double*>malloc(n * sizeof(double))
    
    if not is_scalar:
        arr2 = <double*>malloc(n * sizeof(double))
        if not arr2:
            if arr1: free(arr1)
            if result_arr: free(result_arr)
            raise MemoryError("Failed to allocate memory")
    
    if not arr1 or not result_arr:
        if arr1: free(arr1)
        if arr2: free(arr2)
        if result_arr: free(result_arr)
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy first array
        for i in range(n):
            arr1[i] = <double>data1[i]
        
        if is_scalar:
            # Scalar division
            scalar = <double>data2
            if scalar == 0:
                # Handle division by zero
                for i in range(n):
                    if arr1[i] > 0:
                        result_arr[i] = float('inf')
                    elif arr1[i] < 0:
                        result_arr[i] = float('-inf')
                    else:
                        result_arr[i] = float('nan')
            else:
                for i in range(n):
                    result_arr[i] = arr1[i] / scalar
        else:
            # Element-wise division
            for i in range(n):
                arr2[i] = <double>data2[i]
            for i in range(n):
                if arr2[i] == 0:
                    if arr1[i] > 0:
                        result_arr[i] = float('inf')
                    elif arr1[i] < 0:
                        result_arr[i] = float('-inf')
                    else:
                        result_arr[i] = float('nan')
                else:
                    result_arr[i] = arr1[i] / arr2[i]
        
        # Copy result back
        result_list = [result_arr[i] for i in range(n)]
        
        return result_list, shape1
    
    finally:
        free(arr1)
        if arr2: free(arr2)
        free(result_arr)


def _floor_divide_cython(data1, data2, shape1, shape2):
    """Floor division not yet optimized in Cython."""
    raise NotImplementedError(
        "floor_divide() not yet implemented in Cython backend.\n"
        "Available in: python\n"
        "Switch backends or contribute the implementation!"
    )


def _mod_cython(data1, data2, shape1, shape2):
    """Modulo not yet optimized in Cython."""
    raise NotImplementedError(
        "mod() not yet implemented in Cython backend.\n"
        "Available in: python\n"
        "Switch backends or contribute the implementation!"
    )


def _power_cython(data1, data2, shape1, shape2):
    """Power not yet optimized in Cython."""
    raise NotImplementedError(
        "power() not yet implemented in Cython backend.\n"
        "Available in: python\n"
        "Switch backends or contribute the implementation!"
    )