"""
Array joining functions for ArrPy arrays.

This module provides functions for joining arrays along existing or new axes,
such as concatenate, stack, vstack, and hstack.
"""

from ..core import Array


def concatenate(arrays, axis=0):
    """
    Join arrays along an existing axis.
    
    Parameters
    ----------
    arrays : sequence of Arrays
        The arrays to concatenate.
    axis : int, optional
        The axis along which to concatenate. Default is 0.
        
    Returns
    -------
    Array
        Concatenated array.
        
    Examples
    --------
    >>> a = Array([1, 2])
    >>> b = Array([3, 4])
    >>> concatenate([a, b])
    Array([1, 2, 3, 4])
    """
    if not arrays:
        raise ValueError("Need at least one array to concatenate")
    
    if not all(isinstance(arr, Array) for arr in arrays):
        raise TypeError("All inputs must be Array instances")
    
    first_array = arrays[0]
    
    # Check shape compatibility
    for arr in arrays[1:]:
        if len(arr.shape) != len(first_array.shape):
            raise ValueError("All arrays must have the same number of dimensions")
        
        for i, (dim1, dim2) in enumerate(zip(first_array.shape, arr.shape)):
            if i != axis and dim1 != dim2:
                raise ValueError(f"All arrays must have the same shape except on axis {axis}")
    
    if axis < 0 or axis >= len(first_array.shape):
        raise ValueError(f"axis {axis} is out of bounds for array of dimension {len(first_array.shape)}")
    
    # Calculate new shape
    new_shape = list(first_array.shape)
    new_shape[axis] = sum(arr.shape[axis] for arr in arrays)
    new_shape = tuple(new_shape)
    
    # Concatenate data
    result_data = []
    
    if len(first_array.shape) == 1:
        # 1D case is simple
        for arr in arrays:
            result_data.extend(arr._data)
    else:
        # Multi-dimensional case
        if len(first_array.shape) == 2 and axis == 0:
            # Concatenate rows
            for arr in arrays:
                result_data.extend(arr._data)
        elif len(first_array.shape) == 2 and axis == 1:
            # Concatenate columns
            rows = first_array.shape[0]
            
            for row in range(rows):
                for arr in arrays:
                    arr_cols = arr.shape[1]
                    start_idx = row * arr_cols
                    end_idx = start_idx + arr_cols
                    result_data.extend(arr._data[start_idx:end_idx])
        else:
            raise NotImplementedError("Concatenation for >2D arrays along non-zero axis not yet implemented")
    
    new_array = Array([])
    new_array._data = result_data
    new_array._shape = new_shape
    return new_array


def stack(arrays, axis=0):
    """
    Join arrays along a new axis.
    
    Parameters
    ----------
    arrays : sequence of Arrays
        Arrays to stack. All must have the same shape.
    axis : int, optional
        The axis along which to stack. Default is 0.
        
    Returns
    -------
    Array
        Stacked array with one more dimension than input arrays.
        
    Examples
    --------
    >>> a = Array([1, 2])
    >>> b = Array([3, 4])
    >>> stack([a, b])
    Array([[1, 2], [3, 4]])
    >>> stack([a, b], axis=1)
    Array([[1, 3], [2, 4]])
    """
    if not arrays:
        raise ValueError("Need at least one array to stack")
    
    if not all(isinstance(arr, Array) for arr in arrays):
        raise TypeError("All inputs must be Array instances")
    
    # Check that all arrays have the same shape
    first_shape = arrays[0].shape
    for arr in arrays[1:]:
        if arr.shape != first_shape:
            raise ValueError("All arrays must have the same shape")
    
    # Expand dimensions of all arrays
    from .shape import expand_dims
    expanded_arrays = [expand_dims(arr, axis) for arr in arrays]
    
    # Concatenate along the new axis
    return concatenate(expanded_arrays, axis=axis)


def vstack(arrays):
    """
    Stack arrays vertically (row-wise).
    
    This is equivalent to concatenation along the first axis for 2D arrays.
    
    Parameters
    ----------
    arrays : sequence of Arrays
        Arrays to stack vertically.
        
    Returns
    -------
    Array
        Vertically stacked array.
        
    Examples
    --------
    >>> a = Array([1, 2, 3])
    >>> b = Array([4, 5, 6])
    >>> vstack([a, b])
    Array([[1, 2, 3], [4, 5, 6]])
    """
    if not arrays:
        raise ValueError("Need at least one array to stack")
    
    # For 1D arrays, convert to 2D first
    arrays_2d = []
    for arr in arrays:
        if len(arr.shape) == 1:
            from .shape import expand_dims
            arrays_2d.append(expand_dims(arr, 0))
        else:
            arrays_2d.append(arr)
    
    return concatenate(arrays_2d, axis=0)


def hstack(arrays):
    """
    Stack arrays horizontally (column-wise).
    
    For 1D arrays, this is equivalent to concatenation.
    For 2D arrays, this concatenates along the second axis.
    
    Parameters
    ----------
    arrays : sequence of Arrays
        Arrays to stack horizontally.
        
    Returns
    -------
    Array
        Horizontally stacked array.
        
    Examples
    --------
    >>> a = Array([1, 2, 3])
    >>> b = Array([4, 5, 6])
    >>> hstack([a, b])
    Array([1, 2, 3, 4, 5, 6])
    """
    if not arrays:
        raise ValueError("Need at least one array to stack")
    
    # For 1D arrays, hstack is just concatenation
    if all(len(arr.shape) == 1 for arr in arrays):
        return concatenate(arrays, axis=0)
    else:
        return concatenate(arrays, axis=1)