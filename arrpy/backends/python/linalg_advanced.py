"""
Advanced linear algebra operations for Python backend.
Educational implementations of decompositions and solvers.
"""

import math


def _lu_decomposition_python(data, shape):
    """
    LU decomposition with partial pivoting.
    Returns L, U, and permutation matrix P such that PA = LU.
    
    This is an educational implementation showing the algorithm clearly.
    """
    n = shape[0]
    if shape[0] != shape[1]:
        raise ValueError("LU decomposition requires square matrix")
    
    # Convert flat data to 2D for easier manipulation
    U = [[data[i * n + j] for j in range(n)] for i in range(n)]
    L = [[0.0] * n for _ in range(n)]
    P = list(range(n))  # Permutation vector
    
    # Initialize L as identity
    for i in range(n):
        L[i][i] = 1.0
    
    # Gaussian elimination with partial pivoting
    for k in range(n - 1):
        # Find pivot
        max_val = abs(U[k][k])
        max_row = k
        
        for i in range(k + 1, n):
            if abs(U[i][k]) > max_val:
                max_val = abs(U[i][k])
                max_row = i
        
        # Swap rows in U and P
        if max_row != k:
            U[k], U[max_row] = U[max_row], U[k]
            P[k], P[max_row] = P[max_row], P[k]
            
            # Swap already computed parts of L
            for j in range(k):
                L[k][j], L[max_row][j] = L[max_row][j], L[k][j]
        
        # Check for singular matrix
        if abs(U[k][k]) < 1e-10:
            raise ValueError("Matrix is singular or nearly singular")
        
        # Compute multipliers and eliminate
        for i in range(k + 1, n):
            L[i][k] = U[i][k] / U[k][k]
            for j in range(k + 1, n):
                U[i][j] -= L[i][k] * U[k][j]
            U[i][k] = 0.0
    
    # Convert to flat arrays for consistency
    L_flat = [val for row in L for val in row]
    U_flat = [val for row in U for val in row]
    
    return L_flat, U_flat, P


def _solve_python(A_data, A_shape, b_data, b_shape):
    """
    Solve linear system Ax = b using LU decomposition.
    
    Educational implementation showing forward and backward substitution.
    """
    n = A_shape[0]
    if A_shape[0] != A_shape[1]:
        raise ValueError("Matrix must be square")
    
    # Handle both 1D and 2D b
    if len(b_shape) == 1:
        if b_shape[0] != n:
            raise ValueError("Incompatible dimensions")
    else:
        if b_shape[0] != n:
            raise ValueError("Incompatible dimensions")
    
    b = b_data[:]
    
    # Perform LU decomposition
    L_flat, U_flat, P = _lu_decomposition_python(A_data, A_shape)
    
    # Convert back to 2D
    L = [[L_flat[i * n + j] for j in range(n)] for i in range(n)]
    U = [[U_flat[i * n + j] for j in range(n)] for i in range(n)]
    
    # Apply permutation to b
    b_perm = [b[P[i]] for i in range(n)]
    
    # Forward substitution: Ly = Pb
    y = [0.0] * n
    for i in range(n):
        y[i] = b_perm[i]
        for j in range(i):
            y[i] -= L[i][j] * y[j]
    
    # Backward substitution: Ux = y
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = y[i]
        for j in range(i + 1, n):
            x[i] -= U[i][j] * x[j]
        x[i] /= U[i][i]
    
    return x, (n, 1)


def _qr_decomposition_python(data, shape):
    """
    QR decomposition using Gram-Schmidt orthogonalization.
    Returns Q (orthogonal) and R (upper triangular) such that A = QR.
    
    Educational implementation of modified Gram-Schmidt for numerical stability.
    """
    m, n = shape
    if m < n:
        raise ValueError("QR decomposition requires m >= n")
    
    # Convert to 2D for easier manipulation
    A = [[data[i * n + j] for j in range(n)] for i in range(m)]
    
    # Initialize Q and R
    Q = [[0.0] * n for _ in range(m)]
    R = [[0.0] * n for _ in range(n)]
    
    # Modified Gram-Schmidt process
    for j in range(n):
        # Copy column j of A to column j of Q
        for i in range(m):
            Q[i][j] = A[i][j]
        
        # Orthogonalize against previous columns
        for k in range(j):
            # Compute dot product
            dot_product = 0.0
            for i in range(m):
                dot_product += Q[i][k] * Q[i][j]
            
            R[k][j] = dot_product
            
            # Subtract projection
            for i in range(m):
                Q[i][j] -= dot_product * Q[i][k]
        
        # Normalize
        norm = 0.0
        for i in range(m):
            norm += Q[i][j] * Q[i][j]
        norm = math.sqrt(norm)
        
        if norm < 1e-10:
            raise ValueError("Matrix has linearly dependent columns")
        
        R[j][j] = norm
        for i in range(m):
            Q[i][j] /= norm
    
    # Convert to flat arrays
    Q_flat = [val for row in Q for val in row]
    R_flat = [val for row in R for val in row]
    
    return Q_flat, R_flat


