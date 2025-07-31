"""
Logarithmic and exponential functions for ArrPy arrays.
"""

import math
from ..core import Array


def _apply_elementwise(arr, func):
    """Apply a function element-wise to an array."""
    if not isinstance(arr, Array):
        raise TypeError("Input must be an Array")
    
    # Flatten the array, apply function, then reshape
    result_data = [func(x) for x in arr._data]
    
    # Create array with the result data and reshape if needed
    result = Array(result_data)
    if arr.ndim > 1:
        result = result.reshape(arr.shape)
    
    return result


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