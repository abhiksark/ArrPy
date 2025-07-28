"""
Rounding functions for ArrPy arrays.

This module provides rounding functions that operate element-wise on arrays.
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


def floor(arr):
    """
    Element-wise floor function.
    
    Returns the largest integer less than or equal to each element.
    
    Parameters
    ----------
    arr : Array
        Input array.
        
    Returns
    -------
    Array
        Array with floor of each element.
        
    Examples
    --------
    >>> floor(Array([1.2, 2.7, -1.3]))
    Array([1, 2, -2])
    """
    return _apply_elementwise(arr, math.floor)


def ceil(arr):
    """
    Element-wise ceiling function.
    
    Returns the smallest integer greater than or equal to each element.
    
    Parameters
    ----------
    arr : Array
        Input array.
        
    Returns
    -------
    Array
        Array with ceiling of each element.
        
    Examples
    --------
    >>> ceil(Array([1.2, 2.7, -1.3]))
    Array([2, 3, -1])
    """
    return _apply_elementwise(arr, math.ceil)


def round(arr, decimals=0):
    """
    Element-wise rounding function.
    
    Rounds each element to the given number of decimals.
    
    Parameters
    ----------
    arr : Array
        Input array.
    decimals : int, optional
        Number of decimal places to round to. Default is 0.
        
    Returns
    -------
    Array
        Array with rounded elements.
        
    Examples
    --------
    >>> round(Array([1.234, 2.567, -1.789]))
    Array([1, 3, -2])
    >>> round(Array([1.234, 2.567, -1.789]), 1)
    Array([1.2, 2.6, -1.8])
    """
    builtin_round = __builtins__['round']
    if decimals == 0:
        return _apply_elementwise(arr, lambda x: int(builtin_round(x)))
    else:
        return _apply_elementwise(arr, lambda x: builtin_round(x, decimals))


def trunc(arr):
    """
    Element-wise truncation function.
    
    Returns the integer part of each element (truncate towards zero).
    
    Parameters
    ----------
    arr : Array
        Input array.
        
    Returns
    -------
    Array
        Array with truncated elements.
        
    Examples
    --------
    >>> trunc(Array([1.7, 2.3, -1.8]))
    Array([1, 2, -1])
    """
    return _apply_elementwise(arr, math.trunc)


def fix(arr):
    """
    Element-wise fix function.
    
    Round each element towards zero. Alias for trunc.
    
    Parameters
    ----------
    arr : Array
        Input array.
        
    Returns
    -------
    Array
        Array with fixed elements.
        
    Examples
    --------
    >>> fix(Array([1.7, 2.3, -1.8]))
    Array([1, 2, -1])
    """
    return trunc(arr)


# Aliases for compatibility
around = round