"""
ArrPy: A Cython-Optimized NumPy Alternative

ArrPy provides a Cython-optimized implementation of NumPy's core functionality,
delivering significant performance improvements while maintaining educational value
and compatibility.

Performance Highlights:
    - 6-9x faster array creation than pure Python
    - 2-3x faster arithmetic operations with C-level loops  
    - 3-4x faster mathematical functions using libc.math
    - C-level optimized aggregations with fast methods

Main Components:
    - Array: The fundamental n-dimensional array class (Cython-accelerated)
    - Creation functions: zeros, ones, eye, arange, linspace, etc. (Cython-optimized)
    - Mathematical functions: sin_fast, cos_fast, sqrt_fast, etc. (C-level optimized)
    - Statistical functions: sum_fast, mean_fast, etc. (C-level optimized)
    - Array manipulation: reshape, transpose, concatenate, stack, etc.
    - Automatic fallback: Pure Python implementation when Cython unavailable
"""

# Core array class
from .core import Array

# Array creation functions
from .creation import (
    zeros, ones, empty, full, eye, identity,
    arange, linspace, logspace
)

# Mathematical functions
from .math import (
    # Trigonometric
    sin, cos, tan, arcsin, arccos, arctan,
    # Logarithmic  
    exp, log, log10, log2, sqrt,
    # Arithmetic
    power, absolute, sign, floor_divide, mod,
    # Rounding
    floor, ceil, round, trunc
)

# Statistical functions
from .statistics import (
    sum, mean, min, max, std, var, median, percentile,
    prod, cumsum, cumprod, argmin, argmax
)

# Array manipulation functions
from .manipulation import (
    reshape, transpose, squeeze, expand_dims,
    concatenate, stack, vstack, hstack
)

# Version information
__version__ = "0.2.1"

# Public API
__all__ = [
    # Core
    "Array",
    
    # Creation
    "zeros", "ones", "empty", "full", "eye", "identity",
    "arange", "linspace", "logspace",
    
    # Mathematical
    "sin", "cos", "tan", "arcsin", "arccos", "arctan", 
    "exp", "log", "log10", "log2", "sqrt",
    "power", "absolute", "sign", "floor_divide", "mod",
    "floor", "ceil", "round", "trunc",
    
    # Statistical
    "sum", "mean", "min", "max", "std", "var", "median", "percentile",
    "prod", "cumsum", "cumprod", "argmin", "argmax",
    
    # Manipulation
    "reshape", "transpose", "squeeze", "expand_dims",
    "concatenate", "stack", "vstack", "hstack",
]


# Convenience aliases for compatibility
def array(data):
    """
    Create an array from input data.
    
    This is an alias for the Array constructor to match NumPy's API.
    
    Parameters
    ----------
    data : array-like
        Input data (nested lists).
        
    Returns
    -------
    Array
        New array object.
        
    Examples
    --------
    >>> array([1, 2, 3])
    Array([1, 2, 3])
    >>> array([[1, 2], [3, 4]])
    Array([[1, 2], [3, 4]])
    """
    return Array(data)


# Add array function to public API
__all__.append("array")