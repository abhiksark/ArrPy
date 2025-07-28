"""
Test trigonometric functions.

Tests sin, cos, tan, and inverse trigonometric functions.
"""

import pytest
import math
from arrpy import Array
import arrpy as ap


class TestBasicTrigonometric:
    """Test basic trigonometric functions."""
    
    def test_sin_function(self):
        """Test sine function."""
        arr = Array([0, math.pi/6, math.pi/4, math.pi/3, math.pi/2])
        result = ap.sin(arr)
        
        assert isinstance(result, Array)
        assert result.shape == arr.shape
        
        # Test known values
        assert abs(result[0] - 0.0) < 1e-10
        assert abs(result[1] - 0.5) < 1e-10
        assert abs(result[2] - math.sqrt(2)/2) < 1e-10
        assert abs(result[3] - math.sqrt(3)/2) < 1e-10
        assert abs(result[4] - 1.0) < 1e-10
    
    def test_cos_function(self):
        """Test cosine function."""
        arr = Array([0, math.pi/6, math.pi/4, math.pi/3, math.pi/2])
        result = ap.cos(arr)
        
        assert isinstance(result, Array)
        assert result.shape == arr.shape
        
        # Test known values
        assert abs(result[0] - 1.0) < 1e-10
        assert abs(result[1] - math.sqrt(3)/2) < 1e-10
        assert abs(result[2] - math.sqrt(2)/2) < 1e-10
        assert abs(result[3] - 0.5) < 1e-10
        assert abs(result[4] - 0.0) < 1e-10
    
    def test_tan_function(self):
        """Test tangent function."""
        arr = Array([0, math.pi/6, math.pi/4, math.pi/3])
        result = ap.tan(arr)
        
        assert isinstance(result, Array)
        assert result.shape == arr.shape
        
        # Test known values
        assert abs(result[0] - 0.0) < 1e-10
        assert abs(result[1] - 1/math.sqrt(3)) < 1e-10
        assert abs(result[2] - 1.0) < 1e-10
        assert abs(result[3] - math.sqrt(3)) < 1e-10
    
    def test_sin_method(self):
        """Test sine as array method."""
        arr = Array([0, math.pi/2, math.pi])
        result = arr.sin()
        
        assert abs(result[0] - 0.0) < 1e-10
        assert abs(result[1] - 1.0) < 1e-10
        assert abs(result[2] - 0.0) < 1e-10
    
    def test_cos_method(self):
        """Test cosine as array method."""
        arr = Array([0, math.pi/2, math.pi])
        result = arr.cos()
        
        assert abs(result[0] - 1.0) < 1e-10
        assert abs(result[1] - 0.0) < 1e-10
        assert abs(result[2] + 1.0) < 1e-10


class TestInverseTrigonometric:
    """Test inverse trigonometric functions."""
    
    def test_arcsin_function(self):
        """Test arcsine function."""
        arr = Array([0, 0.5, math.sqrt(2)/2, math.sqrt(3)/2, 1])
        result = ap.arcsin(arr)
        
        assert isinstance(result, Array)
        assert result.shape == arr.shape
        
        # Test known values
        assert abs(result[0] - 0.0) < 1e-10
        assert abs(result[1] - math.pi/6) < 1e-10
        assert abs(result[2] - math.pi/4) < 1e-10
        assert abs(result[3] - math.pi/3) < 1e-10
        assert abs(result[4] - math.pi/2) < 1e-10
    
    def test_arccos_function(self):
        """Test arccosine function."""
        arr = Array([1, math.sqrt(3)/2, math.sqrt(2)/2, 0.5, 0])
        result = ap.arccos(arr)
        
        assert isinstance(result, Array)
        assert result.shape == arr.shape
        
        # Test known values
        assert abs(result[0] - 0.0) < 1e-10
        assert abs(result[1] - math.pi/6) < 1e-10
        assert abs(result[2] - math.pi/4) < 1e-10
        assert abs(result[3] - math.pi/3) < 1e-10
        assert abs(result[4] - math.pi/2) < 1e-10
    
    def test_arctan_function(self):
        """Test arctangent function."""
        arr = Array([0, 1/math.sqrt(3), 1, math.sqrt(3)])
        result = ap.arctan(arr)
        
        assert isinstance(result, Array)
        assert result.shape == arr.shape
        
        # Test known values
        assert abs(result[0] - 0.0) < 1e-10
        assert abs(result[1] - math.pi/6) < 1e-10
        assert abs(result[2] - math.pi/4) < 1e-10
        assert abs(result[3] - math.pi/3) < 1e-10


