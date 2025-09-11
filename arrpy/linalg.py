"""
Linear algebra operations for arrpy arrays.
"""


def dot(a, b):
    """
    Dot product of two arrays.
    
    Parameters
    ----------
    a : arrpy
        First array
    b : arrpy
        Second array
    
    Returns
    -------
    arrpy or scalar
        Dot product
    """
    from .arrpy_backend import ArrPy
    from .backend_selector import get_backend, Backend
    import array
    
    # Handle 1D x 1D -> scalar (simple enough to not need backend dispatch)
    if a.ndim == 1 and b.ndim == 1:
        if a.shape[0] != b.shape[0]:
            raise ValueError(f"Shapes {a.shape} and {b.shape} not aligned")
        
        result = 0
        for i in range(a.shape[0]):
            result += a._data[i] * b._data[i]
        return result
    
    # Handle 2D x 1D -> 1D
    if a.ndim == 2 and b.ndim == 1:
        if a.shape[1] != b.shape[0]:
            raise ValueError(f"Shapes {a.shape} and {b.shape} not aligned")
        
        # Use matrix multiplication with b reshaped to column vector
        b_col = b.reshape(-1, 1)
        result = dot(a, b_col)
        return result.reshape(-1)
    
    # Handle 1D x 2D -> 1D  
    if a.ndim == 1 and b.ndim == 2:
        if a.shape[0] != b.shape[0]:
            raise ValueError(f"Shapes {a.shape} and {b.shape} not aligned")
        
        # Use matrix multiplication with a reshaped to row vector
        a_row = a.reshape(1, -1)
        result = dot(a_row, b)
        return result.reshape(-1)
    
    # Handle 2D x 2D -> 2D (matrix multiplication) with backend dispatch
    if a.ndim == 2 and b.ndim == 2:
        if a.shape[1] != b.shape[0]:
            raise ValueError(f"Shapes {a.shape} and {b.shape} not aligned: {a.shape[1]} != {b.shape[0]}")
        
        backend = get_backend()
        
        # Dispatch to appropriate backend
        if backend == Backend.PYTHON:
            from .backends.python.linalg_ops import _matmul_python
            result_data, result_shape = _matmul_python(a._data, b._data, a._shape, b._shape)
        elif backend == Backend.CYTHON:
            try:
                from .backends.cython.linalg_ops import _matmul_cython
                result_data, result_shape = _matmul_cython(a._data, b._data, a._shape, b._shape)
            except (ImportError, AttributeError):
                # Fallback to Python if Cython not available
                from .backends.python.linalg_ops import _matmul_python
                result_data, result_shape = _matmul_python(a._data, b._data, a._shape, b._shape)
        elif backend == Backend.C:
            try:
                from .backends.c.linalg_ops import _matmul_c
                result_data, result_shape = _matmul_c(a._data, b._data, a._shape, b._shape)
            except (ImportError, AttributeError):
                # Fallback to Python if C not available
                from .backends.python.linalg_ops import _matmul_python
                result_data, result_shape = _matmul_python(a._data, b._data, a._shape, b._shape)
        else:
            from .backends.python.linalg_ops import _matmul_python
            result_data, result_shape = _matmul_python(a._data, b._data, a._shape, b._shape)
        
        # Convert result_data to array.array if it's a list
        if isinstance(result_data, list):
            result_data = array.array('d', result_data)
        
        m, _ = a.shape
        _, n = b.shape
        
        result = ArrPy.__new__(ArrPy)
        result._data = result_data
        result._shape = (m, n)
        result._size = m * n
        result._dtype = a._dtype
        result._strides = result._calculate_strides((m, n))
        return result
    
    # For higher dimensions
    raise NotImplementedError(f"Dot product not implemented for shapes {a.shape} and {b.shape}")


