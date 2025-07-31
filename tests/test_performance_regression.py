"""
Performance regression tests for ArrPy Cython implementation.

These tests ensure that the Cython implementation maintains expected
performance characteristics and doesn't regress over time.
"""

import pytest
import time
import statistics
from typing import List, Tuple

from arrpy.core import Array
from arrpy.creation import zeros, ones, full
from arrpy.math import power, absolute


class PerformanceTimer:
    """Helper class for timing operations with statistical analysis."""
    
    def __init__(self, warmup_runs: int = 3, test_runs: int = 10):
        self.warmup_runs = warmup_runs
        self.test_runs = test_runs
    
    def time_operation(self, operation, *args, **kwargs) -> Tuple[float, List[float]]:
        """
        Time an operation multiple times and return mean and all times.
        
        Returns:
            Tuple of (mean_time, all_times)
        """
        # Warmup runs
        for _ in range(self.warmup_runs):
            operation(*args, **kwargs)
        
        # Actual timing runs
        times = []
        for _ in range(self.test_runs):
            start = time.perf_counter()
            operation(*args, **kwargs)
            end = time.perf_counter()
            times.append(end - start)
        
        return statistics.mean(times), times


class TestArrayCreationPerformance:
    """Test performance of array creation operations."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.timer = PerformanceTimer()
        self.small_data = [[i + j for j in range(10)] for i in range(10)]
        self.medium_data = [[i + j for j in range(50)] for i in range(20)]
        self.large_data = [[i + j for j in range(100)] for i in range(50)]
    
    def test_array_creation_small(self):
        """Test Array creation performance with small data."""
        mean_time, _ = self.timer.time_operation(Array, self.small_data)
        
        # Should complete in reasonable time (< 1ms for small arrays)
        assert mean_time < 0.001, f"Small array creation took {mean_time:.6f}s, expected < 0.001s"
    
    def test_array_creation_medium(self):
        """Test Array creation performance with medium data."""
        mean_time, _ = self.timer.time_operation(Array, self.medium_data)
        
        # Should complete in reasonable time (< 5ms for medium arrays)
        assert mean_time < 0.005, f"Medium array creation took {mean_time:.6f}s, expected < 0.005s"
    
    def test_zeros_creation_performance(self):
        """Test zeros creation performance."""
        shapes = [(100,), (50, 20), (10, 10, 10)]
        
        for shape in shapes:
            mean_time, _ = self.timer.time_operation(zeros, shape)
            elements = 1
            for dim in shape:
                elements *= dim
            
            # Should be very fast for creation functions
            time_per_element = mean_time / elements
            assert time_per_element < 1e-6, f"zeros({shape}) too slow: {time_per_element:.2e}s per element"
    
    def test_ones_creation_performance(self):
        """Test ones creation performance."""
        shapes = [(100,), (50, 20), (10, 10, 10)]
        
        for shape in shapes:
            mean_time, _ = self.timer.time_operation(ones, shape)
            elements = 1
            for dim in shape:
                elements *= dim
            
            time_per_element = mean_time / elements
            assert time_per_element < 1e-6, f"ones({shape}) too slow: {time_per_element:.2e}s per element"


class TestArithmeticPerformance:
    """Test performance of arithmetic operations."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.timer = PerformanceTimer()
        
        # Create test arrays of different sizes
        self.small_arr = Array([[i + j for j in range(10)] for i in range(10)])
        self.medium_arr = Array([[i + j for j in range(50)] for i in range(20)])
        self.large_arr = Array([[i + j for j in range(100)] for i in range(50)])
    
    def test_addition_performance(self):
        """Test addition performance."""
        arrays = [
            ("small", self.small_arr),
            ("medium", self.medium_arr),
            ("large", self.large_arr)
        ]
        
        for size_name, arr in arrays:
            mean_time, _ = self.timer.time_operation(lambda a: a + a, arr)
            
            # Time per element should be very small
            time_per_element = mean_time / arr.size
            assert time_per_element < 1e-6, f"{size_name} addition too slow: {time_per_element:.2e}s per element"
    
    def test_multiplication_performance(self):
        """Test multiplication performance."""
        arrays = [
            ("small", self.small_arr),
            ("medium", self.medium_arr),
            ("large", self.large_arr)
        ]
        
        for size_name, arr in arrays:
            mean_time, _ = self.timer.time_operation(lambda a: a * 2, arr)
            
            time_per_element = mean_time / arr.size
            assert time_per_element < 1e-6, f"{size_name} multiplication too slow: {time_per_element:.2e}s per element"
    
    def test_power_performance(self):
        """Test power function performance."""
        test_arrays = [
            ("small", Array([float(i) for i in range(100)])),
            ("medium", Array([float(i) for i in range(1000)])),
        ]
        
        for size_name, arr in test_arrays:
            mean_time, _ = self.timer.time_operation(power, arr, 2)
            
            time_per_element = mean_time / arr.size
            assert time_per_element < 1e-5, f"{size_name} power too slow: {time_per_element:.2e}s per element"


