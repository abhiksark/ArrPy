# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: nonecheck=False
# cython: cdivision=True

"""
Optimized universal functions (ufuncs) for Cython backend.
Uses C math library for fast transcendental functions.
"""

import cython
from libc.math cimport sin, cos, tan, exp, log, log10, sqrt, pow, fabs
from libc.math cimport asin, acos, atan, sinh, cosh, tanh
from libc.stdlib cimport malloc, free

@cython.boundscheck(False)
@cython.wraparound(False)
def _sin_cython(data, shape):
    """Optimized sine function using C math library."""
    cdef int i
    cdef int n = len(data)
    cdef double* arr = <double*>malloc(n * sizeof(double))
    cdef double* result_arr = <double*>malloc(n * sizeof(double))
    
    if not arr or not result_arr:
        if arr:
            free(arr)
        if result_arr:
            free(result_arr)
        raise MemoryError("Failed to allocate memory")
    
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
        free(arr)
        free(result_arr)

@cython.boundscheck(False)
@cython.wraparound(False)
def _cos_cython(data, shape):
    """Optimized cosine function using C math library."""
    cdef int i
    cdef int n = len(data)
    cdef double* arr = <double*>malloc(n * sizeof(double))
    cdef double* result_arr = <double*>malloc(n * sizeof(double))
    
    if not arr or not result_arr:
        if arr:
            free(arr)
        if result_arr:
            free(result_arr)
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy input data
        for i in range(n):
            arr[i] = float(data[i])
        
        # Apply cosine
        for i in range(n):
            result_arr[i] = cos(arr[i])
        
        # Convert to Python list
        result = []
        for i in range(n):
            result.append(result_arr[i])
        
        return result, shape
    
    finally:
        free(arr)
        free(result_arr)

@cython.boundscheck(False)
@cython.wraparound(False)
def _tan_cython(data, shape):
    """Optimized tangent function using C math library."""
    cdef int i
    cdef int n = len(data)
    cdef double* arr = <double*>malloc(n * sizeof(double))
    cdef double* result_arr = <double*>malloc(n * sizeof(double))
    
    if not arr or not result_arr:
        if arr:
            free(arr)
        if result_arr:
            free(result_arr)
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy input data
        for i in range(n):
            arr[i] = float(data[i])
        
        # Apply tangent
        for i in range(n):
            result_arr[i] = tan(arr[i])
        
        # Convert to Python list
        result = []
        for i in range(n):
            result.append(result_arr[i])
        
        return result, shape
    
    finally:
        free(arr)
        free(result_arr)

@cython.boundscheck(False)
@cython.wraparound(False)
def _exp_cython(data, shape):
    """Optimized exponential function using C math library."""
    cdef int i
    cdef int n = len(data)
    cdef double* arr = <double*>malloc(n * sizeof(double))
    cdef double* result_arr = <double*>malloc(n * sizeof(double))
    
    if not arr or not result_arr:
        if arr:
            free(arr)
        if result_arr:
            free(result_arr)
        raise MemoryError("Failed to allocate memory")
    
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
        free(arr)
        free(result_arr)

@cython.boundscheck(False)
@cython.wraparound(False)
def _log_cython(data, shape):
    """Optimized natural logarithm using C math library."""
    cdef int i
    cdef int n = len(data)
    cdef double* arr = <double*>malloc(n * sizeof(double))
    cdef double* result_arr = <double*>malloc(n * sizeof(double))
    
    if not arr or not result_arr:
        if arr:
            free(arr)
        if result_arr:
            free(result_arr)
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy input data
        for i in range(n):
            arr[i] = float(data[i])
        
        # Apply natural log
        for i in range(n):
            result_arr[i] = log(arr[i])
        
        # Convert to Python list
        result = []
        for i in range(n):
            result.append(result_arr[i])
        
        return result, shape
    
    finally:
        free(arr)
        free(result_arr)

