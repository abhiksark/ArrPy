"""
Comprehensive performance benchmarks comparing arrypy with numpy
"""

import time
import numpy as np
from arrypy import Array
import gc
from functools import wraps

def benchmark(func):
    """Decorator to measure execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Run garbage collection before timing
        gc.collect()
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        return result, execution_time
    return wrapper

class PerformanceBenchmark:
    def __init__(self):
        self.results = {}
        
    def run_benchmark(self, name, arrypy_func, numpy_func, *args, **kwargs):
        """Run a benchmark comparing arrypy and numpy functions"""
        print(f"\n=== {name} ===")
        
        # Benchmark arrypy
        @benchmark
        def arrypy_test():
            return arrypy_func(*args, **kwargs)
        
        # Benchmark numpy
        @benchmark
        def numpy_test():
            return numpy_func(*args, **kwargs)
        
        # Run tests multiple times for better accuracy
        arrypy_times = []
        numpy_times = []
        
        for _ in range(5):  # Run 5 times
            _, arrypy_time = arrypy_test()
            _, numpy_time = numpy_test()
            arrypy_times.append(arrypy_time)
            numpy_times.append(numpy_time)
        
        # Calculate averages
        avg_arrypy = sum(arrypy_times) / len(arrypy_times)
        avg_numpy = sum(numpy_times) / len(numpy_times)
        speedup_ratio = avg_arrypy / avg_numpy
        
        print(f"arrypy average time: {avg_arrypy:.6f} seconds")
        print(f"numpy average time:  {avg_numpy:.6f} seconds")
        print(f"numpy is {speedup_ratio:.2f}x faster")
        
        # Store results
        self.results[name] = {
            'arrypy_time': avg_arrypy,
            'numpy_time': avg_numpy,
            'speedup_ratio': speedup_ratio
        }
        
        return avg_arrypy, avg_numpy, speedup_ratio

def benchmark_initialization():
    """Benchmark array initialization"""
    benchmark = PerformanceBenchmark()
    
    print("=" * 60)
    print("ARRAY INITIALIZATION BENCHMARKS")
    print("=" * 60)
    
    # Small arrays
    small_data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    benchmark.run_benchmark(
        "Small Array Initialization (3x3)",
        lambda: Array(small_data),
        lambda: np.array(small_data)
    )
    
    # Medium arrays
    medium_data = [[i + j for j in range(50)] for i in range(50)]
    benchmark.run_benchmark(
        "Medium Array Initialization (50x50)",
        lambda: Array(medium_data),
        lambda: np.array(medium_data)
    )
    
    # Large 1D arrays
    large_1d = list(range(10000))
    benchmark.run_benchmark(
        "Large 1D Array Initialization (10k elements)",
        lambda: Array(large_1d),
        lambda: np.array(large_1d)
    )
    
    return benchmark

def benchmark_indexing():
    """Benchmark indexing operations"""
    benchmark = PerformanceBenchmark()
    
    print("\n" + "=" * 60)
    print("INDEXING BENCHMARKS")
    print("=" * 60)
    
    # Setup test data
    data = [[i + j for j in range(100)] for i in range(100)]
    arr_arrypy = Array(data)
    arr_numpy = np.array(data)
    
    # Single element access
    def arrypy_single_access():
        result = 0
        for i in range(10):
            for j in range(10):
                result += arr_arrypy[i, j]
        return result
    
    def numpy_single_access():
        result = 0
        for i in range(10):
            for j in range(10):
                result += arr_numpy[i, j]
        return result
    
    benchmark.run_benchmark(
        "Single Element Access (100 operations)",
        arrypy_single_access,
        numpy_single_access
    )
    
    # Row access
    def arrypy_row_access():
        rows = []
        for i in range(10):
            rows.append(arr_arrypy[i])
        return rows
    
    def numpy_row_access():
        rows = []
        for i in range(10):
            rows.append(arr_numpy[i])
        return rows
    
    benchmark.run_benchmark(
        "Row Access (10 operations)",
        arrypy_row_access,
        numpy_row_access
    )
    
    return benchmark

def benchmark_arithmetic():
    """Benchmark arithmetic operations"""
    benchmark = PerformanceBenchmark()
    
    print("\n" + "=" * 60)
    print("ARITHMETIC OPERATIONS BENCHMARKS")
    print("=" * 60)
    
    # Test different sizes
    sizes = [
        (10, "Small (10x10)"),
        (50, "Medium (50x50)"),
        (100, "Large (100x100)")
    ]
    
    for size, size_name in sizes:
        data1 = [[i + j for j in range(size)] for i in range(size)]
        data2 = [[i * j + 1 for j in range(size)] for i in range(size)]
        
        arr1_arrypy = Array(data1)
        arr2_arrypy = Array(data2)
        arr1_numpy = np.array(data1)
        arr2_numpy = np.array(data2)
        
        # Addition
        benchmark.run_benchmark(
            f"Addition {size_name}",
            lambda: arr1_arrypy + arr2_arrypy,
            lambda: arr1_numpy + arr2_numpy
        )
        
        # Scalar multiplication
        benchmark.run_benchmark(
            f"Scalar Multiplication {size_name}",
            lambda: arr1_arrypy * 2.5,
            lambda: arr1_numpy * 2.5
        )
        
        # Element-wise multiplication
        benchmark.run_benchmark(
            f"Element-wise Multiplication {size_name}",
            lambda: arr1_arrypy * arr2_arrypy,
            lambda: arr1_numpy * arr2_numpy
        )
    
    return benchmark

def benchmark_matrix_operations():
    """Benchmark matrix operations"""
    benchmark = PerformanceBenchmark()
    
    print("\n" + "=" * 60)
    print("MATRIX OPERATIONS BENCHMARKS")
    print("=" * 60)
    
    # Test different sizes for matrix operations
    sizes = [
        (10, "Small (10x10)"),
        (25, "Medium (25x25)"),
        (50, "Large (50x50)")
    ]
    
    for size, size_name in sizes:
        data1 = [[i + j + 1 for j in range(size)] for i in range(size)]
        data2 = [[i * j + 2 for j in range(size)] for i in range(size)]
        
        arr1_arrypy = Array(data1)
        arr2_arrypy = Array(data2)
        arr1_numpy = np.array(data1)
        arr2_numpy = np.array(data2)
        
        # Matrix multiplication (dot product)
        benchmark.run_benchmark(
            f"Matrix Multiplication {size_name}",
            lambda: arr1_arrypy.dot(arr2_arrypy),
            lambda: np.dot(arr1_numpy, arr2_numpy)
        )
        
        # Transpose
        benchmark.run_benchmark(
            f"Transpose {size_name}",
            lambda: arr1_arrypy.T,
            lambda: arr1_numpy.T
        )
    
    return benchmark

def benchmark_reshape():
    """Benchmark reshape operations"""
    benchmark = PerformanceBenchmark()
    
    print("\n" + "=" * 60)
    print("RESHAPE OPERATIONS BENCHMARKS")
    print("=" * 60)
    
    # Test reshape with different sizes
    sizes_and_shapes = [
        (100, (10, 10), "Small reshape (100 -> 10x10)"),
        (2500, (50, 50), "Medium reshape (2500 -> 50x50)"),
        (10000, (100, 100), "Large reshape (10000 -> 100x100)")
    ]
    
    for total_size, new_shape, description in sizes_and_shapes:
        data = list(range(total_size))
        
        arr_arrypy = Array(data)
        arr_numpy = np.array(data)
        
        benchmark.run_benchmark(
            description,
            lambda: arr_arrypy.reshape(new_shape),
            lambda: arr_numpy.reshape(new_shape)
        )
    
    return benchmark

def benchmark_aggregations():
    """Benchmark aggregation operations"""
    benchmark = PerformanceBenchmark()
    
    print("\n" + "=" * 60)
    print("AGGREGATION OPERATIONS BENCHMARKS")
    print("=" * 60)
    
    # Test different sizes
    sizes = [
        (1000, "Small (1k elements)"),
        (10000, "Medium (10k elements)"),
        (100000, "Large (100k elements)")
    ]
    
    for size, size_name in sizes:
        data = list(range(size))
        
        arr_arrypy = Array(data)
        arr_numpy = np.array(data)
        
        # Sum
        benchmark.run_benchmark(
            f"Sum {size_name}",
            lambda: arr_arrypy.sum(),
            lambda: arr_numpy.sum()
        )
        
        # Mean
        benchmark.run_benchmark(
            f"Mean {size_name}",
            lambda: arr_arrypy.mean(),
            lambda: arr_numpy.mean()
        )
    
    return benchmark

def benchmark_memory_usage():
    """Benchmark memory usage comparison"""
    print("\n" + "=" * 60)
    print("MEMORY USAGE COMPARISON")
    print("=" * 60)
    
    import sys
    
    sizes = [100, 1000, 10000]
    
    for size in sizes:
        data = list(range(size))
        
        # Measure arrypy memory
        arr_arrypy = Array(data)
        arrypy_size = sys.getsizeof(arr_arrypy._data) + sys.getsizeof(arr_arrypy._shape)
        
        # Measure numpy memory
        arr_numpy = np.array(data)
        numpy_size = arr_numpy.nbytes
        
        memory_ratio = arrypy_size / numpy_size
        
        print(f"\nArray size: {size} elements")
        print(f"arrypy memory: {arrypy_size:,} bytes")
        print(f"numpy memory:  {numpy_size:,} bytes")
        print(f"arrypy uses {memory_ratio:.2f}x more memory")

def run_comprehensive_benchmarks():
    """Run all benchmarks and generate summary report"""
    print("ARRYPY vs NUMPY PERFORMANCE COMPARISON")
    print("=" * 80)
    print("Note: numpy is expected to be significantly faster as it's implemented in C")
    print("This benchmark helps understand the performance trade-offs")
    print("=" * 80)
    
    all_results = {}
    
    # Run all benchmark categories
    benchmark_categories = [
        ("Initialization", benchmark_initialization),
        ("Indexing", benchmark_indexing),
        ("Arithmetic", benchmark_arithmetic),
        ("Matrix Operations", benchmark_matrix_operations),
        ("Reshape", benchmark_reshape),
        ("Aggregations", benchmark_aggregations)
    ]
    
    for category_name, benchmark_func in benchmark_categories:
        results = benchmark_func()
        all_results[category_name] = results.results
    
    # Memory usage comparison
    benchmark_memory_usage()
    
    # Generate summary report
    print("\n" + "=" * 80)
    print("SUMMARY REPORT")
    print("=" * 80)
    
    all_speedups = []
    for category_name, category_results in all_results.items():
        print(f"\n{category_name}:")
        for test_name, test_results in category_results.items():
            speedup = test_results['speedup_ratio']
            all_speedups.append(speedup)
            print(f"  {test_name}: numpy is {speedup:.2f}x faster")
    
    if all_speedups:
        avg_speedup = sum(all_speedups) / len(all_speedups)
        min_speedup = min(all_speedups)
        max_speedup = max(all_speedups)
        
        print(f"\nOverall Performance Summary:")
        print(f"  Average speedup: numpy is {avg_speedup:.2f}x faster")
        print(f"  Minimum speedup: numpy is {min_speedup:.2f}x faster")
        print(f"  Maximum speedup: numpy is {max_speedup:.2f}x faster")
    
    print(f"\nConclusions:")
    print(f"  • numpy consistently outperforms arrypy due to C implementation")
    print(f"  • arrypy provides similar functionality with pure Python")
    print(f"  • Use arrypy for learning, prototyping, or when numpy isn't available")
    print(f"  • Use numpy for production code requiring high performance")

if __name__ == "__main__":
    run_comprehensive_benchmarks()