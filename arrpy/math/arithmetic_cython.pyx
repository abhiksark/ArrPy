# cython: language_level=3, boundscheck=False, wraparound=False
"""
Cython-optimized arithmetic functions for ArrPy arrays.
"""

import cython
from libc.math cimport pow, fabs
from ..core.array_cython cimport Array

@cython.boundscheck(False)
@cython.wraparound(False)
cdef Array _apply_elementwise_fast(Array arr, func):
    """Apply a function element-wise to an array with fast iteration."""
    cdef list result_data = []
    cdef Py_ssize_t i
    
    for i in range(len(arr._data)):
        result_data.append(func(arr._data[i]))
    
    cdef Array new_array = Array([])
    new_array._data = result_data
    new_array._shape = arr._shape
    return new_array

def _apply_elementwise(arr, func):
    """Apply a function element-wise to an array."""
    if not isinstance(arr, Array):
        raise TypeError("Input must be an Array")
    
    return _apply_elementwise_fast(arr, func)

@cython.boundscheck(False)
@cython.wraparound(False)
def power_fast(Array arr, exponent):
    """Element-wise power function with Cython optimization."""
    cdef list result_data = []
    cdef Py_ssize_t i
    cdef double base, exp_val
    
    if isinstance(exponent, Array):
        if arr._shape != exponent._shape:
            raise ValueError("Shape mismatch")
        
        for i in range(len(arr._data)):
            base = arr._data[i]
            exp_val = exponent._data[i]
            result_data.append(pow(base, exp_val))
    else:
        exp_val = exponent
        for i in range(len(arr._data)):
            base = arr._data[i]
            result_data.append(pow(base, exp_val))
    
    cdef Array new_array = Array([])
    new_array._data = result_data
    new_array._shape = arr._shape
    return new_array

def power(arr, exponent):
    """Element-wise power function."""
    if isinstance(arr, Array):
        return power_fast(arr, exponent)
    
    if isinstance(exponent, Array):
        if arr._shape != exponent._shape:
            raise ValueError("Shape mismatch")
        result_data = [a ** b for a, b in zip(arr._data, exponent._data)]
    else:
        result_data = [x ** exponent for x in arr._data]
    
    new_array = Array([])
    new_array._data = result_data
    new_array._shape = arr._shape
    return new_array

@cython.boundscheck(False)
@cython.wraparound(False)
def absolute_fast(Array arr):
    """Element-wise absolute value with Cython optimization."""
    cdef list result_data = []
    cdef Py_ssize_t i
    cdef double x
    
    for i in range(len(arr._data)):
        x = arr._data[i]
        result_data.append(fabs(x))
    
    cdef Array new_array = Array([])
    new_array._data = result_data
    new_array._shape = arr._shape
    return new_array

def absolute(arr):
    """Element-wise absolute value."""
    if isinstance(arr, Array):
        return absolute_fast(arr)
    
    return _apply_elementwise(arr, abs)

@cython.boundscheck(False)
@cython.wraparound(False)
def sign_fast(Array arr):
    """Element-wise sign function with Cython optimization."""
    cdef list result_data = []
    cdef Py_ssize_t i
    cdef double x
    
    for i in range(len(arr._data)):
        x = arr._data[i]
        if x > 0:
            result_data.append(1)
        elif x < 0:
            result_data.append(-1)
        else:
            result_data.append(0)
    
    cdef Array new_array = Array([])
    new_array._data = result_data
    new_array._shape = arr._shape
    return new_array

def sign(arr):
    """Element-wise sign function."""
    if isinstance(arr, Array):
        return sign_fast(arr)
        
    def sign_func(x):
        if x > 0:
            return 1
        elif x < 0:
            return -1
        else:
            return 0
    
    return _apply_elementwise(arr, sign_func)

@cython.boundscheck(False)
@cython.wraparound(False)
def floor_divide_fast(Array arr, divisor):
    """Element-wise floor division with Cython optimization."""
    cdef list result_data = []
    cdef Py_ssize_t i
    cdef double a, b
    
    if isinstance(divisor, Array):
        if arr._shape != divisor._shape:
            raise ValueError("Shape mismatch")
        
        for i in range(len(arr._data)):
            a = arr._data[i]
            b = divisor._data[i]
            result_data.append(a // b)
    else:
        b = divisor
        for i in range(len(arr._data)):
            a = arr._data[i]
            result_data.append(a // b)
    
    cdef Array new_array = Array([])
    new_array._data = result_data
    new_array._shape = arr._shape
    return new_array

def floor_divide(arr, divisor):
    """Element-wise floor division."""
    if isinstance(arr, Array):
        return floor_divide_fast(arr, divisor)
    
    if isinstance(divisor, Array):
        if arr._shape != divisor._shape:
            raise ValueError("Shape mismatch")
        result_data = [a // b for a, b in zip(arr._data, divisor._data)]
    else:
        result_data = [x // divisor for x in arr._data]
    
    new_array = Array([])
    new_array._data = result_data
    new_array._shape = arr._shape
    return new_array

@cython.boundscheck(False)
@cython.wraparound(False)
def mod_fast(Array arr, divisor):
    """Element-wise modulo operation with Cython optimization."""
    cdef list result_data = []
    cdef Py_ssize_t i
    cdef double a, b
    
    if isinstance(divisor, Array):
        if arr._shape != divisor._shape:
            raise ValueError("Shape mismatch")
        
        for i in range(len(arr._data)):
            a = arr._data[i]
            b = divisor._data[i]
            result_data.append(a % b)
    else:
        b = divisor
        for i in range(len(arr._data)):
            a = arr._data[i]
            result_data.append(a % b)
    
    cdef Array new_array = Array([])
    new_array._data = result_data
    new_array._shape = arr._shape
    return new_array

def mod(arr, divisor):
    """Element-wise modulo operation."""
    if isinstance(arr, Array):
        return mod_fast(arr, divisor)
    
    if isinstance(divisor, Array):
        if arr._shape != divisor._shape:
            raise ValueError("Shape mismatch")
        result_data = [a % b for a, b in zip(arr._data, divisor._data)]
    else:
        result_data = [x % divisor for x in arr._data]
    
    new_array = Array([])
    new_array._data = result_data
    new_array._shape = arr._shape
    return new_array

# Aliases
abs = absolute
# Note: Cannot alias 'pow' due to conflict with C math function