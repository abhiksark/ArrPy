"""
Scalability benchmarks to test how arrpy and numpy performance scales with array size
"""

import time
import numpy as np
import sys
import os
import warnings

# Suppress numpy warnings for cleaner output
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
    
    def time_operation(self, func, iterations=5):
        """Time an operation with multiple iterations"""
        times = []
        for _ in range(iterations):
            gc.collect()
            start = time.perf_counter()
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                result = func()
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
    
    # 1D array creation
    sizes_1d = [100, 500, 1000, 2000, 5000, 10000]
    
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
    
    # 2D array creation (square matrices)
    sizes_2d = [10, 20, 50, 75, 100, 150]  # These are edge lengths, total elements = size^2
    
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

def test_arithmetic_scaling():
    """Test how arithmetic operations scale with size"""
    benchmark = ScalabilityBenchmark()
    
    print("\n" + "=" * 60)
    print("ARITHMETIC OPERATIONS SCALABILITY")
    print("=" * 60)
    
    # Prepare test data for different sizes
    sizes = [10, 25, 50, 75, 100, 150]
    test_arrays = {}
    
    for size in sizes:
        data1 = [[i + j for j in range(size)] for i in range(size)]
        data2 = [[i * j + 1 for j in range(size)] for i in range(size)]
        
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
    
    # Test scalar multiplication scaling
    def scalar_mul_arrpy(size):
        arr1, _ = test_arrays[size]['arrpy']
        return arr1 * 3.14159
    
    def scalar_mul_numpy(size):
        arr1, _ = test_arrays[size]['numpy']
        return arr1 * 3.14159
    
    benchmark.test_scaling("Scalar Multiplication", sizes, scalar_mul_arrpy, scalar_mul_numpy)

def test_matrix_operations_scaling():
    """Test how matrix operations scale with size"""
    benchmark = ScalabilityBenchmark()
    
    print("\n" + "=" * 60)
    print("MATRIX OPERATIONS SCALABILITY")
    print("=" * 60)
    
    # Test matrix multiplication scaling (this should show dramatic differences)
    sizes = [5, 10, 20, 30, 40, 50]  # Keep sizes reasonable for O(n³) operation
    test_matrices = {}
    
    for size in sizes:
        data1 = [[i + j + 1 for j in range(size)] for i in range(size)]
        data2 = [[i * j + 2 for j in range(size)] for i in range(size)]
        
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

def test_aggregation_scaling():
    """Test how aggregation operations scale with size"""
    benchmark = ScalabilityBenchmark()
    
    print("\n" + "=" * 60)
    print("AGGREGATION OPERATIONS SCALABILITY")
    print("=" * 60)
    
    # 1D aggregations
    sizes_1d = [1000, 5000, 10000, 25000, 50000, 100000]
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
    
    # 2D aggregations
    sizes_2d = [10, 25, 50, 75, 100, 150]
    test_arrays_2d = {}
    
    for size in sizes_2d:
        data = [[i + j for j in range(size)] for i in range(size)]
        test_arrays_2d[size] = {
            'arrpy': Array(data),
            'numpy': np.array(data)
        }
    
    # 2D Sum scaling
    def sum_2d_arrpy(size):
        return test_arrays_2d[size]['arrpy'].sum()
    
    def sum_2d_numpy(size):
        return test_arrays_2d[size]['numpy'].sum()
    
    benchmark.test_scaling("2D Sum", sizes_2d, sum_2d_arrpy, sum_2d_numpy)

def test_indexing_scaling():
    """Test how indexing operations scale with size"""
    benchmark = ScalabilityBenchmark()
    
    print("\n" + "=" * 60)
    print("INDEXING OPERATIONS SCALABILITY")
    print("=" * 60)
    
    sizes = [25, 50, 100, 150, 200, 300]
    test_arrays = {}
    
    for size in sizes:
        data = [[i + j for j in range(size)] for i in range(size)]
        test_arrays[size] = {
            'arrpy': Array(data),
            'numpy': np.array(data)
        }
    
    # Single element access (repeated)
    def single_access_arrpy(size):
        arr = test_arrays[size]['arrpy']
        total = 0
        for i in range(min(100, size)):  # Access up to 100 elements
            for j in range(min(100, size)):
                total += arr[i, j]
        return total
    
    def single_access_numpy(size):
        arr = test_arrays[size]['numpy']
        total = 0
        for i in range(min(100, size)):
            for j in range(min(100, size)):
                total += arr[i, j]
        return total
    
    benchmark.test_scaling("Single Element Access (100 ops)", sizes, single_access_arrpy, single_access_numpy)
    
    # Row access
    def row_access_arrpy(size):
        arr = test_arrays[size]['arrpy']
        rows = []
        for i in range(min(10, size)):  # Access up to 10 rows
            rows.append(arr[i])
        return rows
    
    def row_access_numpy(size):
        arr = test_arrays[size]['numpy']
        rows = []
        for i in range(min(10, size)):
            rows.append(arr[i])
        return rows
    
    benchmark.test_scaling("Row Access (10 ops)", sizes, row_access_arrpy, row_access_numpy)