def matmul(a, b):
    """
    Matrix multiplication of two arrays.
    
    Parameters
    ----------
    a : arrpy
        First array (at least 1D)
    b : arrpy
        Second array (at least 1D)
    
    Returns
    -------
    arrpy
        Matrix product
    """
    from .arrpy_backend import ArrPy
    
    # Handle 1D cases by promoting to 2D
    a_is_1d = a.ndim == 1
    b_is_1d = b.ndim == 1
    
    if a_is_1d:
        a = a.reshape(1, -1)
    if b_is_1d:
        b = b.reshape(-1, 1)
    
    # Use dot for the actual computation
    result = dot(a, b)
    
    # Squeeze out added dimensions
    if a_is_1d and b_is_1d:
        # Both were 1D, return scalar
        return result._data[0]
    elif a_is_1d:
        # a was 1D, squeeze first dimension
        result = result.reshape(-1)
    elif b_is_1d:
        # b was 1D, squeeze last dimension
        result = result.reshape(-1)
    
    return result


def transpose(a, axes=None):
    """
    Transpose an array.
    
    Parameters
    ----------
    a : arrpy
        Input array
    axes : tuple of ints, optional
        Permutation of axes
    
    Returns
    -------
    arrpy
        Transposed array
    """
    if axes is None:
        return a.transpose()
    else:
        return a.transpose(axes)


def inner(a, b):
    """
    Inner product of two arrays.
    
    Parameters
    ----------
    a : arrpy
        First array
    b : arrpy
        Second array
    
    Returns
    -------
    arrpy or scalar
        Inner product
    """
    # For 1D arrays, this is the same as dot
    if a.ndim == 1 and b.ndim == 1:
        return dot(a, b)
    
    # For higher dimensions, sum product over last axes
    raise NotImplementedError("Inner product for multi-dimensional arrays not yet implemented")


def outer(a, b):
    """
    Outer product of two arrays.
    
    Parameters
    ----------
    a : arrpy
        First array (1D)
    b : arrpy
        Second array (1D)
    
    Returns
    -------
    arrpy
        Outer product (2D)
    """
    from .arrpy_backend import ArrPy
    
    # Flatten inputs to 1D
    a_flat = a.flatten()
    b_flat = b.flatten()
    
    # Compute outer product
    result_data = []
    for a_val in a_flat._data:
        for b_val in b_flat._data:
            result_data.append(a_val * b_val)
    
    result = ArrPy.__new__(ArrPy)
    result._data = result_data
    result._shape = (a_flat.shape[0], b_flat.shape[0])
    result._size = a_flat.shape[0] * b_flat.shape[0]
    result._dtype = a._dtype
    result._strides = result._calculate_strides(result._shape)
    
    return result


def trace(a, offset=0):
    """
    Return the sum along the diagonal.
    
    Parameters
    ----------
    a : arrpy
        Input array (at least 2D)
    offset : int, optional
        Diagonal offset
    
    Returns
    -------
    scalar or arrpy
        Sum along diagonal
    """
    if a.ndim < 2:
        raise ValueError("Trace requires at least 2D array")
    
    rows, cols = a.shape[0], a.shape[1]
    
    # Calculate diagonal indices
    if offset >= 0:
        i_start = 0
        j_start = offset
        diag_len = min(rows, cols - offset)
    else:
        i_start = -offset
        j_start = 0
        diag_len = min(rows + offset, cols)
    
    if diag_len <= 0:
        return 0
    
    # Sum diagonal elements
    trace_sum = 0
    for k in range(diag_len):
        i = i_start + k
        j = j_start + k
        trace_sum += a._data[i * cols + j]
    
    return trace_sum


def solve(a, b):
    """
    Solve linear system Ax = b.
    
    Parameters
    ----------
    a : arrpy
        Coefficient matrix (must be square)
    b : arrpy
        Right-hand side
    
    Returns
    -------
    arrpy
        Solution vector x
    """
    from .backend_selector import get_backend, Backend
    from .arrpy_backend import ArrPy
    
    if a.ndim != 2 or a.shape[0] != a.shape[1]:
        raise ValueError("solve requires square 2D coefficient matrix")
    
    if b.ndim == 1:
        if b.shape[0] != a.shape[0]:
            raise ValueError("Incompatible dimensions")
        b_shape = b._shape
        b_data = b._data
    elif b.ndim == 2:
        if b.shape[0] != a.shape[0]:
            raise ValueError("Incompatible dimensions")
        # For multiple RHS, handle first column for now
        b_shape = (b.shape[0], 1)
        b_data = [b._data[i * b.shape[1]] for i in range(b.shape[0])]
    else:
        raise ValueError("b must be 1D or 2D")
    
    backend = get_backend()
    
    if backend == Backend.PYTHON:
        from .backends.python.linalg_advanced import _solve_python
        result_data, shape = _solve_python(a._data, a._shape, b_data, b_shape)
    else:
        # Fallback to Python
        from .backends.python.linalg_advanced import _solve_python
        result_data, shape = _solve_python(a._data, a._shape, b_data, b_shape)
    
    result = ArrPy.__new__(ArrPy)
    result._data = result_data
    result._shape = shape
    result._size = len(result_data)
    result._dtype = a._dtype
    result._strides = result._calculate_strides(shape)
    
    # Reshape to match input b dimensions
    if b.ndim == 1:
        result = result.flatten()
    
    return result


