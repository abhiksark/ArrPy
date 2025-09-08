"""
Universal functions (ufuncs) for element-wise operations.
"""

import math
from .broadcasting import broadcast_arrays


def _apply_binary_ufunc(x1, x2, operation, dtype_func=None):
    """
    Apply a binary operation element-wise with broadcasting.
    
    Parameters
    ----------
    x1, x2 : arrpy or scalar
        Input arrays or scalars
    operation : callable
        Binary operation to apply
    dtype_func : callable, optional
        Function to determine result dtype
    
    Returns
    -------
    arrpy
        Result array
    """
    from .arrpy_backend import ArrPy
    from .dtype import infer_dtype, float64
    
    # Broadcast inputs to common shape
    x1_b, x2_b = broadcast_arrays(x1, x2)
    
    # Determine result dtype
    if dtype_func:
        result_dtype = dtype_func(x1_b._dtype, x2_b._dtype)
    else:
        # Default: use float64 for most operations
        result_dtype = float64
    
    # Apply operation element-wise
    result_data = []
    for v1, v2 in zip(x1_b._data, x2_b._data):
        result_data.append(operation(v1, v2))
    
    # Create result array
    result = ArrPy.__new__(ArrPy)
    result._data = result_data
    result._shape = x1_b._shape
    result._size = x1_b._size
    result._dtype = result_dtype
    result._strides = result._calculate_strides(result._shape)
    
    return result


def _apply_unary_ufunc(x, operation, dtype_func=None):
    """
    Apply a unary operation element-wise.
    
    Parameters
    ----------
    x : arrpy
        Input array
    operation : callable
        Unary operation to apply
    dtype_func : callable, optional
        Function to determine result dtype
    
    Returns
    -------
    arrpy
        Result array
    """
    from .arrpy_backend import ArrPy
    
    # Determine result dtype
    if dtype_func:
        result_dtype = dtype_func(x._dtype)
    else:
        result_dtype = x._dtype
    
    # Apply operation element-wise
    result_data = [operation(v) for v in x._data]
    
    # Create result array
    result = ArrPy.__new__(ArrPy)
    result._data = result_data
    result._shape = x._shape
    result._size = x._size
    result._dtype = result_dtype
    result._strides = x._strides
    
    return result


# Arithmetic operations
def add(x1, x2):
    """Element-wise addition."""
    def dtype_func(dt1, dt2):
        # Promote to common type
        from .dtype import float64, int64
        if dt1.name == 'float64' or dt2.name == 'float64':
            return float64
        return int64
    
    return _apply_binary_ufunc(x1, x2, lambda a, b: a + b, dtype_func)


def subtract(x1, x2):
    """Element-wise subtraction."""
    def dtype_func(dt1, dt2):
        from .dtype import float64, int64
        if dt1.name == 'float64' or dt2.name == 'float64':
            return float64
        return int64
    
    return _apply_binary_ufunc(x1, x2, lambda a, b: a - b, dtype_func)


def multiply(x1, x2):
    """Element-wise multiplication."""
    def dtype_func(dt1, dt2):
        from .dtype import float64, int64
        if dt1.name == 'float64' or dt2.name == 'float64':
            return float64
        return int64
    
    return _apply_binary_ufunc(x1, x2, lambda a, b: a * b, dtype_func)


def divide(x1, x2):
    """Element-wise true division."""
    from .dtype import float64
    return _apply_binary_ufunc(x1, x2, lambda a, b: a / b, lambda dt1, dt2: float64)