def test_reshape_scaling():
    """Test how reshape operations scale with size"""
    benchmark = ScalabilityBenchmark()
    
    print("\n" + "=" * 60)
    print("RESHAPE OPERATIONS SCALABILITY")
    print("=" * 60)
    
    # Test reshaping from 1D to 2D
    sizes = [100, 500, 1000, 2500, 5000, 10000]
    test_arrays = {}
    
    for size in sizes:
        data = list(range(size))
        # Find a good square-ish shape that exactly divides the size
        sqrt_size = int(size ** 0.5)
        # Ensure the product equals the original size
        while size % sqrt_size != 0:
            sqrt_size -= 1
        new_shape = (sqrt_size, size // sqrt_size)
        
        test_arrays[size] = {
            'arrpy': Array(data),
            'numpy': np.array(data),
            'shape': new_shape
        }
    
    def reshape_arrpy(size):
        arr = test_arrays[size]['arrpy']
        shape = test_arrays[size]['shape']
        return arr.reshape(shape)
    
    def reshape_numpy(size):
        arr = test_arrays[size]['numpy']
        shape = test_arrays[size]['shape']
        return arr.reshape(shape)
    
    benchmark.test_scaling("1D to 2D Reshape", sizes, reshape_arrpy, reshape_numpy)

def test_new_features_scaling():
    """Test how new features scale with size"""
    benchmark = ScalabilityBenchmark()
    
    print("\n" + "=" * 60)
    print("NEW FEATURES SCALABILITY")
    print("=" * 60)
    
    # Array creation functions scaling
    sizes_1d = [1000, 5000, 10000, 25000, 50000]
    
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
    
    # Extended aggregations scaling
    test_arrays_1d = {}
    for size in sizes_1d:
        data = list(range(size))
        test_arrays_1d[size] = {
            'arrpy': Array(data),
            'numpy': np.array(data)
        }
    
    # min scaling
    def min_arrpy(size):
        return test_arrays_1d[size]['arrpy'].min()
    
    def min_numpy(size):
        return test_arrays_1d[size]['numpy'].min()
    
    benchmark.test_scaling("min", sizes_1d, min_arrpy, min_numpy)
    
    # max scaling
    def max_arrpy(size):
        return test_arrays_1d[size]['arrpy'].max()
    
    def max_numpy(size):
        return test_arrays_1d[size]['numpy'].max()
    
    benchmark.test_scaling("max", sizes_1d, max_arrpy, max_numpy)
    
    # std scaling
    def std_arrpy(size):
        return test_arrays_1d[size]['arrpy'].std()
    
    def std_numpy(size):
        return test_arrays_1d[size]['numpy'].std()
    
    benchmark.test_scaling("std", sizes_1d, std_arrpy, std_numpy)
    
    # Mathematical functions scaling (smaller sizes due to computation cost)
    sizes_math = [1000, 2500, 5000, 10000, 20000]
    test_arrays_math = {}
    
    for size in sizes_math:
        # Positive data for sqrt and log
        data_pos = [i + 1 for i in range(size)]
        # Trigonometric data
        data_trig = [i * 2 * math.pi / size for i in range(size)]
        
        test_arrays_math[size] = {
            'arrpy_pos': Array(data_pos),
            'numpy_pos': np.array(data_pos),
            'arrpy_trig': Array(data_trig),
            'numpy_trig': np.array(data_trig)
        }
    
    # sqrt scaling
    def sqrt_arrpy(size):
        return test_arrays_math[size]['arrpy_pos'].sqrt()
    
    def sqrt_numpy(size):
        return np.sqrt(test_arrays_math[size]['numpy_pos'])
    
    benchmark.test_scaling("sqrt", sizes_math, sqrt_arrpy, sqrt_numpy)
    
    # sin scaling
    def sin_arrpy(size):
        return test_arrays_math[size]['arrpy_trig'].sin()
    
    def sin_numpy(size):
        return np.sin(test_arrays_math[size]['numpy_trig'])
    
    benchmark.test_scaling("sin", sizes_math, sin_arrpy, sin_numpy)

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
        print(f"{'Size':>8} {'arrpy (s)':>12} {'numpy (s)':>12} {'Speedup':>10} {'Ratio Growth':>15}")
        print("-" * 70)
        
        prev_arrpy_time = None
        prev_numpy_time = None
        prev_size = None
        
        for i, (size, arrpy_time, numpy_time) in enumerate(zip(sizes, arrpy_times, numpy_times)):
            speedup = arrpy_time / numpy_time
            
            if prev_arrpy_time is not None and prev_size is not None:
                size_ratio = size / prev_size
                arrpy_growth = arrpy_time / prev_arrpy_time
                numpy_growth = numpy_time / prev_numpy_time
                growth_ratio = arrpy_growth / numpy_growth
                growth_str = f"{growth_ratio:.2f}"
            else:
                growth_str = "baseline"
            
            print(f"{size:>8} {arrpy_time:>12.6f} {numpy_time:>12.6f} {speedup:>10.2f}x {growth_str:>15}")
            
            prev_arrpy_time = arrpy_time
            prev_numpy_time = numpy_time
            prev_size = size
        
        # Estimate complexity
        if len(sizes) >= 3:
            # Compare last and first measurements
            size_growth = sizes[-1] / sizes[0]
            arrpy_time_growth = arrpy_times[-1] / arrpy_times[0]
            numpy_time_growth = numpy_times[-1] / numpy_times[0]
            
            # Rough complexity estimation
            import math
            log_size_growth = math.log(size_growth)
            log_arrpy_growth = math.log(arrpy_time_growth)
            log_numpy_growth = math.log(numpy_time_growth)
            
            arrpy_complexity = log_arrpy_growth / log_size_growth
            numpy_complexity = log_numpy_growth / log_size_growth
            
            print(f"Estimated complexity - arrpy: O(n^{arrpy_complexity:.1f}), "
                  f"numpy: O(n^{numpy_complexity:.1f})")

def generate_scalability_plots(all_results):
    """Generate plots showing scalability comparison"""
    if not HAS_MATPLOTLIB:
        print("\n" + "=" * 60)
        print("MATPLOTLIB NOT AVAILABLE - SKIPPING PLOT GENERATION")
        print("=" * 60)
        print("Install matplotlib to generate scalability plots: pip install matplotlib")
        return
        
    print("\n" + "=" * 60)
    print("GENERATING SCALABILITY PLOTS")
    print("=" * 60)
    
    # Create subplots for different operation categories
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('arrpy vs numpy Scalability Comparison', fontsize=16)
    
    plot_configs = [
        ("1D Array Creation", 0, 0),
        ("Addition", 0, 1),
        ("Matrix Multiplication", 0, 2),
        ("1D Sum", 1, 0),
        ("Single Element Access (100 ops)", 1, 1),
        ("1D to 2D Reshape", 1, 2)
    ]
    
    for operation_name, row, col in plot_configs:
        ax = axes[row, col]
        
        # Find the results for this operation
        results = None
        for benchmark_name, benchmark_results in all_results.items():
            if operation_name in benchmark_results.results:
                results = benchmark_results.results[operation_name]
                break
        
        if results:
            sizes = results['sizes']
            arrpy_times = results['arrpy_times']
            numpy_times = results['numpy_times']
            
            ax.loglog(sizes, arrpy_times, 'o-', label='arrpy', linewidth=2)
            ax.loglog(sizes, numpy_times, 's-', label='numpy', linewidth=2)
            ax.set_xlabel('Array Size')
            ax.set_ylabel('Time (seconds)')
            ax.set_title(operation_name)
            ax.grid(True, alpha=0.3)
            ax.legend()
        else:
            ax.text(0.5, 0.5, 'No data', ha='center', va='center', transform=ax.transAxes)
            ax.set_title(operation_name)
    
    plt.tight_layout()
    plt.savefig('scalability_comparison.png', dpi=300, bbox_inches='tight')
    print("Scalability plots saved as 'scalability_comparison.png'")

def run_scalability_tests():
    """Run comprehensive scalability tests"""
    print("ARRYPY vs NUMPY SCALABILITY ANALYSIS")
    print("=" * 80)
    print("Testing how performance scales with input size")
    print("=" * 80)
    
    all_results = {}
    
    # Run all scalability tests
    test_functions = [
        ("Array Creation", test_creation_scaling),
        ("Arithmetic Operations", test_arithmetic_scaling),
        ("Matrix Operations", test_matrix_operations_scaling),
        ("Aggregation Operations", test_aggregation_scaling),
        ("Indexing Operations", test_indexing_scaling),
        ("Reshape Operations", test_reshape_scaling),
        ("New Features", test_new_features_scaling)
    ]
    
    for category_name, test_func in test_functions:
        print(f"\nRunning {category_name} scalability tests...")
        all_results[category_name] = test_func()
    
    # Analyze computational complexity
    for category_name, benchmark in all_results.items():
        analyze_complexity(benchmark.results)
    
    # Generate plots
    generate_scalability_plots(all_results)
    
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