# ArrPy Documentation

## Quick Start

ArrPy is an educational NumPy recreation with three backends (Python, Cython, C++) to demonstrate optimization techniques.

```python
import arrpy

# Create arrays
a = arrpy.array([1, 2, 3, 4])
b = arrpy.ones(4)

# Basic operations
c = a + b
d = arrpy.sum(a)

# Switch backends for performance comparison
arrpy.set_backend('cython')  # Use optimized backend
e = arrpy.matmul(a.reshape(2, 2), b.reshape(2, 2))
```

## Key Documentation

- [API Reference](API_REFERENCE.md) - Complete API documentation
- [Backend Guide](BACKEND_GUIDE.md) - Understanding the three-backend system
- [Performance](PERFORMANCE.md) - Benchmark results and analysis

## Current Status

- **Python Backend**: ~95% complete - Most NumPy operations implemented
- **Cython Backend**: ~10% complete - Key operations optimized (add, multiply, matmul, sum, sqrt)
- **C++ Backend**: ~5% complete - Only matmul implemented with SIMD
- **Test Coverage**: 180 tests passing, 31 skipped (unimplemented features)

## Not Implemented

- 2D/multi-dimensional indexing (use fancy indexing instead)
- Boolean array indexing (array.array storage limitation)
- File I/O operations
- Advanced linear algebra (QR, SVD, eigenvalues)