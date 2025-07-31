# cython: language_level=3, boundscheck=False, wraparound=False
"""
Cython-optimized basic array creation functions.

This module provides functions for creating arrays filled with specific values
or patterns, such as zeros, ones, empty arrays, and identity matrices.
"""

import cython
from ..core.array_cython cimport Array

@cython.boundscheck(False)
@cython.wraparound(False)
def zeros_fast(shape):
    """
    Create an array filled with zeros using Cython optimization.
    
    Parameters
    ----------
    shape : int or tuple of ints
        Shape of the new array.
        
    Returns
    -------
    Array
        Array of zeros with the given shape.
    """
    cdef tuple final_shape
    cdef long total_size = 1
    cdef long dim
    cdef Py_ssize_t i
    
    if isinstance(shape, int):
        if shape < 0:
            raise ValueError("Shape dimensions must be non-negative")
        final_shape = (shape,)
    elif isinstance(shape, (tuple, list)):
        for dim in shape:
            if not isinstance(dim, int) or dim < 0:
                raise ValueError("Shape dimensions must be non-negative integers")
        final_shape = tuple(shape)
    else:
        raise TypeError("Shape must be int or tuple of ints")
    
    for dim in final_shape:
        total_size *= dim
    
    cdef list data = [0] * total_size
    cdef Array arr = Array([])
    arr._data = data
    arr._shape = final_shape
    return arr

def zeros(shape):
    """
    Create an array filled with zeros.
    
    Parameters
    ----------
    shape : int or tuple of ints
        Shape of the new array.
        
    Returns
    -------
    Array
        Array of zeros with the given shape.
        
    Examples
    --------
    >>> zeros(3)
    Array([0, 0, 0])
    >>> zeros((2, 3))
    Array([[0, 0, 0], [0, 0, 0]])
    """
    return zeros_fast(shape)

@cython.boundscheck(False)
@cython.wraparound(False)
def ones_fast(shape):
    """
    Create an array filled with ones using Cython optimization.
    
    Parameters
    ----------
    shape : int or tuple of ints
        Shape of the new array.
        
    Returns
    -------
    Array
        Array of ones with the given shape.
    """
    cdef tuple final_shape
    cdef long total_size = 1
    cdef long dim
    cdef Py_ssize_t i
    
    if isinstance(shape, int):
        if shape < 0:
            raise ValueError("Shape dimensions must be non-negative")
        final_shape = (shape,)
    elif isinstance(shape, (tuple, list)):
        for dim in shape:
            if not isinstance(dim, int) or dim < 0:
                raise ValueError("Shape dimensions must be non-negative integers")
        final_shape = tuple(shape)
    else:
        raise TypeError("Shape must be int or tuple of ints")
    
    for dim in final_shape:
        total_size *= dim
    
    cdef list data = [1] * total_size
    cdef Array arr = Array([])
    arr._data = data
    arr._shape = final_shape
    return arr

def ones(shape):
    """
    Create an array filled with ones.
    
    Parameters
    ----------
    shape : int or tuple of ints
        Shape of the new array.
        
    Returns
    -------
    Array
        Array of ones with the given shape.
        
    Examples
    --------
    >>> ones(3)
    Array([1, 1, 1])
    >>> ones((2, 2))
    Array([[1, 1], [1, 1]])
    """
    return ones_fast(shape)

def empty(shape):
    """
    Create an uninitialized array.
    
    Note: In ArrPy, 'empty' arrays are initialized with zeros
    for consistency and safety.
    
    Parameters
    ----------
    shape : int or tuple of ints
        Shape of the new array.
        
    Returns
    -------
    Array
        Uninitialized array with the given shape.
        
    Examples
    --------
    >>> empty(3)
    Array([0, 0, 0])
    >>> empty((2, 2))
    Array([[0, 0], [0, 0]])
    """
    # In our implementation, we initialize with zeros for safety
    return zeros_fast(shape)

@cython.boundscheck(False)
@cython.wraparound(False)
def full_fast(tuple shape, fill_value):
    """
    Create an array filled with a specific value using Cython optimization.
    
    Parameters
    ----------
    shape : tuple of ints
        Shape of the new array.
    fill_value : scalar
        Value to fill the array with.
        
    Returns
    -------
    Array
        Array filled with fill_value.
    """
    cdef long total_size = 1
    cdef long dim
    
    for dim in shape:
        total_size *= dim
    
    cdef list data = [fill_value] * total_size
    cdef Array arr = Array([])
    arr._data = data
    arr._shape = shape
    return arr

@cython.wraparound(True)  # Allow negative indexing for argument handling
def full(*args):
    """
    Create an array filled with a specific value.
    
    Parameters
    ----------
    shape : int or tuple of ints or multiple ints
        Shape of the new array. Can be specified as:
        - full(shape, fill_value) where shape is int or tuple
        - full(dim1, dim2, ..., fill_value) where dims are individual ints
    fill_value : scalar
        Value to fill the array with.
        
    Returns
    -------
    Array
        Array filled with fill_value.
        
    Examples
    --------
    >>> full(3, 7)
    Array([7, 7, 7])
    >>> full((2, 2), 3.14)
    Array([[3.14, 3.14], [3.14, 3.14]])
    """
    if len(args) < 2:
        raise TypeError("full() missing required arguments")
    
    # Check if first argument is a tuple/list (shape format)
    if isinstance(args[0], (tuple, list)):
        shape = tuple(args[0])
        fill_value = args[1]
    elif len(args) == 2 and isinstance(args[0], int):
        # Single dimension format: full(5, value)
        shape = (args[0],)
        fill_value = args[1]
    else:
        # Multiple dimensions format: full(2, 3, 4, value)
        shape = tuple(args[:-1])
        fill_value = args[-1]
    
    return full_fast(shape, fill_value)

@cython.boundscheck(False)
@cython.wraparound(False)
def eye_fast(long n, long m, long k):
    """
    Create a 2D array with ones on the diagonal using Cython optimization.
    
    Parameters
    ----------
    n : int
        Number of rows.
    m : int
        Number of columns.
    k : int
        Index of the diagonal.
        
    Returns
    -------
    Array
        2D array with ones on the k-th diagonal.
    """
    cdef list data = []
    cdef long i, j
    
    for i in range(n):
        for j in range(m):
            if i == (j - k):
                data.append(1)
            else:
                data.append(0)
    
    cdef Array arr = Array([])
    arr._data = data
    arr._shape = (n, m)
    return arr

def eye(n, m=None, k=0):
    """
    Create a 2D array with ones on the diagonal and zeros elsewhere.
    
    Parameters
    ----------
    n : int
        Number of rows.
    m : int, optional
        Number of columns. If None, defaults to n.
    k : int, optional
        Index of the diagonal. 0 (default) refers to the main diagonal.
        
    Returns
    -------
    Array
        2D array with ones on the k-th diagonal.
        
    Examples
    --------
    >>> eye(3)
    Array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    >>> eye(2, 3)
    Array([[1, 0, 0], [0, 1, 0]])
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a non-negative integer")
    
    if m is None:
        m = n
    elif not isinstance(m, int) or m < 0:
        raise ValueError("m must be a non-negative integer")
    
    return eye_fast(n, m, k)

@cython.wraparound(True)  # Allow negative indexing for this function
def identity(n):
    """
    Create the identity array.
    
    Parameters
    ----------
    n : int
        Number of rows (and columns) in the output.
        
    Returns
    -------
    Array
        n x n array with ones on the main diagonal.
        
    Examples
    --------
    >>> identity(3)
    Array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a non-negative integer")
    return eye_fast(n, n, 0)