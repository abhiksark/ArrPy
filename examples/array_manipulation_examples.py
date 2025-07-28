"""
Array manipulation examples for ArrPy - showcasing concatenation, stacking, and reshaping
"""

from arrpy import (
    Array, array, zeros, ones, arange, eye,
    # Array manipulation functions
    reshape, transpose, squeeze, expand_dims,
    concatenate, stack, vstack, hstack
)

def concatenation_basics():
    """Demonstrate basic array concatenation"""
    print("=== Basic Array Concatenation ===")
    
    # 1D array concatenation
    arr1 = array([1, 2, 3])
    arr2 = array([4, 5, 6])
    arr3 = array([7, 8, 9])
    
    print(f"Array 1: {arr1}")
    print(f"Array 2: {arr2}")
    print(f"Array 3: {arr3}")
    
    # Concatenate two arrays
    concat_2 = concatenate([arr1, arr2])
    print(f"Concatenate arr1 + arr2: {concat_2}")
    
    # Concatenate multiple arrays
    concat_3 = concatenate([arr1, arr2, arr3])
    print(f"Concatenate all three: {concat_3}")
    
    # Using hstack for 1D (same as concatenate)
    hstack_result = hstack([arr1, arr2])
    print(f"hstack arr1 + arr2: {hstack_result}")
    print()

def two_dimensional_concatenation():
    """Demonstrate 2D array concatenation along different axes"""
    print("=== 2D Array Concatenation ===")
    
    # Create sample 2D arrays
    mat1 = array([[1, 2], [3, 4]])
    mat2 = array([[5, 6], [7, 8]])
    mat3 = array([[9, 10]])
    
    print(f"Matrix 1 (2x2): {mat1}")
    print(f"Matrix 2 (2x2): {mat2}")
    print(f"Matrix 3 (1x2): {mat3}")
    
    # Concatenate along axis 0 (rows)
    concat_axis0 = concatenate([mat1, mat2], axis=0)
    print(f"\\nConcatenate along axis 0 (stack rows):")
    print(f"{concat_axis0}")
    
    # Concatenate along axis 1 (columns)
    concat_axis1 = concatenate([mat1, mat2], axis=1)
    print(f"\\nConcatenate along axis 1 (stack columns):")
    print(f"{concat_axis1}")
    
    # Add a row using axis 0
    with_new_row = concatenate([mat1, mat3], axis=0)
    print(f"\\nAdd new row to matrix:")
    print(f"{with_new_row}")
    print()

def stacking_operations():
    """Demonstrate different stacking operations"""
    print("=== Stacking Operations ===")
    
    # Create arrays for stacking
    row1 = array([1, 2, 3])
    row2 = array([4, 5, 6])
    row3 = array([7, 8, 9])
    
    print(f"Row 1: {row1}")
    print(f"Row 2: {row2}")
    print(f"Row 3: {row3}")
    
    # Vertical stacking (vstack)
    vstacked = vstack([row1, row2, row3])
    print(f"\\nVertical stack (vstack):")
    print(f"{vstacked}")
    
    # Create column vectors for horizontal stacking
    col1 = array([[1], [4], [7]])
    col2 = array([[2], [5], [8]])
    col3 = array([[3], [6], [9]])
    
    print(f"\\nColumn 1: {col1}")
    print(f"Column 2: {col2}")
    print(f"Column 3: {col3}")
    
    # Horizontal stacking (hstack)
    hstacked = hstack([col1, col2, col3])
    print(f"\\nHorizontal stack (hstack):")
    print(f"{hstacked}")
    print()

def advanced_stacking():
    """Demonstrate advanced stacking with stack function"""
    print("=== Advanced Stacking with stack() ===")
    
    # Create arrays for stacking
    arr1 = array([[1, 2], [3, 4]])
    arr2 = array([[5, 6], [7, 8]])
    arr3 = array([[9, 10], [11, 12]])
    
    print(f"Array 1: {arr1}")
    print(f"Array 2: {arr2}")
    print(f"Array 3: {arr3}")
    
    try:
        # Stack along new axis (axis=0)
        stacked_axis0 = stack([arr1, arr2, arr3], axis=0)
        print(f"\\nStack along axis 0 (creates 3D array):")
        print(f"Shape: {stacked_axis0.shape}")
        print(f"{stacked_axis0}")
        
        # Stack along different axis
        stacked_axis1 = stack([arr1, arr2, arr3], axis=1)
        print(f"\\nStack along axis 1:")
        print(f"Shape: {stacked_axis1.shape}")
        print(f"{stacked_axis1}")
        
    except Exception as e:
        print(f"Note: stack() function may not be fully implemented: {e}")
    print()

