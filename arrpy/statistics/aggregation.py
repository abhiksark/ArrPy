"""
Aggregation functions for ArrPy arrays.
"""

from ..core import Array


def prod(arr):
    """Calculate product of array elements."""
    if not isinstance(arr, Array):
        raise TypeError("Input must be an Array")
    result = 1
    for x in arr._data:
        result *= x
    return result


def cumsum(arr):
    """Calculate cumulative sum."""
    if not isinstance(arr, Array):
        raise TypeError("Input must be an Array")
    
    result_data = []
    cumulative = 0
    for x in arr._data:
        cumulative += x
        result_data.append(cumulative)
    
    # Create array with the result data and reshape if needed
    result = Array(result_data)
    if arr.ndim > 1:
        result = result.reshape(arr.shape)
    return result


def cumprod(arr):
    """Calculate cumulative product."""
    if not isinstance(arr, Array):
        raise TypeError("Input must be an Array")
    
    result_data = []
    cumulative = 1
    for x in arr._data:
        cumulative *= x
        result_data.append(cumulative)
    
    # Create array with the result data and reshape if needed
    result = Array(result_data)
    if arr.ndim > 1:
        result = result.reshape(arr.shape)
    return result


def argmin(arr):
    """Return index of minimum value."""
    if not isinstance(arr, Array):
        raise TypeError("Input must be an Array")
    if not arr._data:
        raise ValueError("Cannot find argmin of empty array")
    
    min_val = min(arr._data)
    return arr._data.index(min_val)


def argmax(arr):
    """Return index of maximum value."""
    if not isinstance(arr, Array):
        raise TypeError("Input must be an Array")
    if not arr._data:
        raise ValueError("Cannot find argmax of empty array")
    
    max_val = max(arr._data)
    return arr._data.index(max_val)