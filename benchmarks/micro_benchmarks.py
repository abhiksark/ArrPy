"""
Micro-benchmarks for specific operations comparing arrypy vs numpy
"""

import time
import numpy as np
from arrypy import Array
import matplotlib.pyplot as plt
import gc
from statistics import mean, stdev

class MicroBenchmark:
    def __init__(self, iterations=100):
        self.iterations = iterations
        self.results = {}
    
    def time_function(self, func, *args, **kwargs):
        """Time a function execution multiple times and return statistics"""
        times = []
        
        for _ in range(self.iterations):
            gc.collect()  # Force garbage collection
            start = time.perf_counter()
            func(*args, **kwargs)
            end = time.perf_counter()
            times.append(end - start)
        
        return {
            'mean': mean(times),
            'std': stdev(times) if len(times) > 1 else 0,
            'min': min(times),
            'max': max(times),
            'times': times
        }
    
    def compare_operations(self, name, arrypy_func, numpy_func, *args, **kwargs):
        """Compare arrypy and numpy operations"""
        print(f"\nBenchmarking: {name}")
        print(f"Iterations: {self.iterations}")
        
        arrypy_stats = self.time_function(arrypy_func, *args, **kwargs)
        numpy_stats = self.time_function(numpy_func, *args, **kwargs)
        
        speedup = arrypy_stats['mean'] / numpy_stats['mean']
        
        print(f"arrypy: {arrypy_stats['mean']:.6f}s ± {arrypy_stats['std']:.6f}s")
        print(f"numpy:  {numpy_stats['mean']:.6f}s ± {numpy_stats['std']:.6f}s")
        print(f"Speedup: {speedup:.2f}x (numpy faster)")
        
        self.results[name] = {
            'arrypy': arrypy_stats,
            'numpy': numpy_stats,
            'speedup': speedup
        }
        
        return arrypy_stats, numpy_stats, speedup

def benchmark_creation_patterns():
    """Benchmark different array creation patterns"""
    benchmark = MicroBenchmark(iterations=1000)
    
    print("=" * 60)
    print("ARRAY CREATION PATTERN BENCHMARKS")
    print("=" * 60)
    
    # Small arrays (common in loops)
    small_data = [[1, 2, 3], [4, 5, 6]]
    benchmark.compare_operations(
        "Small 2x3 array creation",
        lambda: Array(small_data),
        lambda: np.array(small_data)
    )
    
    # 1D arrays of various sizes
    for size in [10, 100, 1000]:
        data = list(range(size))
        benchmark.compare_operations(
            f"1D array creation ({size} elements)",
            lambda d=data: Array(d),
            lambda d=data: np.array(d)
        )
    
    # Square matrices
    for size in [5, 10, 20]:
        data = [[i*j for j in range(size)] for i in range(size)]
        benchmark.compare_operations(
            f"Square matrix creation ({size}x{size})",
            lambda d=data: Array(d),
            lambda d=data: np.array(d)
        )
    
    return benchmark

def benchmark_arithmetic_patterns():
    """Benchmark arithmetic operation patterns"""
    benchmark = MicroBenchmark(iterations=500)
    
    print("\n" + "=" * 60)
    print("ARITHMETIC OPERATION PATTERN BENCHMARKS")
    print("=" * 60)
    
    # Setup test arrays
    sizes = [10, 50, 100]
    
    for size in sizes:
        data1 = [[i + j for j in range(size)] for i in range(size)]
        data2 = [[i * j + 1 for j in range(size)] for i in range(size)]
        
        arr1_arrypy = Array(data1)
        arr2_arrypy = Array(data2)
        arr1_numpy = np.array(data1)
        arr2_numpy = np.array(data2)
        
        # Binary operations
        operations = [
            ("Addition", lambda a, b: a + b),
            ("Subtraction", lambda a, b: a - b),
            ("Multiplication", lambda a, b: a * b),
            ("Division", lambda a, b: a / b)
        ]
        
        for op_name, op_func in operations:
            benchmark.compare_operations(
                f"{op_name} ({size}x{size})",
                lambda a1=arr1_arrypy, a2=arr2_arrypy: op_func(a1, a2),
                lambda a1=arr1_numpy, a2=arr2_numpy: op_func(a1, a2)
            )
        
        # Scalar operations
        benchmark.compare_operations(
            f"Scalar multiplication ({size}x{size})",
            lambda a=arr1_arrypy: a * 3.14159,
            lambda a=arr1_numpy: a * 3.14159
        )
    
    return benchmark