def reshape_operations():
    """Demonstrate array reshaping operations"""
    print("=== Array Reshaping Operations ===")
    
    # Create a 1D array
    arr_1d = arange(12)
    print(f"Original 1D array: {arr_1d}")
    print(f"Shape: {arr_1d.shape}")
    
    # Reshape to different 2D configurations
    arr_2x6 = reshape(arr_1d, (2, 6))
    print(f"\\nReshape to (2, 6):")
    print(f"{arr_2x6}")
    
    arr_3x4 = reshape(arr_1d, (3, 4))
    print(f"\\nReshape to (3, 4):")
    print(f"{arr_3x4}")
    
    arr_4x3 = reshape(arr_1d, (4, 3))
    print(f"\\nReshape to (4, 3):")
    print(f"{arr_4x3}")
    
    # Reshape back to 1D
    back_to_1d = reshape(arr_3x4, (12,))
    print(f"\\nReshape back to 1D: {back_to_1d}")
    
    # Using method vs function
    method_reshape = arr_1d.reshape((6, 2))
    function_reshape = reshape(arr_1d, (6, 2))
    print(f"\\nMethod vs function (should be identical):")
    print(f"arr.reshape((6, 2)): {method_reshape}")
    print(f"reshape(arr, (6, 2)): {function_reshape}")
    print()

def transpose_operations():
    """Demonstrate transpose operations"""
    print("=== Transpose Operations ===")
    
    # Create matrices for transposition
    rectangular = array([[1, 2, 3], [4, 5, 6]])
    square = array([[1, 2], [3, 4]])
    
    print(f"Rectangular matrix (2x3): {rectangular}")
    print(f"Square matrix (2x2): {square}")
    
    # Transpose using property
    rect_T = rectangular.T
    square_T = square.T
    
    print(f"\\nRectangular transpose (3x2): {rect_T}")
    print(f"Square transpose (2x2): {square_T}")
    
    # Transpose using function
    try:
        func_transpose = transpose(rectangular)
        print(f"\\nUsing transpose function: {func_transpose}")
    except Exception as e:
        print(f"Note: transpose() function behavior: {e}")
    
    # Verify transpose properties
    print(f"\\nTranspose verification:")
    print(f"Original [0,1]: {rectangular[0, 1]}")
    print(f"Transpose [1,0]: {rect_T[1, 0]}")
    print(f"Values match: {rectangular[0, 1] == rect_T[1, 0]}")
    print()

def dimension_manipulation():
    """Demonstrate dimension manipulation (squeeze, expand_dims)"""
    print("=== Dimension Manipulation ===")
    
    # Create arrays with different dimensions
    arr_1d = array([1, 2, 3, 4])
    arr_2d_row = array([[1, 2, 3, 4]])  # 1x4
    arr_2d_col = array([[1], [2], [3], [4]])  # 4x1
    
    print(f"1D array: {arr_1d}, shape: {arr_1d.shape}")
    print(f"2D row: {arr_2d_row}, shape: {arr_2d_row.shape}")
    print(f"2D col: {arr_2d_col}, shape: {arr_2d_col.shape}")
    
    # Try squeeze and expand_dims (if implemented)
    try:
        # Squeeze - remove dimensions of size 1
        squeezed_row = squeeze(arr_2d_row)
        squeezed_col = squeeze(arr_2d_col)
        
        print(f"\\nSqueezed row: {squeezed_row}, shape: {squeezed_row.shape}")
        print(f"Squeezed col: {squeezed_col}, shape: {squeezed_col.shape}")
        
    except Exception as e:
        print(f"\\nNote: squeeze() function: {e}")
    
    try:
        # Expand dims - add new dimensions
        expanded_0 = expand_dims(arr_1d, axis=0)
        expanded_1 = expand_dims(arr_1d, axis=1)
        
        print(f"\\nExpand dims axis 0: {expanded_0}, shape: {expanded_0.shape}")
        print(f"Expand dims axis 1: {expanded_1}, shape: {expanded_1.shape}")
        
    except Exception as e:
        print(f"\\nNote: expand_dims() function: {e}")
    print()

