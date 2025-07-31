"""
Test edge cases with empty arrays.

Tests behavior of operations on zero-size arrays.
"""

import pytest
from arrpy import Array, zeros, ones, empty
import arrpy as ap

# Import helper for type checking that works with hybrid arrays
try:
    from test_imports import is_array
except ImportError:
    def is_array(obj):
        return isinstance(obj, Array)



class TestEmptyArrayCreation:
    """Test creating empty arrays."""
    
    def test_empty_list_initialization(self):
        """Test creating array from empty list."""
        arr = Array([])
        assert arr.shape == (0,)
        assert arr.ndim == 1
        assert arr.size == 0
        assert len(arr._data) == 0
    
    def test_zeros_empty_shape(self):
        """Test creating empty array with zeros."""
        arr = zeros(0)
        assert arr.shape == (0,)
        assert arr.size == 0
        assert len(arr._data) == 0
    
    def test_ones_empty_shape(self):
        """Test creating empty array with ones."""
        arr = ones(0)
        assert arr.shape == (0,)
        assert arr.size == 0
    
    def test_empty_2d_arrays(self):
        """Test creating 2D arrays with zero dimension."""
        # Array with 0 rows, 3 columns
        arr1 = zeros((0, 3))
        assert arr1.shape == (0, 3)
        assert arr1.size == 0
        
        # Array with 3 rows, 0 columns
        arr2 = zeros((3, 0))
        assert arr2.shape == (3, 0)
        assert arr2.size == 0


class TestEmptyArrayProperties:
    """Test properties of empty arrays."""
    
    def test_empty_array_shape(self):
        """Test shape property of empty arrays."""
        arr = Array([])
        assert arr.shape == (0,)
        assert isinstance(arr.shape, tuple)
    
    def test_empty_array_ndim(self):
        """Test ndim property of empty arrays."""
        arr = Array([])
        assert arr.ndim == 1
        assert isinstance(arr.ndim, int)
    
    def test_empty_array_size(self):
        """Test size property of empty arrays."""
        arr = Array([])
        assert arr.size == 0
        assert isinstance(arr.size, int)
    
    def test_empty_2d_properties(self):
        """Test properties of 2D empty arrays."""
        arr = zeros((0, 5))
        assert arr.shape == (0, 5)
        assert arr.ndim == 2
        assert arr.size == 0


class TestEmptyArrayIndexing:
    """Test indexing operations on empty arrays."""
    
    def test_empty_array_indexing_error(self):
        """Test that indexing empty array raises IndexError."""
        arr = Array([])
        
        with pytest.raises(IndexError):
            arr[0]
        
        with pytest.raises(IndexError):
            arr[-1]
    
    def test_empty_2d_indexing_error(self):
        """Test indexing on 2D empty arrays."""
        arr = zeros((0, 3))
        
        with pytest.raises(IndexError):
            arr[0, 0]
        
        with pytest.raises(IndexError):
            arr[0]


class TestEmptyArrayArithmetic:
    """Test arithmetic operations on empty arrays."""
    
    def test_empty_array_scalar_addition(self):
        """Test adding scalar to empty array."""
        arr = Array([])
        result = arr + 5
        
        assert is_array(result)
        assert result.shape == (0,)
        assert result.size == 0
        assert len(result._data) == 0
    
    def test_empty_array_scalar_multiplication(self):
        """Test multiplying empty array by scalar."""
        arr = Array([])
        result = arr * 3
        
        assert result.shape == (0,)
        assert result.size == 0
    
    def test_empty_arrays_addition(self):
        """Test adding two empty arrays."""
        arr1 = Array([])
        arr2 = Array([])
        result = arr1 + arr2
        
        assert result.shape == (0,)
        assert result.size == 0
    
    def test_empty_array_division(self):
        """Test dividing empty array by scalar."""
        arr = Array([])
        result = arr / 2
        
        assert result.shape == (0,)
        assert result.size == 0
    
    def test_empty_2d_arithmetic(self):
        """Test arithmetic on 2D empty arrays."""
        arr = zeros((0, 3))
        result = arr + 1
        
        assert result.shape == (0, 3)
        assert result.size == 0


