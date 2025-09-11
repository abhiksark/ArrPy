"""
Compare performance across all backends for ArrPy operations.
"""

import sys
import os
import argparse

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import arrpy
from arrpy.backend_selector import Backend, set_backend, show_backend_status
from bench_core import Benchmark, BenchmarkSuite


def benchmark_basic_ops(sizes=None):
    """Benchmark basic arithmetic operations."""
    sizes = sizes or [100, 500, 1000]
    suite = BenchmarkSuite("Basic Operations")
    
    # Addition
    bench = Benchmark("Addition", sizes=sizes)
    bench.run(lambda a, b: a + b)
    suite.add(bench)
    
    # Multiplication
    bench = Benchmark("Multiplication", sizes=sizes)
    bench.run(lambda a, b: a * b)
    suite.add(bench)
    
    # Subtraction
    bench = Benchmark("Subtraction", sizes=sizes)
    bench.run(lambda a, b: a - b)
    suite.add(bench)
    
    return suite


def benchmark_linalg(sizes=None):
    """Benchmark linear algebra operations."""
    sizes = sizes or [(10, 10), (50, 50), (100, 100)]
    suite = BenchmarkSuite("Linear Algebra")
    
    # Matrix multiplication
    bench = Benchmark("Matrix Multiply", sizes=sizes)
    bench.run(lambda a, b: arrpy.linalg.matmul(a, b))
    suite.add(bench)
    
    # Dot product
    bench = Benchmark("Dot Product", sizes=[100, 500])
    bench.run(lambda a, b: arrpy.linalg.dot(a, b))
    suite.add(bench)
    
    return suite


def benchmark_reductions(sizes=None):
    """Benchmark reduction operations."""
    sizes = sizes or [100, 500, 1000]
    suite = BenchmarkSuite("Reductions")
    
    # Sum
    bench = Benchmark("Sum", sizes=sizes)
    bench.run(lambda a, b: a.sum())
    suite.add(bench)
    
    # Mean
    bench = Benchmark("Mean", sizes=sizes)
    bench.run(lambda a, b: a.mean())
    suite.add(bench)
    
    return suite


def benchmark_ufuncs(sizes=None):
    """Benchmark universal functions."""
    sizes = sizes or [100, 500, 1000]
    suite = BenchmarkSuite("Universal Functions")
    
    # Square root
    bench = Benchmark("Square Root", sizes=sizes)
    bench.run(lambda a, b: arrpy.sqrt(a))
    suite.add(bench)
    
    # Sine
    bench = Benchmark("Sine", sizes=sizes)
    bench.run(lambda a, b: arrpy.sin(a))
    suite.add(bench)
    
    return suite


def main():
    """Main benchmark runner."""
    parser = argparse.ArgumentParser(description="Compare ArrPy backend performance")
    parser.add_argument('--all', action='store_true', help='Run all benchmarks')
    parser.add_argument('--basic', action='store_true', help='Run basic operation benchmarks')
    parser.add_argument('--linalg', action='store_true', help='Run linear algebra benchmarks')
    parser.add_argument('--reductions', action='store_true', help='Run reduction benchmarks')
    parser.add_argument('--ufuncs', action='store_true', help='Run ufunc benchmarks')
    parser.add_argument('--sizes', type=str, help='Comma-separated sizes to test')
    parser.add_argument('--status', action='store_true', help='Show backend implementation status')
    
    args = parser.parse_args()
    
    # Show status if requested
    if args.status:
        show_backend_status()
        return
    
    # Parse sizes if provided
    sizes = None
    if args.sizes:
        sizes = [int(s) for s in args.sizes.split(',')]
    
    # Determine which benchmarks to run
    run_all = args.all or not any([args.basic, args.linalg, args.reductions, args.ufuncs])
    
    print("=" * 70)
    print("ArrPy Backend Performance Comparison")
    print("=" * 70)
    
    # Show current backend status
    print("\nBackend Implementation Status:")
    print("-" * 40)
    from arrpy.backend_selector import get_backend_capabilities
    for backend in Backend:
        caps = get_backend_capabilities(backend)
        implemented = sum(1 for v in caps.values() if v)
        print(f"{backend.value}: {implemented} operations implemented")
    
    # Run benchmarks
    all_suites = []
    
    if run_all or args.basic:
        suite = benchmark_basic_ops(sizes)
        all_suites.append(suite)
        for bench in suite.benchmarks:
            bench.report()
    
    if run_all or args.linalg:
        suite = benchmark_linalg(sizes if sizes else None)
        all_suites.append(suite)
        for bench in suite.benchmarks:
            bench.report()
    
    if run_all or args.reductions:
        suite = benchmark_reductions(sizes)
        all_suites.append(suite)
        for bench in suite.benchmarks:
            bench.report()
    
    if run_all or args.ufuncs:
        suite = benchmark_ufuncs(sizes)
        all_suites.append(suite)
        for bench in suite.benchmarks:
            bench.report()
    
    # Print overall summary
    if all_suites:
        print("\n" + "=" * 70)
        print("OVERALL SUMMARY")
        print("=" * 70)
        
        for suite in all_suites:
            suite.summary()


if __name__ == "__main__":
    main()