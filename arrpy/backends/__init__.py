"""
Backend implementations for ArrPy.

This module contains three backend implementations:
- python: Pure Python reference implementation
- cython: Optimized Cython implementation
- c: High-performance C/C++ implementation
"""

from ..backend_selector import get_backend, Backend

__all__ = ['get_backend', 'Backend']