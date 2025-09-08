"""
Advanced indexing operations for ArrPy.
"""

from .backend_selector import get_backend, Backend
from .arrpy_backend import ArrPy


def where(condition, x=None, y=None):
    """
    Return elements chosen from x or y depending on condition.
    
    Parameters
    ----------
    condition : ArrPy or array-like
        Where True, yield x, otherwise yield y
    x : ArrPy or scalar, optional
        Values to choose when condition is True
    y : ArrPy or scalar, optional
        Values to choose when condition is False
    
    Returns
    -------
    ArrPy or tuple of ArrPy
        If x and y are given, returns array with elements from x where
        condition is True, and from y elsewhere.
        If only condition is given, returns indices where condition is True.
    """
    from .creation import array
    
    # Convert condition to ArrPy if needed
    if not isinstance(condition, ArrPy):
        condition = array(condition)
    
    if x is None and y is None:
        # Return indices where condition is True
        indices = []
        if condition.ndim == 1:
            for i in range(condition.shape[0]):
                if condition._data[i]:
                    indices.append(i)
            
            result = ArrPy.__new__(ArrPy)
            result._data = indices
            result._shape = (len(indices),)
            result._size = len(indices)
            from .dtype import int64
            result._dtype = int64
            result._strides = (1,)
            return (result,)  # Return as tuple for consistency with numpy
        
        elif condition.ndim == 2:
            row_indices = []
            col_indices = []
            rows, cols = condition.shape
            
            for i in range(rows):
                for j in range(cols):
                    if condition._data[i * cols + j]:
                        row_indices.append(i)
                        col_indices.append(j)
            
            # Create two arrays for row and column indices
            row_arr = ArrPy.__new__(ArrPy)
            row_arr._data = row_indices
            row_arr._shape = (len(row_indices),)
            row_arr._size = len(row_indices)
            from .dtype import int64
            row_arr._dtype = int64
            row_arr._strides = (1,)
            
            col_arr = ArrPy.__new__(ArrPy)
            col_arr._data = col_indices
            col_arr._shape = (len(col_indices),)
            col_arr._size = len(col_indices)
            col_arr._dtype = int64
            col_arr._strides = (1,)
            
            return (row_arr, col_arr)
        
        else:
            raise NotImplementedError(f"where for {condition.ndim}D arrays not implemented")
    
    else:
        # Return array with elements from x or y based on condition
        if x is None or y is None:
            raise ValueError("either both or neither of x and y should be given")
        
        # Convert x and y to ArrPy if needed
        if not isinstance(x, ArrPy):
            x = array(x)
        if not isinstance(y, ArrPy):
            y = array(y)
        
        # Broadcast all arrays to the same shape
        from .broadcasting import broadcast_arrays
        condition, x, y = broadcast_arrays(condition, x, y)
        
        # Select elements
        result_data = []
        for i in range(condition._size):
            if condition._data[i]:
                result_data.append(x._data[i])
            else:
                result_data.append(y._data[i])
        
        result = ArrPy.__new__(ArrPy)
        result._data = result_data
        result._shape = condition._shape
        result._size = condition._size
        result._dtype = x._dtype
        result._strides = result._calculate_strides(condition._shape)
        
        return result


def validate_index(index, shape):
    """
    Validate and normalize an index for given shape.
    
    Parameters
    ----------
    index : int, slice, tuple
        Index to validate
    shape : tuple
        Array shape
    
    Returns
    -------
    tuple
        Normalized index
    """
    if not isinstance(index, tuple):
        index = (index,)
    
    # Expand ellipsis if present
    if Ellipsis in index:
        # Find position of ellipsis
        ellipsis_pos = index.index(Ellipsis)
        # Calculate how many dimensions the ellipsis represents
        n_specified = len([idx for idx in index if idx is not Ellipsis])
        n_ellipsis = len(shape) - n_specified
        # Replace ellipsis with appropriate number of slices
        new_index = index[:ellipsis_pos]
        new_index += (slice(None),) * n_ellipsis
        new_index += index[ellipsis_pos + 1:]
        index = new_index
    
    # Pad with full slices if needed
    if len(index) < len(shape):
        index = index + (slice(None),) * (len(shape) - len(index))
    
    return index


