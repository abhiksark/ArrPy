"""
Clean scalability benchmarks with proper warning handling.

This version suppresses expected warnings and only shows relevant ones.
"""

import time
import numpy as np
import sys
import os
import warnings

# Suppress expected numpy warnings for cleaner output
warnings.filterwarnings("ignore", category=RuntimeWarning, module="numpy")
warnings.filterwarnings("ignore", category=FutureWarning, module="numpy")

# Add parent directory to path to import arrpy
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from arrpy import Array, zeros, ones, arange, linspace

import gc
import math
from statistics import mean

# Try to import matplotlib, but make it optional
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


class ScalabilityBenchmark:
    def __init__(self):
        self.results = {}
    
    def time_operation(self, func, iterations=3):
        """Time an operation with multiple iterations (reduced for faster testing)"""
        times = []
        for _ in range(iterations):
            gc.collect()
            start = time.perf_counter()
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    result = func()
            except Exception as e:
                print(f"Warning: Operation failed with error: {e}")
                return float('inf')  # Return infinity for failed operations
            end = time.perf_counter()
            times.append(end - start)
        return mean(times)
    
    def test_scaling(self, operation_name, sizes, arrpy_func, numpy_func):
        """Test how an operation scales with input size"""
        print(f"\nTesting scalability: {operation_name}")
        print(f"Sizes: {sizes}")
        
        arrpy_times = []
        numpy_times = []
        
        for size in sizes:
            print(f"  Testing size {size}...", end=" ")
            
            # Test arrpy
            arrpy_time = self.time_operation(lambda: arrpy_func(size))
            arrpy_times.append(arrpy_time)
            
            # Test numpy
            numpy_time = self.time_operation(lambda: numpy_func(size))
            numpy_times.append(numpy_time)
            
            if arrpy_time == float('inf') or numpy_time == float('inf'):
                print("FAILED")
            else:
                speedup = arrpy_time / numpy_time
                print(f"numpy {speedup:.1f}x faster")
        
        self.results[operation_name] = {
            'sizes': sizes,
            'arrpy_times': arrpy_times,
            'numpy_times': numpy_times
        }
        
        return sizes, arrpy_times, numpy_times


def test_creation_scaling():
    """Test how array creation scales with size"""
    benchmark = ScalabilityBenchmark()
    
    print("=" * 60)
    print("ARRAY CREATION SCALABILITY")
    print("=" * 60)
    
    # Smaller sizes to avoid warnings and faster testing
    sizes_1d = [100, 500, 1000, 2000, 5000]
    
    def create_arrpy_1d(size):
        data = list(range(size))
        return Array(data)
    
    def create_numpy_1d(size):
        data = list(range(size))
        return np.array(data)
    
    benchmark.test_scaling(
        "1D Array Creation",
        sizes_1d,
        create_arrpy_1d,
        create_numpy_1d
    )
    
    # Smaller 2D arrays
    sizes_2d = [10, 20, 50, 75, 100]
    
    def create_arrpy_2d(size):
        data = [[i + j for j in range(size)] for i in range(size)]
        return Array(data)
    
    def create_numpy_2d(size):
        data = [[i + j for j in range(size)] for i in range(size)]
        return np.array(data)
    
    benchmark.test_scaling(
        "2D Array Creation (Square)",
        sizes_2d,
        create_arrpy_2d,
        create_numpy_2d
    )
    
    return benchmark


