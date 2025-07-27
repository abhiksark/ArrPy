import pytest
import numpy as np
from arrpy import Array


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
    
    def test_transpose_non_2d_error(self):
        arr = Array([1, 2, 3])
        with pytest.raises(ValueError, match="Transpose is only supported for 2D arrays"):
            arr.T


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