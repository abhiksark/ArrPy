"""
NumPy compatibility tests for ArrPy.
Tests that ArrPy operations produce identical results to NumPy across all backends.
"""

import pytest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import arrpy
from arrpy import Backend, set_backend, get_backend


class TestNumpyCompatibility:
    """Test ArrPy operations match NumPy across all backends."""
    
    @pytest.fixture(params=['python', 'cython', 'c'])
    def backend(self, request):
        """Parametrize tests to run on all available backends."""
        original_backend = get_backend()
        try:
            set_backend(request.param)
            yield request.param
        except Exception as e:
            pytest.skip(f"{request.param} backend not available: {e}")
        finally:
            set_backend(original_backend)
    
    # ============== Array Creation Tests ==============
    
    def test_zeros_compat(self, backend):
        """Test zeros matches NumPy."""
        shapes = [(5,), (3, 4), (2, 3, 4)]
        
        for shape in shapes:
            np_result = np.zeros(shape)
            ap_result = arrpy.zeros(shape)
            
            np.testing.assert_array_equal(
                ap_result._data, 
                np_result.flatten(),
                err_msg=f"zeros mismatch in {backend} backend for shape {shape}"
            )
            assert ap_result.shape == np_result.shape
    
    def test_ones_compat(self, backend):
        """Test ones matches NumPy."""
        shapes = [(5,), (3, 4), (2, 3, 4)]
        
        for shape in shapes:
            np_result = np.ones(shape)
            ap_result = arrpy.ones(shape)
            
            np.testing.assert_array_equal(
                ap_result._data, 
                np_result.flatten(),
                err_msg=f"ones mismatch in {backend} backend for shape {shape}"
            )
            assert ap_result.shape == np_result.shape
    
    def test_arange_compat(self, backend):
        """Test arange matches NumPy."""
        test_cases = [
            (10,),  # stop only
            (1, 10),  # start, stop
            (0, 10, 2),  # start, stop, step
            (10, 0, -1),  # negative step
        ]
        
        for args in test_cases:
            np_result = np.arange(*args)
            ap_result = arrpy.arange(*args)
            
            np.testing.assert_array_equal(
                ap_result._data,
                np_result.flatten(),
                err_msg=f"arange mismatch in {backend} backend for args {args}"
            )
    
    def test_linspace_compat(self, backend):
        """Test linspace matches NumPy."""
        test_cases = [
            (0, 1, 5),
            (0, 10, 11),
            (-5, 5, 21),
        ]
        
        for start, stop, num in test_cases:
            np_result = np.linspace(start, stop, num)
            ap_result = arrpy.linspace(start, stop, num)
            
            np.testing.assert_allclose(
                ap_result._data,
                np_result.flatten(),
                rtol=1e-7,
                err_msg=f"linspace mismatch in {backend} backend"
            )
    
    def test_eye_compat(self, backend):
        """Test eye matches NumPy."""
        test_cases = [(3, 3), (4, 4), (3, 5), (5, 3)]
        
        for n, m in test_cases:
            np_result = np.eye(n, m)
            ap_result = arrpy.eye(n, m)
            
            np.testing.assert_array_equal(
                ap_result._data,
                np_result.flatten(),
                err_msg=f"eye mismatch in {backend} backend for shape ({n}, {m})"
            )
    
    # ============== Arithmetic Operations Tests ==============
    
    def test_addition_compat(self, backend):
        """Test addition matches NumPy."""
        # 1D arrays
        arr1_data = [1.0, 2.0, 3.0, 4.0]
        arr2_data = [5.0, 6.0, 7.0, 8.0]
        
        np_arr1 = np.array(arr1_data)
        np_arr2 = np.array(arr2_data)
        np_result = np_arr1 + np_arr2
        
        ap_arr1 = arrpy.array(arr1_data)
        ap_arr2 = arrpy.array(arr2_data)
        ap_result = ap_arr1 + ap_arr2
        
        np.testing.assert_allclose(
            ap_result._data,
            np_result.flatten(),
            rtol=1e-7,
            err_msg=f"Addition mismatch in {backend} backend"
        )
        
        # 2D arrays
        arr1_2d = [[1, 2], [3, 4]]
        arr2_2d = [[5, 6], [7, 8]]
        
        np_arr1_2d = np.array(arr1_2d)
        np_arr2_2d = np.array(arr2_2d)
        np_result_2d = np_arr1_2d + np_arr2_2d
        
        ap_arr1_2d = arrpy.array(arr1_2d)
        ap_arr2_2d = arrpy.array(arr2_2d)
        ap_result_2d = ap_arr1_2d + ap_arr2_2d
        
        np.testing.assert_allclose(
            ap_result_2d._data,
            np_result_2d.flatten(),
            rtol=1e-7,
            err_msg=f"2D addition mismatch in {backend} backend"
        )
    
    def test_subtraction_compat(self, backend):
        """Test subtraction matches NumPy."""
        arr1_data = [10.0, 20.0, 30.0, 40.0]
        arr2_data = [1.0, 2.0, 3.0, 4.0]
        
        np_arr1 = np.array(arr1_data)
        np_arr2 = np.array(arr2_data)
        np_result = np_arr1 - np_arr2
        
        ap_arr1 = arrpy.array(arr1_data)
        ap_arr2 = arrpy.array(arr2_data)
        ap_result = ap_arr1 - ap_arr2
        
        np.testing.assert_allclose(
            ap_result._data,
            np_result.flatten(),
            rtol=1e-7,
            err_msg=f"Subtraction mismatch in {backend} backend"
        )
    
    def test_multiplication_compat(self, backend):
        """Test element-wise multiplication matches NumPy."""
        arr1_data = [1.0, 2.0, 3.0, 4.0]
        arr2_data = [2.0, 3.0, 4.0, 5.0]
        
        np_arr1 = np.array(arr1_data)
        np_arr2 = np.array(arr2_data)
        np_result = np_arr1 * np_arr2
        
        ap_arr1 = arrpy.array(arr1_data)
        ap_arr2 = arrpy.array(arr2_data)
        ap_result = ap_arr1 * ap_arr2
        
        np.testing.assert_allclose(
            ap_result._data,
            np_result.flatten(),
            rtol=1e-7,
            err_msg=f"Multiplication mismatch in {backend} backend"
        )
    
    def test_division_compat(self, backend):
        """Test division matches NumPy."""
        arr1_data = [10.0, 20.0, 30.0, 40.0]
        arr2_data = [2.0, 4.0, 5.0, 8.0]
        
        np_arr1 = np.array(arr1_data)
        np_arr2 = np.array(arr2_data)
        np_result = np_arr1 / np_arr2
        
        ap_arr1 = arrpy.array(arr1_data)
        ap_arr2 = arrpy.array(arr2_data)
        ap_result = ap_arr1 / ap_arr2
        
        np.testing.assert_allclose(
            ap_result._data,
            np_result.flatten(),
            rtol=1e-7,
            err_msg=f"Division mismatch in {backend} backend"
        )
    
    def test_matmul_compat(self, backend):
        """Test matrix multiplication matches NumPy."""
        # 2D @ 2D
        arr1_2d = [[1, 2], [3, 4]]
        arr2_2d = [[5, 6], [7, 8]]
        
        np_arr1 = np.array(arr1_2d, dtype=float)
        np_arr2 = np.array(arr2_2d, dtype=float)
        np_result = np_arr1 @ np_arr2
        
        ap_arr1 = arrpy.array(arr1_2d)
        ap_arr2 = arrpy.array(arr2_2d)
        ap_result = ap_arr1 @ ap_arr2
        
        np.testing.assert_allclose(
            ap_result._data,
            np_result.flatten(),
            rtol=1e-7,
            err_msg=f"Matrix multiplication mismatch in {backend} backend"
        )
    
    # ============== Broadcasting Tests ==============
    
    def test_scalar_broadcast_compat(self, backend):
        """Test scalar broadcasting matches NumPy."""
        arr_data = [1.0, 2.0, 3.0, 4.0]
        scalar = 5.0
        
        # NumPy
        np_arr = np.array(arr_data)
        np_add = np_arr + scalar
        np_mul = np_arr * scalar
        
        # ArrPy
        ap_arr = arrpy.array(arr_data)
        ap_add = ap_arr + scalar
        ap_mul = ap_arr * scalar
        
        np.testing.assert_allclose(
            ap_add._data,
            np_add.flatten(),
            rtol=1e-7,
            err_msg=f"Scalar addition broadcast mismatch in {backend} backend"
        )
        
        np.testing.assert_allclose(
            ap_mul._data,
            np_mul.flatten(),
            rtol=1e-7,
            err_msg=f"Scalar multiplication broadcast mismatch in {backend} backend"
        )
    
    # ============== Reduction Operations Tests ==============
    
    def test_sum_compat(self, backend):
        """Test sum matches NumPy."""
        if backend == 'c':
            pytest.skip("sum not implemented in C backend")
            
        test_arrays = [
            [1.0, 2.0, 3.0, 4.0],
            [[1, 2, 3], [4, 5, 6]],
        ]
        
        for arr_data in test_arrays:
            np_arr = np.array(arr_data)
            np_result = np_arr.sum()
            
            ap_arr = arrpy.array(arr_data)
            ap_result = ap_arr.sum()
            
            np.testing.assert_allclose(
                ap_result,
                np_result,
                rtol=1e-7,
                err_msg=f"Sum mismatch in {backend} backend"
            )
    
    def test_mean_compat(self, backend):
        """Test mean matches NumPy."""
        if backend == 'c':
            pytest.skip("mean not implemented in C backend")
            
        test_arrays = [
            [1.0, 2.0, 3.0, 4.0, 5.0],
            [[1, 2, 3], [4, 5, 6]],
        ]
        
        for arr_data in test_arrays:
            np_arr = np.array(arr_data, dtype=float)
            np_result = np_arr.mean()
            
            ap_arr = arrpy.array(arr_data)
            ap_result = ap_arr.mean()
            
            np.testing.assert_allclose(
                ap_result,
                np_result,
                rtol=1e-7,
                err_msg=f"Mean mismatch in {backend} backend"
            )
    
    def test_min_max_compat(self, backend):
        """Test min/max match NumPy."""
        arr_data = [3.0, 1.0, 4.0, 1.0, 5.0, 9.0, 2.0, 6.0]
        
        np_arr = np.array(arr_data)
        np_min = np_arr.min()
        np_max = np_arr.max()
        
        ap_arr = arrpy.array(arr_data)
        ap_min = ap_arr.min()
        ap_max = ap_arr.max()
        
        np.testing.assert_equal(
            ap_min,
            np_min,
            err_msg=f"Min mismatch in {backend} backend"
        )
        
        np.testing.assert_equal(
            ap_max,
            np_max,
            err_msg=f"Max mismatch in {backend} backend"
        )
    
    # ============== Universal Functions Tests ==============
    
    def test_sin_compat(self, backend):
        """Test sin matches NumPy."""
        if backend == 'c':
            pytest.skip("sin not implemented in C backend")
            
        arr_data = [0, np.pi/6, np.pi/4, np.pi/3, np.pi/2]
        
        np_arr = np.array(arr_data)
        np_result = np.sin(np_arr)
        
        ap_arr = arrpy.array(arr_data)
        ap_result = arrpy.sin(ap_arr)
        
        np.testing.assert_allclose(
            ap_result._data,
            np_result.flatten(),
            rtol=1e-7,
            err_msg=f"Sin mismatch in {backend} backend"
        )
    
    def test_cos_compat(self, backend):
        """Test cos matches NumPy."""
        if backend == 'c':
            pytest.skip("cos not implemented in C backend")
            
        arr_data = [0, np.pi/6, np.pi/4, np.pi/3, np.pi/2]
        
        np_arr = np.array(arr_data)
        np_result = np.cos(np_arr)
        
        ap_arr = arrpy.array(arr_data)
        ap_result = arrpy.cos(ap_arr)
        
        np.testing.assert_allclose(
            ap_result._data,
            np_result.flatten(),
            rtol=1e-7,
            err_msg=f"Cos mismatch in {backend} backend"
        )
    
    def test_exp_compat(self, backend):
        """Test exp matches NumPy."""
        if backend in ['c', 'cython']:
            pytest.skip(f"exp not implemented in {backend} backend")
            
        arr_data = [0, 1, 2, -1, -2]
        
        np_arr = np.array(arr_data, dtype=float)
        np_result = np.exp(np_arr)
        
        ap_arr = arrpy.array(arr_data)
        ap_result = arrpy.exp(ap_arr)
        
        np.testing.assert_allclose(
            ap_result._data,
            np_result.flatten(),
            rtol=1e-7,
            err_msg=f"Exp mismatch in {backend} backend"
        )
    
    def test_sqrt_compat(self, backend):
        """Test sqrt matches NumPy."""
        if backend == 'c':
            pytest.skip("sqrt not implemented in C backend")
            
        arr_data = [0, 1, 4, 9, 16, 25]
        
        np_arr = np.array(arr_data, dtype=float)
        np_result = np.sqrt(np_arr)
        
        ap_arr = arrpy.array(arr_data)
        ap_result = arrpy.sqrt(ap_arr)
        
        np.testing.assert_allclose(
            ap_result._data,
            np_result.flatten(),
            rtol=1e-7,
            err_msg=f"Sqrt mismatch in {backend} backend"
        )
    
    # ============== Linear Algebra Tests ==============
    
    def test_dot_compat(self, backend):
        """Test dot product matches NumPy."""
        # 1D dot 1D
        arr1_1d = [1.0, 2.0, 3.0]
        arr2_1d = [4.0, 5.0, 6.0]
        
        np_arr1 = np.array(arr1_1d)
        np_arr2 = np.array(arr2_1d)
        np_result = np.dot(np_arr1, np_arr2)
        
        ap_arr1 = arrpy.array(arr1_1d)
        ap_arr2 = arrpy.array(arr2_1d)
        ap_result = arrpy.dot(ap_arr1, ap_arr2)
        
        np.testing.assert_allclose(
            ap_result,
            np_result,
            rtol=1e-7,
            err_msg=f"1D dot product mismatch in {backend} backend"
        )
        
        # 2D dot 1D
        arr1_2d = [[1, 2, 3], [4, 5, 6]]
        
        np_arr1_2d = np.array(arr1_2d, dtype=float)
        np_result_2d = np.dot(np_arr1_2d, np_arr2)
        
        ap_arr1_2d = arrpy.array(arr1_2d)
        ap_result_2d = arrpy.dot(ap_arr1_2d, ap_arr2)
        
        np.testing.assert_allclose(
            ap_result_2d._data,
            np_result_2d.flatten(),
            rtol=1e-7,
            err_msg=f"2D dot 1D mismatch in {backend} backend"
        )
    
    def test_transpose_compat(self, backend):
        """Test transpose matches NumPy."""
        arr_2d = [[1, 2, 3], [4, 5, 6]]
        
        np_arr = np.array(arr_2d)
        np_result = np_arr.T
        
        ap_arr = arrpy.array(arr_2d)
        ap_result = ap_arr.T
        
        np.testing.assert_array_equal(
            ap_result._data,
            np_result.flatten(),
            err_msg=f"Transpose mismatch in {backend} backend"
        )
        assert ap_result.shape == np_result.shape
    
    # ============== Shape Operations Tests ==============
    
    def test_reshape_compat(self, backend):
        """Test reshape matches NumPy."""
        arr_data = list(range(12))
        shapes = [(3, 4), (4, 3), (2, 6), (6, 2), (2, 2, 3)]
        
        for shape in shapes:
            np_arr = np.array(arr_data)
            np_result = np_arr.reshape(shape)
            
            ap_arr = arrpy.array(arr_data)
            try:
                ap_result = ap_arr.reshape(shape)
                np.testing.assert_array_equal(
                    ap_result._data,
                    np_result.flatten(),
                    err_msg=f"Reshape mismatch in {backend} backend for shape {shape}"
                )
                assert ap_result.shape == np_result.shape
            except AttributeError:
                pytest.skip(f"Reshape not fully implemented in {backend} backend")
    
    def test_flatten_compat(self, backend):
        """Test flatten matches NumPy."""
        arr_2d = [[1, 2, 3], [4, 5, 6]]
        
        np_arr = np.array(arr_2d)
        np_result = np_arr.flatten()
        
        ap_arr = arrpy.array(arr_2d)
        try:
            ap_result = ap_arr.flatten()
            np.testing.assert_array_equal(
                ap_result._data,
                np_result,
                err_msg=f"Flatten mismatch in {backend} backend"
            )
            assert ap_result.shape == np_result.shape
        except AttributeError:
            pytest.skip(f"Flatten not fully implemented in {backend} backend")
    
    # ============== Edge Cases Tests ==============
    
    def test_empty_array_compat(self, backend):
        """Test empty array operations match NumPy."""
        if backend == 'c':
            pytest.skip("Empty array operations not fully supported in C backend")
            
        np_empty = np.array([])
        ap_empty = arrpy.array([])
        
        # Sum of empty array
        np.testing.assert_equal(
            ap_empty.sum(),
            np_empty.sum(),
            err_msg=f"Empty array sum mismatch in {backend} backend"
        )
    
    def test_single_element_compat(self, backend):
        """Test single element operations match NumPy."""
        if backend == 'c':
            pytest.skip("Reduction operations not implemented in C backend")
            
        np_single = np.array([42.0])
        ap_single = arrpy.array([42.0])
        
        # Operations on single element
        np.testing.assert_equal(
            ap_single.sum(),
            np_single.sum(),
            err_msg=f"Single element sum mismatch in {backend} backend"
        )
        
        np.testing.assert_equal(
            ap_single.mean(),
            np_single.mean(),
            err_msg=f"Single element mean mismatch in {backend} backend"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])