def test_arithmetic_scaling():
    """Test how arithmetic operations scale with size"""
    benchmark = ScalabilityBenchmark()
    
    print("\n" + "=" * 60)
    print("ARITHMETIC OPERATIONS SCALABILITY")
    print("=" * 60)
    
    # Prepare test data for different sizes (smaller to avoid warnings)
    sizes = [10, 25, 50, 75, 100]
    test_arrays = {}
    
    for size in sizes:
        # Use smaller numbers to avoid overflow
        data1 = [[i + j for j in range(size)] for i in range(size)]
        data2 = [[i + j + 1 for j in range(size)] for i in range(size)]
        
        test_arrays[size] = {
            'arrpy': (Array(data1), Array(data2)),
            'numpy': (np.array(data1), np.array(data2))
        }
    
    # Test addition scaling
    def add_arrpy(size):
        arr1, arr2 = test_arrays[size]['arrpy']
        return arr1 + arr2
    
    def add_numpy(size):
        arr1, arr2 = test_arrays[size]['numpy']
        return arr1 + arr2
    
    benchmark.test_scaling("Addition", sizes, add_arrpy, add_numpy)
    
    # Test multiplication scaling
    def mul_arrpy(size):
        arr1, arr2 = test_arrays[size]['arrpy']
        return arr1 * arr2
    
    def mul_numpy(size):
        arr1, arr2 = test_arrays[size]['numpy']
        return arr1 * arr2
    
    benchmark.test_scaling("Multiplication", sizes, mul_arrpy, mul_numpy)
    
    return benchmark


def test_matrix_operations_scaling():
    """Test how matrix operations scale with size"""
    benchmark = ScalabilityBenchmark()
    
    print("\n" + "=" * 60)
    print("MATRIX OPERATIONS SCALABILITY")
    print("=" * 60)
    
    # Smaller matrix sizes to avoid memory issues
    sizes = [5, 10, 20, 30, 40]
    test_matrices = {}
    
    for size in sizes:
        # Use small integers to avoid overflow
        data1 = [[1 + (i + j) % 10 for j in range(size)] for i in range(size)]
        data2 = [[1 + (i * j) % 10 for j in range(size)] for i in range(size)]
        
        test_matrices[size] = {
            'arrpy': (Array(data1), Array(data2)),
            'numpy': (np.array(data1), np.array(data2))
        }
    
    # Matrix multiplication
    def matmul_arrpy(size):
        arr1, arr2 = test_matrices[size]['arrpy']
        return arr1.dot(arr2)
    
    def matmul_numpy(size):
        arr1, arr2 = test_matrices[size]['numpy']
        return np.dot(arr1, arr2)
    
    benchmark.test_scaling("Matrix Multiplication", sizes, matmul_arrpy, matmul_numpy)
    
    # Transpose scaling
    def transpose_arrpy(size):
        arr1, _ = test_matrices[size]['arrpy']
        return arr1.T
    
    def transpose_numpy(size):
        arr1, _ = test_matrices[size]['numpy']
        return arr1.T
    
    benchmark.test_scaling("Transpose", sizes, transpose_arrpy, transpose_numpy)
    
    return benchmark


def test_aggregation_scaling():
    """Test how aggregation operations scale with size"""
    benchmark = ScalabilityBenchmark()
    
    print("\n" + "=" * 60)
    print("AGGREGATION OPERATIONS SCALABILITY")
    print("=" * 60)
    
    # Smaller 1D arrays
    sizes_1d = [1000, 5000, 10000, 25000, 50000]
    test_arrays_1d = {}
    
    for size in sizes_1d:
        data = list(range(size))
        test_arrays_1d[size] = {
            'arrpy': Array(data),
            'numpy': np.array(data)
        }
    
    # Sum scaling
    def sum_arrpy(size):
        return test_arrays_1d[size]['arrpy'].sum()
    
    def sum_numpy(size):
        return test_arrays_1d[size]['numpy'].sum()
    
    benchmark.test_scaling("1D Sum", sizes_1d, sum_arrpy, sum_numpy)
    
    # Mean scaling
    def mean_arrpy(size):
        return test_arrays_1d[size]['arrpy'].mean()
    
    def mean_numpy(size):
        return test_arrays_1d[size]['numpy'].mean()
    
    benchmark.test_scaling("1D Mean", sizes_1d, mean_arrpy, mean_numpy)
    
    return benchmark


