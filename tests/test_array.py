import pytest
import numpy as np
import math
import arrpy as ap
from arrpy import (
    Array, array, zeros, ones, empty, full, eye, identity, 
    arange, linspace, logspace, concatenate, vstack, hstack,
    sin, cos, tan, arcsin, arccos, arctan, exp, log, log10, log2, sqrt,
    power, absolute, sign, floor_divide, mod, floor, ceil, round, trunc,
    sum, mean, min, max, std, var, median, percentile, prod, cumsum, cumprod, argmin, argmax,
    reshape, transpose, squeeze, expand_dims, stack
)


class TestArrayInitialization:
    def test_1d_initialization(self):
        arr = Array([1, 2, 3])
        assert arr.shape == (3,)
        assert arr[0] == 1
        assert arr[1] == 2
        assert arr[2] == 3
    
    def test_2d_initialization(self):
        arr = Array([[1, 2], [3, 4]])
        assert arr.shape == (2, 2)
        assert arr[0, 0] == 1
        assert arr[0, 1] == 2
        assert arr[1, 0] == 3
        assert arr[1, 1] == 4
    
    def test_3d_initialization(self):
        arr = Array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        assert arr.shape == (2, 2, 2)
        assert arr[0, 0, 0] == 1
        assert arr[1, 1, 1] == 8
    
    def test_empty_array(self):
        arr = Array([])
        assert arr.shape == (0,)
    
    def test_ragged_array_error(self):
        with pytest.raises(ValueError, match="ragged"):
            Array([[1, 2], [3, 4, 5]])
    
    def test_invalid_input_type(self):
        with pytest.raises(TypeError):
            Array("not a list")


class TestArrayIndexing:
    def test_1d_indexing(self):
        arr = Array([1, 2, 3, 4, 5])
        assert arr[0] == 1
        assert arr[4] == 5
    
    def test_2d_indexing(self):
        arr = Array([[1, 2, 3], [4, 5, 6]])
        assert arr[0, 0] == 1
        assert arr[0, 2] == 3
        assert arr[1, 1] == 5
    
    def test_single_index_on_2d_returns_subarray(self):
        arr = Array([[1, 2], [3, 4]])
        sub = arr[0]
        assert sub.shape == (2,)
        assert sub[0] == 1
        assert sub[1] == 2
    
    def test_index_out_of_bounds(self):
        arr = Array([1, 2, 3])
        with pytest.raises(IndexError):
            arr[5]
    
    def test_wrong_number_of_indices(self):
        arr = Array([[1, 2], [3, 4]])
        with pytest.raises(IndexError):
            arr[0, 1, 2]


class TestArraySetItem:
    def test_1d_setitem(self):
        arr = Array([1, 2, 3])
        arr[1] = 10
        assert arr[1] == 10
    
    def test_2d_setitem(self):
        arr = Array([[1, 2], [3, 4]])
        arr[0, 1] = 10
        assert arr[0, 1] == 10
    
    def test_setitem_index_error(self):
        arr = Array([1, 2, 3])
        with pytest.raises(IndexError):
            arr[5] = 10


class TestArrayArithmetic:
    def test_scalar_addition(self):
        arr = Array([1, 2, 3])
        result = arr + 5
        expected = [6, 7, 8]
        for i in range(3):
            assert result[i] == expected[i]
    
    def test_array_addition(self):
        arr1 = Array([1, 2, 3])
        arr2 = Array([4, 5, 6])
        result = arr1 + arr2
        expected = [5, 7, 9]
        for i in range(3):
            assert result[i] == expected[i]
    
    def test_scalar_subtraction(self):
        arr = Array([5, 6, 7])
        result = arr - 2
        expected = [3, 4, 5]
        for i in range(3):
            assert result[i] == expected[i]
    
    def test_array_subtraction(self):
        arr1 = Array([5, 6, 7])
        arr2 = Array([1, 2, 3])
        result = arr1 - arr2
        expected = [4, 4, 4]
        for i in range(3):
            assert result[i] == expected[i]
    
    def test_scalar_multiplication(self):
        arr = Array([1, 2, 3])
        result = arr * 3
        expected = [3, 6, 9]
        for i in range(3):
            assert result[i] == expected[i]
    
    def test_array_multiplication(self):
        arr1 = Array([2, 3, 4])
        arr2 = Array([1, 2, 3])
        result = arr1 * arr2
        expected = [2, 6, 12]
        for i in range(3):
            assert result[i] == expected[i]
    
    def test_scalar_division(self):
        arr = Array([6, 8, 10])
        result = arr / 2
        expected = [3, 4, 5]
        for i in range(3):
            assert result[i] == expected[i]
    
    def test_array_division(self):
        arr1 = Array([6, 8, 10])
        arr2 = Array([2, 4, 5])
        result = arr1 / arr2
        expected = [3, 2, 2]
        for i in range(3):
            assert result[i] == expected[i]
    
    def test_shape_mismatch_error(self):
        arr1 = Array([1, 2, 3])
        arr2 = Array([1, 2])
        with pytest.raises(ValueError, match="Shape mismatch"):
            arr1 + arr2


