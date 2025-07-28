"""
Array creation examples for ArrPy - showcasing all array creation functions
"""

from arrpy import Array, array, zeros, ones, empty, full, eye, identity, arange, linspace, logspace

def basic_creation_examples():
    """Demonstrate basic array creation methods"""
    print("=== Basic Array Creation ===")
    
    # Using Array constructor
    arr1 = Array([1, 2, 3, 4, 5])
    print(f"Array constructor: {arr1}")
    
    # Using array() convenience function (NumPy-style)
    arr2 = array([1, 2, 3, 4, 5])
    print(f"array() function: {arr2}")
    
    # 2D array creation
    arr_2d = array([[1, 2, 3], [4, 5, 6]])
    print(f"2D array: {arr_2d}")
    print()

def zeros_and_ones_examples():
    """Demonstrate zeros and ones creation functions"""
    print("=== Zeros and Ones Creation ===")
    
    # 1D zeros
    zeros_1d = zeros(5)
    print(f"zeros(5): {zeros_1d}")
    
    # 2D zeros
    zeros_2d = zeros((3, 4))
    print(f"zeros((3, 4)):")
    print(f"{zeros_2d}")
    
    # 1D ones
    ones_1d = ones(4)
    print(f"ones(4): {ones_1d}")
    
    # 2D ones
    ones_2d = ones((2, 5))
    print(f"ones((2, 5)):")
    print(f"{ones_2d}")
    
    # 3D zeros
    zeros_3d = zeros((2, 2, 2))
    print(f"zeros((2, 2, 2)):")
    print(f"{zeros_3d}")
    print()

def full_and_empty_examples():
    """Demonstrate full and empty array creation"""
    print("=== Full and Empty Array Creation ===")
    
    # Full arrays with specific values
    full_1d = full(4, 7)
    print(f"full(4, 7): {full_1d}")
    
    full_2d = full((2, 3), 3.14)
    print(f"full((2, 3), 3.14):")
    print(f"{full_2d}")
    
    full_custom = full((3, 2), -1)
    print(f"full((3, 2), -1):")
    print(f"{full_custom}")
    
    # Empty arrays (initialized with zeros for safety)
    empty_1d = empty(3)
    print(f"empty(3): {empty_1d}")
    
    empty_2d = empty((2, 2))
    print(f"empty((2, 2)):")
    print(f"{empty_2d}")
    print()

def identity_matrices_examples():
    """Demonstrate identity matrix creation"""
    print("=== Identity Matrix Creation ===")
    
    # Square identity matrices
    id_2x2 = identity(2)
    print(f"identity(2):")
    print(f"{id_2x2}")
    
    id_3x3 = identity(3)
    print(f"identity(3):")
    print(f"{id_3x3}")
    
    # Eye function (more flexible)
    eye_2x2 = eye(2)
    print(f"eye(2):")
    print(f"{eye_2x2}")
    
    # Rectangular identity-like matrices
    eye_2x4 = eye(2, 4)
    print(f"eye(2, 4):")
    print(f"{eye_2x4}")
    
    eye_3x2 = eye(3, 2)
    print(f"eye(3, 2):")
    print(f"{eye_3x2}")
    
    # Identity with diagonal offset
    eye_offset = eye(4, k=1)
    print(f"eye(4, k=1) (diagonal offset):")
    print(f"{eye_offset}")
    print()

def range_based_creation():
    """Demonstrate range-based array creation"""
    print("=== Range-Based Array Creation ===")
    
    # arange - similar to Python's range
    arange_basic = arange(5)
    print(f"arange(5): {arange_basic}")
    
    arange_start_stop = arange(2, 8)
    print(f"arange(2, 8): {arange_start_stop}")
    
    arange_with_step = arange(0, 10, 2)
    print(f"arange(0, 10, 2): {arange_with_step}")
    
    arange_negative = arange(10, 0, -1)
    print(f"arange(10, 0, -1): {arange_negative}")
    
    # linspace - evenly spaced values
    linspace_basic = linspace(0, 1, 11)
    print(f"linspace(0, 1, 11): {linspace_basic}")
    
    linspace_fewer = linspace(0, 10, 5)
    print(f"linspace(0, 10, 5): {linspace_fewer}")
    
    linspace_negative = linspace(-5, 5, 11)
    print(f"linspace(-5, 5, 11): {linspace_negative}")
    
    # logspace - logarithmically spaced values
    try:
        logspace_basic = logspace(0, 2, 5)
        print(f"logspace(0, 2, 5): {logspace_basic}")
    except Exception as e:
        print(f"logspace note: {e}")
    print()