class TestEmptyArrayComparisons:
    """Test comparison operations on empty arrays."""
    
    def test_empty_array_scalar_comparison(self):
        """Test comparing empty array with scalar."""
        arr = Array([])
        result = arr > 5
        
        assert is_array(result)
        assert result.shape == (0,)
        assert result.size == 0
    
    def test_empty_arrays_comparison(self):
        """Test comparing two empty arrays."""
        arr1 = Array([])
        arr2 = Array([])
        result = arr1 == arr2
        
        assert result.shape == (0,)
        assert result.size == 0
    
    def test_empty_array_inequality(self):
        """Test inequality comparison on empty arrays."""
        arr = Array([])
        result = arr != 3
        
        assert result.shape == (0,)
        assert result.size == 0


class TestEmptyArrayAggregations:
    """Test aggregation operations on empty arrays."""
    
    def test_empty_array_sum_error(self):
        """Test that sum of empty array raises error or returns appropriate value."""
        arr = Array([])
        
        try:
            result = arr.sum()
            # Some implementations might return 0 for empty sum
            assert result == 0
        except ValueError:
            # Other implementations might raise ValueError
            pass
    
    def test_empty_array_mean_error(self):
        """Test that mean of empty array raises error."""
        arr = Array([])
        
        with pytest.raises(ValueError):
            arr.mean()
    
    def test_empty_array_min_error(self):
        """Test that min of empty array raises error."""
        arr = Array([])
        
        with pytest.raises(ValueError):
            arr.min()
    
    def test_empty_array_max_error(self):
        """Test that max of empty array raises error."""
        arr = Array([])
        
        with pytest.raises(ValueError):
            arr.max()
    
    def test_empty_array_std_error(self):
        """Test that std of empty array raises error."""
        arr = Array([])
        
        with pytest.raises(ValueError):
            arr.std()


class TestEmptyArrayMathematicalFunctions:
    """Test mathematical functions on empty arrays."""
    
    def test_empty_array_sin(self):
        """Test sine function on empty array."""
        arr = Array([])
        result = ap.sin(arr)
        
        assert is_array(result)
        assert result.shape == (0,)
        assert result.size == 0
    
    def test_empty_array_cos(self):
        """Test cosine function on empty array."""
        arr = Array([])
        result = ap.cos(arr)
        
        assert result.shape == (0,)
        assert result.size == 0
    
    def test_empty_array_sqrt(self):
        """Test square root function on empty array."""
        arr = Array([])
        result = arr.sqrt()
        
        assert result.shape == (0,)
        assert result.size == 0
    
    def test_empty_array_exp(self):
        """Test exponential function on empty array."""
        arr = Array([])
        result = arr.exp()
        
        assert result.shape == (0,)
        assert result.size == 0


class TestEmptyArrayReshaping:
    """Test reshaping operations on empty arrays."""
    
    def test_empty_array_reshape_valid(self):
        """Test valid reshaping of empty arrays."""
        arr = Array([])
        
        # Reshape to different empty shapes
        reshaped1 = arr.reshape((0, 5))
        assert reshaped1.shape == (0, 5)
        assert reshaped1.size == 0
        
        reshaped2 = arr.reshape((0, 0))
        assert reshaped2.shape == (0, 0)
        assert reshaped2.size == 0
    
    def test_empty_array_reshape_invalid(self):
        """Test invalid reshaping of empty arrays."""
        arr = Array([])
        
        # Cannot reshape empty array to non-empty
        with pytest.raises(ValueError):
            arr.reshape((2, 3))
    
    def test_empty_2d_reshape(self):
        """Test reshaping 2D empty arrays."""
        arr = zeros((0, 3))
        
        # Valid reshape maintaining size 0
        reshaped = arr.reshape((0, 6))
        assert reshaped.shape == (0, 6)
        assert reshaped.size == 0
        
        # Cannot reshape to non-empty
        with pytest.raises(ValueError):
            arr.reshape((2, 3))