class TestArrayReshape:
    def test_reshape_1d_to_2d(self):
        arr = Array([1, 2, 3, 4, 5, 6])
        reshaped = arr.reshape((2, 3))
        assert reshaped.shape == (2, 3)
        assert reshaped[0, 0] == 1
        assert reshaped[1, 2] == 6
    
    def test_reshape_2d_to_1d(self):
        arr = Array([[1, 2], [3, 4]])
        reshaped = arr.reshape((4,))
        assert reshaped.shape == (4,)
        assert reshaped[0] == 1
        assert reshaped[3] == 4
    
    def test_reshape_with_int(self):
        arr = Array([1, 2, 3, 4])
        reshaped = arr.reshape(4)
        assert reshaped.shape == (4,)
    
    def test_reshape_invalid_size(self):
        arr = Array([1, 2, 3, 4])
        with pytest.raises(ValueError, match="Cannot reshape"):
            arr.reshape((2, 3))


class TestArrayTranspose:
    def test_2d_transpose(self):
        arr = Array([[1, 2, 3], [4, 5, 6]])
        transposed = arr.T
        assert transposed.shape == (3, 2)
        assert transposed[0, 0] == 1
        assert transposed[0, 1] == 4
        assert transposed[2, 1] == 6
    
    def test_transpose_1d_behavior(self):
        # 1D transpose should return a copy of itself
        arr = Array([1, 2, 3])
        transposed = arr.T
        assert transposed.shape == (3,)
        assert list(transposed._data) == [1, 2, 3]


class TestArrayDot:
    def test_matrix_multiplication(self):
        arr1 = Array([[1, 2], [3, 4]])
        arr2 = Array([[5, 6], [7, 8]])
        result = arr1.dot(arr2)
        
        # Expected: [[1*5+2*7, 1*6+2*8], [3*5+4*7, 3*6+4*8]]
        #          = [[19, 22], [43, 50]]
        assert result.shape == (2, 2)
        assert result[0, 0] == 19
        assert result[0, 1] == 22
        assert result[1, 0] == 43
        assert result[1, 1] == 50
    
    def test_dot_incompatible_shapes(self):
        arr1 = Array([[1, 2, 3]])  # 1x3
        arr2 = Array([[1, 2]])     # 1x2
        with pytest.raises(ValueError, match="Cannot multiply"):
            arr1.dot(arr2)
    
    def test_dot_non_array_error(self):
        arr = Array([[1, 2], [3, 4]])
        with pytest.raises(TypeError, match="Dot product requires another Array"):
            arr.dot([[1, 2], [3, 4]])
    
    def test_dot_non_2d_error(self):
        arr1 = Array([1, 2, 3])
        arr2 = Array([4, 5, 6])
        with pytest.raises(ValueError, match="Dot product requires 2D arrays"):
            arr1.dot(arr2)


class TestArrayAggregations:
    def test_sum_1d(self):
        arr = Array([1, 2, 3, 4, 5])
        assert arr.sum() == 15
    
    def test_sum_2d(self):
        arr = Array([[1, 2], [3, 4]])
        assert arr.sum() == 10
    
    def test_mean_1d(self):
        arr = Array([2, 4, 6, 8])
        assert arr.mean() == 5.0
    
    def test_mean_2d(self):
        arr = Array([[1, 2], [3, 4]])
        assert arr.mean() == 2.5
    
    def test_mean_empty_array_error(self):
        arr = Array([])
        with pytest.raises(ValueError, match="Cannot calculate mean of empty array"):
            arr.mean()