class TestTrigonometric2D:
    """Test trigonometric functions on 2D arrays."""
    
    def test_sin_2d(self):
        """Test sine on 2D array."""
        arr = Array([[0, math.pi/2], [math.pi, 3*math.pi/2]])
        result = ap.sin(arr)
        
        assert result.shape == (2, 2)
        assert abs(result[0, 0] - 0.0) < 1e-10
        assert abs(result[0, 1] - 1.0) < 1e-10
        assert abs(result[1, 0] - 0.0) < 1e-10
        assert abs(result[1, 1] + 1.0) < 1e-10
    
    def test_cos_2d(self):
        """Test cosine on 2D array."""
        arr = Array([[0, math.pi/2], [math.pi, 3*math.pi/2]])
        result = ap.cos(arr)
        
        assert result.shape == (2, 2)
        assert abs(result[0, 0] - 1.0) < 1e-10
        assert abs(result[0, 1] - 0.0) < 1e-10
        assert abs(result[1, 0] + 1.0) < 1e-10
        assert abs(result[1, 1] - 0.0) < 1e-10


class TestTrigonometricSpecialValues:
    """Test trigonometric functions with special values."""
    
    def test_sin_negative_values(self):
        """Test sine with negative values."""
        arr = Array([-math.pi/2, -math.pi/4, 0, math.pi/4, math.pi/2])
        result = ap.sin(arr)
        
        assert abs(result[0] + 1.0) < 1e-10  # sin(-π/2) = -1
        assert abs(result[1] + math.sqrt(2)/2) < 1e-10  # sin(-π/4) = -√2/2
        assert abs(result[2] - 0.0) < 1e-10  # sin(0) = 0
        assert abs(result[3] - math.sqrt(2)/2) < 1e-10  # sin(π/4) = √2/2
        assert abs(result[4] - 1.0) < 1e-10  # sin(π/2) = 1
    
    def test_cos_negative_values(self):
        """Test cosine with negative values (even function)."""
        arr = Array([-math.pi, -math.pi/2, 0, math.pi/2, math.pi])
        result = ap.cos(arr)
        
        assert abs(result[0] + 1.0) < 1e-10  # cos(-π) = -1
        assert abs(result[1] - 0.0) < 1e-10  # cos(-π/2) = 0
        assert abs(result[2] - 1.0) < 1e-10  # cos(0) = 1
        assert abs(result[3] - 0.0) < 1e-10  # cos(π/2) = 0
        assert abs(result[4] + 1.0) < 1e-10  # cos(π) = -1
    
    def test_tan_special_values(self):
        """Test tangent with special values."""
        arr = Array([-math.pi/4, 0, math.pi/4])
        result = ap.tan(arr)
        
        assert abs(result[0] + 1.0) < 1e-10  # tan(-π/4) = -1
        assert abs(result[1] - 0.0) < 1e-10  # tan(0) = 0
        assert abs(result[2] - 1.0) < 1e-10  # tan(π/4) = 1
    
    def test_large_values(self):
        """Test trigonometric functions with large values."""
        arr = Array([10*math.pi, 100*math.pi])
        sin_result = ap.sin(arr)
        cos_result = ap.cos(arr)
        
        # sin and cos should still be bounded [-1, 1]
        for val in sin_result._data:
            assert -1 <= val <= 1
        for val in cos_result._data:
            assert -1 <= val <= 1


