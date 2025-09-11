"""
Linear algebra operations for Python backend.

Pure Python implementations of matrix operations.
"""


def _matmul_python(data1, data2, shape1, shape2):
    """
    Pure Python matrix multiplication - clear but slow.
    
    This is the textbook algorithm with O(n³) complexity.
    
    Parameters
    ----------
    data1, data2 : list
        Flattened array data
    shape1, shape2 : tuple
        Shapes of the arrays (must be compatible for matmul)
        
    Returns
    -------
    tuple
        (result_data, result_shape)
    """
    # Check shape compatibility
    if len(shape1) != 2 or len(shape2) != 2:
        raise ValueError("matmul requires 2D arrays")
    
    m, k1 = shape1
    k2, n = shape2
    
    if k1 != k2:
        raise ValueError(f"Incompatible shapes for matmul: {shape1} and {shape2}")
    
    k = k1  # Inner dimension
    
    # Initialize result
    result = []
    
    # Textbook matrix multiplication
    for i in range(m):
        for j in range(n):
            sum_val = 0
            for idx in range(k):
                # data1[i, idx] = data1[i * k + idx]
                # data2[idx, j] = data2[idx * n + j]
                sum_val += data1[i * k + idx] * data2[idx * n + j]
            result.append(sum_val)
    
    return result, (m, n)


def _dot_python(data1, data2, shape1, shape2):
    """
    Pure Python dot product.
    
    Handles 1D and 2D arrays.
    
    Parameters
    ----------
    data1, data2 : list
        Flattened array data
    shape1, shape2 : tuple
        Shapes of the arrays
        
    Returns
    -------
    tuple
        (result_data, result_shape)
    """
    # 1D dot product
    if len(shape1) == 1 and len(shape2) == 1:
        if shape1[0] != shape2[0]:
            raise ValueError(f"Incompatible shapes for dot: {shape1} and {shape2}")
        
        result = 0
        for i in range(shape1[0]):
            result += data1[i] * data2[i]
        
        return [result], ()  # Scalar result
    
    # 2D: same as matmul
    elif len(shape1) == 2 and len(shape2) == 2:
        return _matmul_python(data1, data2, shape1, shape2)
    
    # 1D x 2D
    elif len(shape1) == 1 and len(shape2) == 2:
        if shape1[0] != shape2[0]:
            raise ValueError(f"Incompatible shapes for dot: {shape1} and {shape2}")
        
        m, n = shape2
        result = []
        
        for j in range(n):
            sum_val = 0
            for i in range(m):
                sum_val += data1[i] * data2[i * n + j]
            result.append(sum_val)
        
        return result, (n,)
    
    # 2D x 1D
    elif len(shape1) == 2 and len(shape2) == 1:
        m, n = shape1
        if n != shape2[0]:
            raise ValueError(f"Incompatible shapes for dot: {shape1} and {shape2}")
        
        result = []
        
        for i in range(m):
            sum_val = 0
            for j in range(n):
                sum_val += data1[i * n + j] * data2[j]
            result.append(sum_val)
        
        return result, (m,)
    
    else:
        raise ValueError(f"Unsupported shapes for dot: {shape1} and {shape2}")


def _inner_python(data1, data2, shape1, shape2):
    """
    Pure Python inner product.
    
    For 1D arrays, this is the same as dot product.
    
    Parameters
    ----------
    data1, data2 : list
        Flattened array data
    shape1, shape2 : tuple
        Shapes of the arrays
        
    Returns
    -------
    tuple
        (result_data, result_shape)
    """
    # For 1D arrays, inner is same as dot
    if len(shape1) == 1 and len(shape2) == 1:
        return _dot_python(data1, data2, shape1, shape2)
    
    # For higher dimensions, more complex
    # For now, just handle 1D case
    raise NotImplementedError("inner product only implemented for 1D arrays")


def _outer_python(data1, data2, shape1, shape2):
    """
    Pure Python outer product.
    
    Computes the outer product of two vectors.
    
    Parameters
    ----------
    data1, data2 : list
        Flattened array data (must be 1D)
    shape1, shape2 : tuple
        Shapes of the arrays (must be 1D)
        
    Returns
    -------
    tuple
        (result_data, result_shape)
    """
    # Check that inputs are 1D
    if len(shape1) != 1 or len(shape2) != 1:
        raise ValueError("outer product requires 1D arrays")
    
    m = shape1[0]
    n = shape2[0]
    
    result = []
    
    # Outer product: result[i,j] = data1[i] * data2[j]
    for i in range(m):
        for j in range(n):
            result.append(data1[i] * data2[j])
    
    return result, (m, n)