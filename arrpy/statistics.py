"""
Statistical functions for ArrPy.
"""

from .backend_selector import get_backend, Backend
from .arrpy_backend import ArrPy


def clip(a, a_min, a_max):
    """
    Clip (limit) the values in an array.
    
    Parameters
    ----------
    a : ArrPy
        Array containing elements to clip
    a_min : scalar or ArrPy
        Minimum value
    a_max : scalar or ArrPy
        Maximum value
    
    Returns
    -------
    ArrPy
        Array with values clipped
    """
    from .creation import array
    
    # Convert to arrays if needed
    if not isinstance(a_min, ArrPy):
        a_min = array(a_min)
    if not isinstance(a_max, ArrPy):
        a_max = array(a_max)
    
    # Broadcast all to same shape
    from .broadcasting import broadcast_arrays
    a_b, min_b, max_b = broadcast_arrays(a, a_min, a_max)
    
    # Clip values
    result_data = []
    for i in range(a_b._size):
        val = a_b._data[i]
        min_val = min_b._data[i]
        max_val = max_b._data[i]
        
        if val < min_val:
            result_data.append(min_val)
        elif val > max_val:
            result_data.append(max_val)
        else:
            result_data.append(val)
    
    result = ArrPy.__new__(ArrPy)
    result._data = result_data
    result._shape = a_b._shape
    result._size = a_b._size
    result._dtype = a._dtype
    result._strides = result._calculate_strides(a_b._shape)
    
    return result


def percentile(a, q, axis=None, keepdims=False):
    """
    Compute the q-th percentile of the data along the specified axis.
    
    Parameters
    ----------
    a : ArrPy
        Input array
    q : float or sequence of floats
        Percentile or sequence of percentiles to compute (0-100)
    axis : int, optional
        Axis along which to compute percentiles
    keepdims : bool, optional
        Keep dimensions
    
    Returns
    -------
    ArrPy or scalar
        Percentile values
    """
    # For simplicity, implement for flattened array first
    if axis is not None:
        raise NotImplementedError("Percentile along axis not yet implemented")
    
    # Flatten and sort
    flat = a.flatten()
    sorted_data = sorted(flat._data)
    n = len(sorted_data)
    
    # Handle single percentile
    if not hasattr(q, '__iter__'):
        q = [q]
        single = True
    else:
        single = False
    
    results = []
    for percentile in q:
        if percentile < 0 or percentile > 100:
            raise ValueError("Percentiles must be in range [0, 100]")
        
        # Calculate position
        pos = (n - 1) * percentile / 100.0
        lower = int(pos)
        upper = lower + 1
        
        if upper >= n:
            results.append(sorted_data[n - 1])
        else:
            # Linear interpolation
            weight = pos - lower
            value = sorted_data[lower] * (1 - weight) + sorted_data[upper] * weight
            results.append(value)
    
    if single:
        return results[0]
    
    result = ArrPy.__new__(ArrPy)
    result._data = results
    result._shape = (len(results),)
    result._size = len(results)
    result._dtype = a._dtype
    result._strides = (1,)
    
    return result


def median(a, axis=None, keepdims=False):
    """
    Compute the median along the specified axis.
    
    Parameters
    ----------
    a : ArrPy
        Input array
    axis : int, optional
        Axis along which to compute median
    keepdims : bool, optional
        Keep dimensions
    
    Returns
    -------
    ArrPy or scalar
        Median value(s)
    """
    return percentile(a, 50, axis=axis, keepdims=keepdims)


def std(a, axis=None, keepdims=False, ddof=0):
    """
    Compute the standard deviation along the specified axis.
    
    Parameters
    ----------
    a : ArrPy
        Input array
    axis : int, optional
        Axis along which to compute std
    keepdims : bool, optional
        Keep dimensions
    ddof : int, optional
        Delta degrees of freedom
    
    Returns
    -------
    ArrPy or scalar
        Standard deviation
    """
    # Compute variance and take square root
    var_result = var(a, axis=axis, keepdims=keepdims, ddof=ddof)
    
    if isinstance(var_result, (int, float)):
        import math
        return math.sqrt(var_result)
    
    # Take square root of variance array
    from .ufuncs import sqrt
    return sqrt(var_result)