def shape_demonstration():
    """Demonstrate various shapes and dimensions"""
    print("=== Shape and Dimension Demonstration ===")
    
    # Different shapes using zeros
    shapes = [
        (5,),           # 1D
        (3, 4),         # 2D
        (2, 3, 2),      # 3D
        (2, 2, 2, 2),   # 4D
    ]
    
    for i, shape in enumerate(shapes, 1):
        arr = zeros(shape)
        print(f"{len(shape)}D array shape {shape}:")
        print(f"  Size: {arr.size} elements")
        print(f"  Dimensions: {arr.ndim}")
        print(f"  Array: {arr}")
        print()

def practical_creation_examples():
    """Show practical use cases for array creation"""
    print("=== Practical Array Creation Examples ===")
    
    # Create coordinate grids
    print("Creating coordinate arrays:")
    x_coords = linspace(-2, 2, 5)
    y_coords = linspace(-1, 1, 3)
    print(f"X coordinates: {x_coords}")
    print(f"Y coordinates: {y_coords}")
    
    # Create matrix for linear algebra
    print("\\nCreating matrices for linear algebra:")
    coefficient_matrix = array([[2, 1], [1, 3]])
    constants = array([8, 1])
    print(f"Coefficient matrix: {coefficient_matrix}")
    print(f"Constants vector: {constants}")
    
    # Create lookup tables
    print("\\nCreating lookup table:")
    angles = linspace(0, 6.28, 8)  # 0 to 2π
    print(f"Angle values (radians): {angles}")
    
    # Create identity for matrix operations
    print("\\nCreating identity for matrix operations:")
    I = identity(3)
    A = full((3, 3), 2)
    print(f"Identity matrix I: {I}")
    print(f"Matrix A: {A}")
    
    # Create template arrays
    print("\\nCreating template arrays:")
    template = ones((2, 3))
    scaled_template = template * 5
    print(f"Template: {template}")
    print(f"Scaled template: {scaled_template}")
    print()

def memory_efficient_creation():
    """Demonstrate memory-efficient array creation patterns"""
    print("=== Memory-Efficient Creation Patterns ===")
    
    # Large arrays - show size info
    large_1d = zeros(1000)
    print(f"Large 1D array: shape {large_1d.shape}, {large_1d.size} elements")
    
    large_2d = zeros((50, 20))
    print(f"Large 2D array: shape {large_2d.shape}, {large_2d.size} elements")
    
    # Using arange for large sequences
    sequence = arange(0, 100, 5)
    print(f"Efficient sequence: {sequence}")
    print(f"Sequence length: {len(sequence._data)}")
    
    # Sparse-like patterns using eye
    sparse_like = eye(5, 8)
    print(f"Sparse-like matrix: {sparse_like}")
    print()

def array_creation_performance_tips():
    """Show performance tips for array creation"""
    print("=== Array Creation Performance Tips ===")
    
    print("1. Use specific creation functions instead of nested lists:")
    print("   Good: zeros((100, 100))")
    print("   Avoid: Array([[0] * 100 for _ in range(100)])")
    print()
    
    print("2. Use arange for sequences instead of list comprehensions:")
    print("   Good: arange(1000)")
    print("   Avoid: Array(list(range(1000)))")
    print()
    
    print("3. Use linspace for evenly spaced values:")
    good_example = linspace(0, 10, 11)
    print(f"   Good: linspace(0, 10, 11) = {good_example}")
    print()
    
    print("4. Pre-allocate with zeros/ones, then fill:")
    preallocated = zeros(5)
    for i in range(5):
        preallocated[i] = i * i
    print(f"   Pre-allocated and filled: {preallocated}")
    print()

if __name__ == "__main__":
    basic_creation_examples()
    zeros_and_ones_examples()
    full_and_empty_examples()
    identity_matrices_examples()
    range_based_creation()
    shape_demonstration()
    practical_creation_examples()
    memory_efficient_creation()
    array_creation_performance_tips()
    
    print("=== All array creation examples completed! ===")