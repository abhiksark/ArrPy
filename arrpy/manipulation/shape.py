"""
Shape manipulation functions for ArrPy arrays.

This module provides functions for changing array shapes, adding/removing
dimensions, and transposing arrays.
"""

from ..core.array import Array


def reshape(arr, new_shape):
    """
    Give a new shape to an array without changing its data.
    
    Parameters
    ----------
    arr : Array
        Input array.
    new_shape : int or tuple of ints
        The new shape should be compatible with the original shape.
        
    Returns
    -------
    Array
        Array with new shape.
        
    Examples
    --------
    >>> a = Array([1, 2, 3, 4, 5, 6])
    >>> reshape(a, (2, 3))
    Array([[1, 2, 3], [4, 5, 6]])
    """
    if not isinstance(arr, Array):
        raise TypeError("Input must be an Array")
    
    if isinstance(new_shape, int):
        new_shape = (new_shape,)
    
    # Calculate total elements
    new_size = 1
    for dim in new_shape:
        new_size *= dim
    
    if new_size != len(arr._data):
        raise ValueError(f"Cannot reshape array of size {len(arr._data)} into shape {new_shape}")
    
    new_array = Array([])
    new_array._data = arr._data.copy()
    new_array._shape = new_shape
    return new_array


def transpose(arr):
    """
    Transpose an array.
    
    For 2D arrays, this swaps rows and columns.
    For higher dimensions, reverses the order of axes.
    
    Parameters
    ----------
    arr : Array
        Input array.
        
    Returns
    -------
    Array
        Transposed array.
        
    Examples
    --------
    >>> a = Array([[1, 2], [3, 4]])
    >>> transpose(a)
    Array([[1, 3], [2, 4]])
    """
    if not isinstance(arr, Array):
        raise TypeError("Input must be an Array")
    
    if len(arr._shape) == 1:
        # 1D array transpose is itself
        return Array(arr._data.copy())
    elif len(arr._shape) == 2:
        # 2D transpose
        rows, cols = arr._shape
        transposed_data = []
        
        for j in range(cols):
            for i in range(rows):
                transposed_data.append(arr._data[i * cols + j])
        
        new_array = Array([])
        new_array._data = transposed_data
        new_array._shape = (cols, rows)
        return new_array
    else:
        raise NotImplementedError("Transpose for >2D arrays not yet implemented")


def squeeze(arr, axis=None):
    """
    Remove single-dimensional entries from the shape of an array.
    
    Parameters
    ----------
    arr : Array
        Input array.
    axis : None or int or tuple of ints, optional
        Selects a subset of entries to squeeze.
        
    Returns
    -------
    Array
        Array with squeezed shape.
        
    Examples
    --------
    >>> a = Array([[[1], [2], [3]]])  # Shape (1, 3, 1)
    >>> squeeze(a).shape
    (3,)
    """
    if not isinstance(arr, Array):
        raise TypeError("Input must be an Array")
    
    old_shape = arr._shape
    
    if axis is None:
        # Remove all dimensions of size 1
        new_shape = tuple(dim for dim in old_shape if dim != 1)
    else:
        # Remove specific axes
        if isinstance(axis, int):
            axis = (axis,)
        
        new_shape = []
        for i, dim in enumerate(old_shape):
            if i not in axis:
                new_shape.append(dim)
            elif dim != 1:
                raise ValueError(f"Cannot squeeze axis {i} with size {dim}")
        new_shape = tuple(new_shape)
    
    # Handle case where all dimensions are squeezed
    if not new_shape:
        new_shape = (1,)
    
    new_array = Array([])
    new_array._data = arr._data.copy()
    new_array._shape = new_shape
    return new_array


def expand_dims(arr, axis):
    """
    Expand the shape of an array by inserting new axes.
    
    Parameters
    ----------
    arr : Array
        Input array.
    axis : int or tuple of ints
        Position(s) of the new axes.
        
    Returns
    -------
    Array
        Array with expanded dimensions.
        
    Examples
    --------
    >>> a = Array([1, 2, 3])  # Shape (3,)
    >>> expand_dims(a, 0).shape
    (1, 3)
    >>> expand_dims(a, 1).shape  
    (3, 1)
    """
    if not isinstance(arr, Array):
        raise TypeError("Input must be an Array")
    
    old_shape = list(arr._shape)
    
    if isinstance(axis, int):
        axis = (axis,)
    
    # Sort axes to insert from left to right
    sorted_axes = sorted(axis)
    
    # Insert new dimensions
    for ax in sorted_axes:
        if ax < 0:
            ax = len(old_shape) + ax + 1
        old_shape.insert(ax, 1)
    
    new_shape = tuple(old_shape)
    
    new_array = Array([])
    new_array._data = arr._data.copy()
    new_array._shape = new_shape
    return new_array