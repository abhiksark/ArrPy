"""
Comprehensive test suite for ArrPy v1.0.0
Tests all major functionality across backends.
"""

import pytest
import math
import numpy as np
import tempfile
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import arrpy
from arrpy import Backend, set_backend


class TestBackendSystem:
    """Test backend switching and capabilities."""
    
    def test_backend_switching(self):
        """Test that backend switching works."""
        original = arrpy.get_backend()
        
        set_backend('python')
        assert arrpy.get_backend() == Backend.PYTHON
        
        try:
            set_backend('cython')
            assert arrpy.get_backend() == Backend.CYTHON
        except:
            pass  # Cython may not be built
        
        set_backend(original)
    
    def test_backend_enum(self):
        """Test backend enum values."""
        assert Backend.PYTHON.value == 'python'
        assert Backend.CYTHON.value == 'cython'
        assert Backend.C.value == 'c'


class TestArrayCreation:
    """Test array creation functions."""
    
    def setup_method(self):
        set_backend('python')
    
    def test_array_from_list(self):
        """Test creating array from list."""
        a = arrpy.array([1, 2, 3, 4, 5])
        assert a.shape == (5,)
        assert a.dtype == 'float64'
        assert list(a._data) == [1.0, 2.0, 3.0, 4.0, 5.0]
    
    def test_array_2d(self):
        """Test creating 2D array."""
        a = arrpy.array([[1, 2], [3, 4]])
        assert a.shape == (2, 2)
        assert a._data == [1.0, 2.0, 3.0, 4.0]
    
    def test_zeros(self):
        """Test zeros creation."""
        a = arrpy.zeros((2, 3))
        assert a.shape == (2, 3)
        assert all(x == 0 for x in a._data)
    
    def test_ones(self):
        """Test ones creation."""
        a = arrpy.ones((2, 3))
        assert a.shape == (2, 3)
        assert all(x == 1 for x in a._data)
    
    def test_eye(self):
        """Test identity matrix."""
        a = arrpy.eye(3)
        expected = [1, 0, 0, 0, 1, 0, 0, 0, 1]
        assert a._data == expected
    
    def test_arange(self):
        """Test arange."""
        a = arrpy.arange(0, 10, 2)
        assert list(a._data) == [0, 2, 4, 6, 8]
    
    def test_linspace(self):
        """Test linspace."""
        a = arrpy.linspace(0, 1, 5)
        expected = [0.0, 0.25, 0.5, 0.75, 1.0]
        np.testing.assert_array_almost_equal(a._data, expected)


class TestIndexing:
    """Test advanced indexing."""
    
    def setup_method(self):
        set_backend('python')
    
    def test_boolean_indexing(self):
        """Test boolean mask indexing."""
        a = arrpy.array([1, 2, 3, 4, 5])
        mask = a > 3
        result = arrpy.boolean_index(a, mask)
        assert list(result._data) == [4, 5]
    
    def test_boolean_indexing_2d(self):
        """Test boolean indexing on 2D arrays."""
        # Create test array
        a = array([[1, 2], [3, 4], [5, 6]])
        
        # Create boolean mask
        mask = array([[True, False], [False, True], [True, True]])
        
        # Test boolean indexing
        result = a[mask]
        assert result.shape == (4,)
        assert list(result._data) == [1, 4, 5, 6]
    
    def test_fancy_indexing_1d(self):
        """Test fancy indexing on 1D arrays."""
        # Create test array
        a = array([10, 20, 30, 40, 50])
        
        # Test with integer array
        indices = array([0, 2, 4])
        result = a[indices]
        assert result.shape == (3,)
        assert list(result._data) == [10, 30, 50]
        
        # Test with list
        result2 = a[[1, 3]]
        assert list(result2._data) == [20, 40]
        
        # Test with negative indices
        indices3 = array([-1, -2, 0])
        result3 = a[indices3]
        assert list(result3._data) == [50, 40, 10]


