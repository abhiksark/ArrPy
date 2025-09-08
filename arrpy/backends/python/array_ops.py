"""
Basic array operations for Python backend.

Pure Python implementations of element-wise operations.
These serve as the reference implementation.
Now optimized to work with array.array for better performance.
"""

import array


def _add_python(data1, data2, shape1, shape2):
    """
    Pure Python addition - clear and educational.
    
    Parameters
    ----------
    data1, data2 : list
        Flattened array data
    shape1, shape2 : tuple
        Shapes of the arrays (must be broadcast-compatible)
        
    Returns
    -------
    tuple
        (result_data, result_shape)
    """
    # For now, assume shapes are the same (broadcasting handled at higher level)
    if shape1 != shape2:
        from ...broadcasting import broadcast_shapes, broadcast_data
        result_shape = broadcast_shapes(shape1, shape2)
        data1 = broadcast_data(data1, shape1, result_shape)
        data2 = broadcast_data(data2, shape2, result_shape)
    else:
        result_shape = shape1
    
    # Element-wise addition with array.array
    if isinstance(data1, array.array) and isinstance(data2, array.array):
        # Efficient array operation - use double for mixed types
        if data1.typecode == data2.typecode:
            result = array.array(data1.typecode)
        else:
            result = array.array('d')  # Use double for mixed types
        for i in range(len(data1)):
            result.append(data1[i] + data2[i])
    else:
        # Fallback for lists
        result = []
        for i in range(len(data1)):
            result.append(data1[i] + data2[i])
    
    return result, result_shape


def _subtract_python(data1, data2, shape1, shape2):
    """
    Pure Python subtraction.
    
    Parameters
    ----------
    data1, data2 : list
        Flattened array data
    shape1, shape2 : tuple
        Shapes of the arrays
        
    Returns
    -------
    tuple
        (result_data, result_shape)
    """
    if shape1 != shape2:
        from ...broadcasting import broadcast_shapes, broadcast_data
        result_shape = broadcast_shapes(shape1, shape2)
        data1 = broadcast_data(data1, shape1, result_shape)
        data2 = broadcast_data(data2, shape2, result_shape)
    else:
        result_shape = shape1
    
    # Element-wise subtraction with array.array
    if isinstance(data1, array.array) and isinstance(data2, array.array):
        # Use double for mixed types
        if data1.typecode == data2.typecode:
            result = array.array(data1.typecode)
        else:
            result = array.array('d')
        for i in range(len(data1)):
            result.append(data1[i] - data2[i])
    else:
        result = []
        for i in range(len(data1)):
            result.append(data1[i] - data2[i])
    
    return result, result_shape


def _multiply_python(data1, data2, shape1, shape2):
    """
    Pure Python multiplication.
    
    Parameters
    ----------
    data1, data2 : list
        Flattened array data
    shape1, shape2 : tuple
        Shapes of the arrays
        
    Returns
    -------
    tuple
        (result_data, result_shape)
    """
    if shape1 != shape2:
        from ...broadcasting import broadcast_shapes, broadcast_data
        result_shape = broadcast_shapes(shape1, shape2)
        data1 = broadcast_data(data1, shape1, result_shape)
        data2 = broadcast_data(data2, shape2, result_shape)
    else:
        result_shape = shape1
    
    # Element-wise multiplication with array.array
    if isinstance(data1, array.array) and isinstance(data2, array.array):
        # Use double for mixed types
        if data1.typecode == data2.typecode:
            result = array.array(data1.typecode)
        else:
            result = array.array('d')
        for i in range(len(data1)):
            result.append(data1[i] * data2[i])
    else:
        result = []
        for i in range(len(data1)):
            result.append(data1[i] * data2[i])
    
    return result, result_shape


def _divide_python(data1, data2, shape1, shape2):
    """
    Pure Python true division.
    
    Parameters
    ----------
    data1, data2 : list
        Flattened array data
    shape1, shape2 : tuple
        Shapes of the arrays
        
    Returns
    -------
    tuple
        (result_data, result_shape)
    """
    if shape1 != shape2:
        from ...broadcasting import broadcast_shapes, broadcast_data
        result_shape = broadcast_shapes(shape1, shape2)
        data1 = broadcast_data(data1, shape1, result_shape)
        data2 = broadcast_data(data2, shape2, result_shape)
    else:
        result_shape = shape1
    
    # Element-wise division with array.array
    if isinstance(data1, array.array) and isinstance(data2, array.array):
        # Always use double for division to maintain precision
        result = array.array('d')
        for i in range(len(data1)):
            if data2[i] == 0:
                # Handle division by zero similar to NumPy
                result.append(float('inf') if data1[i] > 0 else 
                             float('-inf') if data1[i] < 0 else 
                             float('nan'))
            else:
                result.append(data1[i] / data2[i])
    else:
        result = []
        for i in range(len(data1)):
            if data2[i] == 0:
                # Handle division by zero similar to NumPy
                result.append(float('inf') if data1[i] > 0 else 
                             float('-inf') if data1[i] < 0 else 
                             float('nan'))
            else:
                result.append(data1[i] / data2[i])
    
    return result, result_shape


def _power_python(data1, data2, shape1, shape2):
    """
    Pure Python power operation.
    
    Parameters
    ----------
    data1, data2 : list
        Flattened array data
    shape1, shape2 : tuple
        Shapes of the arrays
        
    Returns
    -------
    tuple
        (result_data, result_shape)
    """
    if shape1 != shape2:
        from ...broadcasting import broadcast_shapes, broadcast_data
        result_shape = broadcast_shapes(shape1, shape2)
        data1 = broadcast_data(data1, shape1, result_shape)
        data2 = broadcast_data(data2, shape2, result_shape)
    else:
        result_shape = shape1
    
    result = []
    for i in range(len(data1)):
        result.append(data1[i] ** data2[i])
    
    return result, result_shape


def _negative_python(data, shape):
    """
    Pure Python unary negation.
    
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
        result.append(-value)
    
    return result, shape


def _absolute_python(data, shape):
    """
    Pure Python absolute value.
    
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
        result.append(abs(value))
    
    return result, shape