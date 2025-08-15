"""
Array manipulation functions for arrpy.
"""


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
    # TODO: Implement reshape
    pass


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
    # TODO: Implement flatten
    pass


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
    # TODO: Implement concatenate
    pass


def stack(arrays, axis=0):
    """
    Stack arrays along a new axis.
    
    Parameters
    ----------
    arrays : sequence of arrpy
        Arrays to stack
    axis : int, optional
        Axis along which to stack
    
    Returns
    -------
    arrpy
        Stacked array
    """
    # TODO: Implement stack
    pass


def split(a, indices_or_sections, axis=0):
    """
    Split an array into multiple sub-arrays.
    
    Parameters
    ----------
    a : arrpy
        Array to split
    indices_or_sections : int or sequence of ints
        Indices or number of sections
    axis : int, optional
        Axis along which to split
    
    Returns
    -------
    list of arrpy
        List of sub-arrays
    """
    # TODO: Implement split
    pass


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
    # TODO: Implement squeeze
    pass


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
    # TODO: Implement expand_dims
    pass