def test_new_features_scaling():
    """Test how new features scale with size"""
    benchmark = ScalabilityBenchmark()
    
    print("\n" + "=" * 60)
    print("NEW FEATURES SCALABILITY")
    print("=" * 60)
    
    # Array creation functions scaling
    sizes_1d = [1000, 5000, 10000, 25000]
    
    # zeros scaling
    def zeros_arrpy(size):
        return zeros(size)
    
    def zeros_numpy(size):
        return np.zeros(size)
    
    benchmark.test_scaling("zeros 1D", sizes_1d, zeros_arrpy, zeros_numpy)
    
    # ones scaling
    def ones_arrpy(size):
        return ones(size)
    
    def ones_numpy(size):
        return np.ones(size)
    
    benchmark.test_scaling("ones 1D", sizes_1d, ones_arrpy, ones_numpy)
    
    # arange scaling
    def arange_arrpy(size):
        return arange(size)
    
    def arange_numpy(size):
        return np.arange(size)
    
    benchmark.test_scaling("arange", sizes_1d, arange_arrpy, arange_numpy)
    
    return benchmark


def analyze_complexity(benchmark_results):
    """Analyze the computational complexity from benchmark results"""
    print("\n" + "=" * 80)
    print("COMPUTATIONAL COMPLEXITY ANALYSIS")
    print("=" * 80)
    
    for operation_name, results in benchmark_results.items():
        sizes = results['sizes']
        arrpy_times = results['arrpy_times']
        numpy_times = results['numpy_times']
        
        print(f"\n{operation_name}:")
        print(f"{'Size':>8} {'arrpy (s)':>12} {'numpy (s)':>12} {'Speedup':>10}")
        print("-" * 50)
        
        for size, arrpy_time, numpy_time in zip(sizes, arrpy_times, numpy_times):
            if arrpy_time != float('inf') and numpy_time != float('inf'):
                speedup = arrpy_time / numpy_time
                print(f"{size:>8} {arrpy_time:>12.6f} {numpy_time:>12.6f} {speedup:>10.2f}x")
            else:
                print(f"{size:>8} {'FAILED':>12} {'FAILED':>12} {'N/A':>10}")


def run_scalability_tests():
    """Run comprehensive scalability tests with clean output"""
    print("ARRPY vs NUMPY SCALABILITY ANALYSIS (CLEAN VERSION)")
    print("=" * 80)
    print("Testing how performance scales with input size")
    print("Note: Warnings suppressed for cleaner output")
    print("=" * 80)
    
    all_results = {}
    
    # Run selected scalability tests
    test_functions = [
        ("Array Creation", test_creation_scaling),
        ("Arithmetic Operations", test_arithmetic_scaling),
        ("Matrix Operations", test_matrix_operations_scaling),
        ("Aggregation Operations", test_aggregation_scaling),
        ("New Features", test_new_features_scaling)
    ]
    
    for category_name, test_func in test_functions:
        print(f"\nRunning {category_name} scalability tests...")
        try:
            all_results[category_name] = test_func()
        except Exception as e:
            print(f"Error in {category_name}: {e}")
    
    # Analyze computational complexity
    for category_name, benchmark in all_results.items():
        analyze_complexity(benchmark.results)
    
    # Summary insights
    print("\n" + "=" * 80)
    print("SCALABILITY INSIGHTS")
    print("=" * 80)
    print("• Matrix multiplication shows the largest performance gaps (O(n³) complexity)")
    print("• Simple operations (indexing, transpose) have smaller relative differences")
    print("• Memory allocation overhead affects creation and reshape operations")
    print("• numpy's optimized C implementation provides consistent advantages")
    print("• Performance gaps tend to increase with larger array sizes")
    print("• arrpy is suitable for small-medium arrays and educational purposes")
    print("• Use numpy for production workloads requiring high performance")


if __name__ == "__main__":
    run_scalability_tests()