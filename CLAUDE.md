# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What is ArrPy?

ArrPy is an educational recreation of NumPy that implements the same functionality three times with increasing performance optimizations. By building the same library in Pure Python, Cython, and C++, we experience firsthand the engineering journey that created modern scientific computing.

**Important Implementation Details**: 
1. ArrPy uses Python's `array.array` for efficient storage, NOT Python lists. This provides:
   - Memory-efficient storage (4-8 bytes per number vs 28+ bytes for Python objects)
   - Type homogeneity (all elements same type)
   - Direct memory access for C/Cython backends
   - Buffer protocol support for zero-copy operations

2. **Supported Data Types** (numeric only):
   - `int32`, `int64` - Integer types
   - `float32`, `float64` - Floating-point types
   - `bool_` - Boolean type
   - **Note**: String and complex types are NOT supported to keep the implementation focused on core numeric computing

## Why Build NumPy Three Times?

Every major scientific Python library followed a similar evolution:
- **NumPy** evolved from Numeric (pure Python) to its current C-powered implementation
- **Pandas** gradually moved bottlenecks to Cython for 100x+ speedups
- **Scikit-learn** strategically optimizes only critical paths

By implementing all three levels simultaneously, we can:
- See exactly why and where optimization matters
- Measure real performance differences (1x → 10x → 100x)
- Understand the complexity/performance tradeoff
- Learn when to optimize and when not to

## The Three-Stage Evolution

### Stage 1: Pure Python - Where Everyone Starts
**What it is**: NumPy's API implemented using only Python lists and basic operations.

**Why start here?**
- **Readable algorithms**: You can step through with a debugger and understand every line
- **No magic**: Every operation is explicit, no hidden optimizations
- **Quick prototyping**: Change algorithms instantly, no compilation
- **Universal compatibility**: Runs anywhere Python runs

**The reality check**:
- 100-1000x slower than C implementations
- High memory overhead (each number is a Python object)
- Limited by Python's GIL (Global Interpreter Lock)

**Perfect for**:
- Learning how array operations actually work
- Debugging complex numerical algorithms
- Small datasets where clarity > speed
- Understanding why we need optimization

**Example**:
```python
# Pure Python matrix multiply - clear but slow
def matmul_python(a, b):
    result = []
    for i in range(len(a)):
        row = []
        for j in range(len(b[0])):
            sum = 0
            for k in range(len(b)):
                sum += a[i][k] * b[k][j]
            row.append(sum)
        result.append(row)
    return result
```

### Stage 2: Cython - The Pragmatic Middle Ground
**What it is**: Python syntax compiled to C with type annotations.

**Why Cython?**
- **Incremental optimization**: Start with Python, add types where needed
- **10-50x speedups**: Dramatic improvements with minimal changes
- **Familiar syntax**: Still looks like Python
- **Selective application**: Optimize only the bottlenecks

**The power comes from**:
- Static typing removes dynamic dispatch overhead
- Direct memory access via memoryviews
- Can release GIL for true parallelism
- Compiles to efficient C code

**Perfect for**:
- Tight loops that dominate runtime
- Numerical operations on large arrays
- When you need speed but want to stay in Python ecosystem
- Gradual optimization of existing Python code

**Example**:
```cython
# Same algorithm, now 50x faster
@cython.boundscheck(False)
@cython.wraparound(False)
def matmul_cython(double[:,:] a, double[:,:] b):
    cdef int i, j, k
    cdef double sum
    cdef int n = a.shape[0], m = b.shape[1], p = a.shape[1]
    
    result = np.zeros((n, m))
    cdef double[:,:] res_view = result
    
    for i in range(n):
        for j in range(m):
            sum = 0
            for k in range(p):
                sum += a[i,k] * b[k,j]
            res_view[i,j] = sum
    return result
```

### Stage 3: C/C++ - The Performance Endgame
**What it is**: Native C++ with SIMD vectorization and cache optimization.

**Why go native?**
- **100-1000x faster** than pure Python
- **Hardware features**: Direct access to SIMD instructions (AVX, SSE)
- **Cache optimization**: Control memory layout for CPU efficiency
- **No overhead**: Bare metal performance

**The power comes from**:
- Vectorized operations (process 4-8 numbers simultaneously)
- Cache-friendly memory access patterns
- Zero interpreter overhead
- Can leverage optimized libraries (BLAS, MKL)

**Perfect for**:
- Large matrix operations
- Production systems requiring maximum performance
- Competing with MATLAB/NumPy performance
- When every microsecond counts

**Example**:
```cpp
// Tiled matrix multiply with SIMD - 100x+ faster
void matmul_c(const double* a, const double* b, double* c, int n) {
    #pragma omp parallel for
    for (int i = 0; i < n; i += TILE) {
        for (int j = 0; j < n; j += TILE) {
            for (int k = 0; k < n; k += TILE) {
                // Process tile with AVX instructions
                matmul_kernel_avx(a, b, c, i, j, k, n);
            }
        }
    }
}
```

