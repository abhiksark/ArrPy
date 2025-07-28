"""
Tests for new functions added in the restructured ArrPy.

This module tests the new array creation functions, mathematical functions,
and array manipulation functions added in the restructured version.
"""

import pytest
import math
import arrpy as ap
from arrpy import (
    Array, array, empty, full, identity, logspace,
    tan, arcsin, arccos, arctan, log10, log2, 
    power, absolute, sign, floor_divide, mod,
    floor, ceil, round, trunc, prod, cumsum, cumprod,
    argmin, argmax, squeeze, expand_dims, stack
)


class TestNewArrayCreation:
    """Test new array creation functions."""
    
    def test_empty(self):
        """Test empty array creation."""
        arr = empty(3)
        assert arr.shape == (3,)
        assert all(x == 0 for x in arr._data)  # empty is implemented as zeros
    
    def test_full(self):
        """Test full array creation."""
        arr = full(3, 7)
        assert arr.shape == (3,)
        assert all(x == 7 for x in arr._data)
        
        arr2d = full((2, 3), 3.14)
        assert arr2d.shape == (2, 3)
        assert all(x == 3.14 for x in arr2d._data)
    
    def test_identity(self):
        """Test identity matrix creation."""
        arr = identity(3)
        assert arr.shape == (3, 3)
        # Check diagonal elements are 1
        assert arr[0, 0] == 1
        assert arr[1, 1] == 1
        assert arr[2, 2] == 1
        # Check off-diagonal elements are 0
        assert arr[0, 1] == 0
        assert arr[1, 0] == 0
    
    def test_logspace(self):
        """Test logarithmic space array creation."""
        arr = logspace(0, 2, 3)  # 10^0 to 10^2, 3 points
        assert arr.shape == (3,)
        assert abs(arr._data[0] - 1.0) < 1e-10
        assert abs(arr._data[1] - 10.0) < 1e-10  
        assert abs(arr._data[2] - 100.0) < 1e-10
    
    def test_array_function(self):
        """Test the array() convenience function."""
        arr = array([1, 2, 3])
        assert isinstance(arr, Array)
        assert arr.shape == (3,)
        assert list(arr._data) == [1, 2, 3]


class TestNewMathFunctions:
    """Test new mathematical functions."""
    
    def test_tan(self):
        """Test tangent function."""
        arr = Array([0, math.pi/4, math.pi])
        result = tan(arr)
        assert abs(result._data[0] - 0.0) < 1e-10
        assert abs(result._data[1] - 1.0) < 1e-10
        assert abs(result._data[2]) < 1e-10  # tan(pi) ≈ 0
    
    def test_inverse_trig(self):
        """Test inverse trigonometric functions."""
        arr = Array([0, 0.5, 1])
        
        # Test arcsin
        result = arcsin(arr)
        assert abs(result._data[0] - 0.0) < 1e-10
        assert abs(result._data[2] - math.pi/2) < 1e-10
        
        # Test arccos
        result = arccos(arr)
        assert abs(result._data[0] - math.pi/2) < 1e-10
        assert abs(result._data[2] - 0.0) < 1e-10
        
        # Test arctan
        arr2 = Array([0, 1, -1])
        result = arctan(arr2)
        assert abs(result._data[0] - 0.0) < 1e-10
        assert abs(result._data[1] - math.pi/4) < 1e-10
        assert abs(result._data[2] + math.pi/4) < 1e-10
    
    def test_log_functions(self):
        """Test logarithm functions."""
        arr = Array([1, 10, 100])
        
        # Test log10
        result = log10(arr)
        assert abs(result._data[0] - 0.0) < 1e-10
        assert abs(result._data[1] - 1.0) < 1e-10
        assert abs(result._data[2] - 2.0) < 1e-10
        
        # Test log2
        arr2 = Array([1, 2, 4, 8])
        result = log2(arr2)
        assert abs(result._data[0] - 0.0) < 1e-10
        assert abs(result._data[1] - 1.0) < 1e-10
        assert abs(result._data[2] - 2.0) < 1e-10
        assert abs(result._data[3] - 3.0) < 1e-10
    
    def test_power(self):
        """Test power function."""
        arr = Array([1, 2, 3, 4])
        
        # Test scalar power
        result = power(arr, 2)
        assert result._data == [1, 4, 9, 16]
        
        # Test array power
        exponents = Array([1, 2, 3, 2])
        result = power(arr, exponents)
        assert result._data == [1, 4, 27, 16]
    
    def test_absolute(self):
        """Test absolute value function."""
        arr = Array([-3, -1, 0, 1, 3])
        result = absolute(arr)
        assert result._data == [3, 1, 0, 1, 3]
    
    def test_sign(self):
        """Test sign function."""
        arr = Array([-3, -1, 0, 1, 3])
        result = sign(arr)
        assert result._data == [-1, -1, 0, 1, 1]


