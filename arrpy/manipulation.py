"""
Array manipulation functions for arrpy.
"""

from .arrpy_backend import ArrPy


def reshape(a, newshape):
    """
    Reshape an array.
    
    Parameters
    ----------
    a : arrpy
        Array to reshape
    newshape : tuple of ints
        New shape
    
    Returns
    -------
    arrpy
        Reshaped array
    """
    return a.reshape(newshape)


def flatten(a):
    """
    Flatten an array to 1D.
    
    Parameters
    ----------
    a : arrpy
        Array to flatten
    
    Returns
    -------
    arrpy
        Flattened array
    """
    return a.flatten()


def concatenate(arrays, axis=0):
    """
    Concatenate arrays along an axis.
    
    Parameters
    ----------
    arrays : sequence of arrpy
        Arrays to concatenate
    axis : int, optional
        Axis along which to concatenate
    
    Returns
    -------
    arrpy
        Concatenated array
    """
    if not arrays:
        raise ValueError("Need at least one array to concatenate")
    
    # Convert to list if needed
    arrays = list(arrays)
    
    # Handle 1D case
    if arrays[0].ndim == 1:
        if axis != 0:
            raise ValueError(f"axis {axis} is out of bounds for 1D arrays")
        
        # Concatenate data
        all_data = []
        total_size = 0
        for arr in arrays:
            if arr.ndim != 1:
                raise ValueError("All arrays must have same number of dimensions")
            all_data.extend(arr._data)
            total_size += arr.size
        
        # Create result
        result = arrpy.__new__(arrpy)
        result._data = all_data
        result._shape = (total_size,)
        result._size = total_size
        result._dtype = arrays[0]._dtype
        result._strides = (1,)
        return result
    
    # Handle 2D case
    if arrays[0].ndim == 2:
        # Normalize axis
        if axis < 0:
            axis = arrays[0].ndim + axis
        
        if axis == 0:
            # Concatenate along rows
            # Check all arrays have same number of columns
            ncols = arrays[0].shape[1]
            for arr in arrays[1:]:
                if arr.ndim != 2:
                    raise ValueError("All arrays must have same number of dimensions")
                if arr.shape[1] != ncols:
                    raise ValueError(f"All arrays must have same shape along axis {1-axis}")
            
            # Concatenate data
            all_data = []
            total_rows = 0
            for arr in arrays:
                all_data.extend(arr._data)
                total_rows += arr.shape[0]
            
            # Create result
            result = arrpy.__new__(arrpy)
            result._data = all_data
            result._shape = (total_rows, ncols)
            result._size = total_rows * ncols
            result._dtype = arrays[0]._dtype
            result._strides = result._calculate_strides(result._shape)
            return result
        
        elif axis == 1:
            # Concatenate along columns
            # Check all arrays have same number of rows
            nrows = arrays[0].shape[0]
            for arr in arrays[1:]:
                if arr.ndim != 2:
                    raise ValueError("All arrays must have same number of dimensions")
                if arr.shape[0] != nrows:
                    raise ValueError(f"All arrays must have same shape along axis {1-axis}")
            
            # Concatenate data row by row
            all_data = []
            total_cols = sum(arr.shape[1] for arr in arrays)
            
            for i in range(nrows):
                for arr in arrays:
                    start_idx = i * arr.shape[1]
                    end_idx = start_idx + arr.shape[1]
                    all_data.extend(arr._data[start_idx:end_idx])
            
            # Create result
            result = arrpy.__new__(arrpy)
            result._data = all_data
            result._shape = (nrows, total_cols)
            result._size = nrows * total_cols
            result._dtype = arrays[0]._dtype
            result._strides = result._calculate_strides(result._shape)
            return result
    
    # For higher dimensions
    raise NotImplementedError(f"Concatenation not yet implemented for {arrays[0].ndim}D arrays")


def stack(arrays, axis=0):
    """
    Stack arrays along a new axis.
    
    Parameters
    ----------
    arrays : sequence of arrpy
        Arrays to stack (must have same shape)
    axis : int, optional
        Axis along which to stack
    
    Returns
    -------
    arrpy
        Stacked array
    """
    if not arrays:
        raise ValueError("Need at least one array to stack")
    
    arrays = list(arrays)
    
    # Check all arrays have same shape
    shape = arrays[0].shape
    for arr in arrays[1:]:
        if arr.shape != shape:
            raise ValueError(f"All arrays must have same shape. Got {shape} and {arr.shape}")
    
    # Expand dimensions and concatenate
    expanded = []
    for arr in arrays:
        expanded.append(expand_dims(arr, axis))
    
    return concatenate(expanded, axis=axis)