def inv(a):
    """
    Compute matrix inverse.
    
    Parameters
    ----------
    a : arrpy
        Input matrix (must be square)
    
    Returns
    -------
    arrpy
        Inverse matrix
    """
    from .creation import eye
    
    if a.ndim != 2 or a.shape[0] != a.shape[1]:
        raise ValueError("inv requires square matrix")
    
    n = a.shape[0]
    
    # Solve AX = I to get X = A^(-1)
    identity = eye(n)
    
    # Solve for each column of identity matrix
    inv_cols = []
    for j in range(n):
        # Extract jth column of identity
        col = [identity._data[i * n + j] for i in range(n)]
        
        # Create column vector
        from .arrpy_backend import ArrPy
        b = ArrPy.__new__(ArrPy)
        b._data = col
        b._shape = (n,)
        b._size = n
        b._dtype = a._dtype
        b._strides = (1,)
        
        # Solve for this column
        x = solve(a, b)
        inv_cols.append(x._data)
    
    # Combine columns into inverse matrix
    inv_data = []
    for i in range(n):
        for j in range(n):
            inv_data.append(inv_cols[j][i])
    
    result = ArrPy.__new__(ArrPy)
    result._data = inv_data
    result._shape = (n, n)
    result._size = n * n
    result._dtype = a._dtype
    result._strides = result._calculate_strides((n, n))
    
    return result


def det(a):
    """
    Compute determinant of a matrix.
    
    Parameters
    ----------
    a : arrpy
        Input matrix (must be square)
    
    Returns
    -------
    scalar
        Determinant
    """
    from .backend_selector import get_backend, Backend
    
    if a.ndim != 2 or a.shape[0] != a.shape[1]:
        raise ValueError("Determinant requires square matrix")
    
    backend = get_backend()
    
    if backend == Backend.PYTHON:
        from .backends.python.linalg_advanced import _determinant_python
        return _determinant_python(a._data, a._shape)
    else:
        from .backends.python.linalg_advanced import _determinant_python
        return _determinant_python(a._data, a._shape)


def eig(a):
    """
    Compute eigenvalues and eigenvectors.
    
    Parameters
    ----------
    a : arrpy
        Input matrix (must be square)
    
    Returns
    -------
    eigenvalues : arrpy
        Array of eigenvalues
    eigenvectors : arrpy
        Matrix of eigenvectors (columns)
    """
    from .backend_selector import get_backend, Backend
    from .arrpy_backend import ArrPy
    
    if a.ndim != 2 or a.shape[0] != a.shape[1]:
        raise ValueError("Eigendecomposition requires square matrix")
    
    backend = get_backend()
    
    if backend == Backend.PYTHON:
        from .backends.python.linalg_advanced import _eigenvalues_python
        eigenvals, shape = _eigenvalues_python(a._data, a._shape)
    else:
        from .backends.python.linalg_advanced import _eigenvalues_python
        eigenvals, shape = _eigenvalues_python(a._data, a._shape)
    
    # Create eigenvalue array
    result = ArrPy.__new__(ArrPy)
    result._data = eigenvals
    result._shape = shape
    result._size = len(eigenvals)
    result._dtype = a._dtype
    result._strides = result._calculate_strides(shape)
    
    # For now, return only eigenvalues
    # Full eigenvector computation would require more complex algorithm
    return result


