"""
Advanced matrix operations examples using arrpy
"""

from arrpy import Array, array, zeros, ones, eye, concatenate, vstack, hstack

def linear_algebra_examples():
    """Demonstrate linear algebra operations"""
    print("=== Linear Algebra Examples ===")
    
    # Create matrices
    A = Array([[2, 1], [1, 3]])
    B = Array([[4, 2], [1, 5]])
    
    print(f"Matrix A: {A}")
    print(f"Matrix B: {B}")
    
    # Matrix multiplication
    AB = A.dot(B)
    BA = B.dot(A)
    print(f"A × B = {AB}")
    print(f"B × A = {BA}")
    print(f"Note: Matrix multiplication is not commutative (A×B ≠ B×A)")
    print()
    
    # Transpose operations
    print(f"A^T (A transpose): {A.T}")
    print(f"B^T (B transpose): {B.T}")
    print()

def matrix_chain_operations():
    """Demonstrate chaining matrix operations"""
    print("=== Matrix Chain Operations ===")
    
    # Create a matrix
    M = Array([[1, 2, 3], [4, 5, 6]])
    print(f"Original matrix M (2×3): {M}")
    
    # Transpose and multiply
    MT = M.T
    print(f"M^T (3×2): {MT}")
    
    # M^T × M (should be 3×3)
    MTM = MT.dot(M)
    print(f"M^T × M (3×3): {MTM}")
    
    # M × M^T (should be 2×2)
    MMT = M.dot(MT)
    print(f"M × M^T (2×2): {MMT}")
    print()

def identity_like_operations():
    """Demonstrate operations with identity-like matrices"""
    print("=== Identity-like Operations ===")
    
    # Create an identity-like matrix
    I = Array([[1, 0], [0, 1]])
    A = Array([[3, 4], [5, 6]])
    
    print(f"Identity matrix I: {I}")
    print(f"Matrix A: {A}")
    
    # Multiply with identity
    AI = A.dot(I)
    IA = I.dot(A)
    
    print(f"A × I = {AI}")
    print(f"I × A = {IA}")
    print("Note: Multiplying by identity matrix leaves the matrix unchanged")
    print()

def matrix_powers():
    """Demonstrate matrix powers using repeated multiplication"""
    print("=== Matrix Powers ===")
    
    A = Array([[2, 1], [0, 2]])
    print(f"Matrix A: {A}")
    
    # A^2 = A × A
    A2 = A.dot(A)
    print(f"A^2 = A × A = {A2}")
    
    # A^3 = A^2 × A
    A3 = A2.dot(A)
    print(f"A^3 = A^2 × A = {A3}")
    print()

def vector_operations():
    """Demonstrate vector operations using 1D arrays reshaped as matrices"""
    print("=== Vector Operations ===")
    
    # Create vectors as column matrices
    v1_data = [1, 2, 3]
    v2_data = [4, 5, 6]
    
    # Reshape to column vectors (3×1)
    v1 = Array([[1], [2], [3]])
    v2 = Array([[4], [5], [6]])
    
    print(f"Vector v1 (column): {v1}")
    print(f"Vector v2 (column): {v2}")
    
    # Dot product using transpose: v1^T × v2
    dot_product = v1.T.dot(v2)
    print(f"Dot product v1^T × v2: {dot_product}")
    
    # Outer product: v1 × v2^T
    outer_product = v1.dot(v2.T)
    print(f"Outer product v1 × v2^T: {outer_product}")
    print()

