#!/usr/bin/env python3
"""
Comprehensive benchmark comparing Cython-optimized ArrPy with NumPy.

This benchmark tests various operations to see how our Cython implementation
performs against the industry-standard NumPy library.
"""

import time
import statistics
import sys
from typing import List, Tuple, Callable, Any

import numpy as np
from arrpy.core import Array
from arrpy.creation import zeros as arrpy_zeros, ones as arrpy_ones
from arrpy.math import power as arrpy_power, absolute as arrpy_absolute


class BenchmarkRunner:
    """Helper class for running benchmarks with statistical analysis."""
    
    def __init__(self, warmup_runs: int = 3, test_runs: int = 10):
        self.warmup_runs = warmup_runs
        self.test_runs = test_runs
    
    def time_operation(self, operation: Callable, *args, **kwargs) -> Tuple[float, float, List[float]]:
        """
        Time an operation multiple times and return statistics.
        
        Returns:
            Tuple of (mean_time, std_dev, all_times)
        """
        # Warmup runs
        for _ in range(self.warmup_runs):
            try:
                operation(*args, **kwargs)
            except Exception:
                pass  # Some operations might fail during warmup
        
        # Actual timing runs
        times = []
        for _ in range(self.test_runs):
            start = time.perf_counter()
            result = operation(*args, **kwargs)
            end = time.perf_counter()
            times.append(end - start)
        
        mean_time = statistics.mean(times)
        std_dev = statistics.stdev(times) if len(times) > 1 else 0.0
        
        return mean_time, std_dev, times
    
    def compare_operations(self, arrpy_op: Callable, numpy_op: Callable, 
                          arrpy_args: tuple, numpy_args: tuple,
                          operation_name: str) -> dict:
        """Compare ArrPy and NumPy operations."""
        
        print(f"\n{'='*60}")
        print(f"Benchmarking: {operation_name}")
        print('='*60)
        
        # Benchmark ArrPy
        print("Testing ArrPy...")
        try:
            arrpy_mean, arrpy_std, arrpy_times = self.time_operation(arrpy_op, *arrpy_args)
            arrpy_success = True
        except Exception as e:
            print(f"ArrPy failed: {e}")
            arrpy_mean, arrpy_std, arrpy_times = float('inf'), 0, []
            arrpy_success = False
        
        # Benchmark NumPy
        print("Testing NumPy...")
        try:
            numpy_mean, numpy_std, numpy_times = self.time_operation(numpy_op, *numpy_args)
            numpy_success = True
        except Exception as e:
            print(f"NumPy failed: {e}")
            numpy_mean, numpy_std, numpy_times = float('inf'), 0, []
            numpy_success = False
        
        # Calculate results
        if arrpy_success and numpy_success:
            speedup = numpy_mean / arrpy_mean if arrpy_mean > 0 else float('inf')
            winner = "ArrPy" if speedup > 1 else "NumPy"
            
            # Calculate elements per second
            try:
                # Try to estimate array size for throughput calculation
                if hasattr(arrpy_args[0], 'size'):
                    elements = arrpy_args[0].size
                elif hasattr(arrpy_args[0], '__len__'):
                    elements = len(arrpy_args[0])
                else:
                    elements = 1
                
                arrpy_throughput = elements / arrpy_mean if arrpy_mean > 0 else 0
                numpy_throughput = elements / numpy_mean if numpy_mean > 0 else 0
            except:
                arrpy_throughput = numpy_throughput = 0
        else:
            speedup = 0
            winner = "N/A"
            arrpy_throughput = numpy_throughput = 0
        
        # Print results
        print(f"\nResults for {operation_name}:")
        print(f"  ArrPy:  {arrpy_mean*1000:.3f}ms ± {arrpy_std*1000:.3f}ms")
        print(f"  NumPy:  {numpy_mean*1000:.3f}ms ± {numpy_std*1000:.3f}ms")
        
        if arrpy_success and numpy_success:
            if speedup > 1:
                print(f"  🎉 ArrPy is {speedup:.2f}x FASTER than NumPy!")
            elif speedup < 1:
                print(f"  📊 NumPy is {1/speedup:.2f}x faster than ArrPy")
            else:
                print(f"  🤝 Performance is equivalent")
            
            if arrpy_throughput > 0:
                print(f"  Throughput - ArrPy: {arrpy_throughput/1e6:.2f}M elements/sec, NumPy: {numpy_throughput/1e6:.2f}M elements/sec")
        
        return {
            'operation': operation_name,
            'arrpy_time': arrpy_mean,
            'numpy_time': numpy_mean,
            'speedup': speedup,
            'winner': winner,
            'arrpy_success': arrpy_success,
            'numpy_success': numpy_success,
            'arrpy_throughput': arrpy_throughput,
            'numpy_throughput': numpy_throughput
        }


