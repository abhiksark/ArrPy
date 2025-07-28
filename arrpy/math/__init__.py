"""
Mathematical functions for ArrPy.

This module contains mathematical functions that operate element-wise
on arrays, including trigonometric, logarithmic, and arithmetic functions.
"""

from .trigonometric import sin, cos, tan, arcsin, arccos, arctan
from .logarithmic import exp, log, log10, log2, sqrt
from .arithmetic import power, absolute, sign, floor_divide, mod
from .rounding import floor, ceil, round, trunc

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