## Our Unique Approach: All Three, Side by Side

Instead of replacing implementations, ArrPy keeps all three backends simultaneously:

```python
import arrpy

# Switch backends at runtime - same API, different performance
arrpy.set_backend('python')   # Study the algorithm
result_py = arrpy.matmul(a, b)

arrpy.set_backend('cython')   # See the optimization impact
result_cy = arrpy.matmul(a, b)  # 10-50x faster

arrpy.set_backend('c')        # Maximum performance
result_c = arrpy.matmul(a, b)   # 100-1000x faster

# All results are identical (within floating point precision)
assert np.allclose(result_py, result_cy, result_c)
```

This approach provides:
- **Direct comparison**: Benchmark the same operation across implementations
- **Learning by contrast**: See three ways to solve the same problem
- **No hidden magic**: Explicit about what's implemented where (no silent fallbacks)
- **Real-world insight**: Understand when optimization is worth the complexity

## Architecture: Simple and Explicit

### Backend Selection with Enum

```python
# arrpy/backend_selector.py
from enum import Enum

class Backend(Enum):
    PYTHON = 'python'
    CYTHON = 'cython'
    C = 'c'

# Global backend setting
_backend = Backend.PYTHON

def set_backend(backend):
    """Set the global backend"""
    global _backend
    if isinstance(backend, str):
        backend = Backend(backend)
    _backend = backend
    
def get_backend():
    """Get current backend"""
    return _backend
```

### Simple Delegation Pattern

No complex inheritance or abstract base classes - just simple if/elif:

```python
# arrpy/arrpy_backend.py
from .backend_selector import get_backend, Backend

class ArrPy:
    """Main array class that delegates to selected backend"""
    
    def __add__(self, other):
        backend = get_backend()
        
        if backend == Backend.PYTHON:
            from .backends.python.array_ops import _add_python
            result_data = _add_python(self._data, other._data, self._shape, other._shape)
        elif backend == Backend.CYTHON:
            from .backends.cython.array_ops import _add_cython
            result_data = _add_cython(self._data, other._data, self._shape, other._shape)
        elif backend == Backend.C:
            from .backends.c.array_ops import _add_c
            result_data = _add_c(self._data, other._data, self._shape, other._shape)
            
        return self._create_from_data(result_data, self._shape)
```

### NO Automatic Fallbacks

If an operation isn't implemented in a backend, it tells you explicitly:

```python
# arrpy/backends/c/array_ops.py
def _multiply_c(data1, data2, shape1, shape2):
    raise NotImplementedError(
        "multiply() not yet implemented in C backend.\n"
        "Available in: python, cython\n"
        "Switch backends or contribute the implementation!"
    )
```

This transparency helps you:
- Know exactly what's optimized
- Understand performance measurements
- See opportunities to contribute
- Learn which operations benefit most from optimization

## Directory Structure

```
arrpy/
├── arrpy_backend.py         # Main ArrPy class (delegates to backends)
├── backend_selector.py      # Backend enum and switching logic
├── backends/
│   ├── __init__.py
│   ├── python/             # Complete reference implementation
│   │   ├── __init__.py
│   │   ├── array_ops.py    # _add_python, _multiply_python, etc.
│   │   ├── ufuncs_ops.py   # _sin_python, _cos_python, _exp_python
│   │   ├── linalg_ops.py   # _matmul_python, _solve_python, _inv_python
│   │   └── reduction_ops.py # _sum_python, _mean_python, etc.
│   ├── cython/             # Selective optimizations (compiled)
│   │   ├── __init__.py
│   │   ├── array_ops.pyx   # Optimized add, multiply
│   │   ├── linalg_ops.pyx  # Optimized matmul
│   │   ├── reduction_ops.pyx # Optimized sum with parallelization
│   │   └── ufuncs_ops.pyx  # Optimized sqrt using C math lib
│   └── c/                  # Critical performance paths (stubs ready)
│       ├── __init__.py
│       ├── array_ops.py    # Stubs raising NotImplementedError
│       ├── linalg_ops.py   # matmul and dot placeholders
│       ├── reduction_ops.py # Stubs for reductions
│       └── ufuncs_ops.py   # Stubs for math functions
├── benchmarks/
│   ├── bench_core.py       # Core benchmarking infrastructure
│   ├── compare_backends.py # Backend comparison tool
│   └── bench_vs_numpy.py   # Compare with NumPy
├── ufuncs.py               # Universal functions interface
├── linalg.py               # Linear algebra interface
├── broadcasting.py         # Broadcasting logic
└── [other core modules]
```