def transformation_matrices():
    """Demonstrate 2D transformation matrices"""
    print("=== 2D Transformation Matrices ===")
    
    # Point to transform
    point = Array([[2], [3]])  # Point (2, 3)
    print(f"Original point: {point}")
    
    # Scaling transformation (scale by 2 in x, 1.5 in y)
    scale_matrix = Array([[2, 0], [0, 1.5]])
    scaled_point = scale_matrix.dot(point)
    print(f"After scaling by (2, 1.5): {scaled_point}")
    
    # Rotation by 90 degrees counterclockwise
    rotation_90 = Array([[0, -1], [1, 0]])
    rotated_point = rotation_90.dot(point)
    print(f"After 90° rotation: {rotated_point}")
    
    # Reflection across y-axis
    reflection_y = Array([[-1, 0], [0, 1]])
    reflected_point = reflection_y.dot(point)
    print(f"After reflection across y-axis: {reflected_point}")
    print()

def system_of_equations_example():
    """Demonstrate representing a system of equations"""
    print("=== System of Equations Representation ===")
    
    # System: 2x + 3y = 8
    #         x - y = 1
    
    # Coefficient matrix
    A = Array([[2, 3], [1, -1]])
    # Constants vector
    b = Array([[8], [1]])
    
    print("System of equations:")
    print("2x + 3y = 8")
    print("x - y = 1")
    print()
    print(f"Coefficient matrix A: {A}")
    print(f"Constants vector b: {b}")
    print("This represents the system Ax = b")
    print("(Note: This example shows representation only - solving requires additional methods)")
    print()

def matrix_construction_examples():
    """Demonstrate matrix construction with zeros, ones, and eye"""
    print("=== Matrix Construction Examples ===")
    
    # Create common matrix types
    zero_matrix = zeros((3, 3))
    ones_matrix = ones((2, 4))
    identity_matrix = eye(3)
    
    print(f"Zero matrix (3x3): {zero_matrix}")
    print(f"Ones matrix (2x4): {ones_matrix}")
    print(f"Identity matrix (3x3): {identity_matrix}")
    
    # Create diagonal matrix with eye offset
    diagonal_matrix = eye(4, k=1)  # Superdiagonal
    print(f"Superdiagonal matrix: {diagonal_matrix}")
    print()

def matrix_concatenation_examples():
    """Demonstrate matrix concatenation and stacking"""
    print("=== Matrix Concatenation Examples ===")
    
    # Create sample matrices
    A = array([[1, 2], [3, 4]])
    B = array([[5, 6], [7, 8]])
    C = array([[9, 10]])
    
    print(f"Matrix A: {A}")
    print(f"Matrix B: {B}")
    print(f"Matrix C: {C}")
    
    # Horizontal stacking (side by side)
    horizontal = hstack([A, B])
    print(f"Horizontal stack [A, B]: {horizontal}")
    
    # Vertical stacking (on top of each other)
    vertical = vstack([A, B])
    print(f"Vertical stack (A on B): {vertical}")
    
    # Add row to matrix
    with_row = vstack([A, C])
    print(f"A with new row C: {with_row}")
    print()

def block_matrix_operations():
    """Demonstrate block matrix construction"""
    print("=== Block Matrix Operations ===")
    
    # Create quadrant matrices
    top_left = array([[1, 2], [3, 4]])
    top_right = array([[5, 6], [7, 8]])
    bottom_left = array([[9, 10], [11, 12]])
    bottom_right = array([[13, 14], [15, 16]])
    
    print(f"Top-left: {top_left}")
    print(f"Top-right: {top_right}")
    print(f"Bottom-left: {bottom_left}")
    print(f"Bottom-right: {bottom_right}")
    
    # Construct block matrix
    top_row = hstack([top_left, top_right])
    bottom_row = hstack([bottom_left, bottom_right])
    block_matrix = vstack([top_row, bottom_row])
    
    print(f"Block matrix (4x4): {block_matrix}")
    print()

if __name__ == "__main__":
    linear_algebra_examples()
    matrix_chain_operations()
    identity_like_operations()
    matrix_powers()
    vector_operations()
    transformation_matrices()
    system_of_equations_example()
    matrix_construction_examples()
    matrix_concatenation_examples()
    block_matrix_operations()
    
    print("=== All matrix operation examples completed! ===")