class TestArrayRepresentation:
    def test_1d_repr(self):
        arr = Array([1, 2, 3])
        repr_str = repr(arr)
        assert "Array" in repr_str
        assert "[1, 2, 3]" in repr_str
    
    def test_2d_repr(self):
        arr = Array([[1, 2], [3, 4]])
        repr_str = repr(arr)
        assert "Array" in repr_str
    
    def test_empty_array_repr(self):
        arr = Array([])
        assert repr(arr) == "Array([])"


class TestComparisonWithNumPy:
    """Test that our Array behavior matches NumPy where applicable"""
    
    def test_addition_comparison(self):
        data = [[1, 2], [3, 4]]
        arr = Array(data)
        np_arr = np.array(data)
        
        # Scalar addition
        result = arr + 10
        np_result = np_arr + 10
        
        for i in range(2):
            for j in range(2):
                assert result[i, j] == np_result[i, j]
    
    def test_matrix_multiplication_comparison(self):
        data1 = [[1, 2], [3, 4]]
        data2 = [[5, 6], [7, 8]]
        
        arr1 = Array(data1)
        arr2 = Array(data2)
        np_arr1 = np.array(data1)
        np_arr2 = np.array(data2)
        
        result = arr1.dot(arr2)
        np_result = np_arr1.dot(np_arr2)
        
        for i in range(2):
            for j in range(2):
                assert result[i, j] == np_result[i, j]
    
    def test_transpose_comparison(self):
        data = [[1, 2, 3], [4, 5, 6]]
        arr = Array(data)
        np_arr = np.array(data)
        
        result = arr.T
        np_result = np_arr.T
        
        assert result.shape == np_result.shape
        for i in range(np_result.shape[0]):
            for j in range(np_result.shape[1]):
                assert result[i, j] == np_result[i, j]
    
    def test_reshape_comparison(self):
        data = [1, 2, 3, 4, 5, 6]
        arr = Array(data)
        np_arr = np.array(data)
        
        result = arr.reshape((2, 3))
        np_result = np_arr.reshape((2, 3))
        
        assert result.shape == np_result.shape
        for i in range(2):
            for j in range(3):
                assert result[i, j] == np_result[i, j]


class TestArrayCreationFunctions:
    def test_zeros_1d(self):
        arr = zeros(5)
        assert arr.shape == (5,)
        for i in range(5):
            assert arr[i] == 0
    
    def test_zeros_2d(self):
        arr = zeros((2, 3))
        assert arr.shape == (2, 3)
        for i in range(2):
            for j in range(3):
                assert arr[i, j] == 0
    
    def test_ones_1d(self):
        arr = ones(4)
        assert arr.shape == (4,)
        for i in range(4):
            assert arr[i] == 1
    
    def test_ones_2d(self):
        arr = ones((3, 2))
        assert arr.shape == (3, 2)
        for i in range(3):
            for j in range(2):
                assert arr[i, j] == 1
    
    def test_eye_square(self):
        arr = eye(3)
        assert arr.shape == (3, 3)
        for i in range(3):
            for j in range(3):
                if i == j:
                    assert arr[i, j] == 1
                else:
                    assert arr[i, j] == 0
    
    def test_eye_rectangular(self):
        arr = eye(2, 4)
        assert arr.shape == (2, 4)
        for i in range(2):
            for j in range(4):
                if i == j:
                    assert arr[i, j] == 1
                else:
                    assert arr[i, j] == 0
    
    def test_arange_default_start(self):
        arr = arange(5)
        assert arr.shape == (5,)
        expected = [0, 1, 2, 3, 4]
        for i in range(5):
            assert arr[i] == expected[i]
    
    def test_arange_with_start_stop(self):
        arr = arange(2, 7)
        assert arr.shape == (5,)
        expected = [2, 3, 4, 5, 6]
        for i in range(5):
            assert arr[i] == expected[i]
    
    def test_arange_with_step(self):
        arr = arange(0, 10, 2)
        assert arr.shape == (5,)
        expected = [0, 2, 4, 6, 8]
        for i in range(5):
            assert arr[i] == expected[i]
    
    def test_linspace_default(self):
        arr = linspace(0, 1, 11)
        assert arr.shape == (11,)
        assert arr[0] == 0
        assert arr[10] == 1
        assert abs(arr[5] - 0.5) < 1e-10
    
    def test_linspace_single_point(self):
        arr = linspace(5, 10, 1)
        assert arr.shape == (1,)
        assert arr[0] == 5


