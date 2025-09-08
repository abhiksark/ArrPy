"""
Cython-optimized linear algebra operations.
Matrix multiplication benefits greatly from type annotations and loop optimization.
"""

import cython
from libc.stdlib cimport malloc, free
from libc.string cimport memset
from libc.math cimport sqrt, fabs

# Cache line size for blocking
DEF BLOCK_SIZE = 64

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _matmul_cython(data1, data2, shape1, shape2):
    """
    Cache-efficient blocked matrix multiplication.
    No numpy overhead, uses loop tiling.
    """
    cdef:
        Py_ssize_t m = shape1[0]
        Py_ssize_t n = shape1[1] if len(shape1) > 1 else 1
        Py_ssize_t p = shape2[1] if len(shape2) > 1 else 1
        Py_ssize_t i, j, k, ii, jj, kk
        Py_ssize_t block_size = BLOCK_SIZE
        double* mat1
        double* mat2
        double* result
        double sum_val
        list result_list = []
    
    # Allocate memory
    mat1 = <double*>malloc(m * n * sizeof(double))
    mat2 = <double*>malloc(n * p * sizeof(double))
    result = <double*>malloc(m * p * sizeof(double))
    
    if not mat1 or not mat2 or not result:
        if mat1: free(mat1)
        if mat2: free(mat2)
        if result: free(result)
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Initialize result to zero
        memset(result, 0, m * p * sizeof(double))
        
        # Copy input data
        for i in range(m * n):
            mat1[i] = <double>data1[i]
        for i in range(n * p):
            mat2[i] = <double>data2[i]
        
        # Use blocked algorithm for large matrices, naive for small
        if m * n * p > 64000:  # Threshold for blocking
            # Blocked matrix multiplication
            for ii in range(0, m, block_size):
                for jj in range(0, p, block_size):
                    for kk in range(0, n, block_size):
                        for i in range(ii, min(ii + block_size, m)):
                            for j in range(jj, min(jj + block_size, p)):
                                sum_val = result[i * p + j]
                                for k in range(kk, min(kk + block_size, n)):
                                    sum_val += mat1[i * n + k] * mat2[k * p + j]
                                result[i * p + j] = sum_val
        else:
            # Naive algorithm for small matrices
            for i in range(m):
                for j in range(p):
                    sum_val = 0.0
                    for k in range(n):
                        sum_val += mat1[i * n + k] * mat2[k * p + j]
                    result[i * p + j] = sum_val
        
        # Copy result back
        result_list = [result[i] for i in range(m * p)]
        return result_list, (m, p)
    
    finally:
        free(mat1)
        free(mat2)
        free(result)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _dot_cython(data1, data2, shape1, shape2):
    """
    Optimized dot product for vectors and matrices.
    """
    cdef:
        Py_ssize_t n, m, p
        Py_ssize_t i
        double* vec1
        double* vec2
        double result = 0.0
    
    # Handle vector dot product
    if len(shape1) == 1 and len(shape2) == 1:
        n = shape1[0]
        if n != shape2[0]:
            raise ValueError("Incompatible dimensions for dot product")
        
        vec1 = <double*>malloc(n * sizeof(double))
        vec2 = <double*>malloc(n * sizeof(double))
        
        if not vec1 or not vec2:
            if vec1: free(vec1)
            if vec2: free(vec2)
            raise MemoryError("Failed to allocate memory")
        
        try:
            # Copy data
            for i in range(n):
                vec1[i] = <double>data1[i]
                vec2[i] = <double>data2[i]
            
            # Compute dot product with loop unrolling
            i = 0
            while i < n - 3:
                result += vec1[i] * vec2[i]
                result += vec1[i+1] * vec2[i+1]
                result += vec1[i+2] * vec2[i+2]
                result += vec1[i+3] * vec2[i+3]
                i += 4
            
            # Handle remaining elements
            while i < n:
                result += vec1[i] * vec2[i]
                i += 1
            
            return [result], ()
        
        finally:
            free(vec1)
            free(vec2)
    else:
        # Matrix multiplication case
        return _matmul_cython(data1, data2, shape1, shape2)


def _solve_cython(data_a, data_b, shape_a, shape_b):
    """Linear solve not yet optimized in Cython."""
    raise NotImplementedError(
        "solve() not yet implemented in Cython backend.\n"
        "Available in: python\n"
        "Switch backends or contribute the implementation!"
    )


def _inv_cython(data, shape):
    """Matrix inverse not yet optimized in Cython."""
    raise NotImplementedError(
        "inv() not yet implemented in Cython backend.\n"
        "Available in: python\n"
        "Switch backends or contribute the implementation!"
    )


def _det_cython(data, shape):
    """Determinant not yet optimized in Cython."""
    raise NotImplementedError(
        "det() not yet implemented in Cython backend.\n"
        "Available in: python\n"
        "Switch backends or contribute the implementation!"
    )