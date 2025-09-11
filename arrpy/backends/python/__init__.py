"""
Pure Python backend implementation.

This is the reference implementation that prioritizes clarity and correctness
over performance. All algorithms are implemented in readable Python without
external dependencies.
"""

from .array_ops import (
    _add_python,
    _subtract_python,
    _multiply_python,
    _divide_python,
    _power_python,
    _negative_python,
    _absolute_python,
)

from .linalg_ops import (
    _matmul_python,
    _dot_python,
    _inner_python,
    _outer_python,
)

from .ufuncs_ops import (
    _sin_python,
    _cos_python,
    _exp_python,
    _log_python,
    _sqrt_python,
)

from .reduction_ops import (
    _sum_python,
    _mean_python,
    _min_python,
    _max_python,
    _prod_python,
)

__all__ = [
    # Array operations
    '_add_python',
    '_subtract_python',
    '_multiply_python',
    '_divide_python',
    '_power_python',
    '_negative_python',
    '_absolute_python',
    
    # Linear algebra
    '_matmul_python',
    '_dot_python',
    '_inner_python',
    '_outer_python',
    
    # Universal functions
    '_sin_python',
    '_cos_python',
    '_exp_python',
    '_log_python',
    '_sqrt_python',
    
    # Reductions
    '_sum_python',
    '_mean_python',
    '_min_python',
    '_max_python',
    '_prod_python',
]