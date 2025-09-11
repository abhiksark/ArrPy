# ArrPy Experimental Features

## Overview

The experimental folder contains prototype implementations and optimization experiments that explore different approaches to array operations. These are **not used in production** but serve as educational examples and testing grounds for future optimizations.

## Why Experimental Code?

1. **Performance Exploration**: Test different optimization techniques without affecting stable code
2. **Educational Value**: Show multiple ways to solve the same problem
3. **Future Features**: Prototype new capabilities before integration
4. **Benchmarking**: Compare different implementation strategies

## Available Experimental Features

### 1. Type-Specific Operations (`typed_ops`)
**Status**: ✅ Compiled and Available

Provides type-specific optimized operations using Cython memoryviews:
- Float64: `_add_float64`, `_multiply_float64`, `_subtract_float64`, `_divide_float64`
- Float32: `_add_float32`, `_multiply_float32`
- Int64: `_add_int64`, `_multiply_int64`
- Int32: `_add_int32`

```python
from arrpy.backends.cython.experimental import typed_ops
import numpy as np

# Create numpy arrays
a = np.array([1.0, 2.0, 3.0])
b = np.array([4.0, 5.0, 6.0])

# Use typed operations with memoryviews
result = typed_ops._add_float64(memoryview(a), memoryview(b))
```

### 2. Memory Pool (`memory_pool.pyx`)
**Status**: 🔧 Requires Compilation

Pre-allocates memory blocks to reduce allocation overhead:
- Thread-safe memory pool with configurable size
- Reuses memory blocks for array operations
- Statistics tracking (hit rate, allocation count)

### 3. Alternative Storage Backends
**Status**: ✅ Available as Standalone Tests

Explores different array storage approaches:
- **array.array**: Python's built-in efficient array (4-8 bytes per element)
- **ctypes**: Direct C-compatible arrays
- **mmap**: Memory-mapped arrays for large data
- **DLPack**: Framework interoperability standard

### 4. Optimized Operations
**Status**: 🔧 Requires Compilation

- `array_ops_optimized.pyx`: Optimized array operations without numpy overhead
- `reduction_ops_optimized.pyx`: Parallel reductions with OpenMP
- `linalg_optimized.pyx`: Cache-optimized linear algebra
- `array_ops_pooled.pyx`: Operations using memory pool

### 5. C++ Experimental
**Status**: 🔧 Requires Separate Build

- `array_ops_optimized.cpp`: SIMD-optimized operations
- `array_ops_fast.py`: Python bindings for fast C++ ops

## Running Experimental Code

### Quick Test (What's Available Now)
```bash
# Run the experimental demo
python run_experimental.py

# Test alternative storage approaches
python tests/experimental/test_array_alternatives.py

# Test DLPack prototype
python tests/experimental/test_dlpack_prototype.py

# Test hybrid array backends
python tests/experimental/hybrid_array_prototype.py
```

### Compile Additional Experimental Modules
To compile all experimental Cython modules, add them to `setup.py`:

```python
# In setup.py, add to ext_modules list:
Extension(
    "arrpy.backends.cython.experimental.memory_pool",
    ["arrpy/backends/cython/experimental/memory_pool.pyx"],
    include_dirs=[np.get_include()],
),
# ... add other experimental modules
```

Then compile:
```bash
python setup.py build_ext --inplace
```

## Performance Results

### Type-Specific Operations (10,000 elements)
- add_float64: 0.003 ms
- multiply_float64: 0.003 ms
- subtract_float64: 0.003 ms
- divide_float64: 0.005 ms

### Alternative Storage (100,000 elements)
| Backend | Create(ms) | Access(ms) | Modify(ms) | C-Compatible |
|---------|------------|------------|------------|--------------|
| Python list | 6.796 | 0.079 | 0.097 | No |
| array.array | 8.034 | 0.076 | 0.012 | Yes |
| ctypes | 10.913 | 0.070 | 0.009 | Yes |
| numpy | 8.412 | 0.100 | 0.011 | Yes |

## Educational Value

The experimental code demonstrates:

1. **Memory Management**
   - Memory pooling to reduce allocation overhead
   - Different storage backends with trade-offs
   - Zero-copy operations with memoryviews

2. **Type Specialization**
   - Type-specific implementations for better performance
   - Avoiding Python's dynamic dispatch overhead
   - Template-like programming in Cython

3. **Parallelization**
   - OpenMP pragmas for parallel loops
   - Thread-safe memory pools
   - Parallel reductions

4. **Framework Interoperability**
   - DLPack for tensor exchange between frameworks
   - Buffer protocol for zero-copy sharing
   - C-compatible memory layouts

5. **SIMD Optimization**
   - Vectorized operations in C++
   - Cache-friendly algorithms
   - Platform-specific optimizations

## Why Not in Production?

1. **Complexity**: Adds significant complexity for marginal gains
2. **Maintenance**: More code paths to test and maintain
3. **Portability**: Some optimizations are platform-specific
4. **Educational Focus**: ArrPy prioritizes clarity over maximum performance
5. **Incomplete**: Many experimental features are partially implemented

## Future Integration

Successful experiments could be integrated into the main codebase:
- Memory pooling could reduce allocation overhead in Cython backend
- Type-specific operations could be used via dtype dispatching
- DLPack support would enable framework interoperability

## Contributing

To add experimental features:
1. Create new module in `arrpy/backends/*/experimental/`
2. Add standalone test in `tests/experimental/`
3. Document approach and results
4. Compare with existing implementations
5. Share findings via PR or issue

The experimental folder is perfect for:
- Testing optimization hypotheses
- Learning new techniques
- Prototyping features
- Performance experiments
- Educational demonstrations