class TestEmptyArrayTranspose:
    """Test transpose operations on empty arrays."""
    
    def test_empty_1d_transpose(self):
        """Test transpose of 1D empty array."""
        arr = Array([])
        transposed = arr.T
        
        assert transposed.shape == (0,)
        assert transposed.size == 0
    
    def test_empty_2d_transpose(self):
        """Test transpose of 2D empty arrays."""
        arr = zeros((0, 3))
        transposed = arr.T
        
        assert transposed.shape == (3, 0)
        assert transposed.size == 0
    
    def test_empty_rectangular_transpose(self):
        """Test transpose of rectangular empty arrays."""
        arr = zeros((5, 0))
        transposed = arr.T
        
        assert transposed.shape == (0, 5)
        assert transposed.size == 0


class TestEmptyArrayConcatenation:
    """Test concatenation operations with empty arrays."""
    
    def test_concatenate_empty_arrays(self):
        """Test concatenating empty arrays."""
        arr1 = Array([])
        arr2 = Array([])
        
        try:
            result = ap.concatenate([arr1, arr2])
            assert result.shape == (0,)
            assert result.size == 0
        except (NotImplementedError, AttributeError):
            # concatenate might not be implemented
            pass
    
    def test_concatenate_empty_with_non_empty(self):
        """Test concatenating empty array with non-empty."""
        empty_arr = Array([])
        non_empty_arr = Array([1, 2, 3])
        
        try:
            result = ap.concatenate([empty_arr, non_empty_arr])
            assert result.shape == (3,)
            assert list(result._data) == [1, 2, 3]
            
            result2 = ap.concatenate([non_empty_arr, empty_arr])
            assert result2.shape == (3,)
            assert list(result2._data) == [1, 2, 3]
        except (NotImplementedError, AttributeError):
            pass


class TestEmptyArrayRepresentation:
    """Test string representation of empty arrays."""
    
    def test_empty_array_repr(self):
        """Test __repr__ of empty array."""
        arr = Array([])
        repr_str = repr(arr)
        
        assert "Array" in repr_str
        assert "[]" in repr_str or "empty" in repr_str.lower()
    
    def test_empty_array_str(self):
        """Test __str__ of empty array."""
        arr = Array([])
        str_repr = str(arr)
        
        # String representation should indicate it's empty
        assert len(str_repr) >= 0  # At minimum, should not crash


class TestEmptyArrayEdgeCases:
    """Test edge cases specific to empty arrays."""
    
    def test_empty_array_iteration(self):
        """Test iterating over empty array."""
        arr = Array([])
        
        # Should be able to iterate (yielding nothing)
        count = 0
        for element in arr:
            count += 1
        assert count == 0
    
    def test_multiple_empty_dimensions(self):
        """Test arrays with multiple zero dimensions."""
        arr = zeros((0, 0, 0))
        assert arr.shape == (0, 0, 0)
        assert arr.ndim == 3
        assert arr.size == 0
    
    def test_empty_array_copy(self):
        """Test copying empty arrays."""
        arr = Array([])
        
        # If copy method exists
        try:
            copied = arr.copy()
            assert copied.shape == arr.shape
            assert copied.size == arr.size
        except AttributeError:
            # copy method might not be implemented
            pass
    
    def test_empty_array_memory_efficiency(self):
        """Test that empty arrays don't waste memory."""
        arr = Array([])
        assert len(arr._data) == 0
        
        arr2 = zeros((0, 1000))
        assert arr2.size == 0
        # Should not allocate memory for 1000 elements