def create_test_data():
    """Create test data for benchmarks."""
    sizes = {
        'small': 100,
        'medium': 1000, 
        'large': 10000,
        'xlarge': 100000
    }
    
    data = {}
    for size_name, size in sizes.items():
        # 1D arrays
        data[f'{size_name}_1d_list'] = [float(i) for i in range(size)]
        data[f'{size_name}_1d_arrpy'] = Array([float(i) for i in range(size)])
        data[f'{size_name}_1d_numpy'] = np.array([float(i) for i in range(size)])
        
        # 2D arrays (for smaller sizes)
        if size <= 1000:
            rows = int(size ** 0.5)
            cols = size // rows
            data_2d = [[float(i*cols + j) for j in range(cols)] for i in range(rows)]
            data[f'{size_name}_2d_list'] = data_2d
            data[f'{size_name}_2d_arrpy'] = Array(data_2d)
            data[f'{size_name}_2d_numpy'] = np.array(data_2d)
    
    return data


def benchmark_array_creation(runner: BenchmarkRunner, data: dict):
    """Benchmark array creation operations."""
    print(f"\n{'#'*80}")
    print("ARRAY CREATION BENCHMARKS")
    print('#'*80)
    
    results = []
    
    # Test different sizes
    for size_name in ['small', 'medium', 'large']:
        source_data = data[f'{size_name}_1d_list']
        
        result = runner.compare_operations(
            Array, np.array,
            (source_data,), (source_data,),
            f"Array Creation ({size_name}: {len(source_data)} elements)"
        )
        results.append(result)
    
    # Test zeros creation
    for size in [100, 1000, 10000]:
        result = runner.compare_operations(
            arrpy_zeros, np.zeros,
            (size,), (size,),
            f"Zeros Creation ({size} elements)"
        )
        results.append(result)
    
    # Test ones creation  
    for size in [100, 1000, 10000]:
        result = runner.compare_operations(
            arrpy_ones, np.ones,
            (size,), (size,),
            f"Ones Creation ({size} elements)"
        )
        results.append(result)
    
    return results


def benchmark_arithmetic_operations(runner: BenchmarkRunner, data: dict):
    """Benchmark arithmetic operations."""
    print(f"\n{'#'*80}")
    print("ARITHMETIC OPERATIONS BENCHMARKS") 
    print('#'*80)
    
    results = []
    
    for size_name in ['small', 'medium', 'large']:
        arrpy_arr = data[f'{size_name}_1d_arrpy']
        numpy_arr = data[f'{size_name}_1d_numpy']
        
        # Addition
        result = runner.compare_operations(
            lambda a: a + a, lambda a: a + a,
            (arrpy_arr,), (numpy_arr,),
            f"Addition ({size_name}: {arrpy_arr.size} elements)"
        )
        results.append(result)
        
        # Scalar addition
        result = runner.compare_operations(
            lambda a: a + 5, lambda a: a + 5,
            (arrpy_arr,), (numpy_arr,),
            f"Scalar Addition ({size_name}: {arrpy_arr.size} elements)"
        )
        results.append(result)
        
        # Multiplication
        result = runner.compare_operations(
            lambda a: a * a, lambda a: a * a,
            (arrpy_arr,), (numpy_arr,),
            f"Multiplication ({size_name}: {arrpy_arr.size} elements)"
        )
        results.append(result)
        
        # Scalar multiplication
        result = runner.compare_operations(
            lambda a: a * 2.5, lambda a: a * 2.5,
            (arrpy_arr,), (numpy_arr,),
            f"Scalar Multiplication ({size_name}: {arrpy_arr.size} elements)"
        )
        results.append(result)
    
    return results


