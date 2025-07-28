"""
Range-based array creation functions.

This module provides functions for creating arrays with evenly spaced values,
such as arange, linspace, and logspace.
"""

import math
from ..core.array import Array


def arange(start, stop=None, step=1):
    """
    Create an array with evenly spaced values within a given interval.
    
    Parameters
    ----------
    start : number
        Start of interval. When stop is provided, this is the start.
        When stop is not provided, this becomes the stop and start=0.
    stop : number, optional
        End of interval (exclusive).
    step : number, optional
        Spacing between values. Default is 1.
        
    Returns
    -------
    Array
        Array of evenly spaced values.
        
    Examples
    --------
    >>> arange(3)
    Array([0, 1, 2])
    >>> arange(1, 4)
    Array([1, 2, 3])
    >>> arange(0, 6, 2)
    Array([0, 2, 4])
    """
    if stop is None:
        stop = start
        start = 0
    
    data = []
    current = start
    while current < stop:
        data.append(current)
        current += step
    
    return Array(data)


def linspace(start, stop, num=50, endpoint=True):
    """
    Create an array with evenly spaced numbers over a specified interval.
    
    Parameters
    ----------
    start : scalar
        Starting value of the sequence.
    stop : scalar
        End value of the sequence.
    num : int, optional
        Number of samples to generate. Default is 50.
    endpoint : bool, optional
        If True, stop is the last sample. Otherwise, it is not included.
        Default is True.
        
    Returns
    -------
    Array
        Array of evenly spaced samples.
        
    Examples
    --------
    >>> linspace(0, 1, 5)
    Array([0.0, 0.25, 0.5, 0.75, 1.0])
    >>> linspace(0, 1, 5, endpoint=False)
    Array([0.0, 0.2, 0.4, 0.6, 0.8])
    """
    if num <= 0:
        raise ValueError("Number of samples must be positive")
    
    if num == 1:
        return Array([start])
    
    if endpoint:
        step = (stop - start) / (num - 1)
        data = [start + i * step for i in range(num)]
    else:
        step = (stop - start) / num
        data = [start + i * step for i in range(num)]
    
    return Array(data)


def logspace(start, stop, num=50, endpoint=True, base=10.0):
    """
    Create an array with numbers spaced evenly on a log scale.
    
    Parameters
    ----------
    start : scalar
        Base**start is the starting value of the sequence.
    stop : scalar
        Base**stop is the final value of the sequence.
    num : int, optional
        Number of samples to generate. Default is 50.
    endpoint : bool, optional
        If True, stop is the last sample. Otherwise, it is not included.
        Default is True.
    base : scalar, optional
        The base of the log space. Default is 10.0.
        
    Returns
    -------
    Array
        Array of samples logarithmically spaced.
        
    Examples
    --------
    >>> logspace(0, 2, 5)  # 10^0 to 10^2
    Array([1.0, 3.16..., 10.0, 31.6..., 100.0])
    """
    if num <= 0:
        raise ValueError("Number of samples must be positive")
    
    if num == 1:
        return Array([base ** start])
    
    if endpoint:
        step = (stop - start) / (num - 1)
        exponents = [start + i * step for i in range(num)]
    else:
        step = (stop - start) / num
        exponents = [start + i * step for i in range(num)]
    
    data = [base ** exp for exp in exponents]
    return Array(data)