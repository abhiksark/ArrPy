"""
Test performance regression detection.

Simple performance tests to detect if operations become significantly slower.
"""

import time
import pytest
from arrpy import Array, zeros, ones, arange
import arrpy as ap


class PerformanceTimer:
    """Helper class for timing operations."""
    
    def __init__(self):
        self.times = []
    
    def time_operation(self, func, iterations=5):
        """Time an operation multiple times and return average."""
        times = []
        for _ in range(iterations):
            start = time.perf_counter()
            result = func()
            end = time.perf_counter()
            times.append(end - start)
        
        avg_time = sum(times) / len(times)
        self.times.append(avg_time)
        return avg_time


class TestArrayCreationPerformance:
    """Test performance of array creation operations."""
    
    def test_array_creation_from_list_performance(self):
        """Test that array creation from list is reasonably fast."""
        timer = PerformanceTimer()
        
        sizes = [100, 500, 1000]
        
        for size in sizes:
            data = list(range(size))
            
            def create_array():
                return Array(data)
            
            avg_time = timer.time_operation(create_array)
            
            # Very loose bounds - mainly to catch major regressions
            # For 1000 elements, should complete in well under 1 second
            assert avg_time < 1.0, f"Array creation for size {size} took {avg_time:.4f}s"
    
    def test_zeros_creation_performance(self):
        """Test that zeros() creation is reasonably fast."""
        timer = PerformanceTimer()
        
        sizes = [1000, 5000, 10000]
        
        for size in sizes:
            def create_zeros():
                return zeros(size)
            
            avg_time = timer.time_operation(create_zeros)
            
            # Should be very fast for simple allocation
            assert avg_time < 0.5, f"zeros({size}) took {avg_time:.4f}s"
    
    def test_2d_array_creation_performance(self):
        """Test performance of 2D array creation."""
        timer = PerformanceTimer()
        
        shapes = [(100, 100), (200, 50), (50, 200)]
        
        for shape in shapes:
            data = [[i + j for j in range(shape[1])] for i in range(shape[0])]
            
            def create_2d_array():
                return Array(data)
            
            avg_time = timer.time_operation(create_2d_array)
            
            # Should complete reasonably quickly
            total_elements = shape[0] * shape[1]
            assert avg_time < 2.0, f"2D array creation {shape} took {avg_time:.4f}s"


class TestArithmeticPerformance:
    """Test performance of arithmetic operations."""
    
    def test_scalar_addition_performance(self):
        """Test scalar addition performance."""
        timer = PerformanceTimer()
        
        sizes = [1000, 5000, 10000]
        
        for size in sizes:
            arr = arange(size)
            
            def scalar_add():
                return arr + 5
            
            avg_time = timer.time_operation(scalar_add)
            
            # Scalar operations should be fast
            assert avg_time < 0.1, f"Scalar addition for size {size} took {avg_time:.4f}s"
    
    def test_array_addition_performance(self):
        """Test array addition performance."""
        timer = PerformanceTimer()
        
        sizes = [1000, 5000, 10000]
        
        for size in sizes:
            arr1 = arange(size)
            arr2 = arange(size)
            
            def array_add():
                return arr1 + arr2
            
            avg_time = timer.time_operation(array_add)
            
            # Element-wise operations should scale linearly
            assert avg_time < 0.2, f"Array addition for size {size} took {avg_time:.4f}s"
    
    def test_matrix_multiplication_performance(self):
        """Test matrix multiplication performance."""
        timer = PerformanceTimer()
        
        sizes = [50, 100, 150]  # Keep sizes reasonable for O(n³) operation
        
        for size in sizes:
            data = [[i + j + 1 for j in range(size)] for i in range(size)]
            arr1 = Array(data)
            arr2 = Array(data)
            
            def matrix_mult():
                return arr1.dot(arr2)
            
            avg_time = timer.time_operation(matrix_mult)
            
            # Matrix multiplication is O(n³), so bounds are looser
            max_time = 0.05 * (size / 50) ** 3  # Scale with cube of size, more lenient
            assert avg_time < max_time, f"Matrix mult {size}x{size} took {avg_time:.4f}s"