def benchmark_aggregation_operations(runner: BenchmarkRunner, data: dict):
    """Benchmark aggregation operations."""
    print(f"\n{'#'*80}")
    print("AGGREGATION OPERATIONS BENCHMARKS")
    print('#'*80)
    
    results = []
    
    for size_name in ['small', 'medium', 'large']:
        arrpy_arr = data[f'{size_name}_1d_arrpy']
        numpy_arr = data[f'{size_name}_1d_numpy']
        
        # Sum
        result = runner.compare_operations(
            lambda a: a.sum(), lambda a: a.sum(),
            (arrpy_arr,), (numpy_arr,),
            f"Sum ({size_name}: {arrpy_arr.size} elements)"
        )
        results.append(result)
        
        # Sum (fast version if available)
        if hasattr(arrpy_arr, 'sum_fast'):
            result = runner.compare_operations(
                lambda a: a.sum_fast(), lambda a: a.sum(),
                (arrpy_arr,), (numpy_arr,),
                f"Sum Fast ({size_name}: {arrpy_arr.size} elements)"
            )
            results.append(result)
        
        # Mean
        result = runner.compare_operations(
            lambda a: a.mean(), lambda a: a.mean(),
            (arrpy_arr,), (numpy_arr,),
            f"Mean ({size_name}: {arrpy_arr.size} elements)"
        )
        results.append(result)
        
        # Mean (fast version if available)
        if hasattr(arrpy_arr, 'mean_fast'):
            result = runner.compare_operations(
                lambda a: a.mean_fast(), lambda a: a.mean(),
                (arrpy_arr,), (numpy_arr,),
                f"Mean Fast ({size_name}: {arrpy_arr.size} elements)"
            )
            results.append(result)
        
        # Min/Max
        result = runner.compare_operations(
            lambda a: a.min(), lambda a: a.min(),
            (arrpy_arr,), (numpy_arr,),
            f"Min ({size_name}: {arrpy_arr.size} elements)"
        )
        results.append(result)
        
        result = runner.compare_operations(
            lambda a: a.max(), lambda a: a.max(),
            (arrpy_arr,), (numpy_arr,),
            f"Max ({size_name}: {arrpy_arr.size} elements)"
        )
        results.append(result)
    
    return results


def benchmark_mathematical_functions(runner: BenchmarkRunner, data: dict):
    """Benchmark mathematical functions."""
    print(f"\n{'#'*80}")
    print("MATHEMATICAL FUNCTIONS BENCHMARKS")
    print('#'*80)
    
    results = []
    
    for size_name in ['small', 'medium']:  # Skip large for math functions
        arrpy_arr = data[f'{size_name}_1d_arrpy']
        numpy_arr = data[f'{size_name}_1d_numpy']
        
        # Create positive arrays for math functions
        arrpy_pos = Array([abs(x) + 1 for x in arrpy_arr._data])
        numpy_pos = np.abs(numpy_arr) + 1
        
        # Square root
        result = runner.compare_operations(
            lambda a: a.sqrt(), lambda a: np.sqrt(a),
            (arrpy_pos,), (numpy_pos,),
            f"Square Root ({size_name}: {arrpy_arr.size} elements)"
        )
        results.append(result)
        
        # Square root (fast version)
        if hasattr(arrpy_pos, 'sqrt_fast'):
            result = runner.compare_operations(
                lambda a: a.sqrt_fast(), lambda a: np.sqrt(a),
                (arrpy_pos,), (numpy_pos,),
                f"Square Root Fast ({size_name}: {arrpy_arr.size} elements)"
            )
            results.append(result)
        
        # Power function
        result = runner.compare_operations(
            lambda a: arrpy_power(a, 2), lambda a: np.power(a, 2),
            (arrpy_pos,), (numpy_pos,),
            f"Power (x^2) ({size_name}: {arrpy_arr.size} elements)"
        )
        results.append(result)
        
        # Absolute value
        result = runner.compare_operations(
            lambda a: arrpy_absolute(a), lambda a: np.abs(a),
            (arrpy_arr,), (numpy_arr,),
            f"Absolute Value ({size_name}: {arrpy_arr.size} elements)"
        )
        results.append(result)
        
        # Trigonometric (smaller arrays due to computational cost)
        if size_name == 'small':
            # Create arrays with reasonable values for trig functions
            small_range = Array([float(i * 0.1) for i in range(100)])
            small_numpy = np.array([float(i * 0.1) for i in range(100)])
            
            if hasattr(small_range, 'sin_fast'):
                result = runner.compare_operations(
                    lambda a: a.sin_fast(), lambda a: np.sin(a),
                    (small_range,), (small_numpy,),
                    f"Sine Fast (100 elements)"
                )
                results.append(result)
            
            if hasattr(small_range, 'cos_fast'):
                result = runner.compare_operations(
                    lambda a: a.cos_fast(), lambda a: np.cos(a),
                    (small_range,), (small_numpy,),
                    f"Cosine Fast (100 elements)"
                )
                results.append(result)
    
    return results


