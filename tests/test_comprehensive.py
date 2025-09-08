"""
Comprehensive test suite for ArrPy v1.0.0
Tests all major functionality across backends.
"""

import pytest
import math
import numpy as np
import tempfile
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import arrpy
from arrpy import Backend, set_backend


class TestBackendSystem:
    """Test backend switching and capabilities."""
    
    def test_backend_switching(self):
        """Test that backend switching works."""
        original = arrpy.get_backend()
        
        set_backend('python')
        assert arrpy.get_backend() == Backend.PYTHON
        
        try:
            set_backend('cython')
            assert arrpy.get_backend() == Backend.CYTHON
        except:
            pass  # Cython may not be built
        
        set_backend(original)
    
    def test_backend_enum(self):
        """Test backend enum values."""
        assert Backend.PYTHON.value == 'python'
        assert Backend.CYTHON.value == 'cython'
        assert Backend.C.value == 'c'


class TestArrayCreation:
    """Test array creation functions."""
    
    def setup_method(self):
        set_backend('python')
    
    def test_array_from_list(self):
        """Test creating array from list."""
        a = arrpy.array([1, 2, 3, 4, 5])
        assert a.shape == (5,)
        assert a.dtype == 'float64'
        assert list(a._data) == [1.0, 2.0, 3.0, 4.0, 5.0]
    
    def test_array_2d(self):
        """Test creating 2D array."""
        a = arrpy.array([[1, 2], [3, 4]])
        assert a.shape == (2, 2)
        assert a._data == [1.0, 2.0, 3.0, 4.0]
    
    def test_zeros(self):
        """Test zeros creation."""
        a = arrpy.zeros((2, 3))
        assert a.shape == (2, 3)
        assert all(x == 0 for x in a._data)
    
    def test_ones(self):
        """Test ones creation."""
        a = arrpy.ones((2, 3))
        assert a.shape == (2, 3)
        assert all(x == 1 for x in a._data)
    
    def test_eye(self):
        """Test identity matrix."""
        a = arrpy.eye(3)
        expected = [1, 0, 0, 0, 1, 0, 0, 0, 1]
        assert a._data == expected
    
    def test_arange(self):
        """Test arange."""
        a = arrpy.arange(0, 10, 2)
        assert list(a._data) == [0, 2, 4, 6, 8]
    
    def test_linspace(self):
        """Test linspace."""
        a = arrpy.linspace(0, 1, 5)
        expected = [0.0, 0.25, 0.5, 0.75, 1.0]
        np.testing.assert_array_almost_equal(a._data, expected)


class TestArithmetic:
    """Test arithmetic operations."""
    
    def setup_method(self):
        set_backend('python')
    
    def test_addition(self):
        """Test array addition."""
        a = arrpy.array([1, 2, 3])
        b = arrpy.array([4, 5, 6])
        c = a + b
        assert list(c._data) == [5, 7, 9]
    
    def test_subtraction(self):
        """Test array subtraction."""
        a = arrpy.array([5, 6, 7])
        b = arrpy.array([1, 2, 3])
        c = a - b
        assert list(c._data) == [4, 4, 4]
    
    def test_multiplication(self):
        """Test array multiplication."""
        a = arrpy.array([2, 3, 4])
        b = arrpy.array([5, 6, 7])
        c = a * b
        assert list(c._data) == [10, 18, 28]
    
    def test_division(self):
        """Test array division."""
        a = arrpy.array([10, 20, 30])
        b = arrpy.array([2, 4, 5])
        c = a / b
        assert list(c._data) == [5, 5, 6]
    
    def test_scalar_operations(self):
        """Test scalar broadcasting."""
        a = arrpy.array([1, 2, 3])
        
        b = a + 10
        assert list(b._data) == [11, 12, 13]
        
        c = a * 2
        assert list(c._data) == [2, 4, 6]