class TestAggregationPerformance:
    """Test performance of aggregation operations."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.timer = PerformanceTimer()
        
        # Create test arrays with different sizes
        self.test_arrays = [
            ("tiny", Array([float(i) for i in range(10)])),
            ("small", Array([float(i) for i in range(100)])),
            ("medium", Array([float(i) for i in range(1000)])),
            ("large", Array([float(i) for i in range(10000)])),
        ]
    
    def test_sum_performance(self):
        """Test sum operation performance."""
        for size_name, arr in self.test_arrays:
            mean_time, _ = self.timer.time_operation(lambda a: a.sum(), arr)
            
            time_per_element = mean_time / arr.size
            assert time_per_element < 1e-6, f"{size_name} sum too slow: {time_per_element:.2e}s per element"
    
    def test_sum_fast_performance(self):
        """Test sum_fast performance if available."""
        for size_name, arr in self.test_arrays:
            if hasattr(arr, 'sum_fast'):
                mean_time, _ = self.timer.time_operation(lambda a: a.sum_fast(), arr)
                
                time_per_element = mean_time / arr.size
                assert time_per_element < 1e-6, f"{size_name} sum_fast too slow: {time_per_element:.2e}s per element"
    
    def test_mean_performance(self):
        """Test mean operation performance."""
        for size_name, arr in self.test_arrays:
            mean_time, _ = self.timer.time_operation(lambda a: a.mean(), arr)
            
            time_per_element = mean_time / arr.size
            assert time_per_element < 1e-6, f"{size_name} mean too slow: {time_per_element:.2e}s per element"
    
    def test_mean_fast_performance(self):
        """Test mean_fast performance if available."""
        for size_name, arr in self.test_arrays:
            if hasattr(arr, 'mean_fast'):
                mean_time, _ = self.timer.time_operation(lambda a: a.mean_fast(), arr)
                
                time_per_element = mean_time / arr.size
                assert time_per_element < 1e-6, f"{size_name} mean_fast too slow: {time_per_element:.2e}s per element"


class TestMathematicalFunctionPerformance:
    """Test performance of mathematical functions."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.timer = PerformanceTimer()
        
        # Create test arrays with positive values for math functions
        self.test_arrays = [
            ("small", Array([float(i + 1) for i in range(100)])),
            ("medium", Array([float(i + 1) for i in range(1000)])),
        ]
    
    def test_sqrt_performance(self):
        """Test sqrt operation performance."""
        for size_name, arr in self.test_arrays:
            mean_time, _ = self.timer.time_operation(lambda a: a.sqrt(), arr)
            
            time_per_element = mean_time / arr.size
            assert time_per_element < 1e-5, f"{size_name} sqrt too slow: {time_per_element:.2e}s per element"
    
    def test_sqrt_fast_performance(self):
        """Test sqrt_fast performance if available."""
        for size_name, arr in self.test_arrays:
            if hasattr(arr, 'sqrt_fast'):
                mean_time, _ = self.timer.time_operation(lambda a: a.sqrt_fast(), arr)
                
                time_per_element = mean_time / arr.size
                assert time_per_element < 1e-5, f"{size_name} sqrt_fast too slow: {time_per_element:.2e}s per element"
    
    def test_sin_fast_performance(self):
        """Test sin_fast performance if available."""
        # Use smaller range for trig functions
        arr = Array([float(i * 0.1) for i in range(100)])
        
        if hasattr(arr, 'sin_fast'):
            mean_time, _ = self.timer.time_operation(lambda a: a.sin_fast(), arr)
            
            time_per_element = mean_time / arr.size
            assert time_per_element < 1e-5, f"sin_fast too slow: {time_per_element:.2e}s per element"
    
    def test_exp_fast_performance(self):
        """Test exp_fast performance if available."""
        # Use smaller values for exp to avoid overflow
        arr = Array([float(i * 0.1) for i in range(100)])
        
        if hasattr(arr, 'exp_fast'):
            mean_time, _ = self.timer.time_operation(lambda a: a.exp_fast(), arr)
            
            time_per_element = mean_time / arr.size
            assert time_per_element < 1e-5, f"exp_fast too slow: {time_per_element:.2e}s per element"


