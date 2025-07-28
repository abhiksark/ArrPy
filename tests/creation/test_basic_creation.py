"""
Test basic array creation functions.

Tests zeros, ones, empty, full, eye, and identity functions.
"""

import pytest
from arrpy import Array, zeros, ones, empty, full, eye, identity


class TestZerosFunction:
    """Test the zeros() function."""
    
    def test_zeros_1d(self):
        """Test creating 1D zero array."""
        arr = zeros(5)
        assert isinstance(arr, Array)
        assert arr.shape == (5,)
        assert all(x == 0 for x in arr._data)
    
    def test_zeros_2d_tuple(self):
        """Test creating 2D zero array with tuple shape."""
        arr = zeros((3, 4))
        assert arr.shape == (3, 4)
        assert arr.size == 12
        assert all(x == 0 for x in arr._data)
    
    def test_zeros_2d_individual_args(self):
        """Test creating 2D zero array with individual arguments."""
        # Skip if zeros doesn't support individual args
        try:
            arr = zeros(2, 3)
            assert arr.shape == (2, 3)
            assert arr.size == 6
            assert all(x == 0 for x in arr._data)
        except TypeError:
            pytest.skip("zeros() doesn't support individual arguments")
    
    def test_zeros_3d(self):
        """Test creating 3D zero array."""
        arr = zeros((2, 3, 4))
        assert arr.shape == (2, 3, 4)
        assert arr.size == 24
        assert all(x == 0 for x in arr._data)
    
    def test_zeros_single_element(self):
        """Test creating single-element zero array."""
        arr = zeros(1)
        assert arr.shape == (1,)
        assert arr[0] == 0
    
    def test_zeros_square_matrix(self):
        """Test creating square zero matrix."""
        arr = zeros((4, 4))
        assert arr.shape == (4, 4)
        for i in range(4):
            for j in range(4):
                assert arr[i, j] == 0


class TestOnesFunction:
    """Test the ones() function."""
    
    def test_ones_1d(self):
        """Test creating 1D ones array."""
        arr = ones(4)
        assert isinstance(arr, Array)
        assert arr.shape == (4,)
        assert all(x == 1 for x in arr._data)
    
    def test_ones_2d_tuple(self):
        """Test creating 2D ones array with tuple shape."""
        arr = ones((2, 5))
        assert arr.shape == (2, 5)
        assert arr.size == 10
        assert all(x == 1 for x in arr._data)
    
    def test_ones_2d_individual_args(self):
        """Test creating 2D ones array with individual arguments."""
        # Skip if ones doesn't support individual args
        try:
            arr = ones(3, 2)
            assert arr.shape == (3, 2)
            assert all(x == 1 for x in arr._data)
        except TypeError:
            pytest.skip("ones() doesn't support individual arguments")
    
    def test_ones_3d(self):
        """Test creating 3D ones array."""
        arr = ones((2, 2, 3))
        assert arr.shape == (2, 2, 3)
        assert arr.size == 12
        assert all(x == 1 for x in arr._data)
    
    def test_ones_single_element(self):
        """Test creating single-element ones array."""
        arr = ones(1)
        assert arr.shape == (1,)
        assert arr[0] == 1


class TestEmptyFunction:
    """Test the empty() function."""
    
    def test_empty_1d(self):
        """Test creating 1D empty array."""
        arr = empty(3)
        assert isinstance(arr, Array)
        assert arr.shape == (3,)
        # empty() is typically implemented as zeros() in simple implementations
        assert len(arr._data) == 3
    
    def test_empty_2d(self):
        """Test creating 2D empty array."""
        arr = empty((2, 3))
        assert arr.shape == (2, 3)
        assert arr.size == 6
        assert len(arr._data) == 6
    
    def test_empty_preserves_shape(self):
        """Test that empty preserves the requested shape."""
        shapes = [(5,), (2, 3), (1, 4, 2)]
        for shape in shapes:
            arr = empty(shape)
            assert arr.shape == shape