def practical_manipulation_examples():
    """Show practical examples of array manipulation"""
    print("=== Practical Array Manipulation Examples ===")
    
    # Example 1: Building datasets
    print("1. Building datasets from separate components:")
    
    # Separate data columns
    ids = array([1, 2, 3, 4])
    names_encoded = array([10, 20, 30, 40])  # Encoded names
    scores = array([85, 92, 78, 96])
    
    print(f"   IDs: {ids}")
    print(f"   Name codes: {names_encoded}")
    print(f"   Scores: {scores}")
    
    # Stack into dataset (transpose to get columns)
    try:
        dataset = vstack([ids, names_encoded, scores])
        print(f"   Combined dataset:")
        print(f"   {dataset}")
        print(f"   Shape: {dataset.shape} (3 features x 4 samples)")
    except Exception as e:
        print(f"   Note: {e}")
    
    # Example 2: Matrix operations
    print("\\n2. Matrix operations:")
    
    # Create coefficient matrix and constants for linear system
    A_parts = [
        array([2, 1]),
        array([1, 3])
    ]
    A = vstack(A_parts)
    b = array([8, 1])
    
    print(f"   Coefficient matrix A:")
    print(f"   {A}")
    print(f"   Constants vector b: {b}")
    
    # Example 3: Time series data
    print("\\n3. Time series concatenation:")
    
    jan_data = array([100, 110, 105])
    feb_data = array([120, 115, 125])
    mar_data = array([130, 135, 140])
    
    # Combine monthly data
    q1_data = concatenate([jan_data, feb_data, mar_data])
    print(f"   Jan: {jan_data}")
    print(f"   Feb: {feb_data}")
    print(f"   Mar: {mar_data}")
    print(f"   Q1 combined: {q1_data}")
    print(f"   Q1 length: {len(q1_data._data)} data points")
    print()

def manipulation_performance_tips():
    """Show performance tips for array manipulation"""
    print("=== Array Manipulation Performance Tips ===")
    
    print("1. Concatenation efficiency:")
    print("   Good: concatenate([arr1, arr2, arr3])  # Single operation")
    print("   Avoid: concatenate(concatenate([arr1, arr2]), arr3)  # Multiple operations")
    print()
    
    print("2. Pre-allocate when possible:")
    # Demonstrate pre-allocation
    result_size = 15
    preallocated = zeros(result_size)
    
    # Fill in sections
    arr1 = array([1, 2, 3, 4, 5])
    arr2 = array([6, 7, 8, 9, 10])
    
    # Manual copying (simplified example)
    for i in range(5):
        preallocated[i] = arr1[i]
        preallocated[i + 5] = arr2[i]
    
    print(f"   Pre-allocated result: {preallocated}")
    print()
    
    print("3. Reshape vs recreation:")
    original = arange(12)
    print(f"   Original: {original}")
    
    # Efficient: reshape
    reshaped = original.reshape((3, 4))
    print(f"   Reshaped (efficient): shape {reshaped.shape}")
    
    # Less efficient: recreating
    print("   Avoid recreating arrays when reshape suffices")
    print()
    
    print("4. Choose appropriate stacking:")
    print("   - Use vstack for row-wise combination")
    print("   - Use hstack for column-wise combination") 
    print("   - Use concatenate with axis parameter for control")
    print()

def error_handling_manipulation():
    """Demonstrate error handling in array manipulation"""
    print("=== Error Handling in Array Manipulation ===")
    
    # Shape mismatch in concatenation
    print("1. Shape mismatch errors:")
    arr1 = array([1, 2, 3])
    arr2 = array([[4, 5]])
    
    try:
        invalid_concat = concatenate([arr1, arr2])
        print(f"   This shouldn't work: {invalid_concat}")
    except Exception as e:
        print(f"   ✓ Caught expected error: {type(e).__name__}")
    
    # Invalid reshape
    print("\\n2. Invalid reshape:")
    arr = array([1, 2, 3, 4, 5])  # 5 elements
    
    try:
        invalid_reshape = reshape(arr, (2, 3))  # Needs 6 elements
        print(f"   This shouldn't work: {invalid_reshape}")
    except Exception as e:
        print(f"   ✓ Caught expected error: {type(e).__name__}")
    
    # Empty array concatenation
    print("\\n3. Empty array handling:")
    try:
        empty_concat = concatenate([])
        print(f"   Empty concatenation: {empty_concat}")
    except Exception as e:
        print(f"   ✓ Caught expected error: {type(e).__name__}")
    
    print()

if __name__ == "__main__":
    concatenation_basics()
    two_dimensional_concatenation()
    stacking_operations()
    advanced_stacking()
    reshape_operations()
    transpose_operations()
    dimension_manipulation()
    practical_manipulation_examples()
    manipulation_performance_tips()
    error_handling_manipulation()
    
    print("=== All array manipulation examples completed! ===")