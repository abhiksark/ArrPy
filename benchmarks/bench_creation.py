"""
Benchmarks for array creation operations.
"""

import time
import numpy as np

try:
    import arrpy as ap
    ARRPY_AVAILABLE = True
except ImportError:
    ARRPY_AVAILABLE = False


def benchmark_zeros():
    """Benchmark zeros creation for various sizes."""
    sizes = [
        (10,),
        (100,),
        (1000,),
        (100, 100),
        (1000, 1000),
        (100, 100, 100),
    ]
    
    results = {}
    
    for size in sizes:
        # NumPy benchmark
        start = time.perf_counter()
        np_arr = np.zeros(size)
        np_time = time.perf_counter() - start
        
        results[f"zeros_{size}"] = {
            "numpy": np_time,
        }
        
        if ARRPY_AVAILABLE:
            # ArrPy benchmark
            start = time.perf_counter()
            ap_arr = ap.zeros(size)
            ap_time = time.perf_counter() - start
            
            results[f"zeros_{size}"]["arrpy"] = ap_time
            results[f"zeros_{size}"]["ratio"] = ap_time / np_time
    
    return results


def benchmark_ones():
    """Benchmark ones creation for various sizes."""
    sizes = [
        (10,),
        (100,),
        (1000,),
        (100, 100),
        (1000, 1000),
    ]
    
    results = {}
    
    for size in sizes:
        # NumPy benchmark
        start = time.perf_counter()
        np_arr = np.ones(size)
        np_time = time.perf_counter() - start
        
        results[f"ones_{size}"] = {
            "numpy": np_time,
        }
        
        if ARRPY_AVAILABLE:
            # ArrPy benchmark
            start = time.perf_counter()
            ap_arr = ap.ones(size)
            ap_time = time.perf_counter() - start
            
            results[f"ones_{size}"]["arrpy"] = ap_time
            results[f"ones_{size}"]["ratio"] = ap_time / np_time
    
    return results


def benchmark_arange():
    """Benchmark arange creation for various sizes."""
    sizes = [10, 100, 1000, 10000, 100000]
    
    results = {}
    
    for size in sizes:
        # NumPy benchmark
        start = time.perf_counter()
        np_arr = np.arange(size)
        np_time = time.perf_counter() - start
        
        results[f"arange_{size}"] = {
            "numpy": np_time,
        }
        
        if ARRPY_AVAILABLE:
            # ArrPy benchmark
            start = time.perf_counter()
            ap_arr = ap.arange(size)
            ap_time = time.perf_counter() - start
            
            results[f"arange_{size}"]["arrpy"] = ap_time
            results[f"arange_{size}"]["ratio"] = ap_time / np_time
    
    return results


if __name__ == "__main__":
    print("Array Creation Benchmarks")
    print("=" * 50)
    
    print("\nZeros Creation:")
    zeros_results = benchmark_zeros()
    for key, value in zeros_results.items():
        print(f"{key}: NumPy={value['numpy']:.6f}s", end="")
        if "arrpy" in value:
            print(f", ArrPy={value['arrpy']:.6f}s, Ratio={value['ratio']:.2f}x")
        else:
            print()
    
    print("\nOnes Creation:")
    ones_results = benchmark_ones()
    for key, value in ones_results.items():
        print(f"{key}: NumPy={value['numpy']:.6f}s", end="")
        if "arrpy" in value:
            print(f", ArrPy={value['arrpy']:.6f}s, Ratio={value['ratio']:.2f}x")
        else:
            print()
    
    print("\nArange Creation:")
    arange_results = benchmark_arange()
    for key, value in arange_results.items():
        print(f"{key}: NumPy={value['numpy']:.6f}s", end="")
        if "arrpy" in value:
            print(f", ArrPy={value['arrpy']:.6f}s, Ratio={value['ratio']:.2f}x")
        else:
            print()