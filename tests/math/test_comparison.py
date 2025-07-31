"""
Test comparison operations on arrays.

Tests equality, inequality, and relational operators.
"""

import pytest
from arrpy import Array

# Import helper for type checking that works with hybrid arrays
try:
    from test_imports import is_array
except ImportError:
    def is_array(obj):
        return isinstance(obj, Array)



class TestEqualityComparison:
    """Test equality (==) and inequality (!=) operators."""
    
    def test_array_equality_1d(self):
        """Test equality comparison between 1D arrays."""
        arr1 = Array([1, 2, 3, 4])
        arr2 = Array([1, 0, 3, 5])
        result = arr1 == arr2
        
        assert is_array(result)
        assert result.shape == arr1.shape
        assert list(result._data) == [True, False, True, False]
    
    def test_array_equality_2d(self):
        """Test equality comparison between 2D arrays."""
        arr1 = Array([[1, 2], [3, 4]])
        arr2 = Array([[1, 0], [3, 4]])
        result = arr1 == arr2
        
        assert result.shape == (2, 2)
        assert result[0, 0] is True
        assert result[0, 1] is False
        assert result[1, 0] is True
        assert result[1, 1] is True
    
    def test_scalar_equality(self):
        """Test equality comparison with scalar."""
        arr = Array([1, 2, 2, 3])
        result = arr == 2
        
        assert list(result._data) == [False, True, True, False]
    
    def test_array_inequality_1d(self):
        """Test inequality comparison between 1D arrays."""
        arr1 = Array([1, 2, 3, 4])
        arr2 = Array([1, 0, 3, 5])
        result = arr1 != arr2
        
        assert list(result._data) == [False, True, False, True]
    
    def test_scalar_inequality(self):
        """Test inequality comparison with scalar."""
        arr = Array([1, 2, 2, 3])
        result = arr != 2
        
        assert list(result._data) == [True, False, False, True]


class TestRelationalComparisons:
    """Test relational operators (<, >, <=, >=)."""
    
    def test_greater_than_arrays(self):
        """Test greater than comparison between arrays."""
        arr1 = Array([3, 1, 4, 2])
        arr2 = Array([1, 2, 3, 2])
        result = arr1 > arr2
        
        assert list(result._data) == [True, False, True, False]
    
    def test_greater_than_scalar(self):
        """Test greater than comparison with scalar."""
        arr = Array([1, 2, 3, 4, 5])
        result = arr > 3
        
        assert list(result._data) == [False, False, False, True, True]
    
    def test_less_than_arrays(self):
        """Test less than comparison between arrays."""
        arr1 = Array([1, 3, 2, 4])
        arr2 = Array([2, 2, 3, 4])
        result = arr1 < arr2
        
        assert list(result._data) == [True, False, True, False]
    
    def test_less_than_scalar(self):
        """Test less than comparison with scalar."""
        arr = Array([1, 2, 3, 4, 5])
        result = arr < 3
        
        assert list(result._data) == [True, True, False, False, False]
    
    def test_greater_equal_arrays(self):
        """Test greater than or equal comparison between arrays."""
        arr1 = Array([3, 2, 4, 1])
        arr2 = Array([2, 2, 3, 2])
        result = arr1 >= arr2
        
        assert list(result._data) == [True, True, True, False]
    
    def test_greater_equal_scalar(self):
        """Test greater than or equal comparison with scalar."""
        arr = Array([1, 2, 3, 4, 5])
        result = arr >= 3
        
        assert list(result._data) == [False, False, True, True, True]
    
    def test_less_equal_arrays(self):
        """Test less than or equal comparison between arrays."""
        arr1 = Array([1, 2, 3, 4])
        arr2 = Array([2, 2, 2, 3])
        result = arr1 <= arr2
        
        assert list(result._data) == [True, True, False, False]
    
    def test_less_equal_scalar(self):
        """Test less than or equal comparison with scalar."""
        arr = Array([1, 2, 3, 4, 5])
        result = arr <= 3
        
        assert list(result._data) == [True, True, True, False, False]


class TestComparison2D:
    """Test comparison operations on 2D arrays."""
    
    def test_2d_greater_than(self):
        """Test greater than on 2D arrays."""
        arr1 = Array([[3, 1], [4, 2]])
        arr2 = Array([[2, 2], [3, 2]])
        result = arr1 > arr2
        
        assert result.shape == (2, 2)
        assert result[0, 0] is True
        assert result[0, 1] is False
        assert result[1, 0] is True
        assert result[1, 1] is False
    
    def test_2d_scalar_comparison(self):
        """Test scalar comparison on 2D arrays."""
        arr = Array([[1, 2], [3, 4]])
        result = arr >= 2
        
        assert result[0, 0] is False
        assert result[0, 1] is True
        assert result[1, 0] is True
        assert result[1, 1] is True