def floor_divide(x1, x2):
    """Element-wise floor division."""
    def dtype_func(dt1, dt2):
        from .dtype import float64, int64
        if dt1.name == 'float64' or dt2.name == 'float64':
            return float64
        return int64
    
    return _apply_binary_ufunc(x1, x2, lambda a, b: a // b, dtype_func)


def mod(x1, x2):
    """Element-wise modulo."""
    def dtype_func(dt1, dt2):
        from .dtype import float64, int64
        if dt1.name == 'float64' or dt2.name == 'float64':
            return float64
        return int64
    
    return _apply_binary_ufunc(x1, x2, lambda a, b: a % b, dtype_func)


def power(x1, x2):
    """Element-wise power."""
    from .dtype import float64
    return _apply_binary_ufunc(x1, x2, lambda a, b: a ** b, lambda dt1, dt2: float64)


def negative(x):
    """Element-wise negation."""
    return _apply_unary_ufunc(x, lambda a: -a)


def absolute(x):
    """Element-wise absolute value."""
    return _apply_unary_ufunc(x, abs)


# Comparison operations
def equal(x1, x2):
    """Element-wise equality."""
    from .dtype import bool_
    return _apply_binary_ufunc(x1, x2, lambda a, b: a == b, lambda dt1, dt2: bool_)


def not_equal(x1, x2):
    """Element-wise inequality."""
    from .dtype import bool_
    return _apply_binary_ufunc(x1, x2, lambda a, b: a != b, lambda dt1, dt2: bool_)


def less(x1, x2):
    """Element-wise less than."""
    from .dtype import bool_
    return _apply_binary_ufunc(x1, x2, lambda a, b: a < b, lambda dt1, dt2: bool_)


def less_equal(x1, x2):
    """Element-wise less than or equal."""
    from .dtype import bool_
    return _apply_binary_ufunc(x1, x2, lambda a, b: a <= b, lambda dt1, dt2: bool_)


def greater(x1, x2):
    """Element-wise greater than."""
    from .dtype import bool_
    return _apply_binary_ufunc(x1, x2, lambda a, b: a > b, lambda dt1, dt2: bool_)


def greater_equal(x1, x2):
    """Element-wise greater than or equal."""
    from .dtype import bool_
    return _apply_binary_ufunc(x1, x2, lambda a, b: a >= b, lambda dt1, dt2: bool_)


# Mathematical functions
def sin(x):
    """Element-wise sine."""
    from .backend_selector import get_backend, Backend
    from .dtype import float64
    from .arrpy_backend import ArrPy
    
    backend = get_backend()
    
    if backend == Backend.CYTHON:
        from .backends.cython.ufuncs_ops import _sin_cython
        result_data, shape = _sin_cython(x._data, x._shape)
        
        result = ArrPy.__new__(ArrPy)
        result._data = result_data
        result._shape = shape
        result._size = x._size
        result._dtype = float64
        result._strides = x._strides
        return result
    else:
        return _apply_unary_ufunc(x, math.sin, lambda dt: float64)


def cos(x):
    """Element-wise cosine."""
    from .backend_selector import get_backend, Backend
    from .dtype import float64
    from .arrpy_backend import ArrPy
    
    backend = get_backend()
    
    if backend == Backend.CYTHON:
        from .backends.cython.ufuncs_ops import _cos_cython
        result_data, shape = _cos_cython(x._data, x._shape)
        
        result = ArrPy.__new__(ArrPy)
        result._data = result_data
        result._shape = shape
        result._size = x._size
        result._dtype = float64
        result._strides = x._strides
        return result
    else:
        return _apply_unary_ufunc(x, math.cos, lambda dt: float64)


def tan(x):
    """Element-wise tangent."""
    from .backend_selector import get_backend, Backend
    from .dtype import float64
    from .arrpy_backend import ArrPy
    
    backend = get_backend()
    
    if backend == Backend.CYTHON:
        from .backends.cython.ufuncs_ops import _tan_cython
        result_data, shape = _tan_cython(x._data, x._shape)
        
        result = ArrPy.__new__(ArrPy)
        result._data = result_data
        result._shape = shape
        result._size = x._size
        result._dtype = float64
        result._strides = x._strides
        return result
    else:
        return _apply_unary_ufunc(x, math.tan, lambda dt: float64)


def exp(x):
    """Element-wise exponential."""
    from .backend_selector import get_backend, Backend
    from .dtype import float64
    from .arrpy_backend import ArrPy
    
    backend = get_backend()
    
    if backend == Backend.CYTHON:
        from .backends.cython.ufuncs_ops import _exp_cython
        result_data, shape = _exp_cython(x._data, x._shape)
        
        result = ArrPy.__new__(ArrPy)
        result._data = result_data
        result._shape = shape
        result._size = x._size
        result._dtype = float64
        result._strides = x._strides
        return result
    else:
        return _apply_unary_ufunc(x, math.exp, lambda dt: float64)


def log(x):
    """Element-wise natural logarithm."""
    from .backend_selector import get_backend, Backend
    from .dtype import float64
    from .arrpy_backend import ArrPy
    
    backend = get_backend()
    
    if backend == Backend.CYTHON:
        from .backends.cython.ufuncs_ops import _log_cython
        result_data, shape = _log_cython(x._data, x._shape)
        
        result = ArrPy.__new__(ArrPy)
        result._data = result_data
        result._shape = shape
        result._size = x._size
        result._dtype = float64
        result._strides = x._strides
        return result
    else:
        return _apply_unary_ufunc(x, math.log, lambda dt: float64)


def log10(x):
    """Element-wise base-10 logarithm."""
    from .backend_selector import get_backend, Backend
    from .dtype import float64
    from .arrpy_backend import ArrPy
    
    backend = get_backend()
    
    if backend == Backend.CYTHON:
        from .backends.cython.ufuncs_ops import _log10_cython
        result_data, shape = _log10_cython(x._data, x._shape)
        
        result = ArrPy.__new__(ArrPy)
        result._data = result_data
        result._shape = shape
        result._size = x._size
        result._dtype = float64
        result._strides = x._strides
        return result
    else:
        return _apply_unary_ufunc(x, math.log10, lambda dt: float64)


def sqrt(x):
    """Element-wise square root."""
    from .backend_selector import get_backend, Backend
    from .dtype import float64
    from .arrpy_backend import ArrPy
    
    backend = get_backend()
    
    if backend == Backend.CYTHON:
        from .backends.cython.ufuncs_ops import _sqrt_cython
        result_data, shape = _sqrt_cython(x._data, x._shape)
        
        result = ArrPy.__new__(ArrPy)
        result._data = result_data
        result._shape = shape
        result._size = x._size
        result._dtype = float64
        result._strides = x._strides
        return result
    else:
        return _apply_unary_ufunc(x, math.sqrt, lambda dt: float64)


def square(x):
    """Element-wise square."""
    return _apply_unary_ufunc(x, lambda a: a * a)


def absolute(x):
    """Element-wise absolute value."""
    from .backend_selector import get_backend, Backend
    from .dtype import float64
    from .arrpy_backend import ArrPy
    
    backend = get_backend()
    
    if backend == Backend.CYTHON:
        from .backends.cython.ufuncs_ops import _absolute_cython
        result_data, shape = _absolute_cython(x._data, x._shape)
        
        result = ArrPy.__new__(ArrPy)
        result._data = result_data
        result._shape = shape
        result._size = x._size
        result._dtype = x._dtype
        result._strides = x._strides
        return result
    else:
        return _apply_unary_ufunc(x, abs)


# Reduction operations
def sum(a, axis=None, keepdims=False):
    """
    Sum of array elements over a given axis.
    
    Parameters
    ----------
    a : arrpy
        Input array
    axis : None or int or tuple of ints, optional
        Axis along which to sum
    keepdims : bool, optional
        Whether to keep reduced dimensions
    
    Returns
    -------
    arrpy or scalar
        Sum of array elements
    """
    from .arrpy_backend import ArrPy
    from .creation import array
    
    if axis is None:
        # Sum all elements
        result = 0
        for val in a._data:
            result += val
        
        if keepdims:
            # Return 0-d array
            return array(result, dtype=a._dtype)
        return result
    
    # TODO: Implement axis-specific reduction
    raise NotImplementedError("Axis-specific sum not yet implemented")


def mean(a, axis=None, keepdims=False):
    """
    Mean of array elements over a given axis.
    
    Parameters
    ----------
    a : arrpy
        Input array
    axis : None or int or tuple of ints, optional
        Axis along which to compute mean
    keepdims : bool, optional
        Whether to keep reduced dimensions
    
    Returns
    -------
    arrpy or scalar
        Mean of array elements
    """
    from .creation import array
    
    if axis is None:
        # Mean of all elements
        total = sum(a, axis=None, keepdims=False)
        result = total / a.size
        
        if keepdims:
            return array(result, dtype=a._dtype)
        return result
    
    # TODO: Implement axis-specific reduction
    raise NotImplementedError("Axis-specific mean not yet implemented")


def min(a, axis=None, keepdims=False):
    """
    Minimum of array elements over a given axis.
    
    Parameters
    ----------
    a : arrpy
        Input array
    axis : None or int or tuple of ints, optional
        Axis along which to find minimum
    keepdims : bool, optional
        Whether to keep reduced dimensions
    
    Returns
    -------
    arrpy or scalar
        Minimum of array elements
    """
    from .creation import array
    import builtins
    
    if axis is None:
        # Min of all elements
        result = builtins.min(a._data)
        
        if keepdims:
            return array(result, dtype=a._dtype)
        return result
    
    # TODO: Implement axis-specific reduction
    raise NotImplementedError("Axis-specific min not yet implemented")


def max(a, axis=None, keepdims=False):
    """
    Maximum of array elements over a given axis.
    
    Parameters
    ----------
    a : arrpy
        Input array
    axis : None or int or tuple of ints, optional
        Axis along which to find maximum
    keepdims : bool, optional
        Whether to keep reduced dimensions
    
    Returns
    -------
    arrpy or scalar
        Maximum of array elements
    """
    from .creation import array
    import builtins
    
    if axis is None:
        # Max of all elements
        result = builtins.max(a._data)
        
        if keepdims:
            return array(result, dtype=a._dtype)
        return result
    
    # TODO: Implement axis-specific reduction
    raise NotImplementedError("Axis-specific max not yet implemented")


def prod(a, axis=None, keepdims=False):
    """
    Product of array elements over a given axis.
    
    Parameters
    ----------
    a : arrpy
        Input array
    axis : None or int or tuple of ints, optional
        Axis along which to compute product
    keepdims : bool, optional
        Whether to keep reduced dimensions
    
    Returns
    -------
    arrpy or scalar
        Product of array elements
    """
    from .creation import array
    
    if axis is None:
        # Product of all elements
        result = 1
        for val in a._data:
            result *= val
        
        if keepdims:
            return array(result, dtype=a._dtype)
        return result
    
    # TODO: Implement axis-specific reduction
    raise NotImplementedError("Axis-specific prod not yet implemented")