def var(a, axis=None, keepdims=False, ddof=0):
    """
    Compute the variance along the specified axis.
    
    Parameters
    ----------
    a : ArrPy
        Input array
    axis : int, optional
        Axis along which to compute variance
    keepdims : bool, optional
        Keep dimensions
    ddof : int, optional
        Delta degrees of freedom
    
    Returns
    -------
    ArrPy or scalar
        Variance
    """
    # Compute mean
    mean_val = a.mean(axis=axis, keepdims=True)
    
    # Compute squared differences
    if isinstance(mean_val, (int, float)):
        diff = a - mean_val
    else:
        from .broadcasting import broadcast_arrays
        a_b, mean_b = broadcast_arrays(a, mean_val)
        diff = a_b - mean_b
    
    squared_diff = diff * diff
    
    # Sum squared differences
    sum_sq = squared_diff.sum(axis=axis, keepdims=keepdims)
    
    # Divide by N - ddof
    if axis is None:
        n = a.size
    else:
        n = a.shape[axis] if axis >= 0 else a.shape[a.ndim + axis]
    
    if isinstance(sum_sq, (int, float)):
        return sum_sq / (n - ddof)
    
    # Divide array by scalar
    result_data = [val / (n - ddof) for val in sum_sq._data]
    
    result = ArrPy.__new__(ArrPy)
    result._data = result_data
    result._shape = sum_sq._shape
    result._size = sum_sq._size
    result._dtype = sum_sq._dtype
    result._strides = sum_sq._strides
    
    return result


def histogram(a, bins=10, range=None):
    """
    Compute the histogram of a dataset.
    
    Parameters
    ----------
    a : ArrPy
        Input data
    bins : int or sequence, optional
        Number of bins or bin edges
    range : tuple, optional
        Range of values (min, max)
    
    Returns
    -------
    hist : ArrPy
        Values of the histogram
    bin_edges : ArrPy
        Edges of the bins
    """
    # Flatten input
    flat = a.flatten()
    
    # Determine range
    if range is None:
        min_val = min(flat._data)
        max_val = max(flat._data)
    else:
        min_val, max_val = range
    
    # Create bins
    if isinstance(bins, int):
        # Uniform bins
        bin_edges = []
        step = (max_val - min_val) / bins
        for i in range(bins + 1):
            bin_edges.append(min_val + i * step)
    else:
        bin_edges = list(bins)
        bins = len(bin_edges) - 1
    
    # Count values in each bin
    hist = [0] * bins
    for val in flat._data:
        if val < min_val or val > max_val:
            continue
        
        # Find bin
        if val == max_val:
            # Right edge belongs to last bin
            hist[-1] += 1
        else:
            bin_idx = int((val - min_val) / step)
            if 0 <= bin_idx < bins:
                hist[bin_idx] += 1
    
    # Create result arrays
    hist_arr = ArrPy.__new__(ArrPy)
    hist_arr._data = hist
    hist_arr._shape = (bins,)
    hist_arr._size = bins
    from .dtype import int64
    hist_arr._dtype = int64
    hist_arr._strides = (1,)
    
    edges_arr = ArrPy.__new__(ArrPy)
    edges_arr._data = bin_edges
    edges_arr._shape = (bins + 1,)
    edges_arr._size = bins + 1
    edges_arr._dtype = a._dtype
    edges_arr._strides = (1,)
    
    return hist_arr, edges_arr


