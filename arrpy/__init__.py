"""
ArrPy - Educational NumPy recreation with pluggable backends
"""

from .version import __version__

# Main array class with backend support
from .arrpy_backend import ArrPy

# Backend system
from .backend_selector import (
    Backend,
    set_backend,
    get_backend,
    get_backend_capabilities,
    show_backend_status,
    check_backend_has_operation,
    get_available_backends_for_operation,
)

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
from .ufuncs import (
    sin, cos, tan, exp, log, log10, sqrt, square, absolute, abs,
    add, subtract, multiply, divide, power, mod,
    equal, not_equal, less, less_equal, greater, greater_equal,
    sum, mean, min, max, prod, argmin, argmax
)

# Linear algebra
from . import linalg
from .linalg import (
    dot, matmul, transpose, inner, outer, trace,
    solve, inv, det, eig, svd, qr, cholesky, matrix_rank
)

# Sorting and searching
from .sorting import (
    sort, argsort, searchsorted, partition, unique
)

# FFT operations
from . import fft
from .fft import (
    fft as fft_func, ifft, fft2, rfft, fftfreq, fftshift,
    convolve, dct, idct
)

# Advanced indexing
from .indexing import (
    where, fancy_index, boolean_index
)

# Statistics
from .statistics import (
    clip, percentile, median, std, var,
    cumsum, cumprod, diff, gradient
)

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
    # Main classes
    'ArrPy',
    'arrpy',
    # Backend system
    'Backend',
    'set_backend',
    'get_backend',
    'get_backend_capabilities',
    'show_backend_status',
    'check_backend_has_operation',
    'get_available_backends_for_operation',
    # Array creation
    'zeros', 'ones', 'arange', 'linspace', 'array', 'full', 'empty', 'eye',
    # Data types
    'int32', 'int64', 'float32', 'float64', 'bool_',
    'DType', 'infer_dtype',
    # Modules
    'ufuncs', 'linalg', 'random', 'fft',
    # Ufuncs
    'sin', 'cos', 'tan', 'exp', 'log', 'log10', 'sqrt', 'square', 'absolute', 'abs',
    'add', 'subtract', 'multiply', 'divide', 'power', 'mod',
    'equal', 'not_equal', 'less', 'less_equal', 'greater', 'greater_equal',
    'sum', 'mean', 'min', 'max', 'prod', 'argmin', 'argmax',
    # Linear algebra
    'dot', 'matmul', 'transpose', 'inner', 'outer', 'trace',
    'solve', 'inv', 'det', 'eig', 'svd', 'qr', 'cholesky', 'matrix_rank',
    # Sorting and searching
    'sort', 'argsort', 'searchsorted', 'partition', 'unique',
    # FFT operations
    'fft_func', 'ifft', 'fft2', 'rfft', 'fftfreq', 'fftshift',
    'convolve', 'dct', 'idct',
    # Advanced indexing
    'where', 'fancy_index', 'boolean_index',
    # Statistics
    'clip', 'percentile', 'median', 'std', 'var',
    'cumsum', 'cumprod', 'diff', 'gradient',
    # Array manipulation
    'reshape', 'flatten', 'concatenate', 'stack', 'split',
    'squeeze', 'expand_dims',
    # Broadcasting
    'broadcast_arrays', 'broadcast_shapes',
]