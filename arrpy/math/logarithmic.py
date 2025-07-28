"""
Logarithmic and exponential functions for ArrPy arrays.
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


def exp(arr):
    """Element-wise exponential function."""
    return _apply_elementwise(arr, math.exp)


def log(arr):
    """Element-wise natural logarithm."""
    return _apply_elementwise(arr, math.log)


def log10(arr):
    """Element-wise base-10 logarithm.""" 
    return _apply_elementwise(arr, math.log10)


def log2(arr):
    """Element-wise base-2 logarithm."""
    return _apply_elementwise(arr, math.log2)


def sqrt(arr):
    """Element-wise square root."""
    return _apply_elementwise(arr, math.sqrt)