class TestMemoryPerformance:
    """Test memory-related performance characteristics."""
    
    def test_large_array_creation(self):
        """Test that large arrays can be created without excessive memory overhead."""
        timer = PerformanceTimer()
        
        # Create a reasonably large array
        size = 10000
        data = [float(i) for i in range(size)]
        
        mean_time, _ = timer.time_operation(Array, data)
        
        # Should complete in reasonable time even for large arrays
        assert mean_time < 0.1, f"Large array creation took {mean_time:.6f}s, expected < 0.1s"
    
    def test_repeated_operations_no_degradation(self):
        """Test that repeated operations don't show performance degradation."""
        arr = Array([float(i) for i in range(1000)])
        timer = PerformanceTimer(warmup_runs=5, test_runs=20)
        
        # Test sum operation repeatedly
        _, times = timer.time_operation(lambda a: a.sum(), arr)
        
        # Check that later operations aren't significantly slower than earlier ones
        first_half = times[:len(times)//2]
        second_half = times[len(times)//2:]
        
        first_mean = statistics.mean(first_half)
        second_mean = statistics.mean(second_half)
        
        # Second half shouldn't be more than 50% slower than first half
        assert second_mean < first_mean * 1.5, "Performance degradation detected in repeated operations"


class TestScalabilityPerformance:
    """Test how performance scales with array size."""
    
    def test_linear_scaling_sum(self):
        """Test that sum operation scales roughly linearly with array size."""
        timer = PerformanceTimer()
        
        sizes = [100, 500, 1000, 2000]
        times = []
        
        for size in sizes:
            arr = Array([float(i) for i in range(size)])
            if hasattr(arr, 'sum_fast'):
                mean_time, _ = timer.time_operation(lambda a: a.sum_fast(), arr)
            else:
                mean_time, _ = timer.time_operation(lambda a: a.sum(), arr)
            times.append(mean_time)
        
        # Check that time roughly scales with size
        # Time per element should be relatively constant
        times_per_element = [t/s for t, s in zip(times, sizes)]
        
        # Variance in time per element should be reasonable
        variance = statistics.variance(times_per_element)
        mean_time_per_element = statistics.mean(times_per_element)
        
        # Coefficient of variation should be less than 100%
        cv = (variance ** 0.5) / mean_time_per_element
        assert cv < 1.0, f"Sum operation scaling is inconsistent: CV = {cv:.2f}"
    
    def test_quadratic_operations_scaling(self):
        """Test scaling of operations that should be O(n^2)."""
        timer = PerformanceTimer()
        
        # Test matrix multiplication scaling (if available)
        sizes = [10, 20, 30]  # Keep small for quadratic operations
        times = []
        
        for size in sizes:
            arr1 = Array([[float(i + j) for j in range(size)] for i in range(size)])
            arr2 = Array([[float(i + j) for j in range(size)] for i in range(size)])
            
            mean_time, _ = timer.time_operation(lambda a, b: a.dot(b), arr1, arr2)
            times.append(mean_time)
        
        # For matrix multiplication, time should scale roughly as O(n^3)
        # We'll just check that it doesn't scale exponentially
        if len(times) >= 2:
            ratio = times[-1] / times[0]
            size_ratio = sizes[-1] / sizes[0]
            
            # Should not be worse than O(n^4) scaling
            expected_max_ratio = size_ratio ** 4
            assert ratio < expected_max_ratio, f"Matrix multiplication scaling too poor: {ratio:.2f} vs expected max {expected_max_ratio:.2f}"


@pytest.mark.slow
class TestExtensivePerformance:
    """Extensive performance tests (marked as slow)."""
    
    def test_stress_test_large_arrays(self):
        """Stress test with very large arrays."""
        size = 50000  # Large array
        arr = Array([float(i) for i in range(size)])
        
        timer = PerformanceTimer(warmup_runs=1, test_runs=3)
        
        # Test various operations
        operations = [
            ("sum", lambda a: a.sum()),
            ("mean", lambda a: a.mean()),
            ("min", lambda a: a.min()),
            ("max", lambda a: a.max()),
        ]
        
        if hasattr(arr, 'sum_fast'):
            operations.extend([
                ("sum_fast", lambda a: a.sum_fast()),
                ("mean_fast", lambda a: a.mean_fast()),
            ])
        
        for op_name, op_func in operations:
            mean_time, _ = timer.time_operation(op_func, arr)
            time_per_element = mean_time / size
            
            # Even for large arrays, operations should be reasonably fast
            assert time_per_element < 1e-5, f"{op_name} on large array too slow: {time_per_element:.2e}s per element"
    
    def test_memory_stress_test(self):
        """Test creating and operating on multiple large arrays."""
        size = 10000
        num_arrays = 10
        
        timer = PerformanceTimer(warmup_runs=1, test_runs=1)
        
        def create_and_sum_arrays():
            arrays = []
            for i in range(num_arrays):
                arr = Array([float(j + i) for j in range(size)])
                arrays.append(arr)
            
            # Sum all arrays
            total = 0
            for arr in arrays:
                total += arr.sum()
            return total
        
        mean_time, _ = timer.time_operation(create_and_sum_arrays)
        
        # Should complete within reasonable time
        assert mean_time < 1.0, f"Memory stress test took {mean_time:.6f}s, expected < 1.0s"


if __name__ == "__main__":
    # Run with performance timing
    pytest.main([__file__, "-v", "--tb=short"])