class TestBroadcasting:
    """Test broadcasting functionality."""
    
    def setup_method(self):
        set_backend('python')
    
    def test_scalar_broadcast(self):
        """Test scalar to array broadcasting."""
        a = arrpy.array([[1, 2], [3, 4]])
        b = a + 10
        assert list(b._data) == [11, 12, 13, 14]
    
    def test_row_broadcast(self):
        """Test row vector broadcasting."""
        a = arrpy.array([[1, 2, 3], [4, 5, 6]])
        b = arrpy.array([10, 20, 30])
        c = a + b
        expected = [11, 22, 33, 14, 25, 36]
        assert list(c._data) == expected
    
    def test_column_broadcast(self):
        """Test column vector broadcasting."""
        a = arrpy.array([[1, 2], [3, 4]])
        b = arrpy.array([[10], [20]])
        c = a + b
        expected = [11, 12, 23, 24]
        assert list(c._data) == expected


class TestLinearAlgebra:
    """Test linear algebra operations."""
    
    def setup_method(self):
        set_backend('python')
    
    def test_matmul(self):
        """Test matrix multiplication."""
        a = arrpy.array([[1, 2], [3, 4]])
        b = arrpy.array([[5, 6], [7, 8]])
        c = arrpy.matmul(a, b)
        expected = [19, 22, 43, 50]
        assert list(c._data) == expected
    
    def test_dot(self):
        """Test dot product."""
        a = arrpy.array([1, 2, 3])
        b = arrpy.array([4, 5, 6])
        c = arrpy.dot(a, b)
        assert c == 32  # 1*4 + 2*5 + 3*6
    
    def test_solve(self):
        """Test linear system solver."""
        A = arrpy.array([[3, 1], [1, 2]])
        b = arrpy.array([10, 8])
        x = arrpy.solve(A, b)
        # Should get x = [2, 3]
        np.testing.assert_array_almost_equal(x._data, [2, 3])
    
    def test_inverse(self):
        """Test matrix inverse."""
        A = arrpy.array([[1, 2], [3, 4]])
        A_inv = arrpy.inv(A)
        # Verify A * A_inv = I
        I = arrpy.matmul(A, A_inv)
        np.testing.assert_array_almost_equal(I._data[:2], [1, 0], decimal=10)
        np.testing.assert_array_almost_equal(I._data[2:], [0, 1], decimal=10)
    
    def test_determinant(self):
        """Test determinant calculation."""
        A = arrpy.array([[1, 2], [3, 4]])
        det = arrpy.det(A)
        assert abs(det - (-2)) < 1e-10


class TestReductions:
    """Test reduction operations."""
    
    def setup_method(self):
        set_backend('python')
    
    def test_sum(self):
        """Test sum reduction."""
        a = arrpy.array([1, 2, 3, 4, 5])
        assert a.sum() == 15
        
        b = arrpy.array([[1, 2], [3, 4]])
        assert b.sum() == 10
    
    def test_mean(self):
        """Test mean calculation."""
        a = arrpy.array([1, 2, 3, 4, 5])
        assert a.mean() == 3.0
    
    def test_min_max(self):
        """Test min/max."""
        a = arrpy.array([3, 1, 4, 1, 5, 9, 2, 6])
        assert a.min() == 1
        assert a.max() == 9
    
    def test_argmin_argmax(self):
        """Test argmin/argmax."""
        a = arrpy.array([3, 1, 4, 1, 5, 9, 2, 6])
        assert a.argmin() == 1
        assert a.argmax() == 5


class TestUfuncs:
    """Test universal functions."""
    
    def setup_method(self):
        set_backend('python')
    
    def test_trigonometric(self):
        """Test sin, cos, tan."""
        a = arrpy.array([0, math.pi/2, math.pi])
        
        sin_a = arrpy.sin(a)
        np.testing.assert_array_almost_equal(
            sin_a._data, [0, 1, 0], decimal=10
        )
        
        cos_a = arrpy.cos(a)
        np.testing.assert_array_almost_equal(
            cos_a._data, [1, 0, -1], decimal=10
        )
    
    def test_exponential(self):
        """Test exp and log."""
        a = arrpy.array([0, 1, 2])
        
        exp_a = arrpy.exp(a)
        expected = [1, math.e, math.e**2]
        np.testing.assert_array_almost_equal(exp_a._data, expected)
        
        b = arrpy.array([1, math.e, math.e**2])
        log_b = arrpy.log(b)
        np.testing.assert_array_almost_equal(log_b._data, [0, 1, 2])
    
    def test_sqrt(self):
        """Test square root."""
        a = arrpy.array([1, 4, 9, 16])
        sqrt_a = arrpy.sqrt(a)
        assert list(sqrt_a._data) == [1, 2, 3, 4]
    
    def test_abs(self):
        """Test absolute value."""
        a = arrpy.array([-3, -1, 0, 1, 3])
        abs_a = arrpy.abs(a)
        assert list(abs_a._data) == [3, 1, 0, 1, 3]


