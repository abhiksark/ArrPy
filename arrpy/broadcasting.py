"""
Broadcasting implementation for arrpy arrays.
"""


def broadcast_shapes(*shapes):
    """
    Determine if shapes are broadcast-compatible and return result shape.
    
    Broadcasting rules:
    1. Pad shorter shape with 1s on the left
    2. Dimensions are compatible if equal or one is 1
    3. Result takes max of each dimension
    
    Parameters
    ----------
    *shapes : tuples
        Shapes to broadcast
    
    Returns
    -------
    tuple
        Broadcasted shape
    
    Raises
    ------
    ValueError
        If shapes are not broadcast-compatible
    """
    if not shapes:
        return ()
    
    if len(shapes) == 1:
        return shapes[0]
    
    # Find maximum number of dimensions
    max_ndim = max(len(shape) for shape in shapes)
    
    # Pad shapes with 1s on the left to match max_ndim
    padded_shapes = []
    for shape in shapes:
        padded = (1,) * (max_ndim - len(shape)) + shape
        padded_shapes.append(padded)
    
    # Check compatibility and compute result shape
    result_shape = []
    for dim_sizes in zip(*padded_shapes):
        # Get unique non-1 sizes for this dimension
        non_one_sizes = set(size for size in dim_sizes if size != 1)
        
        if len(non_one_sizes) > 1:
            # Multiple different non-1 sizes - not compatible
            raise ValueError(f"Shapes {shapes} are not compatible for broadcasting")
        
        # Take the maximum size for this dimension
        result_shape.append(max(dim_sizes))
    
    return tuple(result_shape)


def broadcast_arrays(*arrays):
    """
    Broadcast arrays to a common shape.
    
    Parameters
    ----------
    *arrays : arrpy arrays or scalars
        Arrays to broadcast
    
    Returns
    -------
    list of arrpy
        Broadcasted arrays
    """
    from .arrpy_backend import ArrPy
    from .creation import full
    
    if not arrays:
        return []
    
    # Convert scalars to 0-d arrays
    processed = []
    for arr in arrays:
        if not isinstance(arr, ArrPy):
            # Scalar - create 0-d array
            scalar_arr = ArrPy.__new__(ArrPy)
            scalar_arr._data = [arr]
            scalar_arr._shape = ()
            scalar_arr._size = 1
            scalar_arr._strides = ()
            from .dtype import infer_dtype
            scalar_arr._dtype = infer_dtype([arr])
            processed.append(scalar_arr)
        else:
            processed.append(arr)
    
    # Get broadcast shape
    shapes = [arr.shape for arr in processed]
    result_shape = broadcast_shapes(*shapes)
    
    # Broadcast each array
    broadcasted = []
    for arr in processed:
        if arr.shape == result_shape:
            # Already correct shape
            broadcasted.append(arr)
        else:
            # Need to broadcast
            broadcasted.append(_broadcast_to(arr, result_shape))
    
    return broadcasted


def _broadcast_to(array, shape):
    """
    Broadcast array to given shape.
    
    Parameters
    ----------
    array : arrpy
        Array to broadcast
    shape : tuple
        Target shape
    
    Returns
    -------
    arrpy
        Broadcasted array
    """
    from .arrpy_backend import ArrPy
    
    # Handle scalar case
    if array.shape == ():
        # Scalar - replicate to fill shape
        size = 1
        for dim in shape:
            size *= dim
        
        result = ArrPy.__new__(ArrPy)
        result._data = array._data * size
        result._shape = shape
        result._size = size
        result._dtype = array._dtype
        result._strides = result._calculate_strides(shape)
        return result
    
    # Pad array shape with 1s on left
    ndim_diff = len(shape) - len(array.shape)
    padded_shape = (1,) * ndim_diff + array.shape
    
    # Check compatibility
    for i, (dim_old, dim_new) in enumerate(zip(padded_shape, shape)):
        if dim_old != dim_new and dim_old != 1:
            raise ValueError(f"Cannot broadcast shape {array.shape} to {shape}")
    
    # Calculate broadcasting strides
    # Dimensions of size 1 get stride 0 (don't advance when iterating)
    old_strides = (0,) * ndim_diff + array._strides
    broadcast_strides = []
    for old_dim, old_stride, new_dim in zip(padded_shape, old_strides, shape):
        if old_dim == 1 and new_dim != 1:
            # Broadcasting this dimension - use stride 0
            broadcast_strides.append(0)
        else:
            broadcast_strides.append(old_stride)
    
    # Create new data by replicating according to broadcast rules
    new_data = []
    total_size = 1
    for dim in shape:
        total_size *= dim
    
    # Generate indices for new shape and map to old array
    for i in range(total_size):
        # Convert flat index to multi-dimensional index
        multi_idx = []
        remainder = i
        for dim in reversed(shape):
            multi_idx.append(remainder % dim)
            remainder //= dim
        multi_idx = list(reversed(multi_idx))
        
        # Map to old array index using broadcast strides
        old_flat_idx = 0
        for j, (idx, stride) in enumerate(zip(multi_idx, broadcast_strides)):
            if stride != 0:
                old_flat_idx += idx * stride
        
        new_data.append(array._data[old_flat_idx])
    
    # Create result array
    result = ArrPy.__new__(ArrPy)
    result._data = new_data
    result._shape = shape
    result._size = total_size
    result._dtype = array._dtype
    result._strides = result._calculate_strides(shape)
    
    return result