class TestArrayManipulation:
    """Test array manipulation functions."""
    
    def test_reshape(self):
        """Test reshape operation."""
        # Test 1D to 2D
        a = arange(0, 6, 1)
        b = a.reshape(2, 3)
        assert b.shape == (2, 3)
        assert list(b._data) == [0, 1, 2, 3, 4, 5]
        
        # Test with -1 dimension
        c = a.reshape(-1, 2)
        assert c.shape == (3, 2)
        
        d = a.reshape(3, -1)
        assert d.shape == (3, 2)
    
    def test_transpose_2d(self):
        """Test transpose on 2D arrays."""
        # Create test array
        a = array([[1, 2, 3], [4, 5, 6]])
        
        # Test transpose
        b = a.transpose()
        assert b.shape == (3, 2)
        expected = [1, 4, 2, 5, 3, 6]
        assert list(b._data) == expected
        
        # Test T property
        c = a.T
        assert c.shape == (3, 2)
        assert list(c._data) == expected
    
    def test_flatten(self):
        """Test flatten operation."""
        a = array([[1, 2], [3, 4], [5, 6]])
        b = a.flatten()
        assert b.shape == (6,)
        assert list(b._data) == [1, 2, 3, 4, 5, 6]
    
    def test_concatenate_1d(self):
        """Test concatenation of 1D arrays."""
        a = array([1, 2, 3])
        b = array([4, 5, 6])
        c = array([7, 8])
        
        result = concatenate([a, b, c])
        assert result.shape == (8,)
        assert list(result._data) == [1, 2, 3, 4, 5, 6, 7, 8]
    
    def test_concatenate_2d(self):
        """Test concatenation of 2D arrays."""
        a = array([[1, 2], [3, 4]])
        b = array([[5, 6], [7, 8]])
        
        # Concatenate along axis 0 (vertical)
        result1 = concatenate([a, b], axis=0)
        assert result1.shape == (4, 2)
        assert list(result1._data) == [1, 2, 3, 4, 5, 6, 7, 8]
        
        # Concatenate along axis 1 (horizontal)
        result2 = concatenate([a, b], axis=1)
        assert result2.shape == (2, 4)
        expected = [1, 2, 5, 6, 3, 4, 7, 8]
        assert list(result2._data) == expected
    
    def test_stack(self):
        """Test stack operation."""
        a = array([1, 2, 3])
        b = array([4, 5, 6])
        
        # Stack along axis 0
        result = stack([a, b], axis=0)
        assert result.shape == (2, 3)
        assert list(result._data) == [1, 2, 3, 4, 5, 6]
    
    def test_vstack(self):
        """Test vertical stacking."""
        a = array([1, 2, 3])
        b = array([4, 5, 6])
        
        result = vstack([a, b])
        assert result.shape == (2, 3)
        assert list(result._data) == [1, 2, 3, 4, 5, 6]
    
    def test_hstack(self):
        """Test horizontal stacking."""
        a = array([1, 2, 3])
        b = array([4, 5, 6])
        
        # For 1D arrays, hstack concatenates
        result = hstack([a, b])
        assert result.shape == (6,)
        assert list(result._data) == [1, 2, 3, 4, 5, 6]
        
        # For 2D arrays
        a2 = array([[1], [2], [3]])
        b2 = array([[4], [5], [6]])
        result2 = hstack([a2, b2])
        assert result2.shape == (3, 2)
    
    def test_split(self):
        """Test split operation."""
        a = array([1, 2, 3, 4, 5, 6])
        
        # Split into 3 equal parts
        result = split(a, 3)
        assert len(result) == 3
        assert all(r.shape == (2,) for r in result)
        assert list(result[0]._data) == [1, 2]
        assert list(result[1]._data) == [3, 4]
        assert list(result[2]._data) == [5, 6]
        
        # Split at specific indices
        result2 = split(a, [2, 4])
        assert len(result2) == 3
        assert list(result2[0]._data) == [1, 2]
        assert list(result2[1]._data) == [3, 4]
        assert list(result2[2]._data) == [5, 6]
    
    def test_squeeze(self):
        """Test squeeze operation."""
        a = array([[[1, 2, 3]]])
        assert a.shape == (1, 1, 3)
        
        b = squeeze(a)
        assert b.shape == (3,)
        assert list(b._data) == [1, 2, 3]
    
    def test_expand_dims(self):
        """Test expand_dims operation."""
        a = array([1, 2, 3])
        
        # Add dimension at axis 0
        b = expand_dims(a, axis=0)
        assert b.shape == (1, 3)
        
        # Add dimension at axis 1
        c = expand_dims(a, axis=1)
        assert c.shape == (3, 1)


