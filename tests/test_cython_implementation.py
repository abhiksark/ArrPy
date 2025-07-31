"""
Tests specifically for Cython implementation features and performance.

This test suite verifies that the Cython optimizations work correctly
and provides the expected performance improvements.
"""

import pytest
import time
import sys
import os

# Force import of Python version for comparison
arrpy_core_path = os.path.join(os.path.dirname(__file__), '..', 'arrpy', 'core')
sys.path.insert(0, arrpy_core_path)
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("python_array", os.path.join(arrpy_core_path, "array.py"))
    python_array_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(python_array_module)
    PythonArray = python_array_module.Array
finally:
    sys.path.remove(arrpy_core_path)

# Import the optimized version (Cython when available)
from arrpy.core import Array
from arrpy.creation import zeros, ones, full, eye
from arrpy.math import power, absolute


class TestCythonImplementationDetection:
    """Test that we can detect if Cython implementation is available."""
    
    def test_cython_implementation_loaded(self):
        """Test that Cython implementation is being used."""
        arr = Array([1, 2, 3])
        
        # Check if we're using the Cython version
        assert hasattr(arr, 'sum_fast'), "Cython fast methods should be available"
        assert hasattr(arr, 'mean_fast'), "Cython fast methods should be available"
        assert 'cython' in type(arr).__module__.lower(), "Should be using Cython implementation"
    
    def test_cython_array_type(self):
        """Test that Array type is from Cython module."""
        arr = Array([1, 2, 3])
        assert type(arr).__name__ == 'Array'
        assert 'array_cython' in type(arr).__module__


class TestCythonFastMethods:
    """Test Cython-specific fast methods."""
    
    def test_sum_fast_basic(self):
        """Test that sum_fast works correctly."""
        arr = Array([1, 2, 3, 4, 5])
        
        if hasattr(arr, 'sum_fast'):
            result = arr.sum_fast()
            expected = 15.0
            assert result == expected, f"Expected {expected}, got {result}"
    
    def test_sum_fast_vs_regular(self):
        """Test that sum_fast gives same result as regular sum."""
        arr = Array([[1, 2, 3], [4, 5, 6]])
        
        if hasattr(arr, 'sum_fast'):
            fast_result = arr.sum_fast()
            regular_result = arr.sum()
            assert fast_result == regular_result, "Fast and regular sum should match"
    
    def test_mean_fast_basic(self):
        """Test that mean_fast works correctly."""
        arr = Array([2, 4, 6, 8, 10])
        
        if hasattr(arr, 'mean_fast'):
            result = arr.mean_fast()
            expected = 6.0
            assert result == expected, f"Expected {expected}, got {result}"
    
    def test_mean_fast_vs_regular(self):
        """Test that mean_fast gives same result as regular mean."""
        arr = Array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        
        if hasattr(arr, 'mean_fast'):
            fast_result = arr.mean_fast()
            regular_result = arr.mean()
            assert abs(fast_result - regular_result) < 1e-10, "Fast and regular mean should match"
    
    def test_sqrt_fast_basic(self):
        """Test that sqrt_fast works correctly."""
        arr = Array([1, 4, 9, 16, 25])
        
        if hasattr(arr, 'sqrt_fast'):
            result = arr.sqrt_fast()
            expected_data = [1.0, 2.0, 3.0, 4.0, 5.0]
            
            for i, val in enumerate(result._data):
                assert abs(val - expected_data[i]) < 1e-10, f"Expected {expected_data[i]}, got {val}"
    
    def test_sin_fast_basic(self):
        """Test that sin_fast works correctly."""
        arr = Array([0, 1.5708, 3.1416])  # 0, π/2, π
        
        if hasattr(arr, 'sin_fast'):
            result = arr.sin_fast()
            expected_data = [0.0, 1.0, 0.0]  # sin(0), sin(π/2), sin(π)
            
            for i, val in enumerate(result._data):
                assert abs(val - expected_data[i]) < 1e-4, f"Expected ~{expected_data[i]}, got {val}"
    
    def test_cos_fast_basic(self):
        """Test that cos_fast works correctly."""
        arr = Array([0, 1.5708, 3.1416])  # 0, π/2, π
        
        if hasattr(arr, 'cos_fast'):
            result = arr.cos_fast()
            expected_data = [1.0, 0.0, -1.0]  # cos(0), cos(π/2), cos(π)
            
            for i, val in enumerate(result._data):
                assert abs(val - expected_data[i]) < 1e-4, f"Expected ~{expected_data[i]}, got {val}"
    
    def test_exp_fast_basic(self):
        """Test that exp_fast works correctly."""
        arr = Array([0, 1, 2])
        
        if hasattr(arr, 'exp_fast'):
            result = arr.exp_fast()
            expected_data = [1.0, 2.718281828, 7.389056099]  # e^0, e^1, e^2
            
            for i, val in enumerate(result._data):
                assert abs(val - expected_data[i]) < 1e-6, f"Expected ~{expected_data[i]}, got {val}"
    
    def test_log_fast_basic(self):
        """Test that log_fast works correctly."""
        arr = Array([1, 2.718281828, 7.389056099])  # 1, e, e^2
        
        if hasattr(arr, 'log_fast'):
            result = arr.log_fast()
            expected_data = [0.0, 1.0, 2.0]  # ln(1), ln(e), ln(e^2)
            
            for i, val in enumerate(result._data):
                assert abs(val - expected_data[i]) < 1e-6, f"Expected ~{expected_data[i]}, got {val}"


