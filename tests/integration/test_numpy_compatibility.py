"""
Test compatibility with NumPy behavior.

Compares ArrPy results with NumPy to ensure consistent behavior.
"""

import pytest
import numpy as np
import math
from arrpy import Array, zeros, ones, arange, linspace
import arrpy as ap

# Import helper for type checking that works with hybrid arrays
try:
    from test_imports import is_array
except ImportError:
    def is_array(obj):
        return isinstance(obj, Array)



class TestBasicOperationCompatibility:
    """Test that basic operations match NumPy behavior."""
    
    def test_array_creation_compatibility(self):
        """Test that array creation matches NumPy."""
        data = [[1, 2, 3], [4, 5, 6]]
        
        arr = Array(data)
        np_arr = np.array(data)
        
        assert arr.shape == np_arr.shape
        assert arr.ndim == np_arr.ndim
        assert arr.size == np_arr.size
        
        # Check elements match
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                assert arr[i, j] == np_arr[i, j]
    
    def test_arithmetic_compatibility(self):
        """Test that arithmetic operations match NumPy."""
        data = [[1, 2], [3, 4]]
        
        arr = Array(data)
        np_arr = np.array(data)
        
        # Scalar addition
        arr_result = arr + 10
        np_result = np_arr + 10
        
        assert arr_result.shape == np_result.shape
        for i in range(arr_result.shape[0]):
            for j in range(arr_result.shape[1]):
                assert arr_result[i, j] == np_result[i, j]
        
        # Array addition
        arr2 = Array([[5, 6], [7, 8]])
        np_arr2 = np.array([[5, 6], [7, 8]])
        
        arr_sum = arr + arr2
        np_sum = np_arr + np_arr2
        
        assert arr_sum.shape == np_sum.shape
        for i in range(arr_sum.shape[0]):
            for j in range(arr_sum.shape[1]):
                assert arr_sum[i, j] == np_sum[i, j]
    
    def test_matrix_multiplication_compatibility(self):
        """Test that matrix multiplication matches NumPy."""
        data1 = [[1, 2], [3, 4]]
        data2 = [[5, 6], [7, 8]]
        
        arr1 = Array(data1)
        arr2 = Array(data2)
        np_arr1 = np.array(data1)
        np_arr2 = np.array(data2)
        
        arr_result = arr1.dot(arr2)
        np_result = np_arr1.dot(np_arr2)
        
        assert arr_result.shape == np_result.shape
        for i in range(arr_result.shape[0]):
            for j in range(arr_result.shape[1]):
                assert arr_result[i, j] == np_result[i, j]
    
    def test_transpose_compatibility(self):
        """Test that transpose matches NumPy."""
        data = [[1, 2, 3], [4, 5, 6]]
        
        arr = Array(data)
        np_arr = np.array(data)
        
        arr_t = arr.T
        np_t = np_arr.T
        
        assert arr_t.shape == np_t.shape
        for i in range(arr_t.shape[0]):
            for j in range(arr_t.shape[1]):
                assert arr_t[i, j] == np_t[i, j]