def benchmark_indexing_patterns():
    """Benchmark different indexing patterns"""
    benchmark = MicroBenchmark(iterations=10000)  # More iterations for fast operations
    
    print("\n" + "=" * 60)
    print("INDEXING PATTERN BENCHMARKS")
    print("=" * 60)
    
    # Create test array
    size = 50
    data = [[i + j for j in range(size)] for i in range(size)]
    arr_arrypy = Array(data)
    arr_numpy = np.array(data)
    
    # Single element access
    benchmark.compare_operations(
        "Single element access [25, 25]",
        lambda: arr_arrypy[25, 25],
        lambda: arr_numpy[25, 25]
    )
    
    # Row access
    benchmark.compare_operations(
        "Row access [10]",
        lambda: arr_arrypy[10],
        lambda: arr_numpy[10]
    )
    
    # Multiple random accesses
    import random
    random.seed(42)  # Reproducible results
    indices = [(random.randint(0, size-1), random.randint(0, size-1)) for _ in range(10)]
    
    def multiple_access_arrypy():
        total = 0
        for i, j in indices:
            total += arr_arrypy[i, j]
        return total
    
    def multiple_access_numpy():
        total = 0
        for i, j in indices:
            total += arr_numpy[i, j]
        return total
    
    benchmark.compare_operations(
        "Multiple random access (10 elements)",
        multiple_access_arrypy,
        multiple_access_numpy
    )
    
    return benchmark

def benchmark_matrix_operation_patterns():
    """Benchmark matrix operation patterns"""
    benchmark = MicroBenchmark(iterations=100)
    
    print("\n" + "=" * 60)
    print("MATRIX OPERATION PATTERN BENCHMARKS")
    print("=" * 60)
    
    # Test matrix multiplication for different sizes
    for size in [5, 10, 20, 30]:
        data1 = [[i + j + 1 for j in range(size)] for i in range(size)]
        data2 = [[i * j + 2 for j in range(size)] for i in range(size)]
        
        arr1_arrypy = Array(data1)
        arr2_arrypy = Array(data2)
        arr1_numpy = np.array(data1)
        arr2_numpy = np.array(data2)
        
        # Matrix multiplication
        benchmark.compare_operations(
            f"Matrix multiplication ({size}x{size})",
            lambda a1=arr1_arrypy, a2=arr2_arrypy: a1.dot(a2),
            lambda a1=arr1_numpy, a2=arr2_numpy: np.dot(a1, a2)
        )
        
        # Transpose
        benchmark.compare_operations(
            f"Transpose ({size}x{size})",
            lambda a=arr1_arrypy: a.T,
            lambda a=arr1_numpy: a.T
        )
    
    # Chain operations
    size = 10
    data = [[i + j + 1 for j in range(size)] for i in range(size)]
    arr_arrypy = Array(data)
    arr_numpy = np.array(data)
    
    def chain_operations_arrypy():
        return (arr_arrypy.T).dot(arr_arrypy)
    
    def chain_operations_numpy():
        return np.dot(arr_numpy.T, arr_numpy)
    
    benchmark.compare_operations(
        f"Chain operations: A.T @ A ({size}x{size})",
        chain_operations_arrypy,
        chain_operations_numpy
    )
    
    return benchmark

def benchmark_aggregation_patterns():
    """Benchmark aggregation operation patterns"""
    benchmark = MicroBenchmark(iterations=1000)
    
    print("\n" + "=" * 60)
    print("AGGREGATION PATTERN BENCHMARKS")
    print("=" * 60)
    
    # Test different array sizes
    for size in [100, 1000, 10000]:
        data = list(range(size))
        arr_arrypy = Array(data)
        arr_numpy = np.array(data)
        
        # Sum
        benchmark.compare_operations(
            f"Sum ({size} elements)",
            lambda a=arr_arrypy: a.sum(),
            lambda a=arr_numpy: a.sum()
        )
        
        # Mean
        benchmark.compare_operations(
            f"Mean ({size} elements)",
            lambda a=arr_arrypy: a.mean(),
            lambda a=arr_numpy: a.mean()
        )
    
    # 2D aggregations
    for size in [10, 50, 100]:
        data = [[i + j for j in range(size)] for i in range(size)]
        arr_arrypy = Array(data)
        arr_numpy = np.array(data)
        
        benchmark.compare_operations(
            f"2D Sum ({size}x{size})",
            lambda a=arr_arrypy: a.sum(),
            lambda a=arr_numpy: a.sum()
        )
        
        benchmark.compare_operations(
            f"2D Mean ({size}x{size})",
            lambda a=arr_arrypy: a.mean(),
            lambda a=arr_numpy: a.mean()
        )
    
    return benchmark

