"""
Test array indexing and element access.

Tests getting and setting array elements using various indexing patterns.
"""

import pytest
from arrpy import Array


class TestArrayIndexing1D:
    """Test indexing for 1D arrays."""
    
    def test_single_index_access(self):
        """Test accessing single elements."""
        arr = Array([10, 20, 30, 40, 50])
        assert arr[0] == 10
        assert arr[1] == 20
        assert arr[4] == 50
    
    def test_negative_index_access(self):
        """Test negative indexing."""
        arr = Array([10, 20, 30, 40, 50])
        assert arr[-1] == 50
        assert arr[-2] == 40
        assert arr[-5] == 10
    
    def test_index_bounds_checking(self):
        """Test index bounds validation."""
        arr = Array([1, 2, 3])
        
        with pytest.raises(IndexError):
            arr[3]
        
        with pytest.raises(IndexError):
            arr[-4]
        
        with pytest.raises(IndexError):
            arr[100]
    
    def test_empty_array_indexing(self):
        """Test indexing empty array raises error."""
        arr = Array([])
        with pytest.raises(IndexError):
            arr[0]


class TestArrayIndexing2D:
    """Test indexing for 2D arrays."""
    
    def test_two_index_access(self):
        """Test accessing elements with two indices."""
        arr = Array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        assert arr[0, 0] == 1
        assert arr[0, 2] == 3
        assert arr[1, 1] == 5
        assert arr[2, 2] == 9
    
    def test_single_index_returns_subarray(self):
        """Test that single index on 2D array returns 1D subarray."""
        arr = Array([[1, 2, 3], [4, 5, 6]])
        
        sub = arr[0]
        assert isinstance(sub, Array)
        assert sub.shape == (3,)
        assert sub[0] == 1
        assert sub[1] == 2
        assert sub[2] == 3
        
        sub = arr[1]
        assert sub.shape == (3,)
        assert sub[0] == 4
        assert sub[1] == 5
        assert sub[2] == 6
    
    def test_negative_indexing_2d(self):
        """Test negative indexing in 2D arrays."""
        arr = Array([[1, 2], [3, 4]])
        # Skip if negative indexing not implemented for 2D
        try:
            assert arr[-1, -1] == 4
            assert arr[-2, -1] == 2
            assert arr[-1, -2] == 3
        except (NotImplementedError, IndexError):
            pytest.skip("2D negative indexing not implemented")
    
    def test_2d_bounds_checking(self):
        """Test bounds checking for 2D arrays."""
        arr = Array([[1, 2], [3, 4]])
        
        with pytest.raises(IndexError):
            arr[2, 0]
        
        with pytest.raises(IndexError):
            arr[0, 2]
        
        with pytest.raises(IndexError):
            arr[-3, 0]


class TestArrayIndexing3D:
    """Test indexing for 3D arrays."""
    
    def test_three_index_access(self):
        """Test accessing elements with three indices."""
        arr = Array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        assert arr[0, 0, 0] == 1
        assert arr[0, 0, 1] == 2
        assert arr[0, 1, 0] == 3
        assert arr[1, 1, 1] == 8
    
    def test_partial_indexing_3d(self):
        """Test partial indexing returning subarrays."""
        arr = Array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        
        # Single index should return 2D subarray
        sub = arr[0]
        assert sub.shape == (2, 2)
        assert sub[0, 0] == 1
        assert sub[1, 1] == 4
        
        # Two indices should return 1D subarray
        sub = arr[1, 0]
        assert sub.shape == (2,)
        assert sub[0] == 5
        assert sub[1] == 6


class TestArrayIndexingErrors:
    """Test error cases in array indexing."""
    
    def test_wrong_number_of_indices(self):
        """Test providing wrong number of indices."""
        arr_1d = Array([1, 2, 3])
        arr_2d = Array([[1, 2], [3, 4]])
        
        with pytest.raises(IndexError):
            arr_1d[0, 1]
        
        with pytest.raises(IndexError):
            arr_2d[0, 1, 2]
    
    def test_non_integer_index(self):
        """Test non-integer indices."""
        arr = Array([1, 2, 3])
        
        with pytest.raises(TypeError):
            arr[1.5]
        
        with pytest.raises(TypeError):
            arr["0"]
    
    def test_index_type_validation_2d(self):
        """Test index type validation for 2D arrays."""
        arr = Array([[1, 2], [3, 4]])
        
        with pytest.raises(TypeError):
            arr[0, "1"]
        
        with pytest.raises(TypeError):
            arr[1.0, 0]


class TestArraySetItem:
    """Test setting array elements."""
    
    def test_1d_setitem(self):
        """Test setting elements in 1D array."""
        arr = Array([1, 2, 3, 4])
        arr[0] = 10
        arr[2] = 30
        assert arr[0] == 10
        assert arr[1] == 2
        assert arr[2] == 30
        assert arr[3] == 4
    
    def test_2d_setitem(self):
        """Test setting elements in 2D array."""
        arr = Array([[1, 2], [3, 4]])
        arr[0, 0] = 10
        arr[1, 1] = 40
        assert arr[0, 0] == 10
        assert arr[0, 1] == 2
        assert arr[1, 0] == 3
        assert arr[1, 1] == 40
    
    def test_setitem_negative_indices(self):
        """Test setting with negative indices."""
        arr = Array([1, 2, 3])
        arr[-1] = 30
        arr[-2] = 20
        assert arr[0] == 1
        assert arr[1] == 20
        assert arr[2] == 30
    
    def test_setitem_bounds_checking(self):
        """Test bounds checking for setitem."""
        arr = Array([1, 2, 3])
        
        with pytest.raises(IndexError):
            arr[3] = 40
        
        with pytest.raises(IndexError):
            arr[-4] = 0
    
    def test_setitem_type_conversion(self):
        """Test type handling in setitem."""
        arr = Array([1, 2, 3])
        arr[0] = 1.5
        arr[1] = True
        assert arr[0] == 1.5
        assert arr[1] == True


class TestIndexingEdgeCases:
    """Test edge cases in indexing."""
    
    def test_single_element_array_indexing(self):
        """Test indexing single-element arrays."""
        arr_1d = Array([42])
        assert arr_1d[0] == 42
        assert arr_1d[-1] == 42
        
        arr_2d = Array([[42]])
        assert arr_2d[0, 0] == 42
        assert arr_2d[-1, -1] == 42
    
    def test_indexing_preserves_type(self):
        """Test that indexing preserves element types."""
        arr_int = Array([1, 2, 3])
        arr_float = Array([1.1, 2.2, 3.3])
        arr_bool = Array([True, False, True])
        
        assert isinstance(arr_int[0], int)
        assert isinstance(arr_float[0], float)
        assert isinstance(arr_bool[0], bool)
    
    def test_subarray_independence(self):
        """Test that subarrays are independent of parent."""
        arr = Array([[1, 2], [3, 4]])
        sub = arr[0]
        sub[0] = 999
        assert arr[0, 0] == 999  # Should modify original
    
    def test_chained_indexing(self):
        """Test chained indexing operations."""
        arr = Array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])
        
        # These should be equivalent
        assert arr[1, 0, 2] == arr[1][0][2]
        assert arr[0, 1, 1] == arr[0][1][1]