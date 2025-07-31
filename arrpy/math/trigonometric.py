"""
Trigonometric functions for ArrPy arrays.

This module provides trigonometric and inverse trigonometric functions
that operate element-wise on arrays.
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


def sin(arr):
    """
    Element-wise sine function.
    
    Parameters
    ----------
    arr : Array
        Input array.
        
    Returns
    -------
    Array
        Array with sine of each element.
        
    Examples
    --------
    >>> import math
    >>> sin(Array([0, math.pi/2, math.pi]))
    Array([0.0, 1.0, 1.2246...e-16])
    """
    return _apply_elementwise(arr, math.sin)


def cos(arr):
    """
    Element-wise cosine function.
    
    Parameters
    ----------
    arr : Array
        Input array.
        
    Returns
    -------
    Array
        Array with cosine of each element.
        
    Examples
    --------
    >>> import math
    >>> cos(Array([0, math.pi/2, math.pi]))
    Array([1.0, 6.123...e-17, -1.0])
    """
    return _apply_elementwise(arr, math.cos)


def tan(arr):
    """
    Element-wise tangent function.
    
    Parameters
    ----------
    arr : Array
        Input array.
        
    Returns
    -------
    Array
        Array with tangent of each element.
        
    Examples
    --------
    >>> import math
    >>> tan(Array([0, math.pi/4, math.pi]))
    Array([0.0, 1.0, -1.224...e-16])
    """
    return _apply_elementwise(arr, math.tan)


def arcsin(arr):
    """
    Element-wise inverse sine function.
    
    Parameters
    ----------
    arr : Array
        Input array. Values should be in range [-1, 1].
        
    Returns
    -------
    Array
        Array with arcsine of each element in radians.
        
    Examples
    --------
    >>> arcsin(Array([0, 0.5, 1]))
    Array([0.0, 0.523..., 1.570...])
    """
    return _apply_elementwise(arr, math.asin)


def arccos(arr):
    """
    Element-wise inverse cosine function.
    
    Parameters
    ----------
    arr : Array
        Input array. Values should be in range [-1, 1].
        
    Returns
    -------
    Array
        Array with arccosine of each element in radians.
        
    Examples
    --------
    >>> arccos(Array([1, 0.5, 0]))
    Array([0.0, 1.047..., 1.570...])
    """
    return _apply_elementwise(arr, math.acos)


def arctan(arr):
    """
    Element-wise inverse tangent function.
    
    Parameters
    ----------
    arr : Array
        Input array.
        
    Returns
    -------
    Array
        Array with arctangent of each element in radians.
        
    Examples
    --------
    >>> arctan(Array([0, 1, -1]))
    Array([0.0, 0.785..., -0.785...])
    """
    return _apply_elementwise(arr, math.atan)


# Aliases for compatibility
asin = arcsin
acos = arccos  
atan = arctan