def benchmark_reshape_patterns():
    """Benchmark reshape operation patterns"""
    benchmark = MicroBenchmark(iterations=1000)
    
    print("\n" + "=" * 60)
    print("RESHAPE PATTERN BENCHMARKS")
    print("=" * 60)
    
    # Different reshape scenarios
    test_cases = [
        (100, (10, 10), "1D to 2D small"),
        (2500, (50, 50), "1D to 2D medium"),
        (10000, (100, 100), "1D to 2D large"),
        (1000, (10, 10, 10), "1D to 3D"),
    ]
    
    for total_size, new_shape, description in test_cases:
        data = list(range(total_size))
        arr_arrypy = Array(data)
        arr_numpy = np.array(data)
        
        benchmark.compare_operations(
            f"Reshape {description} ({total_size} -> {new_shape})",
            lambda a=arr_arrypy, s=new_shape: a.reshape(s),
            lambda a=arr_numpy, s=new_shape: a.reshape(s)
        )
    
    return benchmark

def generate_performance_report(benchmarks):
    """Generate a comprehensive performance report"""
    print("\n" + "=" * 80)
    print("MICRO-BENCHMARK PERFORMANCE REPORT")
    print("=" * 80)
    
    all_speedups = []
    category_summaries = {}
    
    for category_name, benchmark in benchmarks.items():
        print(f"\n{category_name.upper()}:")
        print("-" * 50)
        
        category_speedups = []
        for test_name, results in benchmark.results.items():
            speedup = results['speedup']
            all_speedups.append(speedup)
            category_speedups.append(speedup)
            
            arrypy_time = results['arrypy']['mean']
            numpy_time = results['numpy']['mean']
            
            print(f"{test_name:40} | numpy {speedup:6.2f}x faster | "
                  f"arrypy: {arrypy_time:.6f}s | numpy: {numpy_time:.6f}s")
        
        if category_speedups:
            category_summaries[category_name] = {
                'avg_speedup': sum(category_speedups) / len(category_speedups),
                'min_speedup': min(category_speedups),
                'max_speedup': max(category_speedups),
                'test_count': len(category_speedups)
            }
    
    # Overall summary
    print("\n" + "=" * 80)
    print("SUMMARY BY CATEGORY")
    print("=" * 80)
    
    for category, summary in category_summaries.items():
        print(f"{category:20} | Avg: {summary['avg_speedup']:6.2f}x | "
              f"Range: {summary['min_speedup']:5.2f}x - {summary['max_speedup']:6.2f}x | "
              f"Tests: {summary['test_count']}")
    
    if all_speedups:
        print(f"\nOVERALL STATISTICS:")
        print(f"Total tests: {len(all_speedups)}")
        print(f"Average speedup: {sum(all_speedups)/len(all_speedups):.2f}x")
        print(f"Median speedup: {sorted(all_speedups)[len(all_speedups)//2]:.2f}x")
        print(f"Min speedup: {min(all_speedups):.2f}x")
        print(f"Max speedup: {max(all_speedups):.2f}x")
    
    # Performance insights
    print(f"\nPERFORMANCE INSIGHTS:")
    print(f"• Operations with higher speedups indicate larger performance gaps")
    print(f"• Matrix operations typically show the largest differences")
    print(f"• Simple operations (indexing) may have smaller gaps")
    print(f"• Memory allocation overhead affects creation benchmarks")

def run_micro_benchmarks():
    """Run all micro-benchmarks"""
    print("ARRYPY vs NUMPY MICRO-BENCHMARKS")
    print("=" * 80)
    print("Detailed performance analysis of individual operations")
    print("=" * 80)
    
    benchmarks = {}
    
    # Run all benchmark categories
    benchmark_functions = [
        ("Array Creation", benchmark_creation_patterns),
        ("Arithmetic Operations", benchmark_arithmetic_patterns),
        ("Indexing Operations", benchmark_indexing_patterns),
        ("Matrix Operations", benchmark_matrix_operation_patterns),
        ("Aggregation Operations", benchmark_aggregation_patterns),
        ("Reshape Operations", benchmark_reshape_patterns)
    ]
    
    for name, func in benchmark_functions:
        benchmarks[name] = func()
    
    # Generate comprehensive report
    generate_performance_report(benchmarks)

if __name__ == "__main__":
    run_micro_benchmarks()