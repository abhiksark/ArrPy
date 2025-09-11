#!/usr/bin/env python3
"""
Profiling infrastructure for ArrPy operations.
Identifies hot paths and performance bottlenecks.
"""

import time
import cProfile
import pstats
from io import StringIO
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import arrpy
from arrpy import Backend, set_backend


class OperationProfiler:
    """Profile operations across backends."""
    
    def __init__(self, operation_name, sizes=[100, 1000, 10000]):
        self.operation_name = operation_name
        self.sizes = sizes
        self.results = {}
    
    def profile_operation(self, func, *args, iterations=100):
        """Profile a single operation."""
        profiler = cProfile.Profile()
        
        # Warmup
        for _ in range(5):
            func(*args)
        
        # Profile
        profiler.enable()
        for _ in range(iterations):
            result = func(*args)
        profiler.disable()
        
        # Get stats
        stream = StringIO()
        stats = pstats.Stats(profiler, stream=stream)
        stats.sort_stats('cumulative')
        stats.print_stats(10)
        
        return result, stream.getvalue()
    
    def benchmark_operation(self, func, *args, iterations=100):
        """Time an operation without profiling overhead."""
        # Warmup
        for _ in range(5):
            func(*args)
        
        # Benchmark
        start = time.perf_counter()
        for _ in range(iterations):
            result = func(*args)
        elapsed = time.perf_counter() - start
        
        return elapsed / iterations
    
    def compare_backends(self, operation):
        """Compare operation across all backends."""
        print(f"\n{'='*60}")
        print(f"Profiling: {self.operation_name}")
        print(f"{'='*60}")
        
        for size in self.sizes:
            print(f"\nArray size: {size}")
            print("-" * 40)
            
            # Create test data
            data1 = list(range(size))
            data2 = list(range(size, size*2))
            
            for backend_name in ['python', 'cython', 'c']:
                try:
                    set_backend(backend_name)
                    a = arrpy.array(data1)
                    b = arrpy.array(data2)
                    
                    # Time the operation
                    time_taken = self.benchmark_operation(
                        lambda: operation(a, b),
                        iterations=100 if size <= 1000 else 10
                    )
                    
                    self.results[(backend_name, size)] = time_taken
                    print(f"  {backend_name:8}: {time_taken*1000:8.3f} ms")
                    
                except NotImplementedError:
                    print(f"  {backend_name:8}: Not implemented")
                except Exception as e:
                    print(f"  {backend_name:8}: Error - {str(e)[:30]}")
    
    def generate_report(self):
        """Generate performance report."""
        print(f"\n{'='*60}")
        print("Performance Summary")
        print(f"{'='*60}")
        
        # Calculate speedups
        for size in self.sizes:
            python_time = self.results.get(('python', size))
            if python_time:
                print(f"\nSize {size}:")
                for backend in ['cython', 'c']:
                    backend_time = self.results.get((backend, size))
                    if backend_time:
                        speedup = python_time / backend_time
                        print(f"  {backend} speedup: {speedup:.2f}x")


def profile_hot_paths():
    """Profile the most common operations."""
    print("ArrPy Operation Profiling")
    print("=" * 60)
    
    operations = [
        ("Addition", lambda a, b: a + b),
        ("Multiplication", lambda a, b: a * 2),
        ("Sum", lambda a, b: a.sum()),
        ("Matrix Multiply", lambda a, b: arrpy.linalg.matmul(a, b)),
    ]
    
    for op_name, op_func in operations:
        profiler = OperationProfiler(op_name)
        profiler.compare_backends(op_func)
        profiler.generate_report()


def detailed_profile(operation_name, size=1000):
    """Detailed profiling of a specific operation."""
    print(f"\nDetailed Profile: {operation_name}")
    print("=" * 60)
    
    # Create test data
    data = list(range(size))
    
    for backend_name in ['python', 'cython']:
        print(f"\n{backend_name.upper()} Backend:")
        print("-" * 40)
        
        try:
            set_backend(backend_name)
            a = arrpy.array(data)
            b = arrpy.array(data)
            
            # Profile the operation
            profiler = cProfile.Profile()
            profiler.enable()
            
            for _ in range(100):
                if operation_name == 'add':
                    result = a + b
                elif operation_name == 'multiply':
                    result = a * 2
                elif operation_name == 'sum':
                    result = a.sum()
                elif operation_name == 'matmul':
                    result = arrpy.linalg.matmul(a, b)
            
            profiler.disable()
            
            # Print stats
            stats = pstats.Stats(profiler)
            stats.sort_stats('cumulative')
            stats.print_stats(15)
            
        except Exception as e:
            print(f"Error: {e}")


def identify_bottlenecks():
    """Identify performance bottlenecks."""
    print("\nBottleneck Analysis")
    print("=" * 60)
    
    # Test different array sizes to identify scaling issues
    sizes = [10, 100, 1000, 10000]
    
    print("\nScaling Analysis (Time Complexity):")
    print("-" * 40)
    
    for backend_name in ['python', 'cython']:
        set_backend(backend_name)
        print(f"\n{backend_name.upper()}:")
        
        times = []
        for size in sizes:
            data = list(range(size))
            a = arrpy.array(data)
            b = arrpy.array(data)
            
            start = time.perf_counter()
            for _ in range(100):
                result = a + b
            elapsed = time.perf_counter() - start
            times.append(elapsed)
            
            print(f"  Size {size:5}: {elapsed:.4f}s")
        
        # Check scaling
        if len(times) >= 2:
            # Calculate scaling factor
            for i in range(1, len(times)):
                scaling = times[i] / times[i-1]
                size_ratio = sizes[i] / sizes[i-1]
                print(f"    {sizes[i-1]}->{sizes[i]}: {scaling:.1f}x time for {size_ratio:.0f}x size")


def main():
    """Main profiling workflow."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Profile ArrPy operations')
    parser.add_argument('--operation', '-o', help='Specific operation to profile')
    parser.add_argument('--size', '-s', type=int, default=1000, help='Array size')
    parser.add_argument('--hot-paths', action='store_true', help='Profile hot paths')
    parser.add_argument('--bottlenecks', action='store_true', help='Identify bottlenecks')
    
    args = parser.parse_args()
    
    if args.operation:
        detailed_profile(args.operation, args.size)
    elif args.hot_paths:
        profile_hot_paths()
    elif args.bottlenecks:
        identify_bottlenecks()
    else:
        # Default: run all profiling
        profile_hot_paths()
        identify_bottlenecks()


if __name__ == "__main__":
    main()