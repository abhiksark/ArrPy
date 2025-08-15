"""
Tests for the main arrpy array class.
"""

import pytest
import numpy as np
import arrpy as ap


class TestArrPyCreation:
    """Test array creation and basic properties."""
    
    def test_create_from_list(self, sample_1d_array):
        """Test creating arrpy from list."""
        # arr = ap.array(sample_1d_array)
        # assert arr.shape == (5,)
        # assert arr.size == 5
        # assert arr.ndim == 1
        pass  # TODO: Implement when arrpy is functional
    
    def test_create_from_nested_list(self, sample_2d_array):
        """Test creating arrpy from nested list."""
        # arr = ap.array(sample_2d_array)
        # assert arr.shape == (2, 3)
        # assert arr.size == 6
        # assert arr.ndim == 2
        pass  # TODO: Implement when arrpy is functional
    
    def test_zeros(self):
        """Test zeros array creation."""
        # arr = ap.zeros((3, 4))
        # assert arr.shape == (3, 4)
        # assert arr.size == 12
        # TODO: Check all elements are zero
        pass
    
    def test_ones(self):
        """Test ones array creation."""
        # arr = ap.ones((2, 3, 4))
        # assert arr.shape == (2, 3, 4)
        # assert arr.size == 24
        # TODO: Check all elements are one
        pass
    
    def test_arange(self):
        """Test arange array creation."""
        # arr = ap.arange(10)
        # assert arr.shape == (10,)
        # assert arr.size == 10
        # TODO: Check values are 0-9
        pass
    
    def test_linspace(self):
        """Test linspace array creation."""
        # arr = ap.linspace(0, 1, 11)
        # assert arr.shape == (11,)
        # assert arr.size == 11
        # TODO: Check values are evenly spaced
        pass


class TestArrPyIndexing:
    """Test array indexing operations."""
    
    def test_basic_indexing_1d(self):
        """Test basic indexing on 1D array."""
        # arr = ap.arange(10)
        # assert arr[0] == 0
        # assert arr[-1] == 9
        # assert arr[5] == 5
        pass
    
    def test_basic_indexing_2d(self):
        """Test basic indexing on 2D array."""
        # arr = ap.arange(12).reshape(3, 4)
        # assert arr[0, 0] == 0
        # assert arr[1, 2] == 6
        # assert arr[-1, -1] == 11
        pass
    
    def test_slice_indexing_1d(self):
        """Test slice indexing on 1D array."""
        # arr = ap.arange(10)
        # sub = arr[2:7]
        # assert sub.shape == (5,)
        # TODO: Check values
        pass
    
    def test_slice_indexing_2d(self):
        """Test slice indexing on 2D array."""
        # arr = ap.arange(12).reshape(3, 4)
        # sub = arr[1:, :2]
        # assert sub.shape == (2, 2)
        # TODO: Check values
        pass


class TestArrPyOperations:
    """Test array operations."""
    
    def test_addition(self):
        """Test element-wise addition."""
        # arr1 = ap.ones((3, 4))
        # arr2 = ap.ones((3, 4))
        # result = arr1 + arr2
        # assert result.shape == (3, 4)
        # TODO: Check all elements are 2
        pass
    
    def test_scalar_addition(self):
        """Test scalar addition."""
        # arr = ap.ones((3, 4))
        # result = arr + 5
        # assert result.shape == (3, 4)
        # TODO: Check all elements are 6
        pass
    
    def test_multiplication(self):
        """Test element-wise multiplication."""
        # arr1 = ap.ones((3, 4)) * 2
        # arr2 = ap.ones((3, 4)) * 3
        # result = arr1 * arr2
        # assert result.shape == (3, 4)
        # TODO: Check all elements are 6
        pass


class TestArrPyManipulation:
    """Test array manipulation operations."""
    
    def test_reshape(self):
        """Test reshape operation."""
        # arr = ap.arange(12)
        # reshaped = arr.reshape(3, 4)
        # assert reshaped.shape == (3, 4)
        # assert reshaped.size == 12
        pass
    
    def test_flatten(self):
        """Test flatten operation."""
        # arr = ap.arange(12).reshape(3, 4)
        # flat = arr.flatten()
        # assert flat.shape == (12,)
        # assert flat.ndim == 1
        pass
    
    def test_transpose(self):
        """Test transpose operation."""
        # arr = ap.arange(6).reshape(2, 3)
        # transposed = arr.T
        # assert transposed.shape == (3, 2)
        pass


class TestArrPyComparison:
    """Test comparison with NumPy."""
    
    def test_compare_creation_with_numpy(self):
        """Compare array creation with NumPy."""
        # data = [[1, 2, 3], [4, 5, 6]]
        # arr_ap = ap.array(data)
        # arr_np = np.array(data)
        # TODO: Compare shapes, values
        pass
    
    def test_compare_operations_with_numpy(self):
        """Compare operations with NumPy."""
        # Create same arrays in both
        # arr_ap = ap.arange(10)
        # arr_np = np.arange(10)
        # 
        # Test addition
        # result_ap = arr_ap + 5
        # result_np = arr_np + 5
        # TODO: Compare results
        pass