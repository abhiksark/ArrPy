"""
Sorting and searching operations for ArrPy.
"""

from .backend_selector import get_backend, Backend
from .arrpy_backend import ArrPy


def sort(a, axis=-1, kind='quicksort'):
    """
    Sort an array along the given axis.
    
    Parameters
    ----------
    a : ArrPy
        Array to sort
    axis : int, optional
        Axis along which to sort. Default is -1 (last axis)
    kind : str, optional
        Sorting algorithm: 'quicksort', 'mergesort', 'heapsort'
    
    Returns
    -------
    ArrPy
        Sorted array (copy)
    """
    backend = get_backend()
    
    if backend == Backend.PYTHON:
        from .backends.python.sorting_ops import _sort_python
        result_data, shape = _sort_python(a._data, a._shape, axis, kind)
    else:
        # Fallback to Python for other backends
        from .backends.python.sorting_ops import _sort_python
        result_data, shape = _sort_python(a._data, a._shape, axis, kind)
    
    result = ArrPy.__new__(ArrPy)
    result._data = result_data
    result._shape = shape
    result._size = a._size
    result._dtype = a._dtype
    result._strides = result._calculate_strides(shape)
    
    return result


def argsort(a, axis=-1, kind='quicksort'):
    """
    Return the indices that would sort an array.
    
    Parameters
    ----------
    a : ArrPy
        Array to sort
    axis : int, optional
        Axis along which to sort
    kind : str, optional
        Sorting algorithm
    
    Returns
    -------
    ArrPy
        Array of indices
    """
    backend = get_backend()
    
    if backend == Backend.PYTHON:
        from .backends.python.sorting_ops import _argsort_python
        result_data, shape = _argsort_python(a._data, a._shape, axis, kind)
    else:
        from .backends.python.sorting_ops import _argsort_python
        result_data, shape = _argsort_python(a._data, a._shape, axis, kind)
    
    from .dtype import int64
    
    result = ArrPy.__new__(ArrPy)
    result._data = result_data
    result._shape = shape
    result._size = a._size
    result._dtype = int64
    result._strides = result._calculate_strides(shape)
    
    return result


def searchsorted(a, v, side='left'):
    """
    Find indices where elements should be inserted to maintain order.
    
    Parameters
    ----------
    a : ArrPy
        Input array (must be sorted)
    v : scalar or ArrPy
        Values to insert
    side : {'left', 'right'}, optional
        If 'left', gives leftmost position; if 'right', rightmost
    
    Returns
    -------
    int or ArrPy
        Insertion indices
    """
    backend = get_backend()
    
    # Handle scalar input
    if not isinstance(v, ArrPy):
        v_data = [v]
        v_shape = (1,)
        return_scalar = True
    else:
        v_data = v._data
        v_shape = v._shape
        return_scalar = False
    
    if backend == Backend.PYTHON:
        from .backends.python.sorting_ops import _searchsorted_python
        result_data, shape = _searchsorted_python(
            a._data, a._shape, v_data, v_shape, side
        )
    else:
        from .backends.python.sorting_ops import _searchsorted_python
        result_data, shape = _searchsorted_python(
            a._data, a._shape, v_data, v_shape, side
        )
    
    if return_scalar:
        return result_data[0]
    
    from .dtype import int64
    
    result = ArrPy.__new__(ArrPy)
    result._data = result_data
    result._shape = shape
    result._size = len(result_data)
    result._dtype = int64
    result._strides = result._calculate_strides(shape)
    
    return result


def partition(a, kth, axis=-1):
    """
    Partition array so that element at kth position is in its sorted position.
    
    Parameters
    ----------
    a : ArrPy
        Array to partition
    kth : int or sequence of ints
        Index of element in the sorted array
    axis : int, optional
        Axis along which to partition
    
    Returns
    -------
    ArrPy
        Partitioned array (copy)
    """
    backend = get_backend()
    
    if backend == Backend.PYTHON:
        from .backends.python.sorting_ops import _partition_python
        result_data, shape = _partition_python(a._data, a._shape, kth, axis)
    else:
        from .backends.python.sorting_ops import _partition_python
        result_data, shape = _partition_python(a._data, a._shape, kth, axis)
    
    result = ArrPy.__new__(ArrPy)
    result._data = result_data
    result._shape = shape
    result._size = a._size
    result._dtype = a._dtype
    result._strides = result._calculate_strides(shape)
    
    return result


def unique(a, return_index=False, return_inverse=False, return_counts=False):
    """
    Find the unique elements of an array.
    
    Parameters
    ----------
    a : ArrPy
        Input array
    return_index : bool, optional
        If True, also return indices of first occurrences
    return_inverse : bool, optional
        If True, also return indices to reconstruct original array
    return_counts : bool, optional
        If True, also return counts of each unique element
    
    Returns
    -------
    unique : ArrPy
        The sorted unique values
    unique_indices : ArrPy, optional
        Indices of first occurrences
    unique_inverse : ArrPy, optional
        Indices to reconstruct original
    unique_counts : ArrPy, optional
        Count of each unique element
    """
    backend = get_backend()
    
    if backend == Backend.PYTHON:
        from .backends.python.sorting_ops import _unique_python
        results = _unique_python(
            a._data, a._shape, return_index, return_inverse, return_counts
        )
    else:
        from .backends.python.sorting_ops import _unique_python
        results = _unique_python(
            a._data, a._shape, return_index, return_inverse, return_counts
        )
    
    # Unpack results
    unique_data, unique_shape = results[0], results[1]
    
    # Create unique array
    unique_arr = ArrPy.__new__(ArrPy)
    unique_arr._data = unique_data
    unique_arr._shape = unique_shape
    unique_arr._size = len(unique_data)
    unique_arr._dtype = a._dtype
    unique_arr._strides = unique_arr._calculate_strides(unique_shape)
    
    # Build return tuple
    ret = [unique_arr]
    idx = 2
    
    from .dtype import int64
    
    if return_index:
        index_data, index_shape = results[idx], results[idx + 1]
        index_arr = ArrPy.__new__(ArrPy)
        index_arr._data = index_data
        index_arr._shape = index_shape
        index_arr._size = len(index_data)
        index_arr._dtype = int64
        index_arr._strides = index_arr._calculate_strides(index_shape)
        ret.append(index_arr)
        idx += 2
    
    if return_inverse:
        inverse_data, inverse_shape = results[idx], results[idx + 1]
        inverse_arr = ArrPy.__new__(ArrPy)
        inverse_arr._data = inverse_data
        inverse_arr._shape = inverse_shape
        inverse_arr._size = len(inverse_data)
        inverse_arr._dtype = int64
        inverse_arr._strides = inverse_arr._calculate_strides(inverse_shape)
        ret.append(inverse_arr)
        idx += 2
    
    if return_counts:
        counts_data, counts_shape = results[idx], results[idx + 1]
        counts_arr = ArrPy.__new__(ArrPy)
        counts_arr._data = counts_data
        counts_arr._shape = counts_shape
        counts_arr._size = len(counts_data)
        counts_arr._dtype = int64
        counts_arr._strides = counts_arr._calculate_strides(counts_shape)
        ret.append(counts_arr)
    
    if len(ret) == 1:
        return ret[0]
    return tuple(ret)