"""
C backend reduction operations.

Stub implementations for reductions.
"""


def _sum_c(data, shape, axis=None, keepdims=False):
    """C backend sum - not implemented."""
    raise NotImplementedError(
        "sum() not yet implemented in C backend.\n"
        "Available in: python, cython\n"
        "Switch backends or contribute the implementation!"
    )


def _mean_c(data, shape, axis=None, keepdims=False):
    """C backend mean - not implemented."""
    raise NotImplementedError(
        "mean() not yet implemented in C backend.\n"
        "Available in: python\n"
        "Switch backends or contribute the implementation!"
    )