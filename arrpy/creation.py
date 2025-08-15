"""
Array creation functions for arrpy.
"""

from .arrpy import arrpy


def zeros(shape, dtype=None):
    """
    Create an array filled with zeros.
    
    Parameters
    ----------
    shape : tuple of ints
        Shape of the array
    dtype : dtype, optional
        Desired data type
    
    Returns
    -------
    arrpy
        Array of zeros with given shape
    """
    # TODO: Implement zeros
    pass


def ones(shape, dtype=None):
    """
    Create an array filled with ones.
    
    Parameters
    ----------
    shape : tuple of ints
        Shape of the array
    dtype : dtype, optional
        Desired data type
    
    Returns
    -------
    arrpy
        Array of ones with given shape
    """
    # TODO: Implement ones
    pass


def arange(start, stop=None, step=1, dtype=None):
    """
    Create an array with evenly spaced values.
    
    Parameters
    ----------
    start : number
        Start of interval (or stop if stop is None)
    stop : number, optional
        End of interval
    step : number, optional
        Spacing between values
    dtype : dtype, optional
        Desired data type
    
    Returns
    -------
    arrpy
        Array of evenly spaced values
    """
    # TODO: Implement arange
    pass


def linspace(start, stop, num=50, endpoint=True, dtype=None):
    """
    Create an array with evenly spaced values over a specified interval.
    
    Parameters
    ----------
    start : number
        Start of interval
    stop : number
        End of interval
    num : int, optional
        Number of samples
    endpoint : bool, optional
        Whether to include stop
    dtype : dtype, optional
        Desired data type
    
    Returns
    -------
    arrpy
        Array of evenly spaced values
    """
    # TODO: Implement linspace
    pass


def array(data, dtype=None):
    """
    Create an array from input data.
    
    Parameters
    ----------
    data : array-like
        Input data
    dtype : dtype, optional
        Desired data type
    
    Returns
    -------
    arrpy
        Array created from input data
    """
    return arrpy(data, dtype=dtype)