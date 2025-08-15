"""
Array creation functions for arrpy.
"""

from .arrpy import arrpy
from .dtype import float64, int64


def zeros(shape, dtype=None):
    """
    Create an array filled with zeros.
    
    Parameters
    ----------
    shape : int or tuple of ints
        Shape of the array
    dtype : dtype, optional
        Desired data type (default: float64)
    
    Returns
    -------
    arrpy
        Array of zeros with given shape
    """
    # Handle scalar shape
    if isinstance(shape, int):
        shape = (shape,)
    
    # Default dtype
    if dtype is None:
        dtype = float64
    
    # Calculate total size
    size = 1
    for dim in shape:
        size *= dim
    
    # Create zero data
    zero_value = dtype.python_type(0)
    data = [zero_value] * size
    
    # Create array from flat data
    result = arrpy.__new__(arrpy)
    result._data = data
    result._shape = shape
    result._dtype = dtype
    result._size = size
    result._strides = result._calculate_strides(shape)
    
    return result


def ones(shape, dtype=None):
    """
    Create an array filled with ones.
    
    Parameters
    ----------
    shape : int or tuple of ints
        Shape of the array
    dtype : dtype, optional
        Desired data type (default: float64)
    
    Returns
    -------
    arrpy
        Array of ones with given shape
    """
    # Handle scalar shape
    if isinstance(shape, int):
        shape = (shape,)
    
    # Default dtype
    if dtype is None:
        dtype = float64
    
    # Calculate total size
    size = 1
    for dim in shape:
        size *= dim
    
    # Create one data
    one_value = dtype.python_type(1)
    data = [one_value] * size
    
    # Create array from flat data
    result = arrpy.__new__(arrpy)
    result._data = data
    result._shape = shape
    result._dtype = dtype
    result._size = size
    result._strides = result._calculate_strides(shape)
    
    return result


def full(shape, fill_value, dtype=None):
    """
    Create an array filled with a specified value.
    
    Parameters
    ----------
    shape : int or tuple of ints
        Shape of the array
    fill_value : scalar
        Fill value
    dtype : dtype, optional
        Desired data type
    
    Returns
    -------
    arrpy
        Array filled with fill_value
    """
    # Handle scalar shape
    if isinstance(shape, int):
        shape = (shape,)
    
    # Infer dtype from fill_value if not specified
    if dtype is None:
        if isinstance(fill_value, bool):
            from .dtype import bool_
            dtype = bool_
        elif isinstance(fill_value, int):
            dtype = int64
        else:
            dtype = float64
    
    # Calculate total size
    size = 1
    for dim in shape:
        size *= dim
    
    # Create filled data
    value = dtype.python_type(fill_value)
    data = [value] * size
    
    # Create array from flat data
    result = arrpy.__new__(arrpy)
    result._data = data
    result._shape = shape
    result._dtype = dtype
    result._size = size
    result._strides = result._calculate_strides(shape)
    
    return result


def empty(shape, dtype=None):
    """
    Create an uninitialized array.
    
    Parameters
    ----------
    shape : int or tuple of ints
        Shape of the array
    dtype : dtype, optional
        Desired data type (default: float64)
    
    Returns
    -------
    arrpy
        Uninitialized array
    """
    # For simplicity, we'll initialize with zeros
    # In a real implementation, this would be uninitialized memory
    return zeros(shape, dtype)


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
    # Handle single argument case (stop only)
    if stop is None:
        stop = start
        start = 0
    
    # Generate values
    values = []
    current = start
    if step > 0:
        while current < stop:
            values.append(current)
            current += step
    elif step < 0:
        while current > stop:
            values.append(current)
            current += step
    else:
        raise ValueError("Step cannot be zero")
    
    # Infer dtype if not specified
    if dtype is None:
        if isinstance(start, float) or isinstance(stop, float) or isinstance(step, float):
            dtype = float64
        else:
            dtype = int64
    
    # Convert values to desired dtype
    values = [dtype.python_type(v) for v in values]
    
    # Create array
    result = arrpy.__new__(arrpy)
    result._data = values
    result._shape = (len(values),)
    result._dtype = dtype
    result._size = len(values)
    result._strides = (1,)
    
    return result


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
    if num < 0:
        raise ValueError("Number of samples must be non-negative")
    
    if num == 0:
        return array([])
    
    if num == 1:
        return array([start], dtype=dtype)
    
    # Calculate step
    if endpoint:
        step = (stop - start) / (num - 1)
    else:
        step = (stop - start) / num
    
    # Generate values
    values = [start + i * step for i in range(num)]
    
    # Default dtype
    if dtype is None:
        dtype = float64
    
    # Convert to desired dtype
    values = [dtype.python_type(v) for v in values]
    
    # Create array
    result = arrpy.__new__(arrpy)
    result._data = values
    result._shape = (len(values),)
    result._dtype = dtype
    result._size = len(values)
    result._strides = (1,)
    
    return result


def eye(N, M=None, k=0, dtype=None):
    """
    Create a 2D array with ones on the diagonal and zeros elsewhere.
    
    Parameters
    ----------
    N : int
        Number of rows
    M : int, optional
        Number of columns (default: N)
    k : int, optional
        Diagonal offset
    dtype : dtype, optional
        Data type
    
    Returns
    -------
    arrpy
        Eye matrix
    """
    if M is None:
        M = N
    
    if dtype is None:
        dtype = float64
    
    # Create zeros array
    result = zeros((N, M), dtype=dtype)
    
    # Set diagonal elements to 1
    one = dtype.python_type(1)
    for i in range(N):
        j = i + k
        if 0 <= j < M:
            result._data[i * M + j] = one
    
    return result


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