"""
Cython backend implementation.

This backend provides optimized implementations of select operations
using Cython's static typing and memory views for improved performance.

Note: Only a subset of operations are implemented in Cython.
Operations not implemented here will raise NotImplementedError.
"""

# Try to import the new memoryview-based implementation first
try:
    from .array_ops_new import (
        _add_cython,
        _subtract_cython,
        _multiply_cython,
        _divide_cython,
        _sum_cython as _sum_cython_new,
        _mean_cython,
    )
    # Use the new implementation
    _sum_cython = _sum_cython_new
    USING_NEW_CYTHON = True
except ImportError:
    # Fall back to old implementation
    from .array_ops import (
        _add_cython,
        _multiply_cython,
    )
    from .reduction_ops import (
        _sum_cython,
    )
    # Old implementation doesn't have these
    def _subtract_cython(data1, data2, shape1, shape2):
        raise NotImplementedError("Subtract not implemented in old Cython backend")
    def _divide_cython(data1, data2, shape1, shape2):
        raise NotImplementedError("Divide not implemented in old Cython backend")
    def _mean_cython(data, shape):
        raise NotImplementedError("Mean not implemented in old Cython backend")
    USING_NEW_CYTHON = False

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
    'USING_NEW_CYTHON',
]