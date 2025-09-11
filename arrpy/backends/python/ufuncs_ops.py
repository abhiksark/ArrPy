"""
Universal functions (ufuncs) for Python backend.

Pure Python implementations of mathematical functions.
"""

import math


def _sin_python(data, shape):
    """
    Pure Python sine function.
    
    Parameters
    ----------
    data : list
        Flattened array data
    shape : tuple
        Shape of the array
        
    Returns
    -------
    tuple
        (result_data, result_shape)
    """
    result = []
    for value in data:
        result.append(math.sin(value))
    
    return result, shape


def _cos_python(data, shape):
    """
    Pure Python cosine function.
    
    Parameters
    ----------
    data : list
        Flattened array data
    shape : tuple
        Shape of the array
        
    Returns
    -------
    tuple
        (result_data, result_shape)
    """
    result = []
    for value in data:
        result.append(math.cos(value))
    
    return result, shape


def _exp_python(data, shape):
    """
    Pure Python exponential function.
    
    Parameters
    ----------
    data : list
        Flattened array data
    shape : tuple
        Shape of the array
        
    Returns
    -------
    tuple
        (result_data, result_shape)
    """
    result = []
    for value in data:
        result.append(math.exp(value))
    
    return result, shape


def _log_python(data, shape):
    """
    Pure Python natural logarithm.
    
    Parameters
    ----------
    data : list
        Flattened array data
    shape : tuple
        Shape of the array
        
    Returns
    -------
    tuple
        (result_data, result_shape)
    """
    result = []
    for value in data:
        if value <= 0:
            result.append(float('-inf') if value == 0 else float('nan'))
        else:
            result.append(math.log(value))
    
    return result, shape


def _sqrt_python(data, shape):
    """
    Pure Python square root.
    
    Parameters
    ----------
    data : list
        Flattened array data
    shape : tuple
        Shape of the array
        
    Returns
    -------
    tuple
        (result_data, result_shape)
    """
    result = []
    for value in data:
        if value < 0:
            result.append(float('nan'))
        else:
            result.append(math.sqrt(value))
    
    return result, shape