class TestTrigonometricIdentities:
    """Test trigonometric identities."""
    
    def test_pythagorean_identity(self):
        """Test sin²(x) + cos²(x) = 1."""
        arr = Array([0, math.pi/6, math.pi/4, math.pi/3, math.pi/2, math.pi])
        sin_result = ap.sin(arr)
        cos_result = ap.cos(arr)
        
        for i in range(len(arr._data)):
            sin_val = sin_result[i]
            cos_val = cos_result[i]
            identity_result = sin_val**2 + cos_val**2
            assert abs(identity_result - 1.0) < 1e-10
    
    def test_tan_identity(self):
        """Test tan(x) = sin(x)/cos(x) where cos(x) ≠ 0."""
        arr = Array([math.pi/6, math.pi/4, math.pi/3])
        sin_result = ap.sin(arr)
        cos_result = ap.cos(arr)
        tan_result = ap.tan(arr)
        
        for i in range(len(arr._data)):
            expected_tan = sin_result[i] / cos_result[i]
            assert abs(tan_result[i] - expected_tan) < 1e-10
    
    def test_even_odd_properties(self):
        """Test even/odd properties of trigonometric functions."""
        arr = Array([math.pi/6, math.pi/4, math.pi/3])
        neg_arr = Array([-math.pi/6, -math.pi/4, -math.pi/3])
        
        sin_pos = ap.sin(arr)
        sin_neg = ap.sin(neg_arr)
        cos_pos = ap.cos(arr)
        cos_neg = ap.cos(neg_arr)
        
        # sin(-x) = -sin(x) (odd function)
        for i in range(len(arr._data)):
            assert abs(sin_neg[i] + sin_pos[i]) < 1e-10
        
        # cos(-x) = cos(x) (even function)
        for i in range(len(arr._data)):
            assert abs(cos_neg[i] - cos_pos[i]) < 1e-10


class TestTrigonometricDomainErrors:
    """Test domain errors in trigonometric functions."""
    
    def test_arcsin_domain_error(self):
        """Test arcsin domain error for values outside [-1, 1]."""
        arr_invalid = Array([1.5, -1.5, 2.0])
        
        with pytest.raises(ValueError):
            ap.arcsin(arr_invalid)
    
    def test_arccos_domain_error(self):
        """Test arccos domain error for values outside [-1, 1]."""
        arr_invalid = Array([1.1, -1.1])
        
        with pytest.raises(ValueError):
            ap.arccos(arr_invalid)
    
    def test_arcsin_boundary_values(self):
        """Test arcsin at domain boundaries."""
        arr = Array([-1, 1])
        result = ap.arcsin(arr)
        
        assert abs(result[0] + math.pi/2) < 1e-10  # arcsin(-1) = -π/2
        assert abs(result[1] - math.pi/2) < 1e-10  # arcsin(1) = π/2
    
    def test_arccos_boundary_values(self):
        """Test arccos at domain boundaries."""
        arr = Array([-1, 1])
        result = ap.arccos(arr)
        
        assert abs(result[0] - math.pi) < 1e-10  # arccos(-1) = π
        assert abs(result[1] - 0.0) < 1e-10    # arccos(1) = 0


class TestTrigonometricEmptyAndSingleElement:
    """Test trigonometric functions on edge cases."""
    
    def test_empty_array(self):
        """Test trigonometric functions on empty array."""
        arr = Array([])
        
        sin_result = ap.sin(arr)
        cos_result = ap.cos(arr)
        tan_result = ap.tan(arr)
        
        assert sin_result.shape == (0,)
        assert cos_result.shape == (0,)
        assert tan_result.shape == (0,)
    
    def test_single_element(self):
        """Test trigonometric functions on single element."""
        arr = Array([math.pi/4])
        
        sin_result = ap.sin(arr)
        cos_result = ap.cos(arr)
        tan_result = ap.tan(arr)
        
        assert sin_result.shape == (1,)
        assert cos_result.shape == (1,)
        assert tan_result.shape == (1,)
        
        assert abs(sin_result[0] - math.sqrt(2)/2) < 1e-10
        assert abs(cos_result[0] - math.sqrt(2)/2) < 1e-10
        assert abs(tan_result[0] - 1.0) < 1e-10


class TestTrigonometricConsistency:
    """Test consistency between function and method forms."""
    
    def test_sin_function_vs_method(self):
        """Test that sin function and method give same results."""
        arr = Array([0, math.pi/4, math.pi/2])
        
        func_result = ap.sin(arr)
        method_result = arr.sin()
        
        assert func_result.shape == method_result.shape
        for i in range(len(arr._data)):
            assert abs(func_result[i] - method_result[i]) < 1e-10
    
    def test_cos_function_vs_method(self):
        """Test that cos function and method give same results."""
        arr = Array([0, math.pi/4, math.pi/2])
        
        func_result = ap.cos(arr)
        method_result = arr.cos()
        
        assert func_result.shape == method_result.shape
        for i in range(len(arr._data)):
            assert abs(func_result[i] - method_result[i]) < 1e-10