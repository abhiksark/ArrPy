"""
Basic usage examples for arrypy Array class
"""

from arrypy import Array

def basic_array_creation():
    """Demonstrate basic array creation and properties"""
    print("=== Basic Array Creation ===")
    
    # 1D array
    arr1d = Array([1, 2, 3, 4, 5])
    print(f"1D Array: {arr1d}")
    print(f"Shape: {arr1d.shape}")
    print()
    
    # 2D array
    arr2d = Array([[1, 2, 3], [4, 5, 6]])
    print(f"2D Array: {arr2d}")
    print(f"Shape: {arr2d.shape}")
    print()
    
    # 3D array
    arr3d = Array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
    print(f"3D Array: {arr3d}")
    print(f"Shape: {arr3d.shape}")
    print()

def indexing_examples():
    """Demonstrate indexing capabilities"""
    print("=== Indexing Examples ===")
    
    arr = Array([[10, 20, 30], [40, 50, 60], [70, 80, 90]])
    print(f"Original array: {arr}")
    
    # Single element access
    print(f"Element at [0, 0]: {arr[0, 0]}")
    print(f"Element at [1, 2]: {arr[1, 2]}")
    print(f"Element at [2, 1]: {arr[2, 1]}")
    
    # Row access
    row = arr[1]
    print(f"Second row: {row}")
    
    # Element modification
    arr[0, 1] = 99
    print(f"After modifying [0, 1] to 99: {arr}")
    print()

def arithmetic_operations():
    """Demonstrate arithmetic operations"""
    print("=== Arithmetic Operations ===")
    
    arr1 = Array([1, 2, 3, 4])
    arr2 = Array([10, 20, 30, 40])
    
    print(f"Array 1: {arr1}")
    print(f"Array 2: {arr2}")
    
    # Scalar operations
    print(f"arr1 + 5: {arr1 + 5}")
    print(f"arr1 * 3: {arr1 * 3}")
    print(f"arr2 / 10: {arr2 / 10}")
    
    # Array operations
    print(f"arr1 + arr2: {arr1 + arr2}")
    print(f"arr2 - arr1: {arr2 - arr1}")
    print(f"arr1 * arr2: {arr1 * arr2}")
    print()

def matrix_operations():
    """Demonstrate matrix operations"""
    print("=== Matrix Operations ===")
    
    # Matrix multiplication
    matrix1 = Array([[1, 2], [3, 4]])
    matrix2 = Array([[5, 6], [7, 8]])
    
    print(f"Matrix 1: {matrix1}")
    print(f"Matrix 2: {matrix2}")
    
    result = matrix1.dot(matrix2)
    print(f"Matrix multiplication result: {result}")
    
    # Transpose
    print(f"Matrix 1 transpose: {matrix1.T}")
    print(f"Matrix 2 transpose: {matrix2.T}")
    print()

def reshape_examples():
    """Demonstrate reshape functionality"""
    print("=== Reshape Examples ===")
    
    # Create 1D array and reshape to 2D
    arr = Array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    print(f"Original 1D array: {arr}")
    print(f"Shape: {arr.shape}")
    
    # Reshape to different 2D configurations
    reshaped_3x4 = arr.reshape((3, 4))
    print(f"Reshaped to 3x4: {reshaped_3x4}")
    
    reshaped_2x6 = arr.reshape((2, 6))
    print(f"Reshaped to 2x6: {reshaped_2x6}")
    
    reshaped_4x3 = arr.reshape((4, 3))
    print(f"Reshaped to 4x3: {reshaped_4x3}")
    
    # Reshape back to 1D
    back_to_1d = reshaped_3x4.reshape((12,))
    print(f"Back to 1D: {back_to_1d}")
    print()

def aggregation_examples():
    """Demonstrate aggregation functions"""
    print("=== Aggregation Examples ===")
    
    arr1d = Array([1, 2, 3, 4, 5])
    arr2d = Array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    
    print(f"1D Array: {arr1d}")
    print(f"Sum: {arr1d.sum()}")
    print(f"Mean: {arr1d.mean()}")
    
    print(f"2D Array: {arr2d}")
    print(f"Sum: {arr2d.sum()}")
    print(f"Mean: {arr2d.mean()}")
    print()

if __name__ == "__main__":
    basic_array_creation()
    indexing_examples()
    arithmetic_operations()
    matrix_operations()
    reshape_examples()
    aggregation_examples()
    
    print("=== All examples completed successfully! ===")