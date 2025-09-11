# Backend Guide

ArrPy implements the same operations three times to demonstrate optimization techniques.

## Python Backend (Default)

Pure Python implementation using Python's `array.array` for storage.

**Characteristics:**
- Clear, readable code
- No compilation required
- 100-1000x slower than optimized code
- Perfect for learning algorithms

**Example:**
```python
# backends/python/array_ops.py
def _add_python(data1, data2, shape1, shape2):
    result = []
    for i in range(len(data1)):
        result.append(data1[i] + data2[i])
    return result
```

## Cython Backend

Python code with type annotations compiled to C.

**Characteristics:**
- 10-50x faster than pure Python
- Still readable Python syntax
- Requires compilation (`make build-cython`)
- Good balance of performance and maintainability

**Example:**
```cython
# backends/cython/array_ops.pyx
@cython.boundscheck(False)
def _add_cython(double[:] a, double[:] b):
    cdef int i, n = a.shape[0]
    cdef double[:] result = np.zeros(n)
    
    for i in range(n):
        result[i] = a[i] + b[i]
    return result
```

**Currently Optimized:**
- Basic operations: add, multiply
- Linear algebra: matmul
- Reductions: sum
- Math: sqrt

## C++ Backend

Native C++ with SIMD vectorization.

**Characteristics:**
- 100-1000x faster than Python
- Uses AVX2/SSE for vectorization
- Complex but maximum performance
- Requires C++ compiler

**Currently Implemented:**
- matmul only (with AVX2 optimization)

**Example:**
```cpp
// backends/c/matmul_ops.cpp
void matmul_avx(const double* a, const double* b, double* c, int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j += 4) {
            __m256d sum = _mm256_setzero_pd();
            for (int k = 0; k < n; k++) {
                __m256d va = _mm256_broadcast_sd(&a[i*n + k]);
                __m256d vb = _mm256_loadu_pd(&b[k*n + j]);
                sum = _mm256_fmadd_pd(va, vb, sum);
            }
            _mm256_storeu_pd(&c[i*n + j], sum);
        }
    }
}
```

## Switching Backends

```python
import arrpy

# Default is Python
a = arrpy.array([1, 2, 3])

# Switch to Cython for better performance
arrpy.set_backend('cython')
b = arrpy.matmul(a, a)  # Uses optimized Cython

# Switch to C++ for maximum performance
arrpy.set_backend('c')
c = arrpy.matmul(a, a)  # Uses SIMD-optimized C++

# Check current backend
print(arrpy.get_backend())  # Backend.C
```

## Performance Comparison

| Operation | Python | Cython | C++ |
|-----------|--------|--------|-----|
| add (1M elements) | 1.0x | 10-15x | Not implemented |
| multiply (1M elements) | 1.0x | 10-15x | Not implemented |
| matmul (500×500) | 1.0x | 10-20x | 100-200x |
| sum (1M elements) | 1.0x | 15-20x | Not implemented |

## Building Backends

```bash
# Build Cython extensions
make build-cython

# Build C++ extensions (if available)
make build-c

# Clean and rebuild
make clean
make build
```