class TestAggregationPerformance:
    """Test performance of aggregation operations."""
    
    def test_sum_performance(self):
        """Test sum operation performance."""
        timer = PerformanceTimer()
        
        sizes = [10000, 50000, 100000]
        
        for size in sizes:
            arr = arange(size)
            
            def sum_operation():
                return arr.sum()
            
            avg_time = timer.time_operation(sum_operation)
            
            # Sum should be linear in size
            assert avg_time < 0.1, f"Sum for size {size} took {avg_time:.4f}s"
    
    def test_mean_performance(self):
        """Test mean operation performance."""
        timer = PerformanceTimer()
        
        sizes = [10000, 50000, 100000]
        
        for size in sizes:
            arr = arange(size)
            
            def mean_operation():
                return arr.mean()
            
            avg_time = timer.time_operation(mean_operation)
            
            # Mean should be similar to sum performance
            assert avg_time < 0.1, f"Mean for size {size} took {avg_time:.4f}s"
    
    def test_min_max_performance(self):
        """Test min/max operation performance."""
        timer = PerformanceTimer()
        
        sizes = [10000, 50000, 100000]
        
        for size in sizes:
            # Create array with random-ish data
            data = [(i * 17 + 23) % 1000 for i in range(size)]
            arr = Array(data)
            
            def min_operation():
                return arr.min()
            
            def max_operation():
                return arr.max()
            
            min_time = timer.time_operation(min_operation)
            max_time = timer.time_operation(max_operation)
            
            # Min/max should be linear
            assert min_time < 0.1, f"Min for size {size} took {min_time:.4f}s"
            assert max_time < 0.1, f"Max for size {size} took {max_time:.4f}s"


class TestMathematicalFunctionPerformance:
    """Test performance of mathematical functions."""
    
    def test_trigonometric_performance(self):
        """Test trigonometric function performance."""
        timer = PerformanceTimer()
        
        sizes = [1000, 5000, 10000]
        
        for size in sizes:
            # Use small values to avoid numerical issues
            data = [i * 0.001 for i in range(size)]
            arr = Array(data)
            
            def sin_operation():
                return ap.sin(arr)
            
            def cos_operation():
                return ap.cos(arr)
            
            sin_time = timer.time_operation(sin_operation)
            cos_time = timer.time_operation(cos_operation)
            
            # Trig functions are more expensive but should still be reasonable
            assert sin_time < 0.5, f"Sin for size {size} took {sin_time:.4f}s"
            assert cos_time < 0.5, f"Cos for size {size} took {cos_time:.4f}s"
    
    def test_exponential_logarithm_performance(self):
        """Test exp/log function performance."""
        timer = PerformanceTimer()
        
        sizes = [100, 500, 1000]  # Smaller sizes to avoid overflow
        
        for size in sizes:
            # Use smaller positive values to avoid overflow
            data = [i * 0.01 + 1 for i in range(size)]
            arr = Array(data)
            
            def exp_operation():
                return arr.exp()
            
            def log_operation():
                return arr.log()
            
            try:
                exp_time = timer.time_operation(exp_operation)
                # Exp/log are expensive operations
                assert exp_time < 1.0, f"Exp for size {size} took {exp_time:.4f}s"
            except OverflowError:
                pytest.skip("Exp overflow with large values")
            
            log_time = timer.time_operation(log_operation)
            assert log_time < 1.0, f"Log for size {size} took {log_time:.4f}s"


