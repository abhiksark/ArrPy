"""
Array manipulation functions for ArrPy.

This module contains functions for manipulating array shapes, joining arrays,
splitting arrays, and rearranging elements.
"""

from .shape import reshape, transpose, squeeze, expand_dims
from .joining import concatenate, stack, vstack, hstack

__all__ = [
    "reshape", "transpose", "squeeze", "expand_dims",
    "concatenate", "stack", "vstack", "hstack"
]