class TestRoundingFunctions:
    """Test rounding functions."""
    
    def test_floor(self):
        """Test floor function."""
        arr = Array([1.2, 2.7, -1.3, -2.8])
        result = floor(arr)
        assert result._data == [1, 2, -2, -3]
    
    def test_ceil(self):
        """Test ceiling function."""
        arr = Array([1.2, 2.7, -1.3, -2.8])
        result = ceil(arr)
        assert result._data == [2, 3, -1, -2]
    
    def test_round(self):
        """Test rounding function."""
        arr = Array([1.2, 2.7, -1.3, -2.8])
        result = round(arr)
        assert result._data == [1, 3, -1, -3]
        
        # Test with decimals
        arr2 = Array([1.234, 2.567])
        result = round(arr2, 1)
        assert abs(result._data[0] - 1.2) < 1e-10
        assert abs(result._data[1] - 2.6) < 1e-10
    
    def test_trunc(self):
        """Test truncation function."""
        arr = Array([1.7, 2.3, -1.8, -2.2])
        result = trunc(arr)
        assert result._data == [1, 2, -1, -2]


class TestNewStatistics:
    """Test new statistical functions."""
    
    def test_prod(self):
        """Test product function."""
        arr = Array([1, 2, 3, 4])
        result = prod(arr)
        assert result == 24
    
    def test_cumsum(self):
        """Test cumulative sum."""
        arr = Array([1, 2, 3, 4])
        result = cumsum(arr)
        assert result._data == [1, 3, 6, 10]
    
    def test_cumprod(self):
        """Test cumulative product."""
        arr = Array([1, 2, 3, 4])
        result = cumprod(arr)
        assert result._data == [1, 2, 6, 24]
    
    def test_argmin_argmax(self):
        """Test argmin and argmax functions."""
        arr = Array([3, 1, 4, 1, 5])
        
        assert argmin(arr) == 1  # Index of first minimum
        assert argmax(arr) == 4  # Index of maximum


class TestNewManipulation:
    """Test new array manipulation functions."""
    
    def test_squeeze(self):
        """Test squeeze function."""
        # Create array with shape (1, 3, 1)
        arr = Array([1, 2, 3])
        reshaped = arr.reshape((1, 3, 1))
        assert reshaped.shape == (1, 3, 1)
        
        squeezed = squeeze(reshaped)
        assert squeezed.shape == (3,)
        assert squeezed._data == [1, 2, 3]
    
    def test_expand_dims(self):
        """Test expand_dims function."""
        arr = Array([1, 2, 3])
        
        # Expand at axis 0
        result = expand_dims(arr, 0)
        assert result.shape == (1, 3)
        
        # Expand at axis 1
        result = expand_dims(arr, 1) 
        assert result.shape == (3, 1)
    
    def test_stack(self):
        """Test stack function."""
        a = Array([1, 2])
        b = Array([3, 4])
        
        # Stack along axis 0 (default)
        result = stack([a, b])
        assert result.shape == (2, 2)
        assert result[0, 0] == 1
        assert result[0, 1] == 2
        assert result[1, 0] == 3 
        assert result[1, 1] == 4
        
        # Stack along axis 1
        result = stack([a, b], axis=1)
        assert result.shape == (2, 2)
        assert result[0, 0] == 1
        assert result[0, 1] == 3
        assert result[1, 0] == 2
        assert result[1, 1] == 4


class TestFunctionVsMethodConsistency:
    """Test that functions and methods produce the same results."""
    
    def test_sum_consistency(self):
        """Test sum function vs method."""
        arr = Array([1, 2, 3, 4])
        assert ap.sum(arr) == arr.sum()
    
    def test_reshape_consistency(self):
        """Test reshape function vs method."""
        arr = Array([1, 2, 3, 4])
        func_result = ap.reshape(arr, (2, 2))
        method_result = arr.reshape((2, 2))
        assert func_result.shape == method_result.shape
        assert func_result._data == method_result._data
    
    def test_transpose_consistency(self):
        """Test transpose function vs property."""
        arr = Array([[1, 2], [3, 4]])
        func_result = ap.transpose(arr)
        prop_result = arr.T
        assert func_result.shape == prop_result.shape
        assert func_result._data == prop_result._data