def vstack(arrays):
    """
    Stack arrays vertically (row-wise).
    
    Parameters
    ----------
    arrays : sequence of arrpy
        Arrays to stack
    
    Returns
    -------
    arrpy
        Stacked array
    """
    arrays = list(arrays)
    
    # Convert 1D arrays to row vectors
    processed = []
    for arr in arrays:
        if arr.ndim == 1:
            processed.append(arr.reshape(1, -1))
        else:
            processed.append(arr)
    
    return concatenate(processed, axis=0)


def hstack(arrays):
    """
    Stack arrays horizontally (column-wise).
    
    Parameters
    ----------
    arrays : sequence of arrpy
        Arrays to stack
    
    Returns
    -------
    arrpy
        Stacked array
    """
    arrays = list(arrays)
    
    # For 1D arrays, concatenate along axis 0
    if arrays[0].ndim == 1:
        return concatenate(arrays, axis=0)
    
    # For higher dimensions, concatenate along axis 1
    return concatenate(arrays, axis=1)


def split(a, indices_or_sections, axis=0):
    """
    Split an array into multiple sub-arrays.
    
    Parameters
    ----------
    a : arrpy
        Array to split
    indices_or_sections : int or sequence of ints
        If int, number of equal sections
        If sequence, indices for splits
    axis : int, optional
        Axis along which to split
    
    Returns
    -------
    list of arrpy
        List of sub-arrays
    """
    # Normalize axis
    if axis < 0:
        axis = a.ndim + axis
    
    if isinstance(indices_or_sections, int):
        # Split into equal sections
        n_sections = indices_or_sections
        size = a.shape[axis]
        
        if size % n_sections != 0:
            raise ValueError(f"Array split does not result in equal division")
        
        section_size = size // n_sections
        indices = [i * section_size for i in range(1, n_sections)]
    else:
        indices = list(indices_or_sections)
    
    # Add boundaries
    indices = [0] + indices + [a.shape[axis]]
    
    # Split array
    results = []
    for i in range(len(indices) - 1):
        start = indices[i]
        end = indices[i + 1]
        
        if a.ndim == 1:
            sub_data = a._data[start:end]
            sub = arrpy.__new__(arrpy)
            sub._data = sub_data
            sub._shape = (len(sub_data),)
            sub._size = len(sub_data)
            sub._dtype = a._dtype
            sub._strides = (1,)
            results.append(sub)
        else:
            # For higher dimensions, use slicing
            # This is simplified - full implementation would handle all cases
            raise NotImplementedError("Split not yet fully implemented for multi-dimensional arrays")
    
    return results


def squeeze(a, axis=None):
    """
    Remove single-dimensional entries from shape.
    
    Parameters
    ----------
    a : arrpy
        Input array
    axis : int or tuple of ints, optional
        Axes to squeeze
    
    Returns
    -------
    arrpy
        Squeezed array
    """
    # Determine which axes to squeeze
    if axis is None:
        # Squeeze all dimensions of size 1
        new_shape = tuple(dim for dim in a.shape if dim != 1)
    else:
        # Squeeze specific axes
        if isinstance(axis, int):
            axis = (axis,)
        
        # Normalize negative axes
        axis = tuple(ax if ax >= 0 else a.ndim + ax for ax in axis)
        
        # Check axes are valid and have size 1
        for ax in axis:
            if ax >= a.ndim:
                raise ValueError(f"axis {ax} is out of bounds")
            if a.shape[ax] != 1:
                raise ValueError(f"Cannot squeeze axis {ax} with size {a.shape[ax]}")
        
        # Create new shape
        new_shape = tuple(dim for i, dim in enumerate(a.shape) if i not in axis)
    
    if new_shape == a.shape:
        return a
    
    return a.reshape(new_shape)


def expand_dims(a, axis):
    """
    Expand the shape of an array.
    
    Parameters
    ----------
    a : arrpy
        Input array
    axis : int
        Position for new axis
    
    Returns
    -------
    arrpy
        Array with expanded dimensions
    """
    # Normalize axis
    if axis < 0:
        axis = a.ndim + 1 + axis
    
    if axis < 0 or axis > a.ndim:
        raise ValueError(f"axis {axis} is out of bounds for array of dimension {a.ndim}")
    
    # Create new shape
    new_shape = list(a.shape)
    new_shape.insert(axis, 1)
    
    return a.reshape(tuple(new_shape))