class TestLinearAlgebra:
    """Test linear algebra operations."""
    
    def test_dot_1d_1d(self):
        """Test dot product of two 1D arrays."""
        a = array([1, 2, 3])
        b = array([4, 5, 6])
        
        result = dot(a, b)
        assert result == 32  # 1*4 + 2*5 + 3*6
    
    def test_dot_2d_1d(self):
        """Test dot product of 2D and 1D arrays."""
        a = array([[1, 2], [3, 4], [5, 6]])
        b = array([2, 3])
        
        result = dot(a, b)
        assert result.shape == (3,)
        assert list(result._data) == [8, 18, 28]  # [1*2+2*3, 3*2+4*3, 5*2+6*3]
    
    def test_dot_1d_2d(self):
        """Test dot product of 1D and 2D arrays."""
        a = array([1, 2, 3])
        b = array([[1, 2], [3, 4], [5, 6]])
        
        result = dot(a, b)
        assert result.shape == (2,)
        assert list(result._data) == [22, 28]  # [1*1+2*3+3*5, 1*2+2*4+3*6]
    
    def test_dot_2d_2d(self):
        """Test matrix multiplication."""
        a = array([[1, 2], [3, 4]])
        b = array([[5, 6], [7, 8]])
        
        result = dot(a, b)
        assert result.shape == (2, 2)
        expected = [19, 22, 43, 50]  # [[1*5+2*7, 1*6+2*8], [3*5+4*7, 3*6+4*8]]
        assert list(result._data) == expected
    
    def test_matmul(self):
        """Test matrix multiplication with @ operator."""
        a = array([[1, 2], [3, 4]])
        b = array([[5, 6], [7, 8]])
        
        result = matmul(a, b)
        assert result.shape == (2, 2)
        expected = [19, 22, 43, 50]
        assert list(result._data) == expected
        
        # Test with 1D arrays
        c = array([1, 2])
        d = array([3, 4])
        result2 = matmul(c, d)
        assert result2 == 11  # 1*3 + 2*4
    
    def test_outer(self):
        """Test outer product."""
        a = array([1, 2, 3])
        b = array([4, 5])
        
        result = outer(a, b)
        assert result.shape == (3, 2)
        expected = [4, 5, 8, 10, 12, 15]
        assert list(result._data) == expected
    
    def test_trace(self):
        """Test trace (sum of diagonal)."""
        a = array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        
        # Main diagonal
        result = trace(a)
        assert result == 15  # 1 + 5 + 9
        
        # Upper diagonal
        result2 = trace(a, offset=1)
        assert result2 == 8  # 2 + 6
        
        # Lower diagonal
        result3 = trace(a, offset=-1)
        assert result3 == 12  # 4 + 8
    
    def test_identity_matrix_operations(self):
        """Test operations with identity matrix."""
        I = eye(3, 3)
        a = array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        
        # Multiplying by identity should give same matrix
        result = dot(a, I)
        assert result.shape == a.shape
        assert list(result._data) == list(a._data)
        
        result2 = dot(I, a)
        assert result2.shape == a.shape
        assert list(result2._data) == list(a._data)


class TestIntegration:
    """Integration tests combining multiple features."""
    
    def test_advanced_workflow(self):
        """Test a complex workflow using multiple Phase 3 features."""
        # Create matrices
        a = arange(0, 9, 1).reshape(3, 3)
        b = ones((3, 2))
        
        # Matrix multiplication
        c = dot(a, b)
        assert c.shape == (3, 2)
        
        # Transpose and reshape
        d = c.T.reshape(-1)
        assert d.shape == (6,)
        
        # Boolean indexing
        mask = d > 5
        e = d[mask]
        assert all(val > 5 for val in e._data)
        
        # Concatenate and stack
        f = concatenate([e, e])
        assert f.shape[0] == 2 * e.shape[0]