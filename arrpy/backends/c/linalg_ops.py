"""
C backend linear algebra operations.
Uses PyBind11 for high-performance C++ implementations.
"""

def _matmul_c(data1, data2, shape1, shape2):
    """C++ backend matrix multiplication with cache blocking"""
    try:
        from . import linalg_ops_cpp
        result, shape = linalg_ops_cpp.matmul(
            list(data1), list(data2),
            (shape1[0] if shape1 else 1, shape1[1] if len(shape1) > 1 else 1),
            (shape2[0] if shape2 else 1, shape2[1] if len(shape2) > 1 else 1)
        )
        return result, shape
    except ImportError:
        raise NotImplementedError(
            "C++ backend not compiled. Run: make build-cpp\n"
            "Available in: python, cython\n"
            "Switch backends with: arrpy.set_backend('cython')"
        )


def _dot_c(data1, data2, shape1, shape2):
    """C++ backend dot product with SIMD"""
    try:
        from . import linalg_ops_cpp
        result, shape = linalg_ops_cpp.dot(
            list(data1), list(data2),
            (shape1[0] if shape1 else 1, shape1[1] if len(shape1) > 1 else 1),
            (shape2[0] if shape2 else 1, shape2[1] if len(shape2) > 1 else 1)
        )
        return result, shape
    except ImportError:
        raise NotImplementedError(
            "C++ backend not compiled. Run: make build-cpp\n"
            "Available in: python, cython\n"
            "Switch backends with: arrpy.set_backend('cython')"
        )


def _transpose_c(data, shape):
    """C++ backend transpose with cache blocking"""
    try:
        from . import linalg_ops_cpp
        result, new_shape = linalg_ops_cpp.transpose(
            list(data),
            (shape[0] if shape else 1, shape[1] if len(shape) > 1 else 1)
        )
        return result, new_shape
    except ImportError:
        raise NotImplementedError(
            "C++ backend not compiled. Run: make build-cpp\n"
            "Available in: python"
        )


def _solve_c(data_a, data_b, shape_a, shape_b):
    """C backend linear solve - not implemented"""
    raise NotImplementedError(
        "solve() not yet implemented in C backend.\n"
        "Available in: python\n"
        "Switch backends or contribute the implementation!"
    )


def _inv_c(data, shape):
    """C backend matrix inverse - not implemented"""
    raise NotImplementedError(
        "inv() not yet implemented in C backend.\n"
        "Available in: python\n"
        "Switch backends or contribute the implementation!"
    )