"""
Test array properties and metadata.

Tests array shape, dimensions, size, and other properties.
"""

import pytest
from arrpy import Array

# Import helper for type checking that works with hybrid arrays
try:
    from test_imports import is_array
except ImportError:
    def is_array(obj):
        return isinstance(obj, Array)



class TestShapeProperty:
    """Test the shape property."""
    
    def test_1d_shape(self):
        """Test shape property for 1D arrays."""
        arr = Array([1, 2, 3, 4, 5])
        assert arr.shape == (5,)
        assert isinstance(arr.shape, tuple)
        assert len(arr.shape) == 1
    
    def test_2d_shape(self):
        """Test shape property for 2D arrays."""
        arr = Array([[1, 2, 3], [4, 5, 6]])
        assert arr.shape == (2, 3)
        assert isinstance(arr.shape, tuple)
        assert len(arr.shape) == 2
    
    def test_3d_shape(self):
        """Test shape property for 3D arrays."""
        arr = Array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        assert arr.shape == (2, 2, 2)
        assert isinstance(arr.shape, tuple)
        assert len(arr.shape) == 3
    
    def test_empty_array_shape(self):
        """Test shape of empty array."""
        arr = Array([])
        assert arr.shape == (0,)
        assert isinstance(arr.shape, tuple)
    
    def test_single_element_shapes(self):
        """Test shapes of single-element arrays."""
        arr_1d = Array([42])
        arr_2d = Array([[42]])
        arr_3d = Array([[[42]]])
        
        assert arr_1d.shape == (1,)
        assert arr_2d.shape == (1, 1)
        assert arr_3d.shape == (1, 1, 1)
    
    def test_irregular_shapes(self):
        """Test various irregular but valid shapes."""
        arr1 = Array([[1], [2], [3]])  # 3x1
        arr2 = Array([[1, 2, 3, 4, 5]])  # 1x5
        
        assert arr1.shape == (3, 1)
        assert arr2.shape == (1, 5)


class TestNdimProperty:
    """Test the ndim (number of dimensions) property."""
    
    def test_ndim_1d(self):
        """Test ndim for 1D arrays."""
        arr = Array([1, 2, 3])
        assert arr.ndim == 1
        assert isinstance(arr.ndim, int)
    
    def test_ndim_2d(self):
        """Test ndim for 2D arrays."""
        arr = Array([[1, 2], [3, 4]])
        assert arr.ndim == 2
        assert isinstance(arr.ndim, int)
    
    def test_ndim_3d(self):
        """Test ndim for 3D arrays."""
        arr = Array([[[1]]])
        assert arr.ndim == 3
        assert isinstance(arr.ndim, int)
    
    def test_ndim_empty_array(self):
        """Test ndim for empty array."""
        arr = Array([])
        assert arr.ndim == 1
    
    def test_ndim_consistency_with_shape(self):
        """Test that ndim equals len(shape)."""
        arrays = [
            Array([1, 2, 3]),
            Array([[1, 2], [3, 4]]),
            Array([[[1, 2]], [[3, 4]]]),
            Array([])
        ]
        
        for arr in arrays:
            assert arr.ndim == len(arr.shape)


class TestSizeProperty:
    """Test the size (total number of elements) property."""
    
    def test_size_1d(self):
        """Test size for 1D arrays."""
        arr = Array([1, 2, 3, 4, 5])
        assert arr.size == 5
        assert isinstance(arr.size, int)
    
    def test_size_2d(self):
        """Test size for 2D arrays."""
        arr = Array([[1, 2, 3], [4, 5, 6]])
        assert arr.size == 6
        assert isinstance(arr.size, int)
    
    def test_size_3d(self):
        """Test size for 3D arrays."""
        arr = Array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        assert arr.size == 8
        assert isinstance(arr.size, int)
    
    def test_size_empty_array(self):
        """Test size of empty array."""
        arr = Array([])
        assert arr.size == 0
    
    def test_size_single_element(self):
        """Test size of single-element arrays."""
        arr_1d = Array([42])
        arr_2d = Array([[42]])
        arr_3d = Array([[[42]]])
        
        assert arr_1d.size == 1
        assert arr_2d.size == 1
        assert arr_3d.size == 1
    
    def test_size_consistency_with_shape(self):
        """Test that size equals product of shape dimensions."""
        arrays = [
            Array([1, 2, 3, 4, 5]),  # size = 5
            Array([[1, 2, 3], [4, 5, 6]]),  # size = 2*3 = 6
            Array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]]),  # size = 2*2*2 = 8
        ]
        
        for arr in arrays:
            expected_size = 1
            for dim in arr.shape:
                expected_size *= dim
            assert arr.size == expected_size