class TestExtendedAggregations:
    def test_min_1d(self):
        arr = Array([3, 1, 4, 1, 5])
        assert arr.min() == 1
    
    def test_max_1d(self):
        arr = Array([3, 1, 4, 1, 5])
        assert arr.max() == 5
    
    def test_std_calculation(self):
        arr = Array([1, 2, 3, 4, 5])
        # Use Python's built-in sum for the expected calculation
        expected_std = math.sqrt(__builtins__['sum']((x - 3) ** 2 for x in [1, 2, 3, 4, 5]) / 5)
        assert abs(arr.std() - expected_std) < 1e-10
    
    def test_var_calculation(self):
        arr = Array([1, 2, 3, 4, 5])
        # Use Python's built-in sum for the expected calculation  
        expected_var = __builtins__['sum']((x - 3) ** 2 for x in [1, 2, 3, 4, 5]) / 5
        assert abs(arr.var() - expected_var) < 1e-10
    
    def test_median_odd_length(self):
        arr = Array([1, 3, 2, 5, 4])
        assert arr.median() == 3
    
    def test_median_even_length(self):
        arr = Array([1, 2, 3, 4])
        assert arr.median() == 2.5
    
    def test_percentile_0(self):
        arr = Array([1, 2, 3, 4, 5])
        assert arr.percentile(0) == 1
    
    def test_percentile_100(self):
        arr = Array([1, 2, 3, 4, 5])
        assert arr.percentile(100) == 5
    
    def test_percentile_50(self):
        arr = Array([1, 2, 3, 4, 5])
        assert arr.percentile(50) == 3
    
    def test_empty_array_errors(self):
        arr = Array([])
        with pytest.raises(ValueError):
            arr.min()
        with pytest.raises(ValueError):
            arr.max()
        with pytest.raises(ValueError):
            arr.std()
        with pytest.raises(ValueError):
            arr.var()
        with pytest.raises(ValueError):
            arr.median()
        with pytest.raises(ValueError):
            arr.percentile(50)


class TestMathematicalFunctions:
    def test_sqrt(self):
        arr = Array([1, 4, 9, 16])
        result = arr.sqrt()
        expected = [1, 2, 3, 4]
        for i in range(4):
            assert abs(result[i] - expected[i]) < 1e-10
    
    def test_sin(self):
        arr = Array([0, math.pi/2, math.pi])
        result = arr.sin()
        expected = [0, 1, 0]
        for i in range(3):
            assert abs(result[i] - expected[i]) < 1e-10
    
    def test_cos(self):
        arr = Array([0, math.pi/2, math.pi])
        result = arr.cos()
        expected = [1, 0, -1]
        for i in range(3):
            assert abs(result[i] - expected[i]) < 1e-10
    
    def test_exp(self):
        arr = Array([0, 1, 2])
        result = arr.exp()
        expected = [1, math.e, math.e**2]
        for i in range(3):
            assert abs(result[i] - expected[i]) < 1e-10
    
    def test_log(self):
        arr = Array([1, math.e, math.e**2])
        result = arr.log()
        expected = [0, 1, 2]
        for i in range(3):
            assert abs(result[i] - expected[i]) < 1e-10


