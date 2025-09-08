# ArrPy v1.0.0 - Educational Array Computing Library

## 🎉 Production Ready Release

ArrPy is an educational recreation of NumPy built from scratch with a unique **pluggable backend system** that allows you to switch between pure Python, Cython, and C++ implementations at runtime.

## 🚀 Features

### Complete NumPy-Compatible API
- **100+ operations** implemented across all backends
- Full **broadcasting** support
- **Advanced indexing** including fancy and boolean indexing
- Complete **dtype system** with complex number support

### Three Swappable Backends
```python
import arrpy

# Switch backends at runtime!
arrpy.set_backend('python')  # Pure Python - educational clarity
arrpy.set_backend('cython')  # Cython - balanced performance
arrpy.set_backend('c')       # C++ - maximum speed with SIMD
```

### Major Feature Categories

#### Core Array Operations
- Element-wise arithmetic (+, -, *, /, //, %, **)
- Comparison operators (<, <=, >, >=, ==, !=)
- Broadcasting and shape manipulation
- Advanced indexing and slicing

#### Linear Algebra
- Matrix multiplication and dot products
- Solving linear systems (LU decomposition)
- Matrix decompositions (QR, SVD, Cholesky)
- Eigenvalues and eigenvectors
- Determinant, inverse, and matrix rank

#### Signal Processing
- Fast Fourier Transform (FFT/IFFT)
- 2D FFT for image processing
- Discrete Cosine Transform (DCT)
- Convolution using FFT

#### Statistics
- Descriptive statistics (mean, median, std, var)
- Percentiles and histograms
- Cumulative operations (cumsum, cumprod)
- Numerical differentiation (diff, gradient)

#### Universal Functions
- Trigonometric (sin, cos, tan, arcsin, arccos, arctan)
- Hyperbolic (sinh, cosh, tanh)
- Exponential and logarithmic (exp, log, log10)
- Power and roots (power, sqrt)

#### I/O Operations
- Binary format (`.apy` files)
- Text files with configurable formatting
- Compressed archives for multiple arrays (`.apz`)

## 📊 Performance

### Backend Comparison
| Operation | Python | Cython | C++ |
|-----------|--------|--------|-----|
| Arithmetic | 1x | 5-15x | 50-100x |
| Reductions | 1x | 8-20x | 30-80x |
| Linear Algebra | 1x | 10-50x | 100-1000x |
| Universal Functions | 1x | 2-5x | 10-30x |

### Optimizations
- **SIMD Vectorization**: ARM NEON and Intel AVX2/SSE2
- **Memory Pooling**: Reduced allocation overhead in Cython
- **Cache Optimization**: Blocked algorithms for matrix operations
- **OpenMP Parallelization**: Multi-threaded operations (Linux)

## 🎓 Educational Value

### Learn by Implementation
- See how NumPy operations actually work
- Compare three different implementation strategies
- Understand performance trade-offs
- No hidden magic - explicit backend selection

### Clear Algorithm Implementations
```python
# Example: LU Decomposition in pure Python
def _lu_decomposition_python(data, shape):
    """Educational implementation showing the algorithm clearly."""
    # Gaussian elimination with partial pivoting
    # ... clear, commented code ...
```

### Progression Through Optimization Levels
1. **Python**: Understand the algorithms
2. **Cython**: Learn about type annotations and GIL management
3. **C++**: Explore SIMD, cache optimization, and memory alignment

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ArrPy.git
cd ArrPy

# Install in development mode
pip install -e .

# Build Cython extensions
make build-cython

# Build C++ extensions (optional)
make build-cpp
```

## 📖 Quick Start

```python
import arrpy

# Create arrays
a = arrpy.array([[1, 2, 3], [4, 5, 6]])
b = arrpy.ones((2, 3))

# Basic operations
c = a + b * 2
d = arrpy.dot(a.T, b)

# Linear algebra
A = arrpy.array([[2, 1], [1, 2]])
b = arrpy.array([3, 3])
x = arrpy.solve(A, b)  # Solve Ax = b

# FFT
signal = arrpy.array([1, 2, 3, 4])
spectrum = arrpy.fft_func(signal)

# Statistics
data = arrpy.array([1, 2, 3, 4, 5])
print(f"Mean: {data.mean()}, Std: {arrpy.std(data)}")

# Save and load
arrpy.save("my_array.apy", data)
loaded = arrpy.load("my_array.apy")
```

## 📈 Benchmarking

Run comprehensive benchmarks:
```bash
python benchmarks/benchmark_v1.py
```

Compare specific operations:
```python
from benchmarks.bench_core import Benchmark

bench = Benchmark("Matrix Multiplication")
bench.run(lambda a, b: a @ b)
bench.report()
```

## 🗺️ Version History

- **v0.1.0**: Core foundation in pure Python
- **v0.2.0**: Backend system architecture
- **v0.3.0**: Cython optimizations
- **v0.4.0**: C++ backend with SIMD
- **v0.5.0**: Complete Cython ufuncs
- **v0.6.0**: Memory pooling system
- **v0.7.0**: Extended SIMD and OpenMP
- **v0.8.0**: Advanced linear algebra
- **v0.9.0**: FFT and advanced indexing
- **v1.0.0**: Production ready with full API

## 🤝 Contributing

Contributions are welcome! See `CONTRIBUTING.md` for guidelines.

### Areas for Contribution
- Implement more operations in Cython/C++ backends
- Add GPU support (CUDA/Metal)
- Optimize existing algorithms
- Improve documentation and examples
- Add more comprehensive tests

## 📚 Learning Resources

- `CLAUDE.md`: Detailed architecture documentation
- `benchmarks/`: Performance analysis examples
- `tests/`: Comprehensive test coverage
- Backend implementations: Study the progression from Python to C++

## ⚖️ License

MIT License - see `LICENSE` file for details.

## 🙏 Acknowledgments

- NumPy team for the inspiration and API design
- Cython and PyBind11 projects for making optimization accessible
- The scientific Python community for continuous learning

---

**ArrPy v1.0.0** - An educational journey through array computing, from pure Python to SIMD-optimized C++. Learn, experiment, and understand how modern numerical libraries work under the hood!