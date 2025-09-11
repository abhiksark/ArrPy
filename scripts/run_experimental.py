#!/usr/bin/env python3
"""
Run and demonstrate experimental features in ArrPy.
This script compiles and tests various experimental optimizations.
"""

import os
import sys
import subprocess
import time

def compile_experimental_cython():
    """Compile experimental Cython modules."""
    print("=" * 60)
    print("Compiling Experimental Cython Modules")
    print("=" * 60)
    
    cython_modules = [
        "arrpy/backends/cython/experimental/array_ops_optimized.pyx",
        "arrpy/backends/cython/experimental/memory_pool.pyx",
        "arrpy/backends/cython/experimental/array_ops_pooled.pyx",
        "arrpy/backends/cython/experimental/reduction_ops_optimized.pyx",
        "arrpy/backends/cython/experimental/linalg_optimized.pyx",
    ]
    
    for module in cython_modules:
        if os.path.exists(module):
            print(f"\n📦 Compiling {os.path.basename(module)}...")
            try:
                # Compile with cythonize
                cmd = [sys.executable, "-m", "cython", "-3", module]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"   ✅ Cython compilation successful")
                else:
                    print(f"   ❌ Cython compilation failed: {result.stderr}")
            except Exception as e:
                print(f"   ❌ Error: {e}")

def test_typed_ops():
    """Test type-specific optimized operations."""
    print("\n" + "=" * 60)
    print("Testing Type-Specific Operations (typed_ops)")
    print("=" * 60)
    
    try:
        from arrpy.backends.cython.experimental import typed_ops
        import numpy as np
        
        # Test data
        size = 10000
        arr1 = np.random.randn(size)
        arr2 = np.random.randn(size)
        
        # Create memoryviews
        data1 = memoryview(arr1)
        data2 = memoryview(arr2)
        
        # Benchmark typed operations
        operations = [
            ('add_float64', typed_ops._add_float64),
            ('multiply_float64', typed_ops._multiply_float64),
            ('subtract_float64', typed_ops._subtract_float64),
            ('divide_float64', typed_ops._divide_float64),
        ]
        
        print(f"\n📊 Array size: {size:,} elements")
        print("-" * 40)
        
        for name, func in operations:
            try:
                # Warmup
                func(data1, data2)
                
                # Benchmark
                start = time.perf_counter()
                for _ in range(100):
                    result = func(data1, data2)
                elapsed = (time.perf_counter() - start) / 100 * 1000
                
                print(f"{name:20} {elapsed:8.3f} ms")
            except Exception as e:
                print(f"{name:20} Not available: {e}")
        
        print("\n✅ Type-specific operations working!")
        
    except ImportError as e:
        print(f"❌ Could not import typed_ops: {e}")

def test_memory_pool():
    """Test memory pool functionality."""
    print("\n" + "=" * 60)
    print("Testing Memory Pool")
    print("=" * 60)
    
    try:
        from arrpy.backends.cython.experimental.memory_pool import get_pool_stats, reset_pool
        
        # Get initial stats
        stats = get_pool_stats()
        print("\nMemory Pool Statistics:")
        print(f"  Total blocks: {stats['total_blocks']}")
        print(f"  Blocks in use: {stats['blocks_in_use']}")
        print(f"  Total allocated: {stats['total_allocated_mb']:.2f} MB")
        print(f"  Hit rate: {stats['hit_rate']:.1%}")
        
        print("\n✅ Memory pool available!")
        
    except ImportError:
        print("❌ Memory pool not compiled. To compile:")
        print("   python setup.py build_ext --inplace")

def test_alternative_backends():
    """Test alternative array storage backends."""
    print("\n" + "=" * 60)
    print("Testing Alternative Storage Backends")
    print("=" * 60)
    
    # Run array alternatives test
    test_file = "tests/experimental/test_array_alternatives.py"
    if os.path.exists(test_file):
        print("\n🔍 Running array alternatives benchmark...")
        subprocess.run([sys.executable, test_file])
    else:
        print(f"❌ Test file not found: {test_file}")

def test_dlpack():
    """Test DLPack prototype."""
    print("\n" + "=" * 60)
    print("Testing DLPack Integration")
    print("=" * 60)
    
    test_file = "tests/experimental/test_dlpack_prototype.py"
    if os.path.exists(test_file):
        print("\n🔗 Testing DLPack array implementation...")
        # Just run a quick test
        try:
            exec(open(test_file).read())
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"❌ Test file not found: {test_file}")

def show_experimental_usage():
    """Show how to use experimental features."""
    print("\n" + "=" * 60)
    print("How to Use Experimental Features")
    print("=" * 60)
    
    print("""
1. **Type-Specific Operations (Currently Available)**
   ```python
   from arrpy.backends.cython.experimental import typed_ops
   
   # Use optimized float64 operations
   result, shape = typed_ops._add_float64(data1, data2, shape1, shape2)
   ```

2. **Memory Pool (Requires Compilation)**
   ```python
   from arrpy.backends.cython.experimental.memory_pool import (
       get_global_pool, get_pool_stats, reset_pool
   )
   
   # Use pooled arrays for reduced allocation overhead
   pool = get_global_pool()
   stats = get_pool_stats()
   ```

3. **Alternative Storage Backends**
   - array.array: Memory efficient, C-compatible
   - ctypes: Direct C integration
   - mmap: Memory-mapped arrays for large data
   - DLPack: Framework interoperability

4. **To Compile All Experimental Modules:**
   ```bash
   # Add to setup.py and run:
   python setup.py build_ext --inplace
   ```

5. **Running Experimental Tests:**
   ```bash
   # Test alternative storage approaches
   python tests/experimental/test_array_alternatives.py
   
   # Test DLPack prototype
   python tests/experimental/test_dlpack_prototype.py
   
   # Test hybrid array backends
   python tests/experimental/hybrid_array_prototype.py
   ```
""")

def main():
    """Run all experimental demonstrations."""
    print("🧪 ArrPy Experimental Features Demo")
    print("=" * 60)
    
    # Test what's currently available
    test_typed_ops()
    test_memory_pool()
    
    # Show usage instructions
    show_experimental_usage()
    
    print("\n" + "=" * 60)
    print("💡 Experimental Features Summary")
    print("=" * 60)
    print("""
✅ Available Now:
- Type-specific Cython operations (typed_ops)
- Alternative storage benchmarks
- DLPack prototype
- Hybrid array prototype

🔧 Requires Compilation:
- Memory pool
- Optimized array operations
- Optimized reductions
- Optimized linear algebra

📚 Educational Value:
- Shows different optimization approaches
- Demonstrates memory management techniques
- Explores framework interoperability
- Tests performance boundaries
""")

if __name__ == "__main__":
    main()