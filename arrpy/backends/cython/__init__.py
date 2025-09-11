"""
Cython backend implementation.

This backend provides optimized implementations of select operations
using Cython's static typing and memory views for improved performance.

Note: Only a subset of operations are implemented in Cython.
Operations not implemented here will raise NotImplementedError.
"""

# Import from the unified array_ops module (formerly array_ops_new)
from .array_ops import (
    _add_cython,
    _subtract_cython,
    _multiply_cython,
    _divide_cython,
    _sum_cython,
    _mean_cython,
)

# Import from reduction_ops if sum is not in array_ops
try:
    from .reduction_ops import (
        _sum_cython as _sum_cython_reduction,
    )
    # If both exist, prefer array_ops version
except ImportError:
    pass

# Always import these from old modules if available
try:
    from .linalg_ops import (
        _matmul_cython,
    )
except ImportError:
    def _matmul_cython(data1, data2, shape1, shape2):
        raise NotImplementedError("Matmul not implemented in Cython backend")

try:
    from .ufuncs_ops import (
        _sqrt_cython,
    )
except ImportError:
    def _sqrt_cython(data, shape):
        raise NotImplementedError("Sqrt not implemented in Cython backend")

__all__ = [
    '_add_cython',
    '_subtract_cython',
    '_multiply_cython',
    '_divide_cython',
    '_matmul_cython',
    '_sum_cython',
    '_mean_cython',
    '_sqrt_cython',
]