"""
Cython-optimized array operations using memoryviews.
Works directly with array.array for zero-copy operations.
"""

import cython
import array
from libc.math cimport sqrt, sin, cos, exp, log

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _add_cython(data1, data2, shape1, shape2):
    """
    Optimized addition using typed memoryviews.
    Zero-copy operation on array.array objects.
    """
    cdef:
        double[:] view1
        double[:] view2
        double[:] result_view
        Py_ssize_t i, n
    
    # Python variable for result
    result = None
    
    # Handle array.array with memoryviews
    if isinstance(data1, array.array) and isinstance(data2, array.array):
        # Get typed memoryviews (zero-copy)
        view1 = data1
        view2 = data2
        n = len(data1)
        
        # Create result array
        result = array.array('d', [0.0] * n)
        result_view = result
        
        # Parallel addition with OpenMP if available
        with nogil:
            for i in range(n):
                result_view[i] = view1[i] + view2[i]
        
        return result, shape1
    else:
        # Fallback for lists
        n = len(data1)
        result = []
        for i in range(n):
            result.append(data1[i] + data2[i])
        return result, shape1


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _subtract_cython(data1, data2, shape1, shape2):
    """
    Optimized subtraction using typed memoryviews.
    """
    cdef:
        double[:] view1
        double[:] view2
        double[:] result_view
        Py_ssize_t i, n
    
    result = None
    
    if isinstance(data1, array.array) and isinstance(data2, array.array):
        view1 = data1
        view2 = data2
        n = len(data1)
        
        result = array.array('d', [0.0] * n)
        result_view = result
        
        with nogil:
            for i in range(n):
                result_view[i] = view1[i] - view2[i]
        
        return result, shape1
    else:
        n = len(data1)
        result = []
        for i in range(n):
            result.append(data1[i] - data2[i])
        return result, shape1


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _multiply_cython(data1, data2, shape1, shape2):
    """
    Optimized multiplication for both scalar and element-wise.
    Handles array.array and scalar multiplication.
    """
    cdef:
        double[:] view1
        double[:] view2
        double[:] result_view
        Py_ssize_t i, n
        double scalar
        bint is_scalar
    
    result = None
    
    # Check if data2 is a scalar
    is_scalar = not isinstance(data2, (list, array.array))
    
    if isinstance(data1, array.array):
        view1 = data1
        n = len(data1)
        
        result = array.array('d', [0.0] * n)
        result_view = result
        
        if is_scalar:
            # Scalar multiplication
            scalar = <double>float(data2)
            with nogil:
                for i in range(n):
                    result_view[i] = view1[i] * scalar
        else:
            # Element-wise multiplication
            if isinstance(data2, array.array):
                view2 = data2
                with nogil:
                    for i in range(n):
                        result_view[i] = view1[i] * view2[i]
            else:
                # data2 is a list
                for i in range(n):
                    result_view[i] = view1[i] * data2[i]
        
        return result, shape1
    else:
        # Fallback for lists
        n = len(data1)
        result = []
        
        if is_scalar:
            scalar = float(data2)
            for i in range(n):
                result.append(data1[i] * scalar)
        else:
            for i in range(n):
                result.append(data1[i] * data2[i])
        
        return result, shape1


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _divide_cython(data1, data2, shape1, shape2):
    """
    Optimized division using typed memoryviews.
    """
    cdef:
        double[:] view1
        double[:] view2
        double[:] result_view
        Py_ssize_t i, n
        double val1, val2
    
    result = None
    
    if isinstance(data1, array.array) and isinstance(data2, array.array):
        view1 = data1
        view2 = data2
        n = len(data1)
        
        result = array.array('d', [0.0] * n)
        result_view = result
        
        # Division with zero handling
        for i in range(n):
            val1 = view1[i]
            val2 = view2[i]
            if val2 != 0:
                result_view[i] = val1 / val2
            else:
                if val1 > 0:
                    result_view[i] = float('inf')
                elif val1 < 0:
                    result_view[i] = float('-inf')
                else:
                    result_view[i] = float('nan')
        
        return result, shape1
    else:
        # Fallback for lists
        n = len(data1)
        result = []
        for i in range(n):
            if data2[i] != 0:
                result.append(data1[i] / data2[i])
            else:
                if data1[i] > 0:
                    result.append(float('inf'))
                elif data1[i] < 0:
                    result.append(float('-inf'))
                else:
                    result.append(float('nan'))
        return result, shape1


@cython.boundscheck(False)
@cython.wraparound(False)
def _sum_cython(data, shape):
    """
    Optimized sum reduction using memoryviews.
    """
    cdef:
        double[:] view
        double total = 0.0
        Py_ssize_t i, n
    
    if isinstance(data, array.array):
        view = data
        n = len(data)
        
        with nogil:
            for i in range(n):
                total += view[i]
        
        return total
    else:
        # Fallback for lists
        return sum(data)


@cython.boundscheck(False)
@cython.wraparound(False)
def _mean_cython(data, shape):
    """
    Optimized mean calculation using memoryviews.
    """
    cdef:
        double[:] view
        double total = 0.0
        Py_ssize_t i, n
    
    if isinstance(data, array.array):
        view = data
        n = len(data)
        
        if n == 0:
            return float('nan')
        
        with nogil:
            for i in range(n):
                total += view[i]
        
        return total / n
    else:
        # Fallback for lists
        n = len(data)
        if n == 0:
            return float('nan')
        return sum(data) / n