def svd(a, full_matrices=True):
    """
    Singular Value Decomposition.
    
    Parameters
    ----------
    a : arrpy
        Input matrix
    full_matrices : bool, optional
        If True, compute full U and V matrices
    
    Returns
    -------
    s : arrpy
        Singular values in descending order
    """
    from .backend_selector import get_backend, Backend
    from .arrpy_backend import ArrPy
    
    if a.ndim != 2:
        raise ValueError("SVD requires 2D matrix")
    
    backend = get_backend()
    
    if backend == Backend.PYTHON:
        from .backends.python.linalg_advanced import _svd_python
        singular_vals, shape = _svd_python(a._data, a._shape)
    else:
        from .backends.python.linalg_advanced import _svd_python
        singular_vals, shape = _svd_python(a._data, a._shape)
    
    # Create singular value array
    result = ArrPy.__new__(ArrPy)
    result._data = singular_vals
    result._shape = shape
    result._size = len(singular_vals)
    result._dtype = a._dtype
    result._strides = result._calculate_strides(shape)
    
    return result


def qr(a):
    """
    QR decomposition.
    
    Parameters
    ----------
    a : arrpy
        Input matrix
    
    Returns
    -------
    q : arrpy
        Orthogonal matrix
    r : arrpy
        Upper triangular matrix
    """
    from .backend_selector import get_backend, Backend
    from .arrpy_backend import ArrPy
    
    if a.ndim != 2:
        raise ValueError("QR decomposition requires 2D matrix")
    
    backend = get_backend()
    
    if backend == Backend.PYTHON:
        from .backends.python.linalg_advanced import _qr_decomposition_python
        q_data, r_data = _qr_decomposition_python(a._data, a._shape)
    else:
        from .backends.python.linalg_advanced import _qr_decomposition_python
        q_data, r_data = _qr_decomposition_python(a._data, a._shape)
    
    m, n = a._shape
    
    # Create Q matrix
    q = ArrPy.__new__(ArrPy)
    q._data = q_data
    q._shape = (m, n)
    q._size = m * n
    q._dtype = a._dtype
    q._strides = q._calculate_strides((m, n))
    
    # Create R matrix
    r = ArrPy.__new__(ArrPy)
    r._data = r_data
    r._shape = (n, n)
    r._size = n * n
    r._dtype = a._dtype
    r._strides = r._calculate_strides((n, n))
    
    return q, r


def cholesky(a):
    """
    Cholesky decomposition.
    
    Parameters
    ----------
    a : arrpy
        Positive definite matrix
    
    Returns
    -------
    arrpy
        Lower triangular matrix L such that a = L @ L.T
    """
    from .backend_selector import get_backend, Backend
    from .arrpy_backend import ArrPy
    
    if a.ndim != 2 or a.shape[0] != a.shape[1]:
        raise ValueError("Cholesky decomposition requires square matrix")
    
    backend = get_backend()
    
    if backend == Backend.PYTHON:
        from .backends.python.linalg_advanced import _cholesky_python
        l_data, shape = _cholesky_python(a._data, a._shape)
    else:
        from .backends.python.linalg_advanced import _cholesky_python
        l_data, shape = _cholesky_python(a._data, a._shape)
    
    # Create L matrix
    result = ArrPy.__new__(ArrPy)
    result._data = l_data
    result._shape = shape
    result._size = len(l_data)
    result._dtype = a._dtype
    result._strides = result._calculate_strides(shape)
    
    return result


def matrix_rank(a, tol=None):
    """
    Compute matrix rank.
    
    Parameters
    ----------
    a : arrpy
        Input matrix
    tol : float, optional
        Tolerance for considering singular values as zero
    
    Returns
    -------
    int
        Matrix rank
    """
    from .backend_selector import get_backend, Backend
    
    if a.ndim != 2:
        raise ValueError("Matrix rank requires 2D matrix")
    
    if tol is None:
        tol = 1e-10
    
    backend = get_backend()
    
    if backend == Backend.PYTHON:
        from .backends.python.linalg_advanced import _matrix_rank_python
        return _matrix_rank_python(a._data, a._shape, tol)
    else:
        from .backends.python.linalg_advanced import _matrix_rank_python
        return _matrix_rank_python(a._data, a._shape, tol)