## Current Implementation Status

See exactly what's been optimized and what hasn't:

| Operation | Python | Cython | C/C++ | Notes |
|-----------|---------|---------|--------|-------|
| **Basic Operations** |
| add | ✅ | ✅ | ✅ | Cython: ~10x faster, C: ~50x |
| multiply | ✅ | ✅ | ✅ | Cython: ~15x faster |
| subtract | ✅ | ✅ | ✅ | All backends implemented |
| divide | ✅ | ✅ | ✅ | All backends implemented |
| **Linear Algebra** |
| matmul (@) | ✅ | ✅ | ✅ | C: ~100x faster, @ operator works |
| dot | ✅ | ❌ | ✅ | C uses optimized routines |
| solve | ✅ | ❌ | ❌ | |
| transpose | ✅ | ❌ | ✅ | |
| **Universal Functions** |
| sin/cos | ✅ | ✅ | ❌ | |
| exp/log | ✅ | ❌ | ❌ | |
| sqrt | ✅ | ✅ | ❌ | Cython: ~8x faster |
| **Reductions** |
| sum | ✅ | ✅ | ❌ | Cython: ~20x faster (parallel) |
| mean | ✅ | ✅ | ❌ | Cython uses memoryviews |
| min/max | ✅ | ❌ | ✅ | |
| **Indexing & Slicing** |
| Basic indexing | ✅ | ✅ | ✅ | a[0], a[1,2] fully working |
| Slicing | ✅ | ✅ | ✅ | a[1:4], a[::2] working |
| Boolean indexing | ✅ | ✅ | ✅ | a[a > 2] working |
| Fancy indexing | ✅ | ✅ | ✅ | a[[0,2,4]] working |

## Benchmarking: Measure Everything

### Quick Performance Check

```bash
# Compare all three backends for common operations
make bench-compare

# Output:
# Matrix Multiply (1000x1000)
# Python:  2.341s
# Cython:  0.187s  (12.5x faster)
# C:       0.023s  (101.8x faster)
```

### Comprehensive Benchmark Suite

```makefile
# Core benchmarking
make bench              # Run all benchmarks
make bench-ops          # Benchmark basic operations
make bench-linalg       # Benchmark linear algebra
make bench-ufuncs       # Benchmark universal functions

# Backend-specific
make bench-python       # Benchmark Python backend only
make bench-cython       # Benchmark Cython backend only
make bench-c           # Benchmark C backend only

# Analysis
make bench-vs-numpy     # Compare with NumPy
make bench-report       # Generate HTML report
make profile-matmul     # Detailed profiling of matrix multiply
make memory-profile     # Memory usage analysis
```

### Performance Expectations

| Operation | Python | Cython | C/C++ | NumPy |
|-----------|--------|--------|-------|-------|
| Element-wise add | 1.0x | 5-15x | 50-100x | 50-100x |
| Matrix multiply | 1.0x | 10-50x | 100-1000x | 100-1000x |
| Broadcasting | 1.0x | 3-8x | 20-50x | 20-50x |
| Reductions | 1.0x | 8-20x | 30-80x | 30-80x |

## Development Roadmap

### Phase 1: Complete NumPy API (Current)
- Implement full NumPy-like API in pure Python
- Focus on correctness and clarity
- Comprehensive test coverage

### Phase 2: Backend System Introduction
- Refactor to pluggable backend architecture
- Move implementations to `backends/python/`
- Add backend switching infrastructure

### Phase 3: Strategic Cython Optimizations
- Profile to identify bottlenecks
- Add Cython implementations for hot paths
- Document performance improvements

### Phase 4: Critical C/C++ Implementations
- Implement performance-critical operations (matmul, BLAS)
- Add SIMD optimizations
- Complete performance comparison suite

## Contributing: Add Your Own Optimizations

### How to Add a Backend Implementation

1. **Choose a function to optimize**
   ```bash
   # Check what's not yet optimized
   python -c "import arrpy; arrpy.show_backend_status()"
   ```

2. **Profile to confirm it's a bottleneck**
   ```bash
   make profile
   ```

3. **Implement your optimization**
   ```python
   # backends/cython/array_ops.pyx
   @cython.boundscheck(False)
   def _add_cython(double[:] a, double[:] b):
       # Your optimized implementation
   ```

4. **Verify correctness**
   ```python
   # Test against Python reference
   def test_add_consistency():
       for backend in ['python', 'cython']:
           arrpy.set_backend(backend)
           result = arrpy.add(a, b)
           assert np.allclose(result, expected)
   ```

5. **Benchmark the improvement**
   ```bash
   make bench-ops
   # Should show: Cython 5-15x faster than Python
   ```

6. **Update the implementation matrix** in this file

## Learning Objectives