@cython.boundscheck(False)
@cython.wraparound(False)
def _log10_cython(data, shape):
    """Optimized base-10 logarithm using C math library."""
    cdef int i
    cdef int n = len(data)
    cdef double* arr = <double*>malloc(n * sizeof(double))
    cdef double* result_arr = <double*>malloc(n * sizeof(double))
    
    if not arr or not result_arr:
        if arr:
            free(arr)
        if result_arr:
            free(result_arr)
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy input data
        for i in range(n):
            arr[i] = float(data[i])
        
        # Apply log10
        for i in range(n):
            result_arr[i] = log10(arr[i])
        
        # Convert to Python list
        result = []
        for i in range(n):
            result.append(result_arr[i])
        
        return result, shape
    
    finally:
        free(arr)
        free(result_arr)

@cython.boundscheck(False)
@cython.wraparound(False)
def _sqrt_cython(data, shape):
    """Optimized square root using C math library."""
    cdef int i
    cdef int n = len(data)
    cdef double* arr = <double*>malloc(n * sizeof(double))
    cdef double* result_arr = <double*>malloc(n * sizeof(double))
    
    if not arr or not result_arr:
        if arr:
            free(arr)
        if result_arr:
            free(result_arr)
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy input data
        for i in range(n):
            arr[i] = float(data[i])
        
        # Apply sqrt
        for i in range(n):
            result_arr[i] = sqrt(arr[i])
        
        # Convert to Python list
        result = []
        for i in range(n):
            result.append(result_arr[i])
        
        return result, shape
    
    finally:
        free(arr)
        free(result_arr)

@cython.boundscheck(False)
@cython.wraparound(False)
def _power_cython(data1, data2, shape1, shape2):
    """Optimized power function using C math library."""
    cdef int i
    cdef int n = len(data1)
    cdef double* arr1 = <double*>malloc(n * sizeof(double))
    cdef double* arr2 = <double*>malloc(n * sizeof(double))
    cdef double* result_arr = <double*>malloc(n * sizeof(double))
    cdef double scalar_power
    cdef int is_scalar = 0
    
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
        
        # Check if second argument is scalar
        if len(data2) == 1:
            is_scalar = 1
            scalar_power = float(data2[0])
        else:
            for i in range(n):
                arr2[i] = float(data2[i])
        
        # Apply power
        if is_scalar:
            for i in range(n):
                result_arr[i] = pow(arr1[i], scalar_power)
        else:
            for i in range(n):
                result_arr[i] = pow(arr1[i], arr2[i])
        
        # Convert to Python list
        result = []
        for i in range(n):
            result.append(result_arr[i])
        
        return result, shape1
    
    finally:
        free(arr1)
        free(arr2)
        free(result_arr)

@cython.boundscheck(False)
@cython.wraparound(False)
def _absolute_cython(data, shape):
    """Optimized absolute value using C math library."""
    cdef int i
    cdef int n = len(data)
    cdef double* arr = <double*>malloc(n * sizeof(double))
    cdef double* result_arr = <double*>malloc(n * sizeof(double))
    
    if not arr or not result_arr:
        if arr:
            free(arr)
        if result_arr:
            free(result_arr)
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy input data
        for i in range(n):
            arr[i] = float(data[i])
        
        # Apply absolute value
        for i in range(n):
            result_arr[i] = fabs(arr[i])
        
        # Convert to Python list
        result = []
        for i in range(n):
            result.append(result_arr[i])
        
        return result, shape
    
    finally:
        free(arr)
        free(result_arr)

# Inverse trig functions
@cython.boundscheck(False)
@cython.wraparound(False)
def _arcsin_cython(data, shape):
    """Optimized arcsine using C math library."""
    cdef int i
    cdef int n = len(data)
    cdef double* arr = <double*>malloc(n * sizeof(double))
    cdef double* result_arr = <double*>malloc(n * sizeof(double))
    
    if not arr or not result_arr:
        if arr:
            free(arr)
        if result_arr:
            free(result_arr)
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy input data
        for i in range(n):
            arr[i] = float(data[i])
        
        # Apply arcsine
        for i in range(n):
            result_arr[i] = asin(arr[i])
        
        # Convert to Python list
        result = []
        for i in range(n):
            result.append(result_arr[i])
        
        return result, shape
    
    finally:
        free(arr)
        free(result_arr)

