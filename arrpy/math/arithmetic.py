"""
Arithmetic functions for ArrPy arrays.
"""

import math
from ..core.array import Array


def _apply_elementwise(arr, func):
    """Apply a function element-wise to an array."""
    if not isinstance(arr, Array):
        raise TypeError("Input must be an Array")
    
    result_data = [func(x) for x in arr._data]
    new_array = Array([])
    new_array._data = result_data
    new_array._shape = arr._shape
    return new_array


def power(arr, exponent):
    """Element-wise power function."""
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


def absolute(arr):
    """Element-wise absolute value."""
    return _apply_elementwise(arr, __builtins__['abs'])


def sign(arr):
    """Element-wise sign function."""
    def sign_func(x):
        if x > 0:
            return 1
        elif x < 0:
            return -1
        else:
            return 0
    
    return _apply_elementwise(arr, sign_func)


def floor_divide(arr, divisor):
    """Element-wise floor division."""
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


def mod(arr, divisor):
    """Element-wise modulo operation."""
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
pow = power