def compute_slice_indices(slice_obj, dim_size):
    """
    Compute actual indices for a slice object.
    
    Parameters
    ----------
    slice_obj : slice
        Slice object
    dim_size : int
        Size of the dimension
    
    Returns
    -------
    tuple
        (start, stop, step) indices
    """
    start = slice_obj.start if slice_obj.start is not None else 0
    stop = slice_obj.stop if slice_obj.stop is not None else dim_size
    step = slice_obj.step if slice_obj.step is not None else 1
    
    # Handle negative indices
    if start < 0:
        start = dim_size + start
    if stop < 0:
        stop = dim_size + stop
    
    # Clamp to valid range
    start = max(0, min(start, dim_size))
    stop = max(0, min(stop, dim_size))
    
    return start, stop, step


def fancy_index(array, indices):
    """
    Perform fancy indexing on an array.
    
    Parameters
    ----------
    array : ArrPy
        Input array
    indices : array-like or tuple of array-like
        Indices to select
    
    Returns
    -------
    ArrPy
        Selected elements
    """
    from .creation import array as create_array
    
    # Convert indices to ArrPy if needed
    if not isinstance(indices, tuple):
        indices = (indices,)
    
    indices_arrays = []
    for idx in indices:
        if not isinstance(idx, ArrPy):
            indices_arrays.append(create_array(idx))
        else:
            indices_arrays.append(idx)
    
    # For 1D array with 1D indices
    if array.ndim == 1 and len(indices_arrays) == 1:
        idx_array = indices_arrays[0]
        result_data = []
        
        for idx in idx_array._data:
            if isinstance(idx, float):
                idx = int(idx)
            if idx < 0:
                idx += array.shape[0]
            if idx < 0 or idx >= array.shape[0]:
                raise IndexError(f"index {idx} is out of bounds")
            result_data.append(array._data[idx])
        
        result = ArrPy.__new__(ArrPy)
        result._data = result_data
        result._shape = idx_array._shape
        result._size = len(result_data)
        result._dtype = array._dtype
        result._strides = result._calculate_strides(idx_array._shape)
        return result
    
    # For 2D array with 2D indices (advanced indexing)
    elif array.ndim == 2 and len(indices_arrays) == 2:
        row_indices = indices_arrays[0]
        col_indices = indices_arrays[1]
        
        # Broadcast indices to same shape
        from .broadcasting import broadcast_arrays
        row_indices, col_indices = broadcast_arrays(row_indices, col_indices)
        
        result_data = []
        rows, cols = array.shape
        
        for i in range(row_indices._size):
            row_idx = row_indices._data[i]
            col_idx = col_indices._data[i]
            
            if isinstance(row_idx, float):
                row_idx = int(row_idx)
            if isinstance(col_idx, float):
                col_idx = int(col_idx)
            
            if row_idx < 0:
                row_idx += rows
            if col_idx < 0:
                col_idx += cols
            
            if row_idx < 0 or row_idx >= rows or col_idx < 0 or col_idx >= cols:
                raise IndexError(f"index ({row_idx}, {col_idx}) is out of bounds")
            
            result_data.append(array._data[row_idx * cols + col_idx])
        
        result = ArrPy.__new__(ArrPy)
        result._data = result_data
        result._shape = row_indices._shape
        result._size = len(result_data)
        result._dtype = array._dtype
        result._strides = result._calculate_strides(row_indices._shape)
        return result
    
    else:
        raise NotImplementedError(f"Fancy indexing for this case not yet implemented")


def boolean_index(array, mask):
    """
    Perform boolean indexing on an array.
    
    Parameters
    ----------
    array : ArrPy
        Input array
    mask : ArrPy of bool
        Boolean mask
    
    Returns
    -------
    ArrPy
        Selected elements (always 1D)
    """
    if mask.shape != array.shape:
        raise ValueError("boolean index did not match indexed array")
    
    result_data = []
    for i in range(array._size):
        if mask._data[i]:
            result_data.append(array._data[i])
    
    result = ArrPy.__new__(ArrPy)
    result._data = result_data
    result._shape = (len(result_data),)
    result._size = len(result_data)
    result._dtype = array._dtype
    result._strides = (1,)
    
    return result