@cython.boundscheck(False)
@cython.wraparound(False)
def _arccos_cython(data, shape):
    """Optimized arccosine using C math library."""
    cdef int i
    cdef int n = len(data)
    cdef double* arr = <double*>malloc(n * sizeof(double))
    cdef double* result_arr = <double*>malloc(n * sizeof(double))
    
    if not arr or not result_arr:
        if arr:
            free(arr)
        if result_arr:
            free(result_arr)
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy input data
        for i in range(n):
            arr[i] = float(data[i])
        
        # Apply arccosine
        for i in range(n):
            result_arr[i] = acos(arr[i])
        
        # Convert to Python list
        result = []
        for i in range(n):
            result.append(result_arr[i])
        
        return result, shape
    
    finally:
        free(arr)
        free(result_arr)

@cython.boundscheck(False)
@cython.wraparound(False)
def _arctan_cython(data, shape):
    """Optimized arctangent using C math library."""
    cdef int i
    cdef int n = len(data)
    cdef double* arr = <double*>malloc(n * sizeof(double))
    cdef double* result_arr = <double*>malloc(n * sizeof(double))
    
    if not arr or not result_arr:
        if arr:
            free(arr)
        if result_arr:
            free(result_arr)
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy input data
        for i in range(n):
            arr[i] = float(data[i])
        
        # Apply arctangent
        for i in range(n):
            result_arr[i] = atan(arr[i])
        
        # Convert to Python list
        result = []
        for i in range(n):
            result.append(result_arr[i])
        
        return result, shape
    
    finally:
        free(arr)
        free(result_arr)

# Hyperbolic functions
@cython.boundscheck(False)
@cython.wraparound(False)
def _sinh_cython(data, shape):
    """Optimized hyperbolic sine using C math library."""
    cdef int i
    cdef int n = len(data)
    cdef double* arr = <double*>malloc(n * sizeof(double))
    cdef double* result_arr = <double*>malloc(n * sizeof(double))
    
    if not arr or not result_arr:
        if arr:
            free(arr)
        if result_arr:
            free(result_arr)
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy input data
        for i in range(n):
            arr[i] = float(data[i])
        
        # Apply hyperbolic sine
        for i in range(n):
            result_arr[i] = sinh(arr[i])
        
        # Convert to Python list
        result = []
        for i in range(n):
            result.append(result_arr[i])
        
        return result, shape
    
    finally:
        free(arr)
        free(result_arr)

@cython.boundscheck(False)
@cython.wraparound(False)
def _cosh_cython(data, shape):
    """Optimized hyperbolic cosine using C math library."""
    cdef int i
    cdef int n = len(data)
    cdef double* arr = <double*>malloc(n * sizeof(double))
    cdef double* result_arr = <double*>malloc(n * sizeof(double))
    
    if not arr or not result_arr:
        if arr:
            free(arr)
        if result_arr:
            free(result_arr)
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy input data
        for i in range(n):
            arr[i] = float(data[i])
        
        # Apply hyperbolic cosine
        for i in range(n):
            result_arr[i] = cosh(arr[i])
        
        # Convert to Python list
        result = []
        for i in range(n):
            result.append(result_arr[i])
        
        return result, shape
    
    finally:
        free(arr)
        free(result_arr)

@cython.boundscheck(False)
@cython.wraparound(False)
def _tanh_cython(data, shape):
    """Optimized hyperbolic tangent using C math library."""
    cdef int i
    cdef int n = len(data)
    cdef double* arr = <double*>malloc(n * sizeof(double))
    cdef double* result_arr = <double*>malloc(n * sizeof(double))
    
    if not arr or not result_arr:
        if arr:
            free(arr)
        if result_arr:
            free(result_arr)
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy input data
        for i in range(n):
            arr[i] = float(data[i])
        
        # Apply hyperbolic tangent
        for i in range(n):
            result_arr[i] = tanh(arr[i])
        
        # Convert to Python list
        result = []
        for i in range(n):
            result.append(result_arr[i])
        
        return result, shape
    
    finally:
        free(arr)
        free(result_arr)