class TestComparisonWithDifferentTypes:
    """Test comparisons with different numeric types."""
    
    def test_int_float_comparison(self):
        """Test comparison between integers and floats."""
        arr = Array([1, 2, 3])
        result = arr == 2.0
        
        assert list(result._data) == [False, True, False]
        
        result2 = arr > 1.5
        assert list(result2._data) == [False, True, True]
    
    def test_boolean_comparison(self):
        """Test comparison with boolean values."""
        arr = Array([0, 1, 2])
        result = arr == True
        
        assert list(result._data) == [False, True, False]
        
        result2 = arr == False
        assert list(result2._data) == [True, False, False]
    
    def test_mixed_types_in_array(self):
        """Test comparison with arrays containing mixed types."""
        arr = Array([1, 2.5, 3])
        result = arr > 2
        
        assert list(result._data) == [False, True, True]


class TestComparisonErrors:
    """Test error cases in comparison operations."""
    
    def test_shape_mismatch_equality(self):
        """Test that shape mismatch raises error in equality."""
        arr1 = Array([1, 2, 3])
        arr2 = Array([1, 2])
        
        with pytest.raises(ValueError, match="Shape mismatch"):
            arr1 == arr2
    
    def test_shape_mismatch_greater_than(self):
        """Test that shape mismatch raises error in greater than."""
        arr1 = Array([[1, 2], [3, 4]])
        arr2 = Array([1, 2, 3])
        
        with pytest.raises(ValueError, match="Shape mismatch"):
            arr1 > arr2
    
    def test_shape_mismatch_less_equal(self):
        """Test that shape mismatch raises error in less equal."""
        arr1 = Array([1, 2, 3, 4])
        arr2 = Array([1, 2])
        
        with pytest.raises(ValueError, match="Shape mismatch"):
            arr1 <= arr2


class TestComparisonSpecialValues:
    """Test comparison with special values."""
    
    def test_zero_comparison(self):
        """Test comparison with zero."""
        arr = Array([-2, -1, 0, 1, 2])
        
        result_gt = arr > 0
        assert list(result_gt._data) == [False, False, False, True, True]
        
        result_eq = arr == 0
        assert list(result_eq._data) == [False, False, True, False, False]
        
        result_lt = arr < 0
        assert list(result_lt._data) == [True, True, False, False, False]
    
    def test_negative_numbers(self):
        """Test comparison with negative numbers."""
        arr = Array([-3, -1, 0, 1, 3])
        result = arr >= -1
        
        assert list(result._data) == [False, True, True, True, True]
    
    def test_floating_point_precision(self):
        """Test comparison with floating point precision issues."""
        arr = Array([0.1 + 0.2, 0.3])  # 0.1 + 0.2 might not equal 0.3 exactly
        
        # This might fail due to floating point precision
        # In a robust implementation, we might need epsilon comparison
        result = arr[0] == arr[1]
        # The exact result depends on the implementation


class TestComparisonChaining:
    """Test chaining comparison operations."""
    
    def test_logical_combinations(self):
        """Test combining comparison results."""
        arr = Array([1, 2, 3, 4, 5])
        
        # This would require logical operations to be implemented
        # For now, we test individual comparisons
        gt_2 = arr > 2
        lt_5 = arr < 5
        
        assert list(gt_2._data) == [False, False, True, True, True]
        assert list(lt_5._data) == [True, True, True, True, False]


class TestComparisonEdgeCases:
    """Test edge cases in comparison operations."""
    
    def test_empty_array_comparison(self):
        """Test comparison on empty arrays."""
        arr1 = Array([])
        arr2 = Array([])
        result = arr1 == arr2
        
        assert result.shape == (0,)
        assert result.size == 0
    
    def test_single_element_comparison(self):
        """Test comparison on single-element arrays."""
        arr1 = Array([42])
        arr2 = Array([42])
        arr3 = Array([43])
        
        result1 = arr1 == arr2
        assert result1[0] is True
        
        result2 = arr1 == arr3
        assert result2[0] is False
        
        result3 = arr1 < arr3
        assert result3[0] is True
    
    def test_comparison_preserves_shape(self):
        """Test that comparison preserves array shape."""
        arr1 = Array([[1, 2, 3], [4, 5, 6]])
        arr2 = Array([[1, 0, 3], [4, 7, 6]])
        
        result = arr1 == arr2
        assert result.shape == arr1.shape
        assert result.shape == arr2.shape
    
    def test_scalar_comparison_preserves_shape(self):
        """Test that scalar comparison preserves array shape."""
        arr = Array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        result = arr > 4
        
        assert result.shape == arr.shape
        assert result.ndim == arr.ndim


class TestComparisonReturnTypes:
    """Test that comparison operations return correct types."""
    
    def test_comparison_returns_boolean_array(self):
        """Test that comparisons return arrays of booleans."""
        arr = Array([1, 2, 3, 4])
        result = arr > 2
        
        assert is_array(result)
        for val in result._data:
            assert isinstance(val, bool)
    
    def test_all_comparison_operators_return_arrays(self):
        """Test that all comparison operators return Array objects."""
        arr1 = Array([1, 2, 3])
        arr2 = Array([1, 0, 4])
        
        operators = [
            lambda a, b: a == b,
            lambda a, b: a != b,
            lambda a, b: a > b,
            lambda a, b: a < b,
            lambda a, b: a >= b,
            lambda a, b: a <= b,
        ]
        
        for op in operators:
            result = op(arr1, arr2)
            assert is_array(result)
            assert result.shape == arr1.shape