class TestAggregationCompatibility:
    """Test that aggregation functions match NumPy."""
    
    def test_sum_compatibility(self):
        """Test that sum matches NumPy."""
        test_cases = [
            [1, 2, 3, 4, 5],
            [[1, 2], [3, 4]],
            [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
        ]
        
        for data in test_cases:
            arr = Array(data)
            np_arr = np.array(data)
            
            assert arr.sum() == np_arr.sum()
    
    def test_mean_compatibility(self):
        """Test that mean matches NumPy."""
        test_cases = [
            [1, 2, 3, 4],
            [[1, 2], [3, 4]],
            [2, 4, 6, 8, 10]
        ]
        
        for data in test_cases:
            arr = Array(data)
            np_arr = np.array(data)
            
            assert abs(arr.mean() - np_arr.mean()) < 1e-10
    
    def test_min_max_compatibility(self):
        """Test that min/max match NumPy."""
        test_cases = [
            [3, 1, 4, 1, 5],
            [[9, 2], [6, 5]],
            [-1, -5, -2, -8]
        ]
        
        for data in test_cases:
            arr = Array(data)
            np_arr = np.array(data)
            
            assert arr.min() == np_arr.min()
            assert arr.max() == np_arr.max()


class TestMathematicalFunctionCompatibility:
    """Test that mathematical functions match NumPy."""
    
    def test_trigonometric_compatibility(self):
        """Test that trigonometric functions match NumPy."""
        data = [0, math.pi/6, math.pi/4, math.pi/3, math.pi/2]
        
        arr = Array(data)
        np_arr = np.array(data)
        
        # Test sine
        arr_sin = ap.sin(arr)
        np_sin = np.sin(np_arr)
        
        assert arr_sin.shape == np_sin.shape
        for i in range(len(data)):
            assert abs(arr_sin[i] - np_sin[i]) < 1e-10
        
        # Test cosine
        arr_cos = ap.cos(arr)
        np_cos = np.cos(np_arr)
        
        for i in range(len(data)):
            assert abs(arr_cos[i] - np_cos[i]) < 1e-10
    
    def test_exponential_logarithmic_compatibility(self):
        """Test that exp/log functions match NumPy."""
        data = [1, 2, 3, 4, 5]
        
        arr = Array(data)
        np_arr = np.array(data)
        
        # Test exponential
        arr_exp = arr.exp()
        np_exp = np.exp(np_arr)
        
        for i in range(len(data)):
            assert abs(arr_exp[i] - np_exp[i]) < 1e-10
        
        # Test natural logarithm
        arr_log = arr.log()
        np_log = np.log(np_arr)
        
        for i in range(len(data)):
            assert abs(arr_log[i] - np_log[i]) < 1e-10
    
    def test_square_root_compatibility(self):
        """Test that square root matches NumPy."""
        data = [1, 4, 9, 16, 25]
        
        arr = Array(data)
        np_arr = np.array(data)
        
        arr_sqrt = arr.sqrt()
        np_sqrt = np.sqrt(np_arr)
        
        for i in range(len(data)):
            assert abs(arr_sqrt[i] - np_sqrt[i]) < 1e-10


class TestCreationFunctionCompatibility:
    """Test that array creation functions match NumPy."""
    
    def test_zeros_compatibility(self):
        """Test that zeros function matches NumPy."""
        shapes = [(5,), (2, 3), (2, 2, 2)]
        
        for shape in shapes:
            arr = zeros(shape)
            np_arr = np.zeros(shape)
            
            assert arr.shape == np_arr.shape
            assert arr.size == np_arr.size
            
            # Check all elements are zero
            if arr.ndim == 1:
                for i in range(arr.size):
                    assert arr._data[i] == np_arr.flat[i]
            elif arr.ndim == 2:
                for i in range(arr.shape[0]):
                    for j in range(arr.shape[1]):
                        assert arr[i, j] == np_arr[i, j]
    
    def test_ones_compatibility(self):
        """Test that ones function matches NumPy."""
        shapes = [(4,), (3, 2), (2, 1, 3)]
        
        for shape in shapes:
            arr = ones(shape)
            np_arr = np.ones(shape)
            
            assert arr.shape == np_arr.shape
            assert arr.size == np_arr.size
            
            # Check all elements are one
            if arr.ndim == 1:
                for i in range(arr.size):
                    assert arr._data[i] == np_arr.flat[i]
    
    def test_arange_compatibility(self):
        """Test that arange function matches NumPy."""
        test_cases = [
            (5,),
            (2, 8),
            (0, 10, 2),
            (1, 6, 1)
        ]
        
        for args in test_cases:
            arr = arange(*args)
            np_arr = np.arange(*args)
            
            assert arr.shape == np_arr.shape
            assert arr.size == np_arr.size
            
            for i in range(arr.size):
                assert arr[i] == np_arr[i]
    
    def test_linspace_compatibility(self):
        """Test that linspace function matches NumPy."""
        test_cases = [
            (0, 1, 11),
            (5, 10, 6),
            (-1, 1, 21)
        ]
        
        for start, stop, num in test_cases:
            arr = linspace(start, stop, num)
            np_arr = np.linspace(start, stop, num)
            
            assert arr.shape == np_arr.shape
            assert arr.size == np_arr.size
            
            for i in range(arr.size):
                assert abs(arr[i] - np_arr[i]) < 1e-10


class TestReshapeCompatibility:
    """Test that reshape operations match NumPy."""
    
    def test_reshape_compatibility(self):
        """Test that reshape matches NumPy behavior."""
        data = [1, 2, 3, 4, 5, 6]
        
        arr = Array(data)
        np_arr = np.array(data)
        
        # Test various reshape operations
        reshape_targets = [(2, 3), (3, 2), (6, 1), (1, 6)]
        
        for new_shape in reshape_targets:
            arr_reshaped = arr.reshape(new_shape)
            np_reshaped = np_arr.reshape(new_shape)
            
            assert arr_reshaped.shape == np_reshaped.shape
            
            # Check element order is preserved
            for i in range(arr_reshaped.shape[0]):
                for j in range(arr_reshaped.shape[1]):
                    assert arr_reshaped[i, j] == np_reshaped[i, j]
    
    def test_reshape_3d_compatibility(self):
        """Test 3D reshape compatibility."""
        data = list(range(24))  # 24 elements
        
        arr = Array(data)
        np_arr = np.array(data)
        
        # Reshape to 3D
        arr_3d = arr.reshape((2, 3, 4))
        np_3d = np_arr.reshape((2, 3, 4))
        
        assert arr_3d.shape == np_3d.shape
        
        for i in range(2):
            for j in range(3):
                for k in range(4):
                    assert arr_3d[i, j, k] == np_3d[i, j, k]


class TestComparisonCompatibility:
    """Test that comparison operations match NumPy."""
    
    def test_equality_compatibility(self):
        """Test that equality comparison matches NumPy."""
        data1 = [1, 2, 3, 4]
        data2 = [1, 0, 3, 5]
        
        arr1 = Array(data1)
        arr2 = Array(data2)
        np_arr1 = np.array(data1)
        np_arr2 = np.array(data2)
        
        arr_result = arr1 == arr2
        np_result = np_arr1 == np_arr2
        
        assert arr_result.shape == np_result.shape
        for i in range(len(data1)):
            assert arr_result[i] == np_result[i]
    
    def test_relational_compatibility(self):
        """Test that relational comparisons match NumPy."""
        data1 = [1, 3, 2, 4]
        data2 = [2, 2, 3, 4]
        
        arr1 = Array(data1)
        arr2 = Array(data2)
        np_arr1 = np.array(data1)
        np_arr2 = np.array(data2)
        
        # Test greater than
        arr_gt = arr1 > arr2
        np_gt = np_arr1 > np_arr2
        
        for i in range(len(data1)):
            assert arr_gt[i] == np_gt[i]
        
        # Test less than or equal
        arr_le = arr1 <= arr2
        np_le = np_arr1 <= np_arr2
        
        for i in range(len(data1)):
            assert arr_le[i] == np_le[i]


class TestEdgeCaseCompatibility:
    """Test that edge cases match NumPy behavior."""
    
    def test_empty_array_compatibility(self):
        """Test that empty arrays behave like NumPy."""
        arr = Array([])
        np_arr = np.array([])
        
        assert arr.shape == np_arr.shape
        assert arr.ndim == np_arr.ndim
        assert arr.size == np_arr.size
        
        # Test operations on empty arrays
        arr_plus = arr + 5
        np_plus = np_arr + 5
        
        assert arr_plus.shape == np_plus.shape
        assert arr_plus.size == np_plus.size
    
    def test_single_element_compatibility(self):
        """Test single-element arrays match NumPy."""
        arr = Array([42])
        np_arr = np.array([42])
        
        assert arr.shape == np_arr.shape
        assert arr[0] == np_arr[0]
        
        # Test operations
        arr_mult = arr * 2
        np_mult = np_arr * 2
        
        assert arr_mult[0] == np_mult[0]
    
    def test_type_preservation_compatibility(self):
        """Test that type behavior matches NumPy where possible."""
        # Integer array
        int_arr = Array([1, 2, 3])
        np_int_arr = np.array([1, 2, 3])
        
        # Float array  
        float_arr = Array([1.1, 2.2, 3.3])
        np_float_arr = np.array([1.1, 2.2, 3.3])
        
        # Boolean array
        bool_arr = Array([True, False, True])
        np_bool_arr = np.array([True, False, True])
        
        # Check that basic operations preserve types similarly
        # Note: ArrPy might use Python native types vs NumPy types
        try:
            assert isinstance(int_arr[0], type(np_int_arr[0]))
        except AssertionError:
            # ArrPy uses Python int, NumPy uses numpy.int64
            assert isinstance(int_arr[0], int)
        
        try:
            assert isinstance(float_arr[0], type(np_float_arr[0]))
        except AssertionError:
            assert isinstance(float_arr[0], float)
        
        try:
            assert isinstance(bool_arr[0], type(np_bool_arr[0]))
        except AssertionError:
            assert isinstance(bool_arr[0], bool)


class TestErrorCompatibility:
    """Test that errors match NumPy behavior."""
    
    def test_shape_mismatch_errors(self):
        """Test that shape mismatch errors are similar to NumPy."""
        arr1 = Array([1, 2, 3])
        arr2 = Array([1, 2])
        
        np_arr1 = np.array([1, 2, 3])
        np_arr2 = np.array([1, 2])
        
        # Both should raise errors for shape mismatch
        with pytest.raises(ValueError):
            arr1 + arr2
        
        with pytest.raises(ValueError):
            np_arr1 + np_arr2
    
    def test_index_error_compatibility(self):
        """Test that index errors are similar to NumPy."""
        arr = Array([1, 2, 3])
        np_arr = np.array([1, 2, 3])
        
        # Both should raise IndexError for out of bounds
        with pytest.raises(IndexError):
            arr[5]
        
        with pytest.raises(IndexError):
            np_arr[5]
    
    def test_reshape_error_compatibility(self):
        """Test that reshape errors are similar to NumPy."""
        arr = Array([1, 2, 3, 4])
        np_arr = np.array([1, 2, 3, 4])
        
        # Both should raise error for incompatible reshape
        with pytest.raises(ValueError):
            arr.reshape((2, 3))
        
        with pytest.raises(ValueError):
            np_arr.reshape((2, 3))


class TestNumericalPrecisionCompatibility:
    """Test numerical precision matches NumPy where possible."""
    
    def test_floating_point_precision(self):
        """Test that floating point operations have similar precision."""
        data = [0.1, 0.2, 0.3]
        
        arr = Array(data)
        np_arr = np.array(data)
        
        arr_sum = arr.sum()
        np_sum = np_arr.sum()
        
        # Should have similar precision (within reasonable tolerance)
        assert abs(arr_sum - np_sum) < 1e-15
    
    def test_trigonometric_precision(self):
        """Test trigonometric function precision."""
        # Test with values that might have precision issues
        data = [math.pi, 2*math.pi, math.pi/2]
        
        arr = Array(data)
        np_arr = np.array(data)
        
        arr_sin = ap.sin(arr)
        np_sin = np.sin(np_arr)
        
        for i in range(len(data)):
            # Allow for small numerical differences
            assert abs(arr_sin[i] - np_sin[i]) < 1e-14