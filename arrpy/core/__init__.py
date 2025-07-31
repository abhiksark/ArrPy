"""
Core array functionality for ArrPy.

This module contains the fundamental Array class and core operations.
"""

# Import the hybrid array implementation that uses C backend when available
try:
    from .hybrid_array import Array, HAS_C_EXTENSION
except ImportError:
    # Fall back to pure Python if hybrid implementation fails
    from .array import Array
    HAS_C_EXTENSION = False

__all__ = ["Array", "HAS_C_EXTENSION"]