### From the Python Backend
- How N-dimensional arrays map to linear memory
- Broadcasting algorithms and their complexity
- Why Python is slow (object overhead, dynamic dispatch)
- The elegance of NumPy's API design

### From the Cython Backend
- Impact of static typing on performance
- Memory views vs Python objects
- When parallelization helps (and when it doesn't)
- The 80/20 rule of optimization

### From the C/C++ Backend
- Modern CPU architecture (caches, SIMD)
- Memory alignment and access patterns
- The complexity cost of maximum performance
- When to reach for low-level optimization

## Testing Strategy

### Ensure All Backends Agree

```python
# tests/test_backend_consistency.py
def test_all_operations_consistent():
    """Verify all backends produce identical results"""
    
    for operation in ['add', 'multiply', 'matmul']:
        results = {}
        
        for backend in ['python', 'cython', 'c']:
            try:
                arrpy.set_backend(backend)
                results[backend] = run_operation(operation)
            except NotImplementedError:
                pass  # Backend doesn't implement this yet
        
        # All implemented backends must agree
        assert all_close(results.values())
```

### Performance Regression Tests

```python
# tests/test_performance.py
def test_optimization_speedups():
    """Ensure optimizations actually improve performance"""
    
    expected_speedups = {
        'add': {'cython': 5.0, 'c': 50.0},
        'matmul': {'cython': 10.0, 'c': 100.0}
    }
    
    for op, speedups in expected_speedups.items():
        py_time = benchmark('python', op)
        
        for backend, min_speedup in speedups.items():
            other_time = benchmark(backend, op)
            actual_speedup = py_time / other_time
            
            assert actual_speedup >= min_speedup, \
                f"{backend} {op} only {actual_speedup}x faster"
```

## Development Commands

```bash
# Setup
make dev              # Install in development mode
make clean            # Clean all build artifacts

# Testing
make test             # Run all tests (unit + compatibility)
make test-compat      # Test NumPy compatibility across all backends
make test-python      # Test Python backend only
make test-cython      # Test Cython backend only
make test-c          # Test C backend only

# Building
make build-cython     # Compile Cython extensions
make build-c         # Compile C++ extensions

# Quality
make lint            # Check code style
make format          # Auto-format code
```

## Recent Improvements (2024)

### 1. **Full Indexing Support Added**
- Implemented `__getitem__` and `__setitem__` methods in ArrPy class
- Supports all NumPy-style indexing:
  - Basic: `a[0]`, `a[1,2]`, `a[-1]`
  - Slicing: `a[1:4]`, `a[::2]`, `a[::-1]`
  - Boolean: `a[a > 2]`
  - Fancy: `a[[0,2,4]]`
- Comprehensive test suite with 28 tests

### 2. **Cython Backend Consolidation**
- Merged `array_ops.pyx` and `array_ops_new.pyx`
- Now uses zero-copy memoryviews exclusively
- Better performance with `nogil` blocks for parallelism

### 3. **NumPy Compatibility Testing**
- Added `test_numpy_compat.py` with 72 tests
- Tests all backends against NumPy for identical results
- Automated compatibility verification with `make test-compat`

### 4. **Code Cleanup**
- Removed deprecated `core.py`
- Fixed import inconsistencies
- Standardized backend naming conventions
- Fixed `broadcast_data` missing function issue

## Resources and References

### Essential Reading
- **"From Python to NumPy"** - Nicolas Rougier
  - Free online book showing this exact journey
- **"High Performance Python"** - Gorelick & Ozsvald
  - Profiling and optimization techniques

### Key Papers
- **"The NumPy Array"** - Van der Walt et al.
  - NumPy's design philosophy
- **"Expression Templates"** - Todd Veldhuizen
  - C++ optimization technique used in libraries

### Source Code to Study
- **NumPy**: See how the professionals did it
- **Numba**: JIT compilation approach
- **CuPy**: GPU acceleration patterns

## Current Status

- **Python Backend**: 85% complete (core features + indexing working)
- **Cython Backend**: 40% complete (arithmetic, reductions, some ufuncs optimized)
- **C++ Backend**: 25% complete (arithmetic ops, matmul, some reductions)
- **Testing Framework**: 80% complete (unit tests + NumPy compatibility tests)
- **Benchmarking Suite**: 70% complete

### Key Features Working:
- ✅ Full NumPy-style indexing and slicing
- ✅ Broadcasting for all operations
- ✅ Matrix multiplication with @ operator
- ✅ Backend switching at runtime
- ✅ Zero-copy operations in Cython
- ✅ NumPy compatibility verified with tests

### Next Steps
1. Fix boolean array dtype handling for proper boolean indexing
2. Implement remaining ufuncs in Cython/C backends
3. Add SIMD optimizations to C backend
4. Complete advanced linear algebra functions