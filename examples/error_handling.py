"""
Error handling examples for arrypy - demonstrating various error conditions
and how to handle them gracefully
"""

from arrypy import Array

def initialization_errors():
    """Demonstrate initialization error handling"""
    print("=== Initialization Error Handling ===")
    
    # Valid initialization
    try:
        valid_array = Array([[1, 2], [3, 4]])
        print(f"Valid array created: {valid_array}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    # Ragged array error
    print("\nTesting ragged array:")
    try:
        ragged_array = Array([[1, 2, 3], [4, 5]])  # Different row lengths
        print(f"This shouldn't print: {ragged_array}")
    except ValueError as e:
        print(f"✓ Caught expected ValueError: {e}")
    except Exception as e:
        print(f"✗ Unexpected error type: {type(e).__name__}: {e}")
    
    # Invalid input type
    print("\nTesting invalid input type:")
    try:
        invalid_array = Array("not a list")
        print(f"This shouldn't print: {invalid_array}")
    except TypeError as e:
        print(f"✓ Caught expected TypeError: {e}")
    except Exception as e:
        print(f"✗ Unexpected error type: {type(e).__name__}: {e}")
    
    print()

def indexing_errors():
    """Demonstrate indexing error handling"""
    print("=== Indexing Error Handling ===")
    
    arr = Array([[1, 2, 3], [4, 5, 6]])
    print(f"Working with array: {arr}")
    
    # Valid indexing
    try:
        value = arr[0, 1]
        print(f"Valid indexing arr[0, 1]: {value}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    # Index out of bounds
    print("\nTesting index out of bounds:")
    try:
        value = arr[5, 0]  # Row 5 doesn't exist
        print(f"This shouldn't print: {value}")
    except IndexError as e:
        print(f"✓ Caught expected IndexError: {e}")
    except Exception as e:
        print(f"✗ Unexpected error type: {type(e).__name__}: {e}")
    
    # Wrong number of indices
    print("\nTesting wrong number of indices:")
    try:
        value = arr[0, 1, 2]  # Too many indices for 2D array
        print(f"This shouldn't print: {value}")
    except IndexError as e:
        print(f"✓ Caught expected IndexError: {e}")
    except Exception as e:
        print(f"✗ Unexpected error type: {type(e).__name__}: {e}")
    
    print()

def arithmetic_errors():
    """Demonstrate arithmetic operation error handling"""
    print("=== Arithmetic Error Handling ===")
    
    arr1 = Array([1, 2, 3])
    arr2 = Array([4, 5])  # Different size
    
    print(f"Array 1: {arr1}")
    print(f"Array 2: {arr2}")
    
    # Valid arithmetic
    try:
        result = arr1 + 10  # Scalar addition
        print(f"Valid scalar addition: {result}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    # Shape mismatch error
    print("\nTesting shape mismatch:")
    try:
        result = arr1 + arr2  # Different shapes
        print(f"This shouldn't print: {result}")
    except ValueError as e:
        print(f"✓ Caught expected ValueError: {e}")
    except Exception as e:
        print(f"✗ Unexpected error type: {type(e).__name__}: {e}")
    
    # Division by zero (with scalar)
    print("\nTesting division by zero:")
    try:
        result = arr1 / 0
        print(f"Result: {result}")  # This might actually work but produce inf
    except ZeroDivisionError as e:
        print(f"✓ Caught expected ZeroDivisionError: {e}")
    except Exception as e:
        print(f"Other error: {type(e).__name__}: {e}")
    
    print()

def reshape_errors():
    """Demonstrate reshape error handling"""
    print("=== Reshape Error Handling ===")
    
    arr = Array([1, 2, 3, 4, 5, 6])
    print(f"Original array: {arr}")
    print(f"Shape: {arr.shape}, Size: {len(arr._data)}")
    
    # Valid reshape
    try:
        reshaped = arr.reshape((2, 3))
        print(f"Valid reshape to (2, 3): {reshaped}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    # Invalid reshape - incompatible size
    print("\nTesting incompatible reshape:")
    try:
        invalid_reshape = arr.reshape((2, 4))  # 2*4=8, but array has 6 elements
        print(f"This shouldn't print: {invalid_reshape}")
    except ValueError as e:
        print(f"✓ Caught expected ValueError: {e}")
    except Exception as e:
        print(f"✗ Unexpected error type: {type(e).__name__}: {e}")
    
    print()

def transpose_errors():
    """Demonstrate transpose error handling"""
    print("=== Transpose Error Handling ===")
    
    # Valid 2D transpose
    arr_2d = Array([[1, 2, 3], [4, 5, 6]])
    try:
        transposed = arr_2d.T
        print(f"Valid 2D transpose: {transposed}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    # Invalid 1D transpose
    print("\nTesting 1D array transpose:")
    arr_1d = Array([1, 2, 3])
    try:
        invalid_transpose = arr_1d.T
        print(f"This shouldn't print: {invalid_transpose}")
    except ValueError as e:
        print(f"✓ Caught expected ValueError: {e}")
    except Exception as e:
        print(f"✗ Unexpected error type: {type(e).__name__}: {e}")
    
    # Invalid 3D transpose
    print("\nTesting 3D array transpose:")
    arr_3d = Array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
    try:
        invalid_transpose = arr_3d.T
        print(f"This shouldn't print: {invalid_transpose}")
    except ValueError as e:
        print(f"✓ Caught expected ValueError: {e}")
    except Exception as e:
        print(f"✗ Unexpected error type: {type(e).__name__}: {e}")
    
    print()

def dot_product_errors():
    """Demonstrate dot product error handling"""
    print("=== Dot Product Error Handling ===")
    
    # Valid dot product
    arr1 = Array([[1, 2], [3, 4]])
    arr2 = Array([[5, 6], [7, 8]])
    try:
        result = arr1.dot(arr2)
        print(f"Valid dot product: {result}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    # Incompatible shapes
    print("\nTesting incompatible shapes:")
    arr3 = Array([[1, 2, 3]])  # 1x3
    arr4 = Array([[1, 2]])     # 1x2
    try:
        invalid_dot = arr3.dot(arr4)
        print(f"This shouldn't print: {invalid_dot}")
    except ValueError as e:
        print(f"✓ Caught expected ValueError: {e}")
    except Exception as e:
        print(f"✗ Unexpected error type: {type(e).__name__}: {e}")
    
    # Non-Array type
    print("\nTesting dot product with non-Array:")
    try:
        invalid_dot = arr1.dot([[1, 2], [3, 4]])  # Regular list, not Array
        print(f"This shouldn't print: {invalid_dot}")
    except TypeError as e:
        print(f"✓ Caught expected TypeError: {e}")
    except Exception as e:
        print(f"✗ Unexpected error type: {type(e).__name__}: {e}")
    
    # Non-2D arrays
    print("\nTesting dot product with 1D arrays:")
    arr_1d_1 = Array([1, 2, 3])
    arr_1d_2 = Array([4, 5, 6])
    try:
        invalid_dot = arr_1d_1.dot(arr_1d_2)
        print(f"This shouldn't print: {invalid_dot}")
    except ValueError as e:
        print(f"✓ Caught expected ValueError: {e}")
    except Exception as e:
        print(f"✗ Unexpected error type: {type(e).__name__}: {e}")
    
    print()

def aggregation_errors():
    """Demonstrate aggregation error handling"""
    print("=== Aggregation Error Handling ===")
    
    # Valid aggregations
    arr = Array([1, 2, 3, 4, 5])
    try:
        total = arr.sum()
        average = arr.mean()
        print(f"Valid aggregations - Sum: {total}, Mean: {average}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    # Empty array mean
    print("\nTesting mean of empty array:")
    empty_arr = Array([])
    try:
        empty_mean = empty_arr.mean()
        print(f"This shouldn't print: {empty_mean}")
    except ValueError as e:
        print(f"✓ Caught expected ValueError: {e}")
    except Exception as e:
        print(f"✗ Unexpected error type: {type(e).__name__}: {e}")
    
    # Empty array sum (this should work and return 0)
    print("\nTesting sum of empty array:")
    try:
        empty_sum = empty_arr.sum()
        print(f"Sum of empty array: {empty_sum}")
    except Exception as e:
        print(f"Error with empty sum: {type(e).__name__}: {e}")
    
    print()

def comprehensive_error_handling_example():
    """A comprehensive example showing defensive programming"""
    print("=== Comprehensive Error Handling Example ===")
    
    def safe_matrix_operation(data1, data2, operation="add"):
        """Safely perform matrix operations with comprehensive error checking"""
        try:
            # Create arrays
            arr1 = Array(data1)
            arr2 = Array(data2)
            
            print(f"Array 1: {arr1}")
            print(f"Array 2: {arr2}")
            
            # Perform operation based on parameter
            if operation == "add":
                result = arr1 + arr2
                print(f"Addition result: {result}")
            elif operation == "multiply":
                result = arr1 * arr2
                print(f"Multiplication result: {result}")
            elif operation == "dot":
                result = arr1.dot(arr2)
                print(f"Dot product result: {result}")
            else:
                print(f"Unknown operation: {operation}")
                return None
            
            return result
            
        except ValueError as e:
            print(f"ValueError occurred: {e}")
            return None
        except TypeError as e:
            print(f"TypeError occurred: {e}")
            return None
        except IndexError as e:
            print(f"IndexError occurred: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error occurred: {type(e).__name__}: {e}")
            return None
    
    # Test with valid data
    print("Testing with valid data:")
    safe_matrix_operation([[1, 2], [3, 4]], [[5, 6], [7, 8]], "add")
    print()
    
    # Test with invalid shapes
    print("Testing with mismatched shapes:")
    safe_matrix_operation([1, 2, 3], [4, 5], "add")
    print()
    
    # Test with ragged data
    print("Testing with ragged arrays:")
    safe_matrix_operation([[1, 2], [3, 4, 5]], [[1, 2], [3, 4]], "add")
    print()

if __name__ == "__main__":
    initialization_errors()
    indexing_errors()
    arithmetic_errors()
    reshape_errors()
    transpose_errors()
    dot_product_errors()
    aggregation_errors()
    comprehensive_error_handling_example()
    
    print("=== All error handling examples completed! ===")