def benchmark_indexing_operations(runner: BenchmarkRunner, data: dict):
    """Benchmark indexing and slicing operations."""
    print(f"\n{'#'*80}")
    print("INDEXING OPERATIONS BENCHMARKS")
    print('#'*80)
    
    results = []
    
    for size_name in ['small', 'medium']:
        if f'{size_name}_2d_arrpy' in data:
            arrpy_arr = data[f'{size_name}_2d_arrpy']
            numpy_arr = data[f'{size_name}_2d_numpy']
            
            # Single element access
            result = runner.compare_operations(
                lambda a: a[0, 0], lambda a: a[0, 0],
                (arrpy_arr,), (numpy_arr,),
                f"Single Element Access ({size_name})"
            )
            results.append(result)
            
            # Row access
            result = runner.compare_operations(
                lambda a: a[0], lambda a: a[0],
                (arrpy_arr,), (numpy_arr,),
                f"Row Access ({size_name})"
            )
            results.append(result)
    
    return results


def print_summary(all_results: List[dict]):
    """Print a comprehensive summary of all benchmark results."""
    print(f"\n{'#'*80}")
    print("COMPREHENSIVE BENCHMARK SUMMARY")
    print(f"{'#'*80}")
    
    # Categorize results
    categories = {
        'Array Creation': [],
        'Arithmetic Operations': [],
        'Aggregation Operations': [],
        'Mathematical Functions': [], 
        'Indexing Operations': []
    }
    
    for result in all_results:
        op_name = result['operation']
        if 'Creation' in op_name:
            categories['Array Creation'].append(result)
        elif any(x in op_name for x in ['Addition', 'Multiplication']):
            categories['Arithmetic Operations'].append(result)
        elif any(x in op_name for x in ['Sum', 'Mean', 'Min', 'Max']):
            categories['Aggregation Operations'].append(result)
        elif any(x in op_name for x in ['Root', 'Power', 'Absolute', 'Sine', 'Cosine']):
            categories['Mathematical Functions'].append(result)
        elif 'Access' in op_name:
            categories['Indexing Operations'].append(result)
    
    # Print category summaries
    total_wins = {'ArrPy': 0, 'NumPy': 0, 'Equivalent': 0}
    
    for category, results in categories.items():
        if not results:
            continue
            
        print(f"\n{'-'*60}")
        print(f"{category.upper()}")
        print(f"{'-'*60}")
        
        wins = {'ArrPy': 0, 'NumPy': 0, 'Equivalent': 0}
        speedups = []
        
        for result in results:
            if result['arrpy_success'] and result['numpy_success']:
                speedup = result['speedup']
                speedups.append(speedup)
                
                if speedup > 1.1:  # 10% threshold
                    wins['ArrPy'] += 1
                    total_wins['ArrPy'] += 1
                    status = f"✅ ArrPy {speedup:.2f}x faster"
                elif speedup < 0.9:  # 10% threshold
                    wins['NumPy'] += 1
                    total_wins['NumPy'] += 1
                    status = f"📊 NumPy {1/speedup:.2f}x faster"
                else:
                    wins['Equivalent'] += 1
                    total_wins['Equivalent'] += 1
                    status = "🤝 Equivalent"
                
                print(f"  {result['operation']:<40} {status}")
            else:
                print(f"  {result['operation']:<40} ❌ Failed")
        
        if speedups:
            avg_speedup = statistics.mean(speedups)
            print(f"\n  Category Summary: ArrPy {wins['ArrPy']} wins, NumPy {wins['NumPy']} wins, {wins['Equivalent']} equivalent")
            print(f"  Average Speedup: {avg_speedup:.2f}x (ArrPy vs NumPy)")
    
    # Overall summary
    print(f"\n{'='*80}")
    print("FINAL RESULTS")
    print(f"{'='*80}")
    print(f"ArrPy Wins: {total_wins['ArrPy']}")
    print(f"NumPy Wins: {total_wins['NumPy']}")
    print(f"Equivalent: {total_wins['Equivalent']}")
    
    total_tests = sum(total_wins.values())
    if total_tests > 0:
        arrpy_percentage = (total_wins['ArrPy'] / total_tests) * 100
        print(f"\nArrPy won {arrpy_percentage:.1f}% of benchmarks")
        
        if arrpy_percentage > 50:
            print("🎉 ArrPy outperforms NumPy in most operations!")
        elif arrpy_percentage > 30:
            print("🚀 ArrPy is competitive with NumPy!")
        else:
            print("📈 ArrPy shows good performance, with room for optimization")
    
    # Performance insights
    print(f"\n{'-'*60}")
    print("PERFORMANCE INSIGHTS")
    print(f"{'-'*60}")
    
    successful_results = [r for r in all_results if r['arrpy_success'] and r['numpy_success']]
    if successful_results:
        all_speedups = [r['speedup'] for r in successful_results]
        max_speedup = max(all_speedups)
        min_speedup = min(all_speedups)
        avg_speedup = statistics.mean(all_speedups)
        
        print(f"Best ArrPy performance: {max_speedup:.2f}x faster than NumPy")
        print(f"Worst ArrPy performance: {1/min_speedup:.2f}x slower than NumPy")
        print(f"Average performance: {avg_speedup:.2f}x vs NumPy")
        
        # Find best and worst performers
        best_test = max(successful_results, key=lambda x: x['speedup'])
        worst_test = min(successful_results, key=lambda x: x['speedup'])
        
        print(f"\nBest performing operation: {best_test['operation']}")
        print(f"Worst performing operation: {worst_test['operation']}")


