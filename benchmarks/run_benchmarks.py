"""
Main benchmark runner for ArrPy.
Compares performance with NumPy.
"""

import time
import sys
import argparse
from typing import Dict, Any
import numpy as np

# Import ArrPy when it's functional
try:
    import arrpy as ap
    ARRPY_AVAILABLE = True
except ImportError:
    ARRPY_AVAILABLE = False
    print("Warning: ArrPy not fully implemented yet")


class BenchmarkRunner:
    """Run and compare benchmarks between ArrPy and NumPy."""
    
    def __init__(self, compare_numpy=False):
        """
        Initialize benchmark runner.
        
        Parameters
        ----------
        compare_numpy : bool
            Whether to compare with NumPy
        """
        self.compare_numpy = compare_numpy
        self.results = {}
    
    def time_operation(self, func, *args, iterations=100, **kwargs):
        """
        Time an operation over multiple iterations.
        
        Parameters
        ----------
        func : callable
            Function to benchmark
        *args : tuple
            Arguments for function
        iterations : int
            Number of iterations
        **kwargs : dict
            Keyword arguments for function
        
        Returns
        -------
        float
            Average time in seconds
        """
        times = []
        for _ in range(iterations):
            start = time.perf_counter()
            func(*args, **kwargs)
            end = time.perf_counter()
            times.append(end - start)
        
        return sum(times) / len(times)
    
    def benchmark_creation(self):
        """Benchmark array creation operations."""
        print("\n=== Array Creation Benchmarks ===")
        sizes = [(100,), (1000, 1000), (100, 100, 100)]
        
        for size in sizes:
            print(f"\nSize: {size}")
            
            # NumPy benchmarks
            np_time = self.time_operation(np.zeros, size)
            print(f"NumPy zeros: {np_time:.6f} seconds")
            
            if ARRPY_AVAILABLE:
                # ArrPy benchmarks
                ap_time = self.time_operation(ap.zeros, size)
                print(f"ArrPy zeros: {ap_time:.6f} seconds")
                print(f"Ratio (ArrPy/NumPy): {ap_time/np_time:.2f}x")
    
    def benchmark_operations(self):
        """Benchmark mathematical operations."""
        print("\n=== Mathematical Operations Benchmarks ===")
        sizes = [(1000,), (100, 100), (50, 50, 50)]
        
        for size in sizes:
            print(f"\nSize: {size}")
            
            # Create test arrays
            np_arr1 = np.random.random(size)
            np_arr2 = np.random.random(size)
            
            # NumPy addition
            np_time = self.time_operation(np.add, np_arr1, np_arr2)
            print(f"NumPy addition: {np_time:.6f} seconds")
            
            if ARRPY_AVAILABLE:
                # ArrPy arrays
                # ap_arr1 = ap.array(np_arr1.tolist())
                # ap_arr2 = ap.array(np_arr2.tolist())
                # ap_time = self.time_operation(ap.add, ap_arr1, ap_arr2)
                # print(f"ArrPy addition: {ap_time:.6f} seconds")
                # print(f"Ratio (ArrPy/NumPy): {ap_time/np_time:.2f}x")
                pass
    
    def benchmark_indexing(self):
        """Benchmark indexing operations."""
        print("\n=== Indexing Benchmarks ===")
        sizes = [(10000,), (1000, 1000)]
        
        for size in sizes:
            print(f"\nSize: {size}")
            
            # Create test array
            np_arr = np.arange(np.prod(size)).reshape(size)
            
            # NumPy indexing
            def np_index():
                return np_arr[size[0]//2] if len(size) == 1 else np_arr[size[0]//2, size[1]//2]
            
            np_time = self.time_operation(np_index, iterations=10000)
            print(f"NumPy indexing: {np_time:.6f} seconds")
            
            if ARRPY_AVAILABLE:
                # ArrPy indexing
                # ap_arr = ap.array(np_arr.tolist())
                # def ap_index():
                #     return ap_arr[size[0]//2] if len(size) == 1 else ap_arr[size[0]//2, size[1]//2]
                # ap_time = self.time_operation(ap_index, iterations=10000)
                # print(f"ArrPy indexing: {ap_time:.6f} seconds")
                # print(f"Ratio (ArrPy/NumPy): {ap_time/np_time:.2f}x")
                pass
    
    def run_all(self):
        """Run all benchmarks."""
        print("=" * 60)
        print("ArrPy Performance Benchmarks")
        print("=" * 60)
        
        self.benchmark_creation()
        self.benchmark_operations()
        self.benchmark_indexing()
        
        print("\n" + "=" * 60)
        print("Benchmark Complete")
        print("=" * 60)
        
        if not ARRPY_AVAILABLE:
            print("\nNote: ArrPy benchmarks will run once implementation is complete")


def main():
    """Main entry point for benchmark runner."""
    parser = argparse.ArgumentParser(description="Run ArrPy benchmarks")
    parser.add_argument(
        "--compare-numpy",
        action="store_true",
        help="Compare with NumPy performance"
    )
    parser.add_argument(
        "--category",
        choices=["creation", "operations", "indexing", "all"],
        default="all",
        help="Benchmark category to run"
    )
    
    args = parser.parse_args()
    
    runner = BenchmarkRunner(compare_numpy=args.compare_numpy)
    
    if args.category == "all":
        runner.run_all()
    elif args.category == "creation":
        runner.benchmark_creation()
    elif args.category == "operations":
        runner.benchmark_operations()
    elif args.category == "indexing":
        runner.benchmark_indexing()


if __name__ == "__main__":
    main()