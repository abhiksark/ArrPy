"""
ArrPy - Educational NumPy recreation
Pure Python implementation (v0.x)
"""

from .version import __version__

# Main array class
from .arrpy import arrpy

# Array creation functions
from .creation import (
    zeros, ones, arange, linspace, array, full, empty, eye
)

# Data types
from .dtype import (
    int32, int64, float32, float64, bool_,
    DType, infer_dtype
)

# Universal functions
from . import ufuncs

# Linear algebra
from . import linalg

# Random number generation
from . import random

# Array manipulation
from .manipulation import (
    reshape, flatten, concatenate, stack, split,
    squeeze, expand_dims
)

# Broadcasting
from .broadcasting import broadcast_arrays, broadcast_shapes

__all__ = [
    '__version__',
    'arrpy',
    'zeros', 'ones', 'arange', 'linspace', 'array', 'full', 'empty', 'eye',
    'int32', 'int64', 'float32', 'float64', 'bool_',
    'DType', 'infer_dtype',
    'ufuncs', 'linalg', 'random',
    'reshape', 'flatten', 'concatenate', 'stack', 'split',
    'squeeze', 'expand_dims',
    'broadcast_arrays', 'broadcast_shapes',
]