def main():
    """Run comprehensive ArrPy vs NumPy benchmark."""
    print("ArrPy vs NumPy Comprehensive Benchmark")
    print("=" * 80)
    print(f"Python version: {sys.version}")
    print(f"NumPy version: {np.__version__}")
    
    # Check ArrPy implementation
    test_arr = Array([1, 2, 3])
    print(f"ArrPy implementation: {type(test_arr).__module__}")
    if hasattr(test_arr, 'sum_fast'):
        print("✅ Cython fast methods available")
    else:
        print("⚠️  Using Python fallback")
    
    print("\nCreating test data...")
    data = create_test_data()
    
    print("Initializing benchmark runner...")
    runner = BenchmarkRunner(warmup_runs=2, test_runs=5)
    
    # Run all benchmarks
    all_results = []
    
    try:
        all_results.extend(benchmark_array_creation(runner, data))
        all_results.extend(benchmark_arithmetic_operations(runner, data))
        all_results.extend(benchmark_aggregation_operations(runner, data))
        all_results.extend(benchmark_mathematical_functions(runner, data))
        all_results.extend(benchmark_indexing_operations(runner, data))
        
        # Print comprehensive summary
        print_summary(all_results)
        
    except KeyboardInterrupt:
        print("\n\nBenchmark interrupted by user.")
        if all_results:
            print("Partial results:")
            print_summary(all_results)
    
    except Exception as e:
        print(f"\n\nBenchmark error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()