class TestPropertyImmutability:
    """Test that properties are read-only."""
    
    def test_shape_immutable(self):
        """Test that shape cannot be modified directly."""
        arr = Array([[1, 2], [3, 4]])
        original_shape = arr.shape
        
        # Attempting to modify the tuple itself won't work (tuples are immutable)
        # But we can test that the property doesn't have a setter
        with pytest.raises(AttributeError):
            arr.shape = (3, 3)
    
    def test_ndim_immutable(self):
        """Test that ndim cannot be modified."""
        arr = Array([1, 2, 3])
        
        with pytest.raises(AttributeError):
            arr.ndim = 2
    
    def test_size_immutable(self):
        """Test that size cannot be modified."""
        arr = Array([1, 2, 3])
        
        with pytest.raises(AttributeError):
            arr.size = 5


class TestPropertyConsistency:
    """Test consistency between different properties."""
    
    def test_properties_after_creation(self):
        """Test that all properties are consistent after creation."""
        test_cases = [
            ([1, 2, 3, 4], (4,), 1, 4),
            ([[1, 2], [3, 4]], (2, 2), 2, 4),
            ([[[1]], [[2]]], (2, 1, 1), 3, 2),
            ([], (0,), 1, 0),
        ]
        
        for data, expected_shape, expected_ndim, expected_size in test_cases:
            arr = Array(data)
            assert arr.shape == expected_shape
            assert arr.ndim == expected_ndim
            assert arr.size == expected_size
    
    def test_properties_mathematical_relationship(self):
        """Test mathematical relationships between properties."""
        arrays = [
            Array([1, 2, 3, 4, 5]),
            Array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
            Array([[[1, 2, 3, 4]]]),
        ]
        
        for arr in arrays:
            # ndim should equal len(shape)
            assert arr.ndim == len(arr.shape)
            
            # size should equal product of shape dimensions
            expected_size = 1
            for dim in arr.shape:
                expected_size *= dim
            assert arr.size == expected_size
            
            # All dimensions should be positive (except for empty arrays)
            for dim in arr.shape:
                assert dim >= 0
    
    def test_empty_array_properties_consistency(self):
        """Test that empty array properties are consistent."""
        arr = Array([])
        assert arr.shape == (0,)
        assert arr.ndim == 1
        assert arr.size == 0
        assert len(arr._data) == 0


class TestPropertyTypes:
    """Test the types of property values."""
    
    def test_shape_type(self):
        """Test that shape is always a tuple of integers."""
        arr = Array([[1, 2, 3], [4, 5, 6]])
        assert isinstance(arr.shape, tuple)
        for dim in arr.shape:
            assert isinstance(dim, int)
    
    def test_ndim_type(self):
        """Test that ndim is always an integer."""
        arrays = [
            Array([1, 2, 3]),
            Array([[1, 2], [3, 4]]),
            Array([[[1]]]),
        ]
        
        for arr in arrays:
            assert isinstance(arr.ndim, int)
            assert arr.ndim >= 1
    
    def test_size_type(self):
        """Test that size is always a non-negative integer."""
        arrays = [
            Array([]),
            Array([1]),
            Array([1, 2, 3]),
            Array([[1, 2], [3, 4]]),
        ]
        
        for arr in arrays:
            assert isinstance(arr.size, int)
            assert arr.size >= 0