class TestFFT:
    """Test FFT operations."""
    
    def setup_method(self):
        set_backend('python')
    
    def test_fft_simple(self):
        """Test simple FFT."""
        # Create a simple signal
        a = arrpy.array([1, 0, 1, 0, 1, 0, 1, 0])
        fft_a = arrpy.fft_func(a)
        
        # Should have non-zero DC component
        assert abs(fft_a._data[0]) > 0
    
    def test_fftfreq(self):
        """Test frequency bins."""
        freqs = arrpy.fftfreq(8, 0.125)
        expected = [0, 1, 2, 3, -4, -3, -2, -1]
        assert list(freqs._data) == expected
    
    def test_dct(self):
        """Test discrete cosine transform."""
        a = arrpy.array([1, 2, 3, 4])
        dct_a = arrpy.dct(a)
        # DCT should preserve energy
        assert len(dct_a._data) == 4


class TestIndexing:
    """Test advanced indexing."""
    
    def setup_method(self):
        set_backend('python')
    
    def test_boolean_indexing(self):
        """Test boolean mask indexing."""
        a = arrpy.array([1, 2, 3, 4, 5])
        mask = a > 3
        result = arrpy.boolean_index(a, mask)
        assert list(result._data) == [4, 5]
    
    def test_where(self):
        """Test where function."""
        a = arrpy.array([1, 2, 3, 4, 5])
        result = arrpy.where(a > 3, a, 0)
        assert list(result._data) == [0, 0, 0, 4, 5]
    
    def test_fancy_indexing(self):
        """Test fancy indexing."""
        a = arrpy.array([10, 20, 30, 40, 50])
        indices = arrpy.array([0, 2, 4])
        result = arrpy.fancy_index(a, indices)
        assert list(result._data) == [10, 30, 50]


class TestSorting:
    """Test sorting operations."""
    
    def setup_method(self):
        set_backend('python')
    
    def test_sort(self):
        """Test sorting."""
        a = arrpy.array([3, 1, 4, 1, 5, 9, 2, 6])
        sorted_a = arrpy.sort(a)
        assert list(sorted_a._data) == [1, 1, 2, 3, 4, 5, 6, 9]
    
    def test_argsort(self):
        """Test argsort."""
        a = arrpy.array([3, 1, 4])
        indices = arrpy.argsort(a)
        assert list(indices._data) == [1, 0, 2]
    
    def test_unique(self):
        """Test unique values."""
        a = arrpy.array([1, 2, 2, 3, 3, 3])
        unique_vals, counts = arrpy.unique(a, return_counts=True)
        assert list(unique_vals._data) == [1, 2, 3]
        assert list(counts._data) == [1, 2, 3]


class TestStatistics:
    """Test statistical functions."""
    
    def setup_method(self):
        set_backend('python')
    
    def test_std_var(self):
        """Test standard deviation and variance."""
        a = arrpy.array([1, 2, 3, 4, 5])
        std = arrpy.std(a)
        var = arrpy.var(a)
        
        # Variance should be std^2
        assert abs(var - std**2) < 1e-10
        
        # Check approximate values
        assert abs(std - 1.414) < 0.01
        assert abs(var - 2.0) < 0.01
    
    def test_percentile(self):
        """Test percentile calculation."""
        a = arrpy.array([1, 2, 3, 4, 5])
        
        p0 = arrpy.percentile(a, 0)
        assert p0 == 1
        
        p50 = arrpy.percentile(a, 50)
        assert p50 == 3
        
        p100 = arrpy.percentile(a, 100)
        assert p100 == 5
    
    def test_median(self):
        """Test median."""
        a = arrpy.array([1, 2, 3, 4, 5])
        assert arrpy.median(a) == 3
        
        b = arrpy.array([1, 2, 3, 4])
        assert arrpy.median(b) == 2.5
    
    def test_histogram(self):
        """Test histogram."""
        a = arrpy.array([1, 2, 2, 3, 3, 3])
        hist, edges = arrpy.histogram(a, bins=3)
        
        assert len(hist._data) == 3
        assert len(edges._data) == 4
        assert sum(hist._data) == 6


