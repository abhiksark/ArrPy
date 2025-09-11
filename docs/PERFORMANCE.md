# Performance Analysis

## Benchmark Results

### Element-wise Operations (1M elements)

| Operation | Python | Cython | Speedup |
|-----------|--------|--------|---------|
| Addition | 245ms | 19ms | 12.9x |
| Multiplication | 312ms | 21ms | 14.9x |
| Square root | 487ms | 61ms | 8.0x |

### Matrix Operations

| Operation | Size | Python | Cython | C++ | Best Speedup |
|-----------|------|--------|--------|-----|--------------|
| Matrix Multiply | 100×100 | 45ms | 8ms | 0.5ms | 90x |
| Matrix Multiply | 500×500 | 1824ms | 156ms | 8.3ms | 220x |
| Dot Product | 1M elements | 189ms | 15ms | - | 12.6x |

### Reductions

| Operation | Size | Python | Cython | Speedup |
|-----------|------|--------|--------|---------|
| Sum | 1M elements | 187ms | 12ms | 15.6x |
| Mean | 1M elements | 201ms | - | - |
| Min/Max | 1M elements | 176ms | - | - |

## Memory Usage

ArrPy uses Python's `array.array` for efficient storage:

| Type | Python list | array.array | Savings |
|------|------------|-------------|---------|
| float64 | 28 bytes/element | 8 bytes | 71% |
| int64 | 28 bytes/element | 8 bytes | 71% |
| float32 | 28 bytes/element | 4 bytes | 86% |

## Running Benchmarks

```bash
# Run all benchmarks
make bench

# Compare backends
make bench-compare

# Specific operation benchmarks
python benchmarks/bench_core.py --operation matmul
python benchmarks/bench_core.py --size 1000000

# Compare with NumPy
python benchmarks/bench_vs_numpy.py
```

## Optimization Techniques Used

### Python Backend
- Uses `array.array` for efficient storage
- List comprehensions where possible
- Minimal function call overhead

### Cython Backend
- Static typing with `cdef`
- Memory views for direct array access
- Disabled bounds checking with `@cython.boundscheck(False)`
- Disabled wraparound with `@cython.wraparound(False)`

### C++ Backend (matmul only)
- AVX2 SIMD instructions (4 doubles at once)
- Cache-friendly tiling
- Loop unrolling
- Aligned memory access

## Performance Tips

1. **Use Cython backend for production** - 10-50x faster for most operations
2. **Batch operations** - Minimize Python/C boundary crossings
3. **Use appropriate dtypes** - float32 is faster than float64
4. **Avoid repeated backend switching** - Has overhead

## Comparison with NumPy

ArrPy is an educational implementation and is not optimized to NumPy's level:

| Operation | ArrPy/NumPy Speed Ratio |
|-----------|------------------------|
| Element-wise ops | 5-20x slower |
| Matrix multiply | 10-100x slower |
| Reductions | 10-30x slower |
| Fancy indexing | 3-10x slower |

This is expected as NumPy uses:
- Highly optimized BLAS libraries (MKL, OpenBLAS)
- Years of optimization work
- Platform-specific optimizations
- More sophisticated algorithms

ArrPy's value is in education and transparency, not production performance.