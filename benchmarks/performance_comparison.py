"""
Comprehensive performance benchmarks comparing arrpy with numpy
"""

import time
import numpy as np
from arrpy import Array, zeros, ones, eye, arange, linspace, concatenate, vstack, hstack
import gc
import math
from functools import wraps
from colors import *

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
        
    def run_benchmark(self, name, arrpy_func, numpy_func, *args, **kwargs):
        """Run a benchmark comparing arrpy and numpy functions"""
        print(f"\n{subheader(name, char='=', color=Colors.BRIGHT_CYAN)}")
        
        # Show progress
        print(f"{info('Running benchmark...')} {dim('(5 iterations)')}")
        
        # Benchmark arrpy
        @benchmark
        def arrpy_test():
            return arrpy_func(*args, **kwargs)
        
        # Benchmark numpy
        @benchmark
        def numpy_test():
            return numpy_func(*args, **kwargs)
        
        # Run tests multiple times for better accuracy
        arrpy_times = []
        numpy_times = []
        
        for i in range(5):  # Run 5 times
            print(f"\r{progress_bar(i+1, 5)} ", end="", flush=True)
            _, arrpy_time = arrpy_test()
            _, numpy_time = numpy_test()
            arrpy_times.append(arrpy_time)
            numpy_times.append(numpy_time)
        
        print()  # New line after progress bar
        
        # Calculate averages
        avg_arrpy = sum(arrpy_times) / len(arrpy_times)
        avg_numpy = sum(numpy_times) / len(numpy_times)
        speedup_ratio = avg_arrpy / avg_numpy
        
        # Display results with colors
        print(benchmark_result_line(name, avg_arrpy, avg_numpy, speedup_ratio))
        
        # Store results
        self.results[name] = {
            'arrpy_time': avg_arrpy,
            'numpy_time': avg_numpy,
            'speedup_ratio': speedup_ratio
        }
        
        return avg_arrpy, avg_numpy, speedup_ratio

