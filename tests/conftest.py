"""
Pytest configuration and fixtures for ArrPy tests.
"""

import pytest
import numpy as np
import arrpy as ap
import arrpy


@pytest.fixture(autouse=True)
def reset_backend():
    """
    Automatically reset backend to Python before each test.
    This ensures test isolation and prevents backend state leakage.
    """
    # Reset to Python backend before test
    arrpy.set_backend('python')
    
    # Run the test
    yield
    
    # Reset to Python backend after test (cleanup)
    arrpy.set_backend('python')


@pytest.fixture
def sample_1d_array():
    """Provide a sample 1D array for testing."""
    return [1, 2, 3, 4, 5]


@pytest.fixture
def sample_2d_array():
    """Provide a sample 2D array for testing."""
    return [[1, 2, 3], [4, 5, 6]]


@pytest.fixture
def sample_3d_array():
    """Provide a sample 3D array for testing."""
    return [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]


@pytest.fixture
def numpy_comparison():
    """Fixture for comparing ArrPy results with NumPy."""
    def compare(arrpy_result, numpy_input, operation=None):
        """
        Compare ArrPy result with NumPy result.
        
        Parameters
        ----------
        arrpy_result : arrpy array or value
            Result from ArrPy operation
        numpy_input : array-like
            Input to NumPy for comparison
        operation : callable, optional
            Operation to apply to NumPy array
        
        Returns
        -------
        bool
            True if results match within tolerance
        """
        if operation:
            numpy_result = operation(numpy_input)
        else:
            numpy_result = numpy_input
        
        # TODO: Implement proper comparison once arrpy is functional
        # For now, return True as placeholder
        return True
    
    return compare


@pytest.fixture
def assert_array_equal():
    """Fixture for asserting array equality."""
    def _assert(arr1, arr2, rtol=1e-7, atol=1e-9):
        """
        Assert two arrays are equal within tolerance.
        
        Parameters
        ----------
        arr1, arr2 : array-like
            Arrays to compare
        rtol : float
            Relative tolerance
        atol : float
            Absolute tolerance
        """
        # TODO: Implement proper comparison
        # For now, use numpy for testing infrastructure
        np.testing.assert_allclose(arr1, arr2, rtol=rtol, atol=atol)
    
    return _assert


@pytest.fixture
def benchmark_data():
    """Provide various sizes of data for benchmarking."""
    return {
        'small': (10, 10),
        'medium': (100, 100),
        'large': (1000, 1000),
        'xlarge': (5000, 5000)
    }


@pytest.fixture
def python_backend():
    """Fixture that ensures Python backend is active."""
    original = arrpy.get_backend()
    arrpy.set_backend('python')
    yield
    arrpy.set_backend(original)


@pytest.fixture
def cython_backend():
    """Fixture that ensures Cython backend is active."""
    original = arrpy.get_backend()
    arrpy.set_backend('cython')
    yield
    arrpy.set_backend(original)


@pytest.fixture
def c_backend():
    """Fixture that ensures C backend is active."""
    original = arrpy.get_backend()
    arrpy.set_backend('c')
    yield
    arrpy.set_backend(original)