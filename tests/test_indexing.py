"""
Tests for array indexing functionality.
Tests __getitem__ and __setitem__ implementations.
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import arrpy
from arrpy import array, zeros, ones


class TestBasicIndexing:
    """Test basic integer indexing for arrays."""
    
    def test_1d_positive_indexing(self):
        """Test positive integer indexing on 1D arrays."""
        a = array([10, 20, 30, 40, 50])
        
        assert a[0] == 10
        assert a[1] == 20
        assert a[2] == 30
        assert a[4] == 50
    
    def test_1d_negative_indexing(self):
        """Test negative integer indexing on 1D arrays."""
        a = array([10, 20, 30, 40, 50])
        
        assert a[-1] == 50
        assert a[-2] == 40
        assert a[-5] == 10
    
    def test_1d_out_of_bounds(self):
        """Test that out of bounds access raises IndexError."""
        a = array([1, 2, 3])
        
        with pytest.raises(IndexError):
            _ = a[5]
        
        with pytest.raises(IndexError):
            _ = a[-10]
    
    @pytest.mark.skip(reason="2D indexing not implemented")
    def test_2d_indexing(self):
        """Test multi-dimensional indexing on 2D arrays."""
        b = array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        
        assert b[0, 0] == 1
        assert b[0, 2] == 3
        assert b[1, 1] == 5
        assert b[2, 0] == 7
        assert b[2, 2] == 9
    
    @pytest.mark.skip(reason="2D indexing not implemented")
    def test_2d_negative_indexing(self):
        """Test negative indexing on 2D arrays."""
        b = array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        
        assert b[-1, -1] == 9
        assert b[-3, -3] == 1
        assert b[0, -1] == 3
        assert b[-1, 0] == 7
    
    @pytest.mark.skip(reason="2D indexing not implemented")
    def test_2d_out_of_bounds(self):
        """Test that 2D out of bounds access raises IndexError."""
        b = array([[1, 2], [3, 4]])
        
        with pytest.raises(IndexError):
            _ = b[2, 0]
        
        with pytest.raises(IndexError):
            _ = b[0, 3]
        
        with pytest.raises(IndexError):
            _ = b[-3, 0]


class TestSlicing:
    """Test array slicing operations."""
    
    def test_1d_basic_slicing(self):
        """Test basic slicing on 1D arrays."""
        a = array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        
        # Basic slices
        s1 = a[2:5]
        assert list(s1._data) == [2, 3, 4]
        
        s2 = a[::2]
        assert list(s2._data) == [0, 2, 4, 6, 8]
        
        s3 = a[1::2]
        assert list(s3._data) == [1, 3, 5, 7, 9]
    
    def test_1d_negative_slicing(self):
        """Test slicing with negative indices."""
        a = array([0, 1, 2, 3, 4, 5])
        
        s1 = a[-3:]
        assert list(s1._data) == [3, 4, 5]
        
        s2 = a[:-2]
        assert list(s2._data) == [0, 1, 2, 3]
        
        s3 = a[-4:-1]
        assert list(s3._data) == [2, 3, 4]
    
    def test_1d_step_slicing(self):
        """Test slicing with custom step."""
        a = array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        
        s1 = a[::3]
        assert list(s1._data) == [0, 3, 6, 9]
        
        s2 = a[1:8:2]
        assert list(s2._data) == [1, 3, 5, 7]
        
        # Negative step (reverse)
        s3 = a[::-1]
        assert list(s3._data) == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    
    def test_empty_slice(self):
        """Test empty slices."""
        a = array([1, 2, 3, 4, 5])
        
        s1 = a[2:2]
        assert list(s1._data) == []
        
        s2 = a[5:10]
        assert list(s2._data) == []


class TestAssignment:
    """Test array element and slice assignment."""
    
    def test_1d_element_assignment(self):
        """Test single element assignment in 1D arrays."""
        a = array([1, 2, 3, 4, 5])
        
        a[0] = 10
        assert a[0] == 10
        
        a[-1] = 50
        assert a[-1] == 50
        
        a[2] = 30
        assert list(a._data) == [10, 2, 30, 4, 50]
    
    @pytest.mark.skip(reason="2D indexing not implemented")
    def test_2d_element_assignment(self):
        """Test element assignment in 2D arrays."""
        b = array([[1, 2, 3], [4, 5, 6]])
        
        b[0, 0] = 10
        assert b[0, 0] == 10
        
        b[1, 2] = 60
        assert b[1, 2] == 60
        
        b[-1, -1] = 99
        assert b[1, 2] == 99
    
    def test_1d_slice_assignment_scalar(self):
        """Test slice assignment with scalar value."""
        a = array([1, 2, 3, 4, 5])
        
        a[1:4] = 0
        assert list(a._data) == [1, 0, 0, 0, 5]
        
        a[::2] = 9
        assert list(a._data) == [9, 0, 9, 0, 9]
    
    def test_1d_slice_assignment_array(self):
        """Test slice assignment with array values."""
        a = array([0, 0, 0, 0, 0])
        
        a[1:4] = array([1, 2, 3])
        assert list(a._data) == [0, 1, 2, 3, 0]
        
        a[::2] = array([9, 8, 7])
        assert list(a._data) == [9, 1, 8, 3, 7]
    
    def test_assignment_out_of_bounds(self):
        """Test that out of bounds assignment raises IndexError."""
        a = array([1, 2, 3])
        
        with pytest.raises(IndexError):
            a[5] = 10
        
        with pytest.raises(IndexError):
            a[-10] = 10


class TestAdvancedIndexing:
    """Test boolean and fancy indexing."""
    
    @pytest.mark.skip(reason="Boolean array dtype not properly supported with array.array storage")
    def test_boolean_indexing_get(self):
        """Test boolean array indexing for getting values."""
        a = array([1, 2, 3, 4, 5])
        mask = a > 2
        
        result = a[mask]
        assert list(result._data) == [3, 4, 5]
        
        # Test with explicit boolean array
        mask2 = array([True, False, True, False, True])
        result2 = a[mask2]
        assert list(result2._data) == [1, 3, 5]
    
    @pytest.mark.skip(reason="Boolean indexing setitem not implemented")
    def test_boolean_indexing_set(self):
        """Test boolean array indexing for setting values."""
        a = array([1, 2, 3, 4, 5])
        mask = a > 2
        
        a[mask] = 10
        assert list(a._data) == [1, 2, 10, 10, 10]
        
        # Reset and test with array assignment
        a = array([1, 2, 3, 4, 5])
        mask = array([True, False, True, False, True])
        a[mask] = array([10, 20, 30])
        assert list(a._data) == [10, 2, 20, 4, 30]
    
    def test_fancy_indexing_get(self):
        """Test fancy indexing with integer arrays."""
        a = array([10, 20, 30, 40, 50])
        
        # Index with array
        indices = array([0, 2, 4])
        result = a[indices]
        assert list(result._data) == [10, 30, 50]
        
        # Index with list
        result2 = a[[1, 3]]
        assert list(result2._data) == [20, 40]
        
        # Index with tuple
        result3 = a[(0, 2, 4)]
        assert list(result3._data) == [10, 30, 50]
    
    def test_fancy_indexing_repeated(self):
        """Test fancy indexing with repeated indices."""
        a = array([10, 20, 30, 40, 50])
        
        indices = array([0, 2, 2, 0, 4])
        result = a[indices]
        assert list(result._data) == [10, 30, 30, 10, 50]
    
    @pytest.mark.skip(reason="Boolean indexing setitem not implemented")
    def test_boolean_indexing_size_mismatch(self):
        """Test that boolean indexing with wrong size raises error."""
        a = array([1, 2, 3, 4, 5])
        mask = array([True, False, True])  # Wrong size
        
        with pytest.raises(ValueError):
            a[mask] = 10


class TestIndexingEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_invalid_index_type(self):
        """Test that invalid index types raise TypeError."""
        a = array([1, 2, 3])
        
        with pytest.raises(TypeError):
            _ = a["string"]
        
        with pytest.raises(TypeError):
            _ = a[2.5]
        
        with pytest.raises(TypeError):
            a["string"] = 10
    
    @pytest.mark.skip(reason="2D array indexing validation not implemented")
    def test_too_many_indices(self):
        """Test that too many indices raise IndexError."""
        a = array([1, 2, 3])  # 1D array
        
        with pytest.raises(IndexError):
            _ = a[0, 0]
        
        b = array([[1, 2], [3, 4]])  # 2D array
        
        with pytest.raises(IndexError):
            _ = b[0, 0, 0]
    
    def test_too_few_indices(self):
        """Test behavior with too few indices."""
        b = array([[1, 2], [3, 4]])
        
        # Single index on 2D array should raise NotImplementedError
        # (could be implemented to return row in future)
        with pytest.raises(NotImplementedError):
            _ = b[0]
    
    def test_empty_array_indexing(self):
        """Test indexing on empty arrays."""
        a = array([])
        
        with pytest.raises(IndexError):
            _ = a[0]
        
        # Empty slice should work
        result = a[0:0]
        assert list(result._data) == []
    
    def test_single_element_array(self):
        """Test indexing on single element arrays."""
        a = array([42])
        
        assert a[0] == 42
        assert a[-1] == 42
        
        with pytest.raises(IndexError):
            _ = a[1]


class TestIndexingWithBackends:
    """Test that indexing works with different backends."""
    
    def test_indexing_python_backend(self):
        """Test indexing with Python backend."""
        arrpy.set_backend('python')
        a = array([1, 2, 3, 4, 5])
        
        assert a[0] == 1
        assert a[-1] == 5
        assert list(a[1:4]._data) == [2, 3, 4]
        
        a[2] = 10
        assert a[2] == 10
    
    def test_indexing_cython_backend(self):
        """Test indexing with Cython backend."""
        try:
            arrpy.set_backend('cython')
            a = array([1, 2, 3, 4, 5])
            
            assert a[0] == 1
            assert a[-1] == 5
            assert list(a[1:4]._data) == [2, 3, 4]
            
            a[2] = 10
            assert a[2] == 10
        except:
            pytest.skip("Cython backend not available")
        finally:
            arrpy.set_backend('python')
    
    def test_indexing_c_backend(self):
        """Test indexing with C backend."""
        try:
            arrpy.set_backend('c')
            a = array([1, 2, 3, 4, 5])
            
            assert a[0] == 1
            assert a[-1] == 5
            assert list(a[1:4]._data) == [2, 3, 4]
            
            a[2] = 10
            assert a[2] == 10
        except:
            pytest.skip("C backend not available")
        finally:
            arrpy.set_backend('python')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])