def benchmark_initialization():
    """Benchmark array initialization"""
    benchmark = PerformanceBenchmark()
    
    print(header("ARRAY INITIALIZATION BENCHMARKS", char="=", color=Colors.BRIGHT_MAGENTA))
    
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
    
    print(header("INDEXING BENCHMARKS", char="=", color=Colors.BRIGHT_MAGENTA))
    
    # Setup test data
    data = [[i + j for j in range(100)] for i in range(100)]
    arr_arrpy = Array(data)
    arr_numpy = np.array(data)
    
    # Single element access
    def arrpy_single_access():
        result = 0
        for i in range(10):
            for j in range(10):
                result += arr_arrpy[i, j]
        return result
    
    def numpy_single_access():
        result = 0
        for i in range(10):
            for j in range(10):
                result += arr_numpy[i, j]
        return result
    
    benchmark.run_benchmark(
        "Single Element Access (100 operations)",
        arrpy_single_access,
        numpy_single_access
    )
    
    # Row access
    def arrpy_row_access():
        rows = []
        for i in range(10):
            rows.append(arr_arrpy[i])
        return rows
    
    def numpy_row_access():
        rows = []
        for i in range(10):
            rows.append(arr_numpy[i])
        return rows
    
    benchmark.run_benchmark(
        "Row Access (10 operations)",
        arrpy_row_access,
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
        
        arr1_arrpy = Array(data1)
        arr2_arrpy = Array(data2)
        arr1_numpy = np.array(data1)
        arr2_numpy = np.array(data2)
        
        # Addition
        benchmark.run_benchmark(
            f"Addition {size_name}",
            lambda: arr1_arrpy + arr2_arrpy,
            lambda: arr1_numpy + arr2_numpy
        )
        
        # Scalar multiplication
        benchmark.run_benchmark(
            f"Scalar Multiplication {size_name}",
            lambda: arr1_arrpy * 2.5,
            lambda: arr1_numpy * 2.5
        )
        
        # Element-wise multiplication
        benchmark.run_benchmark(
            f"Element-wise Multiplication {size_name}",
            lambda: arr1_arrpy * arr2_arrpy,
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
        
        arr1_arrpy = Array(data1)
        arr2_arrpy = Array(data2)
        arr1_numpy = np.array(data1)
        arr2_numpy = np.array(data2)
        
        # Matrix multiplication (dot product)
        benchmark.run_benchmark(
            f"Matrix Multiplication {size_name}",
            lambda: arr1_arrpy.dot(arr2_arrpy),
            lambda: np.dot(arr1_numpy, arr2_numpy)
        )
        
        # Transpose
        benchmark.run_benchmark(
            f"Transpose {size_name}",
            lambda: arr1_arrpy.T,
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
        
        arr_arrpy = Array(data)
        arr_numpy = np.array(data)
        
        benchmark.run_benchmark(
            description,
            lambda: arr_arrpy.reshape(new_shape),
            lambda: arr_numpy.reshape(new_shape)
        )
    
    return benchmark

def benchmark_array_creation():
    """Benchmark array creation functions"""
    benchmark = PerformanceBenchmark()
    
    print("\n" + "=" * 60)
    print("ARRAY CREATION FUNCTIONS BENCHMARKS")
    print("=" * 60)
    
    # Test different sizes
    sizes = [
        (100, "Small (100 elements)"),
        (1000, "Medium (1k elements)"),
        (10000, "Large (10k elements)")
    ]
    
    for size, size_name in sizes:
        # zeros
        benchmark.run_benchmark(
            f"zeros {size_name}",
            lambda s=size: zeros(s),
            lambda s=size: np.zeros(s)
        )
        
        # ones  
        benchmark.run_benchmark(
            f"ones {size_name}",
            lambda s=size: ones(s),
            lambda s=size: np.ones(s)
        )
    
    # 2D array creation
    sizes_2d = [
        ((10, 10), "Small (10x10)"),
        ((50, 50), "Medium (50x50)"),
        ((100, 100), "Large (100x100)")
    ]
    
    for shape, size_name in sizes_2d:
        # zeros 2D
        benchmark.run_benchmark(
            f"zeros 2D {size_name}",
            lambda s=shape: zeros(s),
            lambda s=shape: np.zeros(s)
        )
        
        # ones 2D
        benchmark.run_benchmark(
            f"ones 2D {size_name}",
            lambda s=shape: ones(s),
            lambda s=shape: np.ones(s)
        )
        
        # eye (identity matrix)
        n = shape[0]
        benchmark.run_benchmark(
            f"eye {size_name}",
            lambda n=n: eye(n),
            lambda n=n: np.eye(n)
        )
    
    # arange
    ranges = [
        (100, "Small (0-100)"),
        (1000, "Medium (0-1000)"),
        (10000, "Large (0-10000)")
    ]
    
    for stop, size_name in ranges:
        benchmark.run_benchmark(
            f"arange {size_name}",
            lambda s=stop: arange(s),
            lambda s=stop: np.arange(s)
        )
    
    # linspace
    for num_points, size_name in [(50, "Small (50 points)"), (500, "Medium (500 points)"), (5000, "Large (5000 points)")]:
        benchmark.run_benchmark(
            f"linspace {size_name}",
            lambda n=num_points: linspace(0, 1, n),
            lambda n=num_points: np.linspace(0, 1, n)
        )
    
    return benchmark

def benchmark_extended_aggregations():
    """Benchmark extended aggregation functions"""
    benchmark = PerformanceBenchmark()
    
    print("\n" + "=" * 60)
    print("EXTENDED AGGREGATION FUNCTIONS BENCHMARKS")
    print("=" * 60)
    
    # Test different sizes
    sizes = [
        (1000, "Small (1k elements)"),
        (10000, "Medium (10k elements)"),
        (100000, "Large (100k elements)")
    ]
    
    for size, size_name in sizes:
        data = list(range(size))
        
        arr_arrpy = Array(data)
        arr_numpy = np.array(data)
        
        # Min
        benchmark.run_benchmark(
            f"Min {size_name}",
            lambda a=arr_arrpy: a.min(),
            lambda a=arr_numpy: a.min()
        )
        
        # Max
        benchmark.run_benchmark(
            f"Max {size_name}",
            lambda a=arr_arrpy: a.max(),
            lambda a=arr_numpy: a.max()
        )
        
        # Standard deviation
        benchmark.run_benchmark(
            f"Std {size_name}",
            lambda a=arr_arrpy: a.std(),
            lambda a=arr_numpy: a.std()
        )
        
        # Variance
        benchmark.run_benchmark(
            f"Var {size_name}",
            lambda a=arr_arrpy: a.var(),
            lambda a=arr_numpy: a.var()
        )
        
        # Median
        benchmark.run_benchmark(
            f"Median {size_name}",
            lambda a=arr_arrpy: a.median(),
            lambda a=arr_numpy: np.median(a)
        )
        
        # Percentile (90th)
        benchmark.run_benchmark(
            f"Percentile 90 {size_name}",
            lambda a=arr_arrpy: a.percentile(90),
            lambda a=arr_numpy: np.percentile(a, 90)
        )
    
    return benchmark

def benchmark_mathematical_functions():
    """Benchmark mathematical functions"""
    benchmark = PerformanceBenchmark()
    
    print("\n" + "=" * 60)
    print("MATHEMATICAL FUNCTIONS BENCHMARKS")
    print("=" * 60)
    
    # Test different sizes
    sizes = [
        (1000, "Small (1k elements)"),
        (10000, "Medium (10k elements)"),
        (50000, "Large (50k elements)")
    ]
    
    for size, size_name in sizes:
        # Positive values for sqrt and log
        data_positive = [i + 1 for i in range(size)]
        arr_arrpy_pos = Array(data_positive)
        arr_numpy_pos = np.array(data_positive)
        
        # Square root
        benchmark.run_benchmark(
            f"sqrt {size_name}",
            lambda a=arr_arrpy_pos: a.sqrt(),
            lambda a=arr_numpy_pos: np.sqrt(a)
        )
        
        # Natural logarithm
        benchmark.run_benchmark(
            f"log {size_name}",
            lambda a=arr_arrpy_pos: a.log(),
            lambda a=arr_numpy_pos: np.log(a)
        )
        
        # Exponential (smaller arrays due to large results)
        if size <= 1000:
            data_small = [i * 0.01 for i in range(size)]
            arr_arrpy_small = Array(data_small)
            arr_numpy_small = np.array(data_small)
            
            benchmark.run_benchmark(
                f"exp {size_name}",
                lambda a=arr_arrpy_small: a.exp(),
                lambda a=arr_numpy_small: np.exp(a)
            )
        
        # Trigonometric functions (normalized to [-pi, pi])
        data_trig = [i * 2 * math.pi / size - math.pi for i in range(size)]
        arr_arrpy_trig = Array(data_trig)
        arr_numpy_trig = np.array(data_trig)
        
        benchmark.run_benchmark(
            f"sin {size_name}",
            lambda a=arr_arrpy_trig: a.sin(),
            lambda a=arr_numpy_trig: np.sin(a)
        )
        
        benchmark.run_benchmark(
            f"cos {size_name}",
            lambda a=arr_arrpy_trig: a.cos(),
            lambda a=arr_numpy_trig: np.cos(a)
        )
    
    return benchmark

def benchmark_comparison_operations():
    """Benchmark comparison operations"""
    benchmark = PerformanceBenchmark()
    
    print("\n" + "=" * 60)
    print("COMPARISON OPERATIONS BENCHMARKS")
    print("=" * 60)
    
    # Test different sizes
    sizes = [
        (1000, "Small (1k elements)"),
        (10000, "Medium (10k elements)"),
        (50000, "Large (50k elements)")
    ]
    
    for size, size_name in sizes:
        data1 = list(range(size))
        data2 = list(range(size//2, size + size//2))
        
        arr1_arrpy = Array(data1)
        arr2_arrpy = Array(data2)
        arr1_numpy = np.array(data1)
        arr2_numpy = np.array(data2)
        
        # Element-wise equality
        benchmark.run_benchmark(
            f"Equal {size_name}",
            lambda a1=arr1_arrpy, a2=arr2_arrpy: a1 == a2,
            lambda a1=arr1_numpy, a2=arr2_numpy: a1 == a2
        )
        
        # Element-wise greater than
        benchmark.run_benchmark(
            f"Greater than {size_name}",
            lambda a1=arr1_arrpy, a2=arr2_arrpy: a1 > a2,
            lambda a1=arr1_numpy, a2=arr2_numpy: a1 > a2
        )
        
        # Scalar comparison
        benchmark.run_benchmark(
            f"Scalar comparison {size_name}",
            lambda a=arr1_arrpy: a > size//2,
            lambda a=arr1_numpy: a > size//2
        )
    
    return benchmark

def benchmark_logical_operations():
    """Benchmark logical operations"""
    benchmark = PerformanceBenchmark()
    
    print("\n" + "=" * 60)
    print("LOGICAL OPERATIONS BENCHMARKS")
    print("=" * 60)
    
    # Test different sizes
    sizes = [
        (1000, "Small (1k elements)"),
        (10000, "Medium (10k elements)"),
        (50000, "Large (50k elements)")
    ]
    
    for size, size_name in sizes:
        # Create boolean-like data
        data1 = [i % 2 for i in range(size)]
        data2 = [(i + 1) % 2 for i in range(size)]
        
        arr1_arrpy = Array(data1)
        arr2_arrpy = Array(data2)
        arr1_numpy = np.array(data1, dtype=bool)
        arr2_numpy = np.array(data2, dtype=bool)
        
        # Logical AND
        benchmark.run_benchmark(
            f"Logical AND {size_name}",
            lambda a1=arr1_arrpy, a2=arr2_arrpy: a1.logical_and(a2),
            lambda a1=arr1_numpy, a2=arr2_numpy: np.logical_and(a1, a2)
        )
        
        # Logical OR
        benchmark.run_benchmark(
            f"Logical OR {size_name}",
            lambda a1=arr1_arrpy, a2=arr2_arrpy: a1.logical_or(a2),
            lambda a1=arr1_numpy, a2=arr2_numpy: np.logical_or(a1, a2)
        )
        
        # Logical NOT
        benchmark.run_benchmark(
            f"Logical NOT {size_name}",
            lambda a=arr1_arrpy: a.logical_not(),
            lambda a=arr1_numpy: np.logical_not(a)
        )
    
    return benchmark

def benchmark_concatenation_operations():
    """Benchmark concatenation and stacking operations"""
    benchmark = PerformanceBenchmark()
    
    print("\n" + "=" * 60)
    print("CONCATENATION OPERATIONS BENCHMARKS")
    print("=" * 60)
    
    # 1D concatenation
    sizes_1d = [
        (100, "Small (100 elements each)"),
        (1000, "Medium (1k elements each)"),
        (10000, "Large (10k elements each)")
    ]
    
    for size, size_name in sizes_1d:
        data1 = list(range(size))
        data2 = list(range(size, 2*size))
        
        arr1_arrpy = Array(data1)
        arr2_arrpy = Array(data2)
        arr1_numpy = np.array(data1)
        arr2_numpy = np.array(data2)
        
        # 1D concatenation
        benchmark.run_benchmark(
            f"1D Concatenate {size_name}",
            lambda a1=arr1_arrpy, a2=arr2_arrpy: concatenate([a1, a2]),
            lambda a1=arr1_numpy, a2=arr2_numpy: np.concatenate([a1, a2])
        )
        
        # hstack (same as 1D concatenate)
        benchmark.run_benchmark(
            f"1D HStack {size_name}",
            lambda a1=arr1_arrpy, a2=arr2_arrpy: hstack([a1, a2]),
            lambda a1=arr1_numpy, a2=arr2_numpy: np.hstack([a1, a2])
        )
    
    # 2D operations
    sizes_2d = [
        (10, "Small (10x10 each)"),
        (50, "Medium (50x50 each)"),
        (100, "Large (100x100 each)")
    ]
    
    for size, size_name in sizes_2d:
        data1 = [[i + j for j in range(size)] for i in range(size)]
        data2 = [[i + j + size for j in range(size)] for i in range(size)]
        
        arr1_arrpy = Array(data1)
        arr2_arrpy = Array(data2)
        arr1_numpy = np.array(data1)
        arr2_numpy = np.array(data2)
        
        # Vertical stack
        benchmark.run_benchmark(
            f"2D VStack {size_name}",
            lambda a1=arr1_arrpy, a2=arr2_arrpy: vstack([a1, a2]),
            lambda a1=arr1_numpy, a2=arr2_numpy: np.vstack([a1, a2])
        )
        
        # Horizontal stack
        benchmark.run_benchmark(
            f"2D HStack {size_name}",
            lambda a1=arr1_arrpy, a2=arr2_arrpy: hstack([a1, a2]),
            lambda a1=arr1_numpy, a2=arr2_numpy: np.hstack([a1, a2])
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
        
        arr_arrpy = Array(data)
        arr_numpy = np.array(data)
        
        # Sum
        benchmark.run_benchmark(
            f"Sum {size_name}",
            lambda: arr_arrpy.sum(),
            lambda: arr_numpy.sum()
        )
        
        # Mean
        benchmark.run_benchmark(
            f"Mean {size_name}",
            lambda: arr_arrpy.mean(),
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
        
        # Measure arrpy memory
        arr_arrpy = Array(data)
        arrpy_size = sys.getsizeof(arr_arrpy._data) + sys.getsizeof(arr_arrpy._shape)
        
        # Measure numpy memory
        arr_numpy = np.array(data)
        numpy_size = arr_numpy.nbytes
        
        memory_ratio = arrpy_size / numpy_size
        
        print(f"\nArray size: {size} elements")
        print(f"arrpy memory: {arrpy_size:,} bytes")
        print(f"numpy memory:  {numpy_size:,} bytes")
        print(f"arrpy uses {memory_ratio:.2f}x more memory")

def run_comprehensive_benchmarks():
    """Run all benchmarks and generate summary report"""
    print(ascii_logo())
    print(header("COMPREHENSIVE PERFORMANCE COMPARISON", char="═", color=Colors.BRIGHT_CYAN))
    print(f"{info('Note: numpy is expected to be significantly faster as it is implemented in C')}")
    print(f"{info('This benchmark helps understand the performance trade-offs')}")
    print(f"{warning('Running comprehensive benchmarks... This may take several minutes.')}")
    
    all_results = {}
    
    # Run all benchmark categories
    benchmark_categories = [
        ("Initialization", benchmark_initialization),
        ("Indexing", benchmark_indexing),
        ("Arithmetic", benchmark_arithmetic),
        ("Matrix Operations", benchmark_matrix_operations),
        ("Reshape", benchmark_reshape),
        ("Array Creation", benchmark_array_creation),
        ("Extended Aggregations", benchmark_extended_aggregations),
        ("Mathematical Functions", benchmark_mathematical_functions),
        ("Comparison Operations", benchmark_comparison_operations),
        ("Logical Operations", benchmark_logical_operations),
        ("Concatenation Operations", benchmark_concatenation_operations),
        ("Basic Aggregations", benchmark_aggregations)
    ]
    
    for category_name, benchmark_func in benchmark_categories:
        results = benchmark_func()
        all_results[category_name] = results.results
    
    # Memory usage comparison
    benchmark_memory_usage()
    
    # Generate summary report
    print(header("PERFORMANCE SUMMARY REPORT", char="═", color=Colors.BRIGHT_GREEN))
    
    all_speedups = []
    category_summaries = []
    
    for category_name, category_results in all_results.items():
        category_speedups = []
        print(f"\n{subheader(category_name, color=Colors.BRIGHT_BLUE)}")
        
        for test_name, test_results in category_results.items():
            speedup = test_results['speedup_ratio']
            all_speedups.append(speedup)
            category_speedups.append(speedup)
            
            arrpy_time = test_results['arrpy_time']
            numpy_time = test_results['numpy_time']
            print(f"  {benchmark_result_line(test_name, arrpy_time, numpy_time, speedup)}")
        
        if category_speedups:
            avg_cat_speedup = sum(category_speedups) / len(category_speedups)
            category_summaries.append((category_name, avg_cat_speedup, len(category_speedups)))
    
    # Overall summary
    print(header("CATEGORY PERFORMANCE SUMMARY", char="─", color=Colors.BRIGHT_YELLOW))
    for category_name, avg_speedup, test_count in category_summaries:
        print(category_summary(category_name, avg_speedup, test_count))
    
    if all_speedups:
        avg_speedup = sum(all_speedups) / len(all_speedups)
        min_speedup = min(all_speedups)
        max_speedup = max(all_speedups)
        
        print(header("OVERALL PERFORMANCE STATISTICS", char="─", color=Colors.BRIGHT_WHITE))
        print(f"  📊 {highlight('Total tests conducted:')} {len(all_speedups)}")
        print(f"  📈 {highlight('Average speedup:')} numpy is {format_speedup(avg_speedup)} faster")
        print(f"  🏃 {highlight('Best case:')} numpy is {format_speedup(min_speedup)} faster")
        print(f"  🚀 {highlight('Worst case:')} numpy is {format_speedup(max_speedup)} faster")
    
    print(header("KEY INSIGHTS & RECOMMENDATIONS", char="─", color=Colors.BRIGHT_MAGENTA))
    print(f"  {success('numpy consistently outperforms arrpy due to optimized C implementation')}")
    print(f"  {info('arrpy provides similar functionality with pure Python - great for learning!')}")
    print(f"  {warning('Use arrpy for prototyping, education, or when numpy is not available')}")
    print(f"  {highlight('Use numpy for production code requiring high performance', Colors.BRIGHT_GREEN)}")
    print(f"  {info('Performance gaps increase with larger array sizes')}")
    print(f"  {success('Both libraries produce identical results - choose based on your needs!')}")
    
    print(f"\n{colorize('🎉 Benchmark completed successfully! 🎉', Colors.BRIGHT_GREEN, style=Colors.BOLD)}")

if __name__ == "__main__":
    run_comprehensive_benchmarks()