class TestIndexingPerformance:
    """Test performance of indexing operations."""
    
    def test_single_element_access_performance(self):
        """Test single element access performance."""
        timer = PerformanceTimer()
        
        size = 10000
        arr = arange(size)
        
        def access_elements():
            total = 0
            # Access 1000 random elements
            for i in range(0, min(1000, size), 10):
                total += arr[i]
            return total
        
        avg_time = timer.time_operation(access_elements)
        
        # Individual element access should be very fast
        assert avg_time < 0.01, f"Element access took {avg_time:.4f}s"
    
    def test_2d_indexing_performance(self):
        """Test 2D indexing performance."""
        timer = PerformanceTimer()
        
        size = 100  # 100x100 = 10,000 elements
        data = [[i + j for j in range(size)] for i in range(size)]
        arr = Array(data)
        
        def access_2d_elements():
            total = 0
            # Access elements along diagonal and some others
            for i in range(0, size, 5):
                for j in range(0, size, 5):
                    total += arr[i, j]
            return total
        
        avg_time = timer.time_operation(access_2d_elements)
        
        # 2D access should still be fast
        assert avg_time < 0.05, f"2D element access took {avg_time:.4f}s"


class TestReshapePerformance:
    """Test performance of reshape operations."""
    
    def test_reshape_performance(self):
        """Test reshape operation performance."""
        timer = PerformanceTimer()
        
        sizes = [1000, 5000, 10000]
        
        for size in sizes:
            # Create array that can be reshaped to different forms
            arr = arange(size)
            
            def reshape_operation():
                # Find a valid reshape target
                sqrt_size = int(size ** 0.5)
                while size % sqrt_size != 0:
                    sqrt_size -= 1
                target_shape = (sqrt_size, size // sqrt_size)
                return arr.reshape(target_shape)
            
            avg_time = timer.time_operation(reshape_operation)
            
            # Reshape should be fast (mainly metadata changes)
            assert avg_time < 0.1, f"Reshape for size {size} took {avg_time:.4f}s"
    
    def test_transpose_performance(self):
        """Test transpose operation performance."""
        timer = PerformanceTimer()
        
        sizes = [(100, 100), (200, 50), (50, 200)]
        
        for shape in sizes:
            data = [[i + j for j in range(shape[1])] for i in range(shape[0])]
            arr = Array(data)
            
            def transpose_operation():
                return arr.T
            
            avg_time = timer.time_operation(transpose_operation)
            
            # Transpose should be relatively fast
            total_elements = shape[0] * shape[1]
            assert avg_time < 0.1, f"Transpose {shape} took {avg_time:.4f}s"


class TestComparisonPerformance:
    """Test performance of comparison operations."""
    
    def test_equality_comparison_performance(self):
        """Test equality comparison performance."""
        timer = PerformanceTimer()
        
        sizes = [10000, 50000, 100000]
        
        for size in sizes:
            arr1 = arange(size)
            arr2 = arange(size)
            # Modify a few elements to make comparison interesting
            arr2._data[size//2] = -1
            
            def equality_operation():
                return arr1 == arr2
            
            avg_time = timer.time_operation(equality_operation)
            
            # Comparison should be linear
            assert avg_time < 0.1, f"Equality for size {size} took {avg_time:.4f}s"
    
    def test_relational_comparison_performance(self):
        """Test relational comparison performance."""
        timer = PerformanceTimer()
        
        sizes = [10000, 50000, 100000]
        
        for size in sizes:
            arr = arange(size)
            
            def greater_than_operation():
                return arr > size // 2
            
            avg_time = timer.time_operation(greater_than_operation)
            
            # Relational comparison should be linear
            assert avg_time < 0.1, f"Greater than for size {size} took {avg_time:.4f}s"


class TestMemoryEfficiency:
    """Test memory usage patterns (basic checks)."""
    
    def test_array_memory_not_excessive(self):
        """Test that arrays don't use excessive memory."""
        import sys
        
        # Create a reasonably large array
        size = 10000
        arr = arange(size)
        
        # Get memory usage (rough estimate)
        memory_usage = sys.getsizeof(arr._data)
        
        # Should not use more than a few times the basic data size
        # This is a very rough check
        expected_max = size * 8 * 10  # 10x overhead allowance
        assert memory_usage < expected_max, f"Memory usage {memory_usage} seems excessive"
    
    def test_empty_array_memory_efficiency(self):
        """Test that empty arrays don't waste memory."""
        import sys

# Import helper for type checking that works with hybrid arrays
try:
    from test_imports import is_array
except ImportError:
    def is_array(obj):
        return isinstance(obj, Array)

        
        empty_arr = Array([])
        memory_usage = sys.getsizeof(empty_arr._data)
        
        # Empty array should use very little memory
        assert memory_usage < 1000, f"Empty array uses {memory_usage} bytes"


class TestPerformanceScaling:
    """Test that performance scales appropriately with size."""
    
    def test_linear_operations_scale_linearly(self):
        """Test that O(n) operations scale approximately linearly."""
        timer = PerformanceTimer()
        
        # Test sum operation at different sizes
        sizes = [1000, 2000, 4000]
        times = []
        
        for size in sizes:
            arr = arange(size)
            
            def sum_op():
                return arr.sum()
            
            avg_time = timer.time_operation(sum_op, iterations=3)
            times.append(avg_time)
        
        # Check that time roughly doubles as size doubles
        # Allow for significant variation due to system factors
        ratio1 = times[1] / times[0] if times[0] > 0 else float('inf')
        ratio2 = times[2] / times[1] if times[1] > 0 else float('inf')
        
        # Ratios should be reasonably close to 2 (within factor of 4)
        assert 0.5 < ratio1 < 4, f"Scaling ratio 1: {ratio1}"
        assert 0.5 < ratio2 < 4, f"Scaling ratio 2: {ratio2}"
    
    def test_quadratic_operations_scale_appropriately(self):
        """Test that O(n²) operations scale appropriately."""
        timer = PerformanceTimer()
        
        # Test matrix multiplication at different sizes
        sizes = [50, 70, 100]  # Keep small due to O(n³) complexity
        times = []
        
        for size in sizes:
            data = [[1 for _ in range(size)] for _ in range(size)]
            arr = Array(data)
            
            def matmul_op():
                return arr.dot(arr)
            
            avg_time = timer.time_operation(matmul_op, iterations=2)
            times.append(avg_time)
        
        # Matrix multiplication is O(n³), so time should grow cubically
        # This is a very loose check due to the complexity
        assert times[2] > times[0], "Time should increase with size"
        assert times[1] > times[0], "Time should increase with size"


@pytest.mark.slow
class TestLongRunningPerformance:
    """Performance tests that take longer to run."""
    
    def test_large_array_operations(self):
        """Test operations on larger arrays."""
        timer = PerformanceTimer()
        
        # Test with a larger array
        size = 100000
        arr = arange(size)
        
        def large_sum():
            return arr.sum()
        
        def large_mean():
            return arr.mean()
        
        sum_time = timer.time_operation(large_sum, iterations=3)
        mean_time = timer.time_operation(large_mean, iterations=3)
        
        # Even large operations should complete in reasonable time
        assert sum_time < 1.0, f"Large sum took {sum_time:.4f}s"
        assert mean_time < 1.0, f"Large mean took {mean_time:.4f}s"
    
    def test_repeated_operations_performance(self):
        """Test that repeated operations don't degrade performance."""
        timer = PerformanceTimer()
        
        arr = arange(1000)
        
        # Time the first few operations
        initial_times = []
        for _ in range(5):
            def operation():
                return (arr + 1) * 2
            
            time_taken = timer.time_operation(operation, iterations=1)
            initial_times.append(time_taken)
        
        # Time operations after many repetitions
        for _ in range(100):
            (arr + 1) * 2  # Do operation many times
        
        later_times = []
        for _ in range(5):
            def operation():
                return (arr + 1) * 2
            
            time_taken = timer.time_operation(operation, iterations=1)
            later_times.append(time_taken)
        
        # Later operations shouldn't be significantly slower
        avg_initial = sum(initial_times) / len(initial_times)
        avg_later = sum(later_times) / len(later_times)
        
        # Allow for some variation, but shouldn't be much slower
        assert avg_later < avg_initial * 3, f"Performance degraded: {avg_initial:.4f} -> {avg_later:.4f}"