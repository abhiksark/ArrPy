"""
Main arrpy array class - Pure Python implementation of NumPy-like arrays.
"""

class arrpy:
    """
    N-dimensional array class mimicking NumPy's ndarray.
    
    This is the pure Python implementation (v0.x) focusing on correctness
    over performance.
    """
    
    def __init__(self, data, dtype=None):
        """
        Initialize an arrpy array.
        
        Parameters
        ----------
        data : array-like
            Input data (list, tuple, or nested sequences)
        dtype : dtype, optional
            Desired data type for the array
        """
        # TODO: Implement initialization
        pass
    
    @property
    def shape(self):
        """Get the shape of the array."""
        # TODO: Implement shape property
        pass
    
    @property
    def size(self):
        """Get the total number of elements."""
        # TODO: Implement size property
        pass
    
    @property
    def ndim(self):
        """Get the number of dimensions."""
        # TODO: Implement ndim property
        pass
    
    def __repr__(self):
        """String representation of the array."""
        # TODO: Implement repr
        return f"arrpy(shape={self.shape})"
    
    def __str__(self):
        """Pretty string representation."""
        # TODO: Implement str
        return self.__repr__()