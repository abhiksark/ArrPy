"""
Mathematical functions for ArrPy.

This module contains mathematical functions that operate element-wise
on arrays, including trigonometric, logarithmic, and arithmetic functions.
Automatically imports Cython optimized versions when available.
"""

from .trigonometric import sin, cos, tan, arcsin, arccos, arctan
from .logarithmic import exp, log, log10, log2, sqrt
from .rounding import floor, ceil, round, trunc

# Import arithmetic functions, preferring Cython versions
try:
    from .arithmetic_cython import power, absolute, sign, floor_divide, mod
    _using_cython_arithmetic = True
except ImportError:
    from .arithmetic import power, absolute, sign, floor_divide, mod
    _using_cython_arithmetic = False

__all__ = [
    # Trigonometric
    "sin", "cos", "tan", "arcsin", "arccos", "arctan",
    # Logarithmic
    "exp", "log", "log10", "log2", "sqrt", 
    # Arithmetic
    "power", "absolute", "sign", "floor_divide", "mod",
    # Rounding
    "floor", "ceil", "round", "trunc"
]