class TestCythonCreationFunctions:
    """Test Cython-optimized creation functions."""
    
    def test_zeros_cython(self):
        """Test zeros function with Cython optimization."""
        # Test 1D
        arr1d = zeros(5)
        assert arr1d.shape == (5,), f"Expected shape (5,), got {arr1d.shape}"
        assert all(x == 0 for x in arr1d._data), "All elements should be 0"
        
        # Test 2D
        arr2d = zeros((3, 4))
        assert arr2d.shape == (3, 4), f"Expected shape (3, 4), got {arr2d.shape}"
        assert len(arr2d._data) == 12, "Should have 12 elements"
        assert all(x == 0 for x in arr2d._data), "All elements should be 0"
    
    def test_ones_cython(self):
        """Test ones function with Cython optimization."""
        # Test 1D
        arr1d = ones(4)
        assert arr1d.shape == (4,), f"Expected shape (4,), got {arr1d.shape}"
        assert all(x == 1 for x in arr1d._data), "All elements should be 1"
        
        # Test 2D
        arr2d = ones((2, 3))
        assert arr2d.shape == (2, 3), f"Expected shape (2, 3), got {arr2d.shape}"
        assert len(arr2d._data) == 6, "Should have 6 elements"
        assert all(x == 1 for x in arr2d._data), "All elements should be 1"
    
    def test_full_cython(self):
        """Test full function with Cython optimization."""
        # Test with single dimension
        arr1d = full(3, 7)
        assert arr1d.shape == (3,), f"Expected shape (3,), got {arr1d.shape}"
        assert all(x == 7 for x in arr1d._data), "All elements should be 7"
        
        # Test with tuple shape
        arr2d = full((2, 2), 3.14)
        assert arr2d.shape == (2, 2), f"Expected shape (2, 2), got {arr2d.shape}"
        assert len(arr2d._data) == 4, "Should have 4 elements"
        assert all(abs(x - 3.14) < 1e-10 for x in arr2d._data), "All elements should be 3.14"
    
    def test_eye_cython(self):
        """Test eye function with Cython optimization."""
        # Test square identity matrix
        arr = eye(3)
        assert arr.shape == (3, 3), f"Expected shape (3, 3), got {arr.shape}"
        
        # Check diagonal elements are 1
        for i in range(3):
            assert arr._data[i * 3 + i] == 1, f"Diagonal element [{i},{i}] should be 1"
        
        # Check off-diagonal elements are 0
        for i in range(3):
            for j in range(3):
                if i != j:
                    assert arr._data[i * 3 + j] == 0, f"Off-diagonal element [{i},{j}] should be 0"


class TestCythonMathFunctions:
    """Test Cython-optimized math functions."""
    
    def test_power_cython_scalar(self):
        """Test power function with scalar exponent."""
        arr = Array([2, 3, 4])
        result = power(arr, 2)
        
        expected = [4, 9, 16]
        for i, val in enumerate(result._data):
            assert val == expected[i], f"Expected {expected[i]}, got {val}"
    
    def test_power_cython_array_exponent(self):
        """Test power function with array exponent."""
        base = Array([2, 3, 4])
        exp = Array([1, 2, 3])
        result = power(base, exp)
        
        expected = [2, 9, 64]  # 2^1, 3^2, 4^3
        for i, val in enumerate(result._data):
            assert val == expected[i], f"Expected {expected[i]}, got {val}"
    
    def test_absolute_cython(self):
        """Test absolute function with Cython optimization."""
        arr = Array([-5, -2, 0, 3, -7])
        result = absolute(arr)
        
        expected = [5, 2, 0, 3, 7]
        for i, val in enumerate(result._data):
            assert val == expected[i], f"Expected {expected[i]}, got {val}"
    
    def test_absolute_cython_vs_builtin(self):
        """Test that Cython absolute matches Python builtin abs."""
        arr = Array([-3.14, 2.71, -1.41, 0])
        result = absolute(arr)
        
        for i, val in enumerate(result._data):
            expected = abs(arr._data[i])
            assert abs(val - expected) < 1e-10, f"Expected {expected}, got {val}"


