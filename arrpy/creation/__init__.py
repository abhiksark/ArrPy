"""
Array creation functions for ArrPy.

This module contains functions for creating new arrays with various
initialization patterns, similar to numpy's array creation routines.
"""

from .basic import zeros, ones, empty, full, eye, identity
from .ranges import arange, linspace, logspace

__all__ = [
    "zeros", "ones", "empty", "full", "eye", "identity",
    "arange", "linspace", "logspace"
]