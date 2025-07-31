"""
Array creation functions for ArrPy.

This module contains functions for creating new arrays with various
initialization patterns, similar to numpy's array creation routines.
Automatically imports Cython optimized versions when available.
"""

from .ranges import arange, linspace, logspace

# Import basic creation functions, preferring Cython versions
try:
    from .basic_cython import zeros, ones, empty, full, eye, identity
    _using_cython_basic = True
except ImportError:
    from .basic import zeros, ones, empty, full, eye, identity
    _using_cython_basic = False

__all__ = [
    "zeros", "ones", "empty", "full", "eye", "identity",
    "arange", "linspace", "logspace"
]