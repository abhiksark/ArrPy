"""
Test arithmetic operations on arrays.

Tests addition, subtraction, multiplication, division, and other arithmetic operations.
"""

import pytest
import math
from arrpy import Array
import arrpy as ap


class TestArrayAddition:
    """Test addition operations."""
    
    def test_scalar_addition(self):
        """Test adding scalar to array."""
        arr = Array([1, 2, 3, 4])
        result = arr + 5
        assert isinstance(result, Array)
        assert result.shape == arr.shape
        assert list(result._data) == [6, 7, 8, 9]
    
    def test_array_addition_1d(self):
        """Test adding two 1D arrays."""
        arr1 = Array([1, 2, 3])
        arr2 = Array([4, 5, 6])
        result = arr1 + arr2
        assert isinstance(result, Array)
        assert result.shape == (3,)
        assert list(result._data) == [5, 7, 9]
    
    def test_array_addition_2d(self):
        """Test adding two 2D arrays."""
        arr1 = Array([[1, 2], [3, 4]])
        arr2 = Array([[5, 6], [7, 8]])
        result = arr1 + arr2
        assert result.shape == (2, 2)
        assert result[0, 0] == 6
        assert result[0, 1] == 8
        assert result[1, 0] == 10
        assert result[1, 1] == 12
    
    def test_addition_with_negative_numbers(self):
        """Test addition with negative numbers."""
        arr = Array([-1, -2, -3])
        result = arr + 5
        assert list(result._data) == [4, 3, 2]
        
        result2 = arr + Array([1, 2, 3])
        assert list(result2._data) == [0, 0, 0]
    
    def test_addition_with_floats(self):
        """Test addition with floating point numbers."""
        arr = Array([1.5, 2.5, 3.5])
        result = arr + 0.5
        assert abs(result[0] - 2.0) < 1e-10
        assert abs(result[1] - 3.0) < 1e-10
        assert abs(result[2] - 4.0) < 1e-10


class TestArraySubtraction:
    """Test subtraction operations."""
    
    def test_scalar_subtraction(self):
        """Test subtracting scalar from array."""
        arr = Array([5, 6, 7, 8])
        result = arr - 3
        assert list(result._data) == [2, 3, 4, 5]
    
    def test_array_subtraction_1d(self):
        """Test subtracting two 1D arrays."""
        arr1 = Array([10, 8, 6])
        arr2 = Array([3, 2, 1])
        result = arr1 - arr2
        assert list(result._data) == [7, 6, 5]
    
    def test_array_subtraction_2d(self):
        """Test subtracting two 2D arrays."""
        arr1 = Array([[10, 9], [8, 7]])
        arr2 = Array([[3, 2], [1, 4]])
        result = arr1 - arr2
        assert result[0, 0] == 7
        assert result[0, 1] == 7
        assert result[1, 0] == 7
        assert result[1, 1] == 3
    
    def test_subtraction_with_negative_result(self):
        """Test subtraction resulting in negative numbers."""
        arr = Array([1, 2, 3])
        result = arr - 5
        assert list(result._data) == [-4, -3, -2]


class TestArrayMultiplication:
    """Test multiplication operations."""
    
    def test_scalar_multiplication(self):
        """Test multiplying array by scalar."""
        arr = Array([2, 3, 4])
        result = arr * 3
        assert list(result._data) == [6, 9, 12]
    
    def test_array_multiplication_1d(self):
        """Test element-wise multiplication of 1D arrays."""
        arr1 = Array([2, 3, 4])
        arr2 = Array([5, 6, 7])
        result = arr1 * arr2
        assert list(result._data) == [10, 18, 28]
    
    def test_array_multiplication_2d(self):
        """Test element-wise multiplication of 2D arrays."""
        arr1 = Array([[2, 3], [4, 5]])
        arr2 = Array([[6, 7], [8, 9]])
        result = arr1 * arr2
        assert result[0, 0] == 12
        assert result[0, 1] == 21
        assert result[1, 0] == 32
        assert result[1, 1] == 45
    
    def test_multiplication_with_zero(self):
        """Test multiplication by zero."""
        arr = Array([1, 2, 3, 4])
        result = arr * 0
        assert list(result._data) == [0, 0, 0, 0]
    
    def test_multiplication_with_one(self):
        """Test multiplication by one (identity)."""
        arr = Array([1, 2, 3, 4])
        result = arr * 1
        assert list(result._data) == [1, 2, 3, 4]


class TestArrayDivision:
    """Test division operations."""
    
    def test_scalar_division(self):
        """Test dividing array by scalar."""
        arr = Array([6, 8, 10])
        result = arr / 2
        assert list(result._data) == [3, 4, 5]
    
    def test_array_division_1d(self):
        """Test element-wise division of 1D arrays."""
        arr1 = Array([12, 15, 18])
        arr2 = Array([3, 5, 6])
        result = arr1 / arr2
        assert list(result._data) == [4, 3, 3]
    
    def test_array_division_2d(self):
        """Test element-wise division of 2D arrays."""
        arr1 = Array([[12, 15], [18, 21]])
        arr2 = Array([[3, 5], [6, 7]])
        result = arr1 / arr2
        assert result[0, 0] == 4
        assert result[0, 1] == 3
        assert result[1, 0] == 3
        assert result[1, 1] == 3
    
    def test_division_with_floats(self):
        """Test division resulting in floats."""
        arr = Array([5, 7, 9])
        result = arr / 2
        assert abs(result[0] - 2.5) < 1e-10
        assert abs(result[1] - 3.5) < 1e-10
        assert abs(result[2] - 4.5) < 1e-10
    
    def test_division_by_one(self):
        """Test division by one (identity)."""
        arr = Array([1, 2, 3, 4])
        result = arr / 1
        assert list(result._data) == [1, 2, 3, 4]


