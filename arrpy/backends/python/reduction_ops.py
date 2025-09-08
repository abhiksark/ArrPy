"""
Reduction operations for Python backend.

Pure Python implementations of reduction operations like sum, mean, etc.
"""


def _sum_python(data, shape, axis=None, keepdims=False):
    """
    Pure Python sum reduction.
    
    Parameters
    ----------
    data : list
        Flattened array data
    shape : tuple
        Shape of the array
    axis : int or None
        Axis to reduce along. None means reduce all.
    keepdims : bool
        Whether to keep reduced dimensions as size 1
        
    Returns
    -------
    tuple
        (result_data, result_shape)
    """
    # Full reduction (sum all elements)
    if axis is None:
        result = sum(data)
        if keepdims:
            result_shape = tuple(1 for _ in shape)
            return [result], result_shape
        else:
            return [result], ()
    
    # Axis reduction - more complex, simplified for now
    # Just handle 2D case
    if len(shape) == 2 and axis in [0, 1]:
        m, n = shape
        
        if axis == 0:  # Sum along rows (result has n elements)
            result = []
            for j in range(n):
                col_sum = 0
                for i in range(m):
                    col_sum += data[i * n + j]
                result.append(col_sum)
            
            if keepdims:
                return result, (1, n)
            else:
                return result, (n,)
        
        else:  # axis == 1, sum along columns (result has m elements)
            result = []
            for i in range(m):
                row_sum = 0
                for j in range(n):
                    row_sum += data[i * n + j]
                result.append(row_sum)
            
            if keepdims:
                return result, (m, 1)
            else:
                return result, (m,)
    
    # For other cases, raise NotImplementedError
    raise NotImplementedError(f"sum with axis={axis} not fully implemented for shape {shape}")


def _mean_python(data, shape, axis=None, keepdims=False):
    """
    Pure Python mean reduction.
    
    Parameters
    ----------
    data : list
        Flattened array data
    shape : tuple
        Shape of the array
    axis : int or None
        Axis to reduce along
    keepdims : bool
        Whether to keep reduced dimensions
        
    Returns
    -------
    tuple
        (result_data, result_shape)
    """
    # Get sum first
    sum_data, sum_shape = _sum_python(data, shape, axis, keepdims)
    
    # Calculate count for division
    if axis is None:
        count = len(data)
    elif axis == 0:
        count = shape[0]
    elif axis == 1:
        count = shape[1]
    else:
        raise NotImplementedError(f"mean with axis={axis} not implemented")
    
    # Divide sum by count
    result = []
    for val in sum_data:
        result.append(val / count)
    
    return result, sum_shape


def _min_python(data, shape, axis=None, keepdims=False):
    """
    Pure Python minimum reduction.
    
    Parameters
    ----------
    data : list
        Flattened array data
    shape : tuple
        Shape of the array
    axis : int or None
        Axis to reduce along
    keepdims : bool
        Whether to keep reduced dimensions
        
    Returns
    -------
    tuple
        (result_data, result_shape)
    """
    # Full reduction
    if axis is None:
        result = min(data)
        if keepdims:
            result_shape = tuple(1 for _ in shape)
            return [result], result_shape
        else:
            return [result], ()
    
    # Simplified axis reduction for 2D
    if len(shape) == 2 and axis in [0, 1]:
        m, n = shape
        
        if axis == 0:  # Min along rows
            result = []
            for j in range(n):
                col_min = float('inf')
                for i in range(m):
                    col_min = min(col_min, data[i * n + j])
                result.append(col_min)
            
            if keepdims:
                return result, (1, n)
            else:
                return result, (n,)
        
        else:  # axis == 1, min along columns
            result = []
            for i in range(m):
                row_min = float('inf')
                for j in range(n):
                    row_min = min(row_min, data[i * n + j])
                result.append(row_min)
            
            if keepdims:
                return result, (m, 1)
            else:
                return result, (m,)
    
    raise NotImplementedError(f"min with axis={axis} not implemented for shape {shape}")


def _max_python(data, shape, axis=None, keepdims=False):
    """
    Pure Python maximum reduction.
    
    Parameters
    ----------
    data : list
        Flattened array data
    shape : tuple
        Shape of the array
    axis : int or None
        Axis to reduce along
    keepdims : bool
        Whether to keep reduced dimensions
        
    Returns
    -------
    tuple
        (result_data, result_shape)
    """
    # Full reduction
    if axis is None:
        result = max(data)
        if keepdims:
            result_shape = tuple(1 for _ in shape)
            return [result], result_shape
        else:
            return [result], ()
    
    # Simplified axis reduction for 2D
    if len(shape) == 2 and axis in [0, 1]:
        m, n = shape
        
        if axis == 0:  # Max along rows
            result = []
            for j in range(n):
                col_max = float('-inf')
                for i in range(m):
                    col_max = max(col_max, data[i * n + j])
                result.append(col_max)
            
            if keepdims:
                return result, (1, n)
            else:
                return result, (n,)
        
        else:  # axis == 1, max along columns
            result = []
            for i in range(m):
                row_max = float('-inf')
                for j in range(n):
                    row_max = max(row_max, data[i * n + j])
                result.append(row_max)
            
            if keepdims:
                return result, (m, 1)
            else:
                return result, (m,)
    
    raise NotImplementedError(f"max with axis={axis} not implemented for shape {shape}")


def _prod_python(data, shape, axis=None, keepdims=False):
    """
    Pure Python product reduction.
    
    Parameters
    ----------
    data : list
        Flattened array data
    shape : tuple
        Shape of the array
    axis : int or None
        Axis to reduce along
    keepdims : bool
        Whether to keep reduced dimensions
        
    Returns
    -------
    tuple
        (result_data, result_shape)
    """
    # Full reduction
    if axis is None:
        result = 1
        for val in data:
            result *= val
        
        if keepdims:
            result_shape = tuple(1 for _ in shape)
            return [result], result_shape
        else:
            return [result], ()
    
    # Axis reduction - simplified for 2D
    if len(shape) == 2 and axis in [0, 1]:
        m, n = shape
        
        if axis == 0:  # Product along rows
            result = []
            for j in range(n):
                col_prod = 1
                for i in range(m):
                    col_prod *= data[i * n + j]
                result.append(col_prod)
            
            if keepdims:
                return result, (1, n)
            else:
                return result, (n,)
        
        else:  # axis == 1, product along columns
            result = []
            for i in range(m):
                row_prod = 1
                for j in range(n):
                    row_prod *= data[i * n + j]
                result.append(row_prod)
            
            if keepdims:
                return result, (m, 1)
            else:
                return result, (m,)
    
    raise NotImplementedError(f"prod with axis={axis} not implemented for shape {shape}")