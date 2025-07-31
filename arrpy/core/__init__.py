"""
Core array functionality for ArrPy.

This module contains the fundamental Array class and core operations.
Automatically imports the Cython version if available, otherwise falls back to Python.
"""

try:
    # Try to import the Cython version
    from .array_cython import Array
    _using_cython = True
except ImportError:
    # Fall back to pure Python version
    from .array import Array
    _using_cython = False

__all__ = ["Array"]