class TestIO:
    """Test I/O operations."""
    
    def setup_method(self):
        set_backend('python')
    
    def test_save_load_binary(self):
        """Test binary save/load."""
        a = arrpy.array([[1, 2, 3], [4, 5, 6]])
        
        with tempfile.NamedTemporaryFile(suffix='.apy', delete=False) as f:
            temp_file = f.name
        
        try:
            arrpy.save(temp_file, a)
            loaded = arrpy.load(temp_file)
            
            assert loaded.shape == a.shape
            assert list(loaded._data) == list(a._data)
        finally:
            os.unlink(temp_file)
    
    def test_save_load_text(self):
        """Test text save/load."""
        a = arrpy.array([[1, 2], [3, 4]])
        
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            temp_file = f.name
        
        try:
            arrpy.savetxt(temp_file, a, delimiter=',')
            loaded = arrpy.loadtxt(temp_file, delimiter=',')
            
            assert loaded.shape == a.shape
            np.testing.assert_array_almost_equal(loaded._data, a._data)
        finally:
            os.unlink(temp_file)
    
    def test_savez_loadz(self):
        """Test compressed archive save/load."""
        a = arrpy.array([1, 2, 3])
        b = arrpy.array([4, 5, 6])
        
        with tempfile.NamedTemporaryFile(suffix='.apz', delete=False) as f:
            temp_file = f.name
        
        try:
            arrpy.savez(temp_file, array1=a, array2=b)
            loaded = arrpy.loadz(temp_file)
            
            assert 'array1' in loaded
            assert 'array2' in loaded
            assert list(loaded['array1']._data) == [1, 2, 3]
            assert list(loaded['array2']._data) == [4, 5, 6]
        finally:
            os.unlink(temp_file)


class TestBackendConsistency:
    """Test that different backends produce consistent results."""
    
    def test_arithmetic_consistency(self):
        """Test arithmetic operations across backends."""
        data1 = [1, 2, 3, 4, 5]
        data2 = [6, 7, 8, 9, 10]
        
        results = {}
        
        for backend_name in ['python', 'cython']:
            try:
                set_backend(backend_name)
                a = arrpy.array(data1)
                b = arrpy.array(data2)
                
                results[backend_name] = {
                    'add': (a + b)._data,
                    'mul': (a * b)._data,
                    'sum': a.sum(),
                }
            except:
                pass  # Backend may not be available
        
        # If we have multiple backends, check consistency
        if len(results) > 1:
            backends = list(results.keys())
            for i in range(1, len(backends)):
                for op in ['add', 'mul', 'sum']:
                    np.testing.assert_array_almost_equal(
                        results[backends[0]][op],
                        results[backends[i]][op],
                        err_msg=f"{op} inconsistent between {backends[0]} and {backends[i]}"
                    )


class TestComparison:
    """Test comparison operators."""
    
    def setup_method(self):
        set_backend('python')
    
    def test_comparison_operators(self):
        """Test all comparison operators."""
        a = arrpy.array([1, 2, 3, 4, 5])
        b = arrpy.array([3, 3, 3, 3, 3])
        
        # Greater than
        gt = a > b
        assert list(gt._data) == [0, 0, 0, 1, 1]
        
        # Less than
        lt = a < b
        assert list(lt._data) == [1, 1, 0, 0, 0]
        
        # Equal
        eq = a == b
        assert list(eq._data) == [0, 0, 1, 0, 0]
        
        # Not equal
        ne = a != b
        assert list(ne._data) == [1, 1, 0, 1, 1]
        
        # Greater or equal
        ge = a >= b
        assert list(ge._data) == [0, 0, 1, 1, 1]
        
        # Less or equal
        le = a <= b
        assert list(le._data) == [1, 1, 1, 0, 0]
    
    def test_scalar_comparison(self):
        """Test comparison with scalars."""
        a = arrpy.array([1, 2, 3, 4, 5])
        
        gt3 = a > 3
        assert list(gt3._data) == [0, 0, 0, 1, 1]
        
        eq3 = a == 3
        assert list(eq3._data) == [0, 0, 1, 0, 0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])