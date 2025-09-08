"""
C/C++ backend implementation.

This backend provides maximum performance implementations for critical operations
using C++ with SIMD optimizations and efficient memory management.

Note: Only the most performance-critical operations are implemented in C.
Operations not implemented here will raise NotImplementedError.
"""

from .linalg_ops import (
    _matmul_c,
    _dot_c,
)

__all__ = [
    '_matmul_c',
    '_dot_c',
]