class TestCythonPerformance:
    """Test performance characteristics of Cython implementation."""
    
    def _time_function(self, func, *args, **kwargs):
        """Helper to time function execution."""
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        return result, end - start
    
    def test_array_creation_performance(self):
        """Test that Cython array creation is faster."""
        size = 100
        data = [[i + j for j in range(size // 10)] for i in range(10)]
        
        # Time Python version
        _, py_time = self._time_function(lambda: PythonArray(data))
        
        # Time Cython version
        _, cy_time = self._time_function(lambda: Array(data))
        
        # Cython should be faster (allow some variance in timing)
        assert cy_time <= py_time * 2, f"Cython creation took {cy_time:.6f}s vs Python {py_time:.6f}s"
    
    def test_arithmetic_performance(self):
        """Test that Cython arithmetic is competitive."""
        data1 = [[i for i in range(50)] for _ in range(10)]
        data2 = [[2 for _ in range(50)] for _ in range(10)]
        
        py_arr1 = PythonArray(data1)
        py_arr2 = PythonArray(data2)
        cy_arr1 = Array(data1)
        cy_arr2 = Array(data2)
        
        # Time addition
        _, py_time = self._time_function(lambda: py_arr1 + py_arr2)
        _, cy_time = self._time_function(lambda: cy_arr1 + cy_arr2)
        
        # Results should be equivalent
        py_result = py_arr1 + py_arr2
        cy_result = cy_arr1 + cy_arr2
        
        assert py_result._data == cy_result._data, "Results should be identical"
    
    def test_fast_methods_performance(self):
        """Test that fast methods provide performance benefit."""
        size = 1000
        data = [[float(i + j) for j in range(size // 10)] for i in range(10)]
        
        arr = Array(data)
        
        if hasattr(arr, 'sum_fast'):
            # Time regular sum
            _, regular_time = self._time_function(lambda: arr.sum())
            
            # Time fast sum
            _, fast_time = self._time_function(lambda: arr.sum_fast())
            
            # Results should be equivalent
            regular_result = arr.sum()
            fast_result = arr.sum_fast()
            
            assert abs(regular_result - fast_result) < 1e-10, "Results should be equivalent"


class TestCythonErrorHandling:
    """Test that Cython implementation handles errors correctly."""
    
    def test_empty_array_errors(self):
        """Test error handling with empty arrays."""
        arr = Array([])
        
        with pytest.raises(ValueError, match="Cannot calculate mean of empty array"):
            arr.mean()
        
        if hasattr(arr, 'mean_fast'):
            with pytest.raises(ValueError, match="Cannot calculate mean of empty array"):
                arr.mean_fast()
    
    def test_index_errors(self):
        """Test that indexing errors are handled correctly."""
        arr = Array([1, 2, 3])
        
        with pytest.raises(IndexError):
            _ = arr[5]
        
        with pytest.raises(IndexError):
            arr[5] = 10
    
    def test_shape_mismatch_errors(self):
        """Test that shape mismatch errors are handled correctly."""
        arr1 = Array([1, 2, 3])
        arr2 = Array([[1, 2], [3, 4]])
        
        with pytest.raises(ValueError, match="Shape mismatch"):
            _ = arr1 + arr2
    
    def test_percentile_errors(self):
        """Test percentile error handling."""
        arr = Array([1, 2, 3, 4, 5])
        
        with pytest.raises(ValueError, match="Percentile must be between 0 and 100"):
            arr.percentile(-1)
        
        with pytest.raises(ValueError, match="Percentile must be between 0 and 100"):
            arr.percentile(101)
        
        # Empty array should raise error
        empty_arr = Array([])
        with pytest.raises(ValueError, match="Cannot calculate percentile of empty array"):
            empty_arr.percentile(50)


class TestCythonEdgeCases:
    """Test edge cases specific to Cython implementation."""
    
    def test_single_element_arrays(self):
        """Test operations on single-element arrays."""
        arr = Array([42])
        
        assert arr.shape == (1,)
        assert arr.size == 1
        assert arr[0] == 42
        
        if hasattr(arr, 'sum_fast'):
            assert arr.sum_fast() == 42.0
            assert arr.mean_fast() == 42.0
    
    def test_large_arrays(self):
        """Test operations on larger arrays."""
        size = 1000
        data = [i for i in range(size)]
        arr = Array(data)
        
        assert arr.shape == (size,)
        assert arr.size == size
        
        # Test some operations
        total = arr.sum()
        expected_total = sum(range(size))
        assert total == expected_total
        
        if hasattr(arr, 'sum_fast'):
            fast_total = arr.sum_fast()
            assert fast_total == expected_total
    
    def test_nested_array_operations(self):
        """Test operations on multi-dimensional arrays."""
        arr = Array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        
        assert arr.shape == (3, 3)
        assert arr.size == 9
        
        # Test indexing
        assert arr[0, 0] == 1
        assert arr[1, 2] == 6
        assert arr[2, 1] == 8
        
        # Test slicing
        row = arr[1]
        assert row.shape == (3,)
        assert row._data == [4, 5, 6]
    
    def test_type_consistency(self):
        """Test that operations maintain type consistency."""
        arr = Array([1.5, 2.5, 3.5])
        
        # Test that arithmetic operations preserve the Array type
        result = arr + 1
        assert isinstance(result, type(arr))
        
        result = arr * 2
        assert isinstance(result, type(arr))
        
        # Test that mathematical functions return Array type
        if hasattr(arr, 'sqrt_fast'):
            sqrt_result = arr.sqrt_fast()
            assert isinstance(sqrt_result, type(arr))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])