def _eigenvalues_python(data, shape, max_iter=1000, tol=1e-10):
    """
    Compute eigenvalues using QR algorithm.
    
    Educational implementation of the QR iteration method.
    For symmetric matrices, this converges to eigenvalues on the diagonal.
    """
    n = shape[0]
    if shape[0] != shape[1]:
        raise ValueError("Eigenvalues require square matrix")
    
    # Convert to 2D
    A = [[data[i * n + j] for j in range(n)] for i in range(n)]
    
    # QR iteration
    for iteration in range(max_iter):
        # QR decomposition of A
        A_flat = [val for row in A for val in row]
        Q_flat, R_flat = _qr_decomposition_python(A_flat, shape)
        
        # Convert back to 2D
        Q = [[Q_flat[i * n + j] for j in range(n)] for i in range(n)]
        R = [[R_flat[i * n + j] for j in range(n)] for i in range(n)]
        
        # Form A = RQ for next iteration
        A_new = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    A_new[i][j] += R[i][k] * Q[k][j]
        
        # Check for convergence (lower triangular part should approach zero)
        converged = True
        for i in range(n):
            for j in range(i):
                if abs(A_new[i][j]) > tol:
                    converged = False
                    break
            if not converged:
                break
        
        A = A_new
        
        if converged:
            break
    
    # Extract eigenvalues from diagonal
    eigenvalues = [A[i][i] for i in range(n)]
    
    return eigenvalues, (n,)


def _svd_python(data, shape):
    """
    Singular Value Decomposition (SVD).
    Returns U, S, V such that A = U @ diag(S) @ V.T
    
    Educational implementation using eigenvalue decomposition of A.T @ A.
    """
    m, n = shape
    
    # Convert to 2D
    A = [[data[i * n + j] for j in range(n)] for i in range(m)]
    
    # Compute A.T @ A
    ATA = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(m):
                ATA[i][j] += A[k][i] * A[k][j]
    
    # Get eigenvalues and eigenvectors of A.T @ A
    ATA_flat = [val for row in ATA for val in row]
    eigenvalues, _ = _eigenvalues_python(ATA_flat, (n, n))
    
    # Singular values are square roots of eigenvalues
    singular_values = [math.sqrt(max(0, ev)) for ev in eigenvalues]
    
    # Sort in descending order
    singular_values.sort(reverse=True)
    
    # For educational purposes, return simplified SVD
    # (full implementation would compute U and V matrices)
    return singular_values, (min(m, n),)


def _determinant_python(data, shape):
    """
    Compute determinant using LU decomposition.
    
    det(A) = det(P) * det(L) * det(U) = ±1 * 1 * product(diag(U))
    """
    n = shape[0]
    if shape[0] != shape[1]:
        raise ValueError("Determinant requires square matrix")
    
    try:
        L_flat, U_flat, P = _lu_decomposition_python(data, shape)
    except ValueError:
        # Singular matrix
        return 0.0
    
    # Count permutation swaps for sign
    swaps = 0
    for i in range(n):
        if P[i] != i:
            swaps += 1
    
    # Determinant is product of U diagonal elements
    det = 1.0 if swaps % 2 == 0 else -1.0
    for i in range(n):
        det *= U_flat[i * n + i]
    
    return det


def _matrix_rank_python(data, shape, tol=1e-10):
    """
    Compute matrix rank using SVD.
    
    Rank is the number of non-zero singular values.
    """
    m, n = shape
    
    # Get singular values
    singular_values, _ = _svd_python(data, shape)
    
    # Count non-zero singular values
    rank = sum(1 for sv in singular_values if sv > tol)
    
    return rank


def _cholesky_python(data, shape):
    """
    Cholesky decomposition for positive definite matrices.
    Returns L such that A = L @ L.T
    
    Educational implementation of the Cholesky-Banachiewicz algorithm.
    """
    n = shape[0]
    if shape[0] != shape[1]:
        raise ValueError("Cholesky decomposition requires square matrix")
    
    # Convert to 2D
    A = [[data[i * n + j] for j in range(n)] for i in range(n)]
    
    # Check symmetry
    for i in range(n):
        for j in range(i + 1, n):
            if abs(A[i][j] - A[j][i]) > 1e-10:
                raise ValueError("Matrix must be symmetric")
    
    # Initialize L
    L = [[0.0] * n for _ in range(n)]
    
    # Cholesky-Banachiewicz algorithm
    for i in range(n):
        for j in range(i + 1):
            if i == j:
                # Diagonal elements
                sum_sq = sum(L[i][k] ** 2 for k in range(j))
                val = A[i][i] - sum_sq
                if val <= 0:
                    raise ValueError("Matrix is not positive definite")
                L[i][j] = math.sqrt(val)
            else:
                # Off-diagonal elements
                sum_prod = sum(L[i][k] * L[j][k] for k in range(j))
                L[i][j] = (A[i][j] - sum_prod) / L[j][j]
    
    # Convert to flat array
    L_flat = [val for row in L for val in row]
    
    return L_flat, shape