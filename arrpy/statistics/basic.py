"""
Basic statistical functions for ArrPy arrays.

This module provides fundamental statistical functions that operate
on array data, such as sum, mean, min, max, std, var, etc.
"""

from ..core import Array


def sum(arr):
    """
    Calculate the sum of array elements.
    
    Parameters
    ----------
    arr : Array
        Input array.
        
    Returns
    -------
    scalar
        Sum of array elements.
        
    Examples
    --------
    >>> sum(Array([1, 2, 3, 4]))
    10
    """
    if not isinstance(arr, Array):
        raise TypeError("Input must be an Array")
    return __builtins__['sum'](arr._data)


def mean(arr):
    """
    Calculate the arithmetic mean of array elements.
    
    Parameters
    ----------
    arr : Array
        Input array.
        
    Returns
    -------
    scalar
        Mean of array elements.
        
    Examples
    --------
    >>> mean(Array([1, 2, 3, 4]))
    2.5
    """
    if not isinstance(arr, Array):
        raise TypeError("Input must be an Array")
    if not arr._data:
        raise ValueError("Cannot calculate mean of empty array")
    return __builtins__['sum'](arr._data) / len(arr._data)


def min(arr):
    """
    Find the minimum value in the array.
    
    Parameters
    ----------
    arr : Array
        Input array.
        
    Returns
    -------
    scalar
        Minimum value in the array.
        
    Examples
    --------
    >>> min(Array([3, 1, 4, 1, 5]))
    1
    """
    if not isinstance(arr, Array):
        raise TypeError("Input must be an Array")
    if not arr._data:
        raise ValueError("Cannot calculate min of empty array")
    return __builtins__['min'](arr._data)


def max(arr):
    """
    Find the maximum value in the array.
    
    Parameters
    ----------
    arr : Array
        Input array.
        
    Returns
    -------
    scalar
        Maximum value in the array.
        
    Examples
    --------
    >>> max(Array([3, 1, 4, 1, 5]))
    5
    """
    if not isinstance(arr, Array):
        raise TypeError("Input must be an Array")
    if not arr._data:
        raise ValueError("Cannot calculate max of empty array")
    return __builtins__['max'](arr._data)


def std(arr, ddof=0):
    """
    Calculate the standard deviation of array elements.
    
    Parameters
    ----------
    arr : Array
        Input array.
    ddof : int, optional
        Delta degrees of freedom. Default is 0.
        
    Returns
    -------
    scalar
        Standard deviation of array elements.
        
    Examples
    --------
    >>> std(Array([1, 2, 3, 4]))
    1.118...
    """
    if not isinstance(arr, Array):
        raise TypeError("Input must be an Array")
    if not arr._data:
        raise ValueError("Cannot calculate std of empty array")
    
    mean_val = mean(arr)
    variance = __builtins__['sum']((x - mean_val) ** 2 for x in arr._data) / (len(arr._data) - ddof)
    return variance ** 0.5


def var(arr, ddof=0):
    """
    Calculate the variance of array elements.
    
    Parameters
    ----------
    arr : Array
        Input array.
    ddof : int, optional
        Delta degrees of freedom. Default is 0.
        
    Returns
    -------
    scalar
        Variance of array elements.
        
    Examples
    --------
    >>> var(Array([1, 2, 3, 4]))
    1.25
    """
    if not isinstance(arr, Array):
        raise TypeError("Input must be an Array")
    if not arr._data:
        raise ValueError("Cannot calculate var of empty array")
    
    mean_val = mean(arr)
    return __builtins__['sum']((x - mean_val) ** 2 for x in arr._data) / (len(arr._data) - ddof)


def median(arr):
    """
    Calculate the median of array elements.
    
    Parameters
    ----------
    arr : Array
        Input array.
        
    Returns
    -------
    scalar
        Median of array elements.
        
    Examples
    --------
    >>> median(Array([3, 1, 4, 1, 5]))
    3
    """
    if not isinstance(arr, Array):
        raise TypeError("Input must be an Array")
    if not arr._data:
        raise ValueError("Cannot calculate median of empty array")
    
    sorted_data = sorted(arr._data)
    n = len(sorted_data)
    if n % 2 == 0:
        return (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
    else:
        return sorted_data[n//2]


def percentile(arr, q):
    """
    Calculate the q-th percentile of array elements.
    
    Parameters
    ----------
    arr : Array
        Input array.
    q : float or array-like
        Percentile to compute (0-100).
        
    Returns
    -------
    scalar
        q-th percentile of array elements.
        
    Examples
    --------
    >>> percentile(Array([1, 2, 3, 4, 5]), 50)
    3
    >>> percentile(Array([1, 2, 3, 4, 5]), 25)
    2
    """
    if not isinstance(arr, Array):
        raise TypeError("Input must be an Array")
    if not arr._data:
        raise ValueError("Cannot calculate percentile of empty array")
    if not 0 <= q <= 100:
        raise ValueError("Percentile must be between 0 and 100")
    
    sorted_data = sorted(arr._data)
    if q == 0:
        return sorted_data[0]
    if q == 100:
        return sorted_data[-1]
    
    index = (len(sorted_data) - 1) * q / 100
    lower = int(index)
    upper = lower + 1
    
    if upper >= len(sorted_data):
        return sorted_data[lower]
    
    weight = index - lower
    return sorted_data[lower] * (1 - weight) + sorted_data[upper] * weight