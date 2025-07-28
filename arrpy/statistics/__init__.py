"""
Statistical functions for ArrPy.

This module contains statistical functions for analyzing array data,
including basic statistics, aggregations, and advanced statistical operations.
"""

from .basic import sum, mean, min, max, std, var, median, percentile
from .aggregation import prod, cumsum, cumprod, argmin, argmax

__all__ = [
    "sum", "mean", "min", "max", "std", "var", "median", "percentile",
    "prod", "cumsum", "cumprod", "argmin", "argmax"
]