"""
Core benchmarking infrastructure for ArrPy.

Provides tools to benchmark operations across different backends.
"""

import time
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import arrpy
from arrpy.backend_selector import Backend, set_backend, get_backend


class Benchmark:
    """
    Benchmark runner for comparing backend performance.
    
    Examples
    --------
    >>> bench = Benchmark("Matrix Multiply", sizes=[10, 100, 1000])
    >>> bench.run(lambda a, b: a @ b)
    >>> bench.report()
    """
    
    def __init__(self, name, sizes=None):
        """
        Initialize benchmark.
        
        Parameters
        ----------
        name : str
            Name of the benchmark
        sizes : list, optional
            Array sizes to test
        """
        self.name = name
        # Use reasonable sizes to avoid timeouts
        self.sizes = sizes or [100, 500]
        self.results = {}
        
    def run(self, operation, backends=None, warmup=5, iterations=10):
        """
        Run benchmark across specified backends.
        
        Parameters
        ----------
        operation : callable
            Function to benchmark (takes two arrays)
        backends : list of Backend, optional
            Backends to test. If None, tests all.
        warmup : int
            Number of warmup iterations
        iterations : int
            Number of timed iterations
        """
        if backends is None:
            backends = list(Backend)
        
        for backend in backends:
            print(f"\nBenchmarking {backend.value} backend...")
            self.results[backend] = []
            
            for size in self.sizes:
                try:
                    # Set backend
                    set_backend(backend)
                    
                    # Create test arrays
                    if isinstance(size, tuple):
                        shape = size
                    else:
                        shape = (size, size) if self._needs_2d(operation) else (size,)
                    
                    a = arrpy.ones(shape)
                    b = arrpy.ones(shape)
                    
                    # Warmup
                    for _ in range(warmup):
                        _ = operation(a, b)
                    
                    # Benchmark
                    start = time.perf_counter()
                    for _ in range(iterations):
                        _ = operation(a, b)
                    elapsed = time.perf_counter() - start
                    
                    avg_time = elapsed / iterations
                    self.results[backend].append(avg_time)
                    print(f"  Size {size}: {avg_time:.6f}s")
                    
                except NotImplementedError as e:
                    print(f"  Size {size}: Not implemented - {str(e).split('.')[0]}")
                    self.results[backend].append(None)
                except Exception as e:
                    print(f"  Size {size}: Error - {e}")
                    self.results[backend].append(None)
    
    def _needs_2d(self, operation):
        """Check if operation needs 2D arrays (like matmul)."""
        # Simple heuristic - could be improved
        return 'matmul' in str(operation) or '@' in str(operation)
    
    def report(self):
        """Generate and print performance report."""
        print(f"\n{'='*70}")
        print(f"{self.name} Benchmark Results")
        print(f"{'='*70}")
        
        # Header
        header = f"{'Size':<12}"
        for backend in Backend:
            header += f"{backend.value:^15}"
        header += "Speedup"
        print(header)
        print("-" * 70)
        
        # Results for each size
        for i, size in enumerate(self.sizes):
            row = f"{str(size):<12}"
            py_time = None
            
            for backend in Backend:
                if backend in self.results:
                    time_val = self.results[backend][i] if i < len(self.results[backend]) else None
                else:
                    time_val = None
                
                if time_val is not None:
                    row += f"{time_val:^15.6f}"
                    if backend == Backend.PYTHON:
                        py_time = time_val
                else:
                    row += f"{'N/A':^15}"
            
            # Calculate speedup vs Python
            speedups = []
            if py_time:
                for backend in [Backend.CYTHON, Backend.C]:
                    if backend in self.results and i < len(self.results[backend]):
                        other_time = self.results[backend][i]
                        if other_time:
                            speedup = py_time / other_time
                            speedups.append(f"{backend.value[0].upper()}: {speedup:.1f}x")
            
            if speedups:
                row += "  " + ", ".join(speedups)
            
            print(row)
        
        print("=" * 70)
    
    def to_dict(self):
        """Export results as dictionary."""
        return {
            'name': self.name,
            'sizes': self.sizes,
            'results': {
                backend.value: times 
                for backend, times in self.results.items()
            }
        }


class BenchmarkSuite:
    """
    Collection of benchmarks to run together.
    """
    
    def __init__(self, name="ArrPy Benchmark Suite"):
        self.name = name
        self.benchmarks = []
    
    def add(self, benchmark):
        """Add a benchmark to the suite."""
        self.benchmarks.append(benchmark)
    
    def run_all(self, backends=None):
        """Run all benchmarks."""
        print(f"\n{'#'*70}")
        print(f"# {self.name}")
        print(f"{'#'*70}")
        
        for bench in self.benchmarks:
            bench.run(backends=backends)
            bench.report()
    
    def summary(self):
        """Print summary of all benchmark results."""
        print(f"\n{'='*70}")
        print("SUMMARY")
        print(f"{'='*70}")
        
        for bench in self.benchmarks:
            print(f"\n{bench.name}:")
            
            # Calculate average speedups
            speedups = {'cython': [], 'c': []}
            
            for i, size in enumerate(bench.sizes):
                if Backend.PYTHON in bench.results:
                    py_time = bench.results[Backend.PYTHON][i]
                    
                    if py_time:
                        for backend in [Backend.CYTHON, Backend.C]:
                            if backend in bench.results:
                                other_time = bench.results[backend][i]
                                if other_time:
                                    speedup = py_time / other_time
                                    speedups[backend.value].append(speedup)
            
            for backend, values in speedups.items():
                if values:
                    avg_speedup = sum(values) / len(values)
                    print(f"  {backend}: Average {avg_speedup:.1f}x speedup")


def compare_backends_quick():
    """Quick comparison of backends for common operations."""
    suite = BenchmarkSuite("Quick Backend Comparison")
    
    # Basic operations
    add_bench = Benchmark("Addition", sizes=[100, 1000])
    add_bench.run(lambda a, b: a + b, warmup=2, iterations=5)
    suite.add(add_bench)
    
    # Matrix multiplication
    matmul_bench = Benchmark("Matrix Multiply", sizes=[(10, 10), (100, 100)])
    matmul_bench.run(lambda a, b: arrpy.linalg.matmul(a, b), warmup=2, iterations=5)
    suite.add(matmul_bench)
    
    # Show results
    for bench in suite.benchmarks:
        bench.report()
    
    suite.summary()


if __name__ == "__main__":
    compare_backends_quick()