def cumsum(a, axis=None):
    """
    Return the cumulative sum of elements along a given axis.
    
    Parameters
    ----------
    a : ArrPy
        Input array
    axis : int, optional
        Axis along which to compute cumsum
    
    Returns
    -------
    ArrPy
        Cumulative sum array
    """
    if axis is not None:
        raise NotImplementedError("Cumsum along axis not yet implemented")
    
    # Flatten and compute cumsum
    flat = a.flatten()
    result_data = []
    cumsum = 0
    
    for val in flat._data:
        cumsum += val
        result_data.append(cumsum)
    
    result = ArrPy.__new__(ArrPy)
    result._data = result_data
    result._shape = flat._shape
    result._size = flat._size
    result._dtype = a._dtype
    result._strides = (1,)
    
    return result


def cumprod(a, axis=None):
    """
    Return the cumulative product of elements along a given axis.
    
    Parameters
    ----------
    a : ArrPy
        Input array
    axis : int, optional
        Axis along which to compute cumprod
    
    Returns
    -------
    ArrPy
        Cumulative product array
    """
    if axis is not None:
        raise NotImplementedError("Cumprod along axis not yet implemented")
    
    # Flatten and compute cumprod
    flat = a.flatten()
    result_data = []
    cumprod = 1
    
    for val in flat._data:
        cumprod *= val
        result_data.append(cumprod)
    
    result = ArrPy.__new__(ArrPy)
    result._data = result_data
    result._shape = flat._shape
    result._size = flat._size
    result._dtype = a._dtype
    result._strides = (1,)
    
    return result


def diff(a, n=1, axis=-1):
    """
    Calculate the n-th discrete difference along the given axis.
    
    Parameters
    ----------
    a : ArrPy
        Input array
    n : int, optional
        Number of times to difference
    axis : int, optional
        Axis along which to difference
    
    Returns
    -------
    ArrPy
        Differenced array
    """
    if n == 0:
        return a
    
    if n < 0:
        raise ValueError("n must be non-negative")
    
    # For simplicity, implement for 1D arrays
    if a.ndim > 1:
        raise NotImplementedError("Diff for multi-dimensional arrays not yet implemented")
    
    result = a
    for _ in range(n):
        if result.shape[0] <= 1:
            # Empty result
            result = ArrPy.__new__(ArrPy)
            result._data = []
            result._shape = (0,)
            result._size = 0
            result._dtype = a._dtype
            result._strides = ()
            return result
        
        # Compute differences
        diff_data = []
        for i in range(1, result.shape[0]):
            diff_data.append(result._data[i] - result._data[i - 1])
        
        result = ArrPy.__new__(ArrPy)
        result._data = diff_data
        result._shape = (len(diff_data),)
        result._size = len(diff_data)
        result._dtype = a._dtype
        result._strides = (1,)
    
    return result


def gradient(a, *varargs, axis=None):
    """
    Return the gradient of an N-dimensional array.
    
    Parameters
    ----------
    a : ArrPy
        Input array
    varargs : scalar or array, optional
        Spacing between values
    axis : int, optional
        Axis along which to compute gradient
    
    Returns
    -------
    ArrPy or list of ArrPy
        Gradient array(s)
    """
    # Simple implementation for 1D
    if a.ndim > 1 and axis is None:
        raise NotImplementedError("Multi-dimensional gradient not yet implemented")
    
    n = a.shape[0] if axis is None else a.shape[axis]
    
    # Spacing
    if varargs:
        h = varargs[0]
    else:
        h = 1.0
    
    # Compute gradient using central differences
    grad_data = []
    
    for i in range(n):
        if i == 0:
            # Forward difference at start
            grad = (a._data[1] - a._data[0]) / h
        elif i == n - 1:
            # Backward difference at end
            grad = (a._data[-1] - a._data[-2]) / h
        else:
            # Central difference
            grad = (a._data[i + 1] - a._data[i - 1]) / (2 * h)
        
        grad_data.append(grad)
    
    result = ArrPy.__new__(ArrPy)
    result._data = grad_data
    result._shape = a._shape
    result._size = a._size
    result._dtype = a._dtype
    result._strides = a._strides
    
    return result