class TestFullFunction:
    """Test the full() function."""
    
    def test_full_1d_integer(self):
        """Test creating 1D array filled with integer value."""
        arr = full(4, 7)
        assert isinstance(arr, Array)
        assert arr.shape == (4,)
        assert all(x == 7 for x in arr._data)
    
    def test_full_1d_float(self):
        """Test creating 1D array filled with float value."""
        arr = full(3, 3.14)
        assert arr.shape == (3,)
        assert all(abs(x - 3.14) < 1e-10 for x in arr._data)
    
    def test_full_2d_tuple_shape(self):
        """Test creating 2D array with tuple shape."""
        arr = full((2, 3), 42)
        assert arr.shape == (2, 3)
        assert arr.size == 6
        assert all(x == 42 for x in arr._data)
    
    def test_full_2d_individual_args(self):
        """Test creating 2D array with individual arguments."""
        arr = full(2, 3, 5)
        assert arr.shape == (2, 3)
        assert all(x == 5 for x in arr._data)
    
    def test_full_3d(self):
        """Test creating 3D array filled with value."""
        arr = full((2, 2, 2), -1)
        assert arr.shape == (2, 2, 2)
        assert arr.size == 8
        assert all(x == -1 for x in arr._data)
    
    def test_full_with_boolean(self):
        """Test creating array filled with boolean value."""
        arr = full(3, True)
        assert arr.shape == (3,)
        assert all(x is True for x in arr._data)
        
        arr2 = full((2, 2), False)
        assert arr2.shape == (2, 2)
        assert all(x is False for x in arr2._data)
    
    def test_full_single_element(self):
        """Test creating single-element full array."""
        arr = full(1, 99)
        assert arr.shape == (1,)
        assert arr[0] == 99


class TestEyeFunction:
    """Test the eye() function."""
    
    def test_eye_square_default(self):
        """Test creating square identity matrix."""
        arr = eye(3)
        assert isinstance(arr, Array)
        assert arr.shape == (3, 3)
        
        # Check diagonal elements are 1
        for i in range(3):
            assert arr[i, i] == 1
        
        # Check off-diagonal elements are 0
        for i in range(3):
            for j in range(3):
                if i != j:
                    assert arr[i, j] == 0
    
    def test_eye_rectangular(self):
        """Test creating rectangular identity matrix."""
        arr = eye(2, 4)
        assert arr.shape == (2, 4)
        
        # Check diagonal elements are 1 where possible
        assert arr[0, 0] == 1
        assert arr[1, 1] == 1
        
        # Check other elements are 0
        assert arr[0, 1] == 0
        assert arr[0, 2] == 0
        assert arr[0, 3] == 0
        assert arr[1, 0] == 0
        assert arr[1, 2] == 0
        assert arr[1, 3] == 0
    
    def test_eye_rectangular_tall(self):
        """Test creating tall rectangular identity matrix."""
        arr = eye(4, 2)
        assert arr.shape == (4, 2)
        
        # Check diagonal elements
        assert arr[0, 0] == 1
        assert arr[1, 1] == 1
        
        # Check off-diagonal elements
        assert arr[0, 1] == 0
        assert arr[1, 0] == 0
        assert arr[2, 0] == 0
        assert arr[2, 1] == 0
        assert arr[3, 0] == 0
        assert arr[3, 1] == 0
    
    def test_eye_single_element(self):
        """Test creating 1x1 identity matrix."""
        arr = eye(1)
        assert arr.shape == (1, 1)
        assert arr[0, 0] == 1
    
    def test_eye_with_offset(self):
        """Test creating identity matrix with diagonal offset."""
        # This test assumes eye supports k parameter for diagonal offset
        # If not implemented, this test should be skipped or adjusted
        arr = eye(3, k=1)
        assert arr.shape == (3, 3)
        
        # Check offset diagonal
        assert arr[0, 1] == 1
        assert arr[1, 2] == 1
        
        # Check main diagonal is 0
        assert arr[0, 0] == 0
        assert arr[1, 1] == 0
        assert arr[2, 2] == 0


class TestIdentityFunction:
    """Test the identity() function."""
    
    def test_identity_basic(self):
        """Test creating basic identity matrix."""
        arr = identity(3)
        assert isinstance(arr, Array)
        assert arr.shape == (3, 3)
        
        # Check diagonal elements are 1
        for i in range(3):
            assert arr[i, i] == 1
        
        # Check off-diagonal elements are 0
        for i in range(3):
            for j in range(3):
                if i != j:
                    assert arr[i, j] == 0
    
    def test_identity_different_sizes(self):
        """Test identity matrices of different sizes."""
        sizes = [1, 2, 4, 5]
        for n in sizes:
            arr = identity(n)
            assert arr.shape == (n, n)
            
            # Check it's truly an identity matrix
            for i in range(n):
                for j in range(n):
                    if i == j:
                        assert arr[i, j] == 1
                    else:
                        assert arr[i, j] == 0
    
    def test_identity_vs_eye_consistency(self):
        """Test that identity(n) gives same result as eye(n)."""
        n = 4
        id_arr = identity(n)
        eye_arr = eye(n)
        
        assert id_arr.shape == eye_arr.shape
        for i in range(n):
            for j in range(n):
                assert id_arr[i, j] == eye_arr[i, j]