class TestArithmeticErrors:
    """Test error cases in arithmetic operations."""
    
    def test_shape_mismatch_addition(self):
        """Test that shape mismatch raises error in addition."""
        arr1 = Array([1, 2, 3])
        arr2 = Array([1, 2])
        
        with pytest.raises(ValueError, match="Shape mismatch"):
            arr1 + arr2
    
    def test_shape_mismatch_subtraction(self):
        """Test that shape mismatch raises error in subtraction."""
        arr1 = Array([[1, 2], [3, 4]])
        arr2 = Array([1, 2, 3])
        
        with pytest.raises(ValueError, match="Shape mismatch"):
            arr1 - arr2
    
    def test_shape_mismatch_multiplication(self):
        """Test that shape mismatch raises error in multiplication."""
        arr1 = Array([1, 2])
        arr2 = Array([[1, 2], [3, 4]])
        
        with pytest.raises(ValueError, match="Shape mismatch"):
            arr1 * arr2
    
    def test_shape_mismatch_division(self):
        """Test that shape mismatch raises error in division."""
        arr1 = Array([1, 2, 3, 4])
        arr2 = Array([1, 2])
        
        with pytest.raises(ValueError, match="Shape mismatch"):
            arr1 / arr2
    
    def test_division_by_zero_scalar(self):
        """Test division by zero scalar."""
        arr = Array([1, 2, 3])
        with pytest.raises(ZeroDivisionError):
            arr / 0
    
    def test_division_by_zero_array(self):
        """Test division by array containing zero."""
        arr1 = Array([1, 2, 3])
        arr2 = Array([1, 0, 3])
        with pytest.raises(ZeroDivisionError):
            arr1 / arr2


class TestArithmeticCommutativity:
    """Test commutativity properties where applicable."""
    
    def test_addition_commutativity(self):
        """Test that a + b = b + a for arrays."""
        arr1 = Array([1, 2, 3])
        arr2 = Array([4, 5, 6])
        
        result1 = arr1 + arr2
        result2 = arr2 + arr1
        
        assert list(result1._data) == list(result2._data)
    
    def test_multiplication_commutativity(self):
        """Test that a * b = b * a for arrays."""
        arr1 = Array([2, 3, 4])
        arr2 = Array([5, 6, 7])
        
        result1 = arr1 * arr2
        result2 = arr2 * arr1
        
        assert list(result1._data) == list(result2._data)
    
    def test_scalar_commutativity(self):
        """Test commutativity with scalars."""
        arr = Array([1, 2, 3])
        scalar = 5
        
        # Addition commutativity
        result1 = arr + scalar
        try:
            result2 = scalar + arr
            assert list(result1._data) == list(result2._data)
        except TypeError:
            # Right-hand side operations might not be implemented
            pytest.skip("Right-hand scalar operations not implemented")
        
        # Multiplication commutativity
        result3 = arr * scalar
        try:
            result4 = scalar * arr
            assert list(result3._data) == list(result4._data)
        except TypeError:
            pytest.skip("Right-hand scalar operations not implemented")


class TestArithmeticChaining:
    """Test chaining multiple arithmetic operations."""
    
    def test_addition_subtraction_chain(self):
        """Test chaining addition and subtraction."""
        arr = Array([10, 20, 30])
        result = arr + 5 - 3
        assert list(result._data) == [12, 22, 32]
    
    def test_multiplication_division_chain(self):
        """Test chaining multiplication and division."""
        arr = Array([2, 4, 6])
        result = arr * 3 / 2
        assert list(result._data) == [3, 6, 9]
    
    def test_complex_expression(self):
        """Test complex arithmetic expression."""
        arr1 = Array([1, 2, 3])
        arr2 = Array([4, 5, 6])
        result = (arr1 + arr2) * 2 - 1
        assert list(result._data) == [9, 13, 17]
    
    def test_mixed_operations(self):
        """Test mixing different arithmetic operations."""
        arr = Array([1, 2, 3])
        result = arr * 2 + 1
        assert list(result._data) == [3, 5, 7]
        
        result2 = (arr + 1) / 2
        assert abs(result2[0] - 1.0) < 1e-10
        assert abs(result2[1] - 1.5) < 1e-10
        assert abs(result2[2] - 2.0) < 1e-10


class TestArithmeticSpecialCases:
    """Test special cases in arithmetic operations."""
    
    def test_empty_array_arithmetic(self):
        """Test arithmetic on empty arrays."""
        arr = Array([])
        result = arr + 5
        assert result.shape == (0,)
        assert result.size == 0
    
    def test_single_element_arithmetic(self):
        """Test arithmetic on single-element arrays."""
        arr = Array([42])
        result = arr + 8
        assert result[0] == 50
        
        arr2 = Array([6])
        result2 = arr * arr2
        assert result2[0] == 252
    
    def test_boolean_arithmetic(self):
        """Test arithmetic with boolean arrays."""
        arr = Array([True, False, True])
        result = arr + 1
        assert list(result._data) == [2, 1, 2]
        
        result2 = arr * 5
        assert list(result2._data) == [5, 0, 5]
    
    def test_mixed_types_arithmetic(self):
        """Test arithmetic with mixed numeric types."""
        arr = Array([1, 2.5, 3])
        result = arr + 0.5
        assert abs(result[0] - 1.5) < 1e-10
        assert abs(result[1] - 3.0) < 1e-10
        assert abs(result[2] - 3.5) < 1e-10