class TestComparisonOperations:
    def test_equality(self):
        arr1 = Array([1, 2, 3])
        arr2 = Array([1, 0, 3])
        result = arr1 == arr2
        expected = [True, False, True]
        for i in range(3):
            assert result[i] == expected[i]
    
    def test_not_equal(self):
        arr1 = Array([1, 2, 3])
        arr2 = Array([1, 0, 3])
        result = arr1 != arr2
        expected = [False, True, False]
        for i in range(3):
            assert result[i] == expected[i]
    
    def test_greater_than(self):
        arr1 = Array([3, 1, 2])
        arr2 = Array([1, 2, 2])
        result = arr1 > arr2
        expected = [True, False, False]
        for i in range(3):
            assert result[i] == expected[i]
    
    def test_less_than(self):
        arr1 = Array([1, 3, 2])
        arr2 = Array([2, 2, 2])
        result = arr1 < arr2
        expected = [True, False, False]
        for i in range(3):
            assert result[i] == expected[i]
    
    def test_greater_equal(self):
        arr1 = Array([3, 2, 1])
        arr2 = Array([2, 2, 2])
        result = arr1 >= arr2
        expected = [True, True, False]
        for i in range(3):
            assert result[i] == expected[i]
    
    def test_less_equal(self):
        arr1 = Array([1, 2, 3])
        arr2 = Array([2, 2, 2])
        result = arr1 <= arr2
        expected = [True, True, False]
        for i in range(3):
            assert result[i] == expected[i]
    
    def test_scalar_comparison(self):
        arr = Array([1, 2, 3])
        result = arr > 2
        expected = [False, False, True]
        for i in range(3):
            assert result[i] == expected[i]


class TestLogicalOperations:
    def test_logical_and(self):
        arr1 = Array([True, True, False, False])
        arr2 = Array([True, False, True, False])
        result = arr1.logical_and(arr2)
        expected = [True, False, False, False]
        for i in range(4):
            assert result[i] == expected[i]
    
    def test_logical_or(self):
        arr1 = Array([True, True, False, False])
        arr2 = Array([True, False, True, False])
        result = arr1.logical_or(arr2)
        expected = [True, True, True, False]
        for i in range(4):
            assert result[i] == expected[i]
    
    def test_logical_not(self):
        arr = Array([True, False, True, False])
        result = arr.logical_not()
        expected = [False, True, False, True]
        for i in range(4):
            assert result[i] == expected[i]
    
    def test_logical_with_numbers(self):
        arr1 = Array([1, 0, 2, 0])
        arr2 = Array([3, 0, 0, 4])
        result = arr1.logical_and(arr2)
        expected = [True, False, False, False]
        for i in range(4):
            assert result[i] == expected[i]


class TestConcatenationFunctions:
    def test_concatenate_1d(self):
        arr1 = Array([1, 2])
        arr2 = Array([3, 4])
        result = concatenate([arr1, arr2])
        assert result.shape == (4,)
        expected = [1, 2, 3, 4]
        for i in range(4):
            assert result[i] == expected[i]
    
    def test_concatenate_2d_axis0(self):
        arr1 = Array([[1, 2], [3, 4]])
        arr2 = Array([[5, 6]])
        result = concatenate([arr1, arr2], axis=0)
        assert result.shape == (3, 2)
        assert result[0, 0] == 1
        assert result[2, 1] == 6
    
    def test_concatenate_2d_axis1(self):
        arr1 = Array([[1, 2], [3, 4]])
        arr2 = Array([[5], [6]])
        result = concatenate([arr1, arr2], axis=1)
        assert result.shape == (2, 3)
        assert result[0, 0] == 1
        assert result[1, 2] == 6
    
    def test_vstack(self):
        arr1 = Array([[1, 2]])
        arr2 = Array([[3, 4]])
        result = vstack([arr1, arr2])
        assert result.shape == (2, 2)
        assert result[0, 0] == 1
        assert result[1, 1] == 4
    
    def test_hstack_1d(self):
        arr1 = Array([1, 2])
        arr2 = Array([3, 4])
        result = hstack([arr1, arr2])
        assert result.shape == (4,)
        expected = [1, 2, 3, 4]
        for i in range(4):
            assert result[i] == expected[i]
    
    def test_hstack_2d(self):
        arr1 = Array([[1], [3]])
        arr2 = Array([[2], [4]])
        result = hstack([arr1, arr2])
        assert result.shape == (2, 2)
        assert result[0, 0] == 1
        assert result[1, 1] == 4
    
    def test_concatenate_errors(self):
        arr1 = Array([1, 2])
        arr2 = Array([[1, 2]])
        
        with pytest.raises(ValueError):
            concatenate([arr1, arr2])
        
        with pytest.raises(ValueError):
            concatenate([])
        
        with pytest.raises(TypeError):
            concatenate([arr1, [1, 2, 3]])