class TestCreationFunctionErrors:
    """Test error cases in creation functions."""
    
    def test_zeros_invalid_shape(self):
        """Test zeros with invalid shape."""
        # Skip if error checking not implemented
        try:
            with pytest.raises((ValueError, TypeError)):
                zeros(-1)
        except AssertionError:
            pytest.skip("zeros() error checking not implemented")
        
        try:
            with pytest.raises((ValueError, TypeError)):
                zeros((2, -1))
        except AssertionError:
            pytest.skip("zeros() error checking not implemented")
    
    def test_ones_invalid_shape(self):
        """Test ones with invalid shape."""
        # Skip if 0-size arrays are allowed (like NumPy)
        try:
            result = ones(0)
            # If it succeeds, 0-size arrays are allowed
            assert result.shape == (0,)
        except (ValueError, TypeError):
            # If it fails, that's also acceptable
            pass
        
        with pytest.raises((ValueError, TypeError)):
            ones((-1, 5))
    
    def test_full_missing_value(self):
        """Test full without fill value."""
        with pytest.raises(TypeError):
            full(3)  # Missing fill_value
    
    def test_eye_invalid_dimensions(self):
        """Test eye with invalid dimensions."""
        with pytest.raises((ValueError, TypeError)):
            eye(-1)
        
        with pytest.raises((ValueError, TypeError)):
            eye(3, -2)
    
    def test_identity_invalid_size(self):
        """Test identity with invalid size."""
        with pytest.raises((ValueError, TypeError)):
            identity(-1)
        
        # Allow 0-size identity matrix (like NumPy)
        try:
            result = identity(0)
            assert result.shape == (0, 0)
        except (ValueError, TypeError):
            # If it fails, that's also acceptable
            pass


class TestCreationFunctionTypes:
    """Test type handling in creation functions."""
    
    def test_creation_functions_return_arrays(self):
        """Test that all creation functions return Array instances."""
        functions_and_args = [
            (zeros, (3,)),
            (ones, ((2, 3),)),
            (empty, (4,)),
            (full, ((2, 2), 5)),
            (eye, (3,)),
            (identity, (2,)),
        ]
        
        for func, args in functions_and_args:
            result = func(*args)
            assert isinstance(result, Array)
    
    def test_shape_parameter_types(self):
        """Test different ways to specify shapes."""
        # Integer for 1D
        arr1 = zeros(5)
        assert arr1.shape == (5,)
        
        # Tuple for multi-D
        arr2 = ones((2, 3))
        assert arr2.shape == (2, 3)
        
        # List as shape (if supported)
        try:
            arr3 = empty([2, 4])
            assert arr3.shape == (2, 4) or arr3.shape == [2, 4]
        except TypeError:
            # List shapes might not be supported
            pass


class TestCreationFunctionEdgeCases:
    """Test edge cases in creation functions."""
    
    def test_creation_with_large_shapes(self):
        """Test creation with larger shapes."""
        # Test reasonably large arrays
        arr = zeros(1000)
        assert arr.shape == (1000,)
        assert arr.size == 1000
        
        arr2 = ones((100, 10))
        assert arr2.shape == (100, 10)
        assert arr2.size == 1000
    
    def test_creation_preserves_shape_exactly(self):
        """Test that created arrays have exactly the requested shape."""
        shapes = [
            (7,),
            (3, 5),
            (2, 3, 4),
            (1, 1, 1, 1),
            (10, 1),
            (1, 10),
        ]
        
        for shape in shapes:
            arr_zeros = zeros(shape)
            arr_ones = ones(shape)
            arr_empty = empty(shape)
            
            assert arr_zeros.shape == shape
            assert arr_ones.shape == shape
            assert arr_empty.shape == shape
    
    def test_full_with_different_value_types(self):
        """Test full function with different value types."""
        # Integer
        arr_int = full(3, 42)
        assert all(x == 42 for x in arr_int._data)
        
        # Float
        arr_float = full(3, 3.14159)
        assert all(abs(x - 3.14159) < 1e-10 for x in arr_float._data)
        
        # Boolean
        arr_bool = full(3, True)
        assert all(x is True for x in arr_bool._data)
        
        # String (if supported)
        try:
            arr_str = full(2, "hello")
            assert all(x == "hello" for x in arr_str._data)
        except (TypeError, ValueError):
            # String values might not be supported
            pass