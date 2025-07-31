"""
Test array creation and initialization.

Tests the Array class constructor and various initialization patterns.
"""

import pytest
import arrpy as ap
from arrpy import Array

# Import helper for type checking that works with hybrid arrays
try:
    from test_imports import is_array
except ImportError:
    def is_array(obj):
        return isinstance(obj, Array)



class TestArrayInitialization:
    """Test Array class initialization."""
    
    def test_1d_list_initialization(self):
        """Test creating 1D array from list."""
        arr = Array([1, 2, 3, 4, 5])
        assert arr.shape == (5,)
        assert arr.ndim == 1
        assert arr.size == 5
        assert list(arr._data) == [1, 2, 3, 4, 5]
    
    def test_2d_list_initialization(self):
        """Test creating 2D array from nested list."""
        arr = Array([[1, 2, 3], [4, 5, 6]])
        assert arr.shape == (2, 3)
        assert arr.ndim == 2
        assert arr.size == 6
        assert arr[0, 0] == 1
        assert arr[1, 2] == 6
    
    def test_3d_list_initialization(self):
        """Test creating 3D array from nested list."""
        data = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
        arr = Array(data)
        assert arr.shape == (2, 2, 2)
        assert arr.ndim == 3
        assert arr.size == 8
        assert arr[0, 0, 0] == 1
        assert arr[1, 1, 1] == 8
    
    def test_empty_list_initialization(self):
        """Test creating array from empty list."""
        arr = Array([])
        assert arr.shape == (0,)
        assert arr.ndim == 1
        assert arr.size == 0
        assert len(arr._data) == 0
    
    def test_single_element_array(self):
        """Test creating array with single element."""
        arr = Array([42])
        assert arr.shape == (1,)
        assert arr.ndim == 1
        assert arr.size == 1
        assert arr[0] == 42
    
    def test_nested_single_element(self):
        """Test creating 2D array with single element."""
        arr = Array([[42]])
        assert arr.shape == (1, 1)
        assert arr.ndim == 2
        assert arr.size == 1
        assert arr[0, 0] == 42
    
    def test_mixed_numeric_types(self):
        """Test creating array with mixed int/float."""
        arr = Array([1, 2.5, 3])
        assert arr.shape == (3,)
        assert arr[0] == 1
        assert arr[1] == 2.5
        assert arr[2] == 3
    
    def test_boolean_array(self):
        """Test creating array with boolean values."""
        arr = Array([True, False, True])
        assert arr.shape == (3,)
        assert arr[0] is True
        assert arr[1] is False
        assert arr[2] is True


class TestArrayInitializationErrors:
    """Test error cases in array initialization."""
    
    def test_ragged_array_error(self):
        """Test that ragged arrays raise ValueError."""
        with pytest.raises(ValueError, match="ragged"):
            Array([[1, 2], [3, 4, 5]])
    
    def test_inconsistent_dimensions_error(self):
        """Test inconsistent nested dimensions."""
        with pytest.raises(ValueError, match="ragged"):
            Array([[[1, 2]], [[3, 4, 5]]])
    
    def test_invalid_input_type_string(self):
        """Test that string input raises TypeError."""
        with pytest.raises(TypeError):
            Array("not a list")
    
    def test_invalid_input_type_number(self):
        """Test that single number input raises TypeError."""
        with pytest.raises(TypeError):
            Array(42)
    
    def test_invalid_input_type_none(self):
        """Test that None input raises TypeError."""
        with pytest.raises(TypeError):
            Array(None)
    
    def test_deeply_nested_inconsistent(self):
        """Test deeply nested inconsistent structure."""
        with pytest.raises(ValueError, match="ragged"):
            Array([[[[1]], [[2, 3]]]])


class TestArrayProperties:
    """Test array properties after creation."""
    
    def test_shape_property_1d(self):
        """Test shape property for 1D array."""
        arr = Array([1, 2, 3, 4])
        assert arr.shape == (4,)
        assert isinstance(arr.shape, tuple)
    
    def test_shape_property_2d(self):
        """Test shape property for 2D array."""
        arr = Array([[1, 2, 3], [4, 5, 6]])
        assert arr.shape == (2, 3)
        assert isinstance(arr.shape, tuple)
    
    def test_shape_property_3d(self):
        """Test shape property for 3D array."""
        arr = Array([[[1, 2]], [[3, 4]]])
        assert arr.shape == (2, 1, 2)
        assert isinstance(arr.shape, tuple)
    
    def test_ndim_property(self):
        """Test ndim property for various dimensions."""
        arr_1d = Array([1, 2, 3])
        arr_2d = Array([[1, 2], [3, 4]])
        arr_3d = Array([[[1]]])
        
        assert arr_1d.ndim == 1
        assert arr_2d.ndim == 2
        assert arr_3d.ndim == 3
    
    def test_size_property(self):
        """Test size property for various shapes."""
        arr_1d = Array([1, 2, 3, 4, 5])
        arr_2d = Array([[1, 2, 3], [4, 5, 6]])
        arr_3d = Array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        
        assert arr_1d.size == 5
        assert arr_2d.size == 6
        assert arr_3d.size == 8
    
    def test_empty_array_properties(self):
        """Test properties of empty array."""
        arr = Array([])
        assert arr.shape == (0,)
        assert arr.ndim == 1
        assert arr.size == 0


class TestArrayDataAccess:
    """Test internal data access patterns."""
    
    def test_flat_data_storage_1d(self):
        """Test that 1D data is stored flat."""
        arr = Array([1, 2, 3, 4])
        assert arr._data == [1, 2, 3, 4]
    
    def test_flat_data_storage_2d(self):
        """Test that 2D data is stored flat (row-major)."""
        arr = Array([[1, 2], [3, 4]])
        assert arr._data == [1, 2, 3, 4]
    
    def test_flat_data_storage_3d(self):
        """Test that 3D data is stored flat (row-major)."""
        arr = Array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        assert arr._data == [1, 2, 3, 4, 5, 6, 7, 8]
    
    def test_data_independence(self):
        """Test that array data is independent of source."""
        source = [1, 2, 3]
        arr = Array(source)
        source[0] = 999
        assert arr[0] == 1  # Array should be unchanged