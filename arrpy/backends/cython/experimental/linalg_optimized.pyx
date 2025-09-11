"""
Cache-efficient linear algebra operations.
Implements blocking, loop tiling, and SIMD-friendly patterns.
"""

import cython
from libc.stdlib cimport malloc, free
from libc.string cimport memset
from libc.math cimport sqrt, fabs
from cython.parallel import prange

# Cache line size (typical 64 bytes = 8 doubles)
DEF CACHE_LINE = 64
DEF BLOCK_SIZE = 64  # Tile size for cache blocking

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _matmul_blocked(data1, data2, shape1, shape2):
    """
    Cache-efficient blocked matrix multiplication.
    Uses loop tiling to improve cache locality.
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
    
    # Allocate aligned memory for better cache performance
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
        
        # Copy input data (row-major order)
        for i in range(m * n):
            mat1[i] = <double>data1[i]
        for i in range(n * p):
            mat2[i] = <double>data2[i]
        
        # Blocked matrix multiplication (cache-efficient)
        for ii in range(0, m, block_size):
            for jj in range(0, p, block_size):
                for kk in range(0, n, block_size):
                    # Process block
                    for i in range(ii, min(ii + block_size, m)):
                        for j in range(jj, min(jj + block_size, p)):
                            sum_val = result[i * p + j]
                            for k in range(kk, min(kk + block_size, n)):
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
def _matmul_naive_optimized(data1, data2, shape1, shape2):
    """
    Optimized naive matrix multiplication without numpy.
    Better than Python but not cache-efficient.
    """
    cdef:
        Py_ssize_t m = shape1[0]
        Py_ssize_t n = shape1[1] if len(shape1) > 1 else 1
        Py_ssize_t p = shape2[1] if len(shape2) > 1 else 1
        Py_ssize_t i, j, k
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
        # Copy input data
        for i in range(m * n):
            mat1[i] = <double>data1[i]
        for i in range(n * p):
            mat2[i] = <double>data2[i]
        
        # Standard matrix multiplication (ijk order)
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
def _dot_optimized(data1, data2, shape1, shape2):
    """
    Optimized dot product for vectors and matrices.
    """
    cdef:
        Py_ssize_t n
        Py_ssize_t i
        double* vec1
        double* vec2
        double result = 0.0
        double local_sum
    
    # Handle different cases
    if len(shape1) == 1 and len(shape2) == 1:
        # Vector dot product
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
            
            # Compute dot product (unrolled for better performance)
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
        return _matmul_naive_optimized(data1, data2, shape1, shape2)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _transpose_optimized(data, shape):
    """
    Cache-efficient matrix transpose.
    Uses blocking to improve cache locality.
    """
    cdef:
        Py_ssize_t m = shape[0]
        Py_ssize_t n = shape[1] if len(shape) > 1 else 1
        Py_ssize_t i, j, ii, jj
        Py_ssize_t block_size = BLOCK_SIZE
        double* mat
        double* result
        list result_list = []
    
    mat = <double*>malloc(m * n * sizeof(double))
    result = <double*>malloc(n * m * sizeof(double))
    
    if not mat or not result:
        if mat: free(mat)
        if result: free(result)
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy input data
        for i in range(m * n):
            mat[i] = <double>data[i]
        
        # Blocked transpose for cache efficiency
        for ii in range(0, m, block_size):
            for jj in range(0, n, block_size):
                for i in range(ii, min(ii + block_size, m)):
                    for j in range(jj, min(jj + block_size, n)):
                        result[j * m + i] = mat[i * n + j]
        
        # Copy result back
        result_list = [result[i] for i in range(n * m)]
        return result_list, (n, m)
    
    finally:
        free(mat)
        free(result)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _gemm_optimized(double alpha, data_a, data_b, double beta, data_c, shape_a, shape_b, shape_c):
    """
    General matrix multiply: C = alpha*A*B + beta*C
    Building block for many linear algebra operations.
    """
    cdef:
        Py_ssize_t m = shape_a[0]
        Py_ssize_t n = shape_a[1] if len(shape_a) > 1 else 1
        Py_ssize_t p = shape_b[1] if len(shape_b) > 1 else 1
        Py_ssize_t i, j, k
        double* mat_a
        double* mat_b
        double* mat_c
        double sum_val
        list result_list = []
    
    # Allocate memory
    mat_a = <double*>malloc(m * n * sizeof(double))
    mat_b = <double*>malloc(n * p * sizeof(double))
    mat_c = <double*>malloc(m * p * sizeof(double))
    
    if not mat_a or not mat_b or not mat_c:
        if mat_a: free(mat_a)
        if mat_b: free(mat_b)
        if mat_c: free(mat_c)
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy input data
        for i in range(m * n):
            mat_a[i] = <double>data_a[i]
        for i in range(n * p):
            mat_b[i] = <double>data_b[i]
        if data_c is not None:
            for i in range(m * p):
                mat_c[i] = <double>data_c[i]
        else:
            memset(mat_c, 0, m * p * sizeof(double))
        
        # GEMM operation
        for i in range(m):
            for j in range(p):
                sum_val = 0.0
                for k in range(n):
                    sum_val += mat_a[i * n + k] * mat_b[k * p + j]
                mat_c[i * p + j] = alpha * sum_val + beta * mat_c[i * p + j]
        
        # Copy result back
        result_list = [mat_c[i] for i in range(m * p)]
        return result_list, (m, p)
    
    finally:
        free(mat_a)
        free(mat_b)
        free(mat_c)