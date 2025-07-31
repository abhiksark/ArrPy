# ArrPy Documentation

Welcome to ArrPy's comprehensive documentation! ArrPy is a high-performance, educational NumPy alternative that combines pure Python readability with optional C acceleration for production-grade performance.

## 📚 Complete Documentation Index

### 🚀 Getting Started
- [**Installation Guide**](INSTALLATION.md) - Complete installation instructions for all platforms
  - Standard Python installation
  - C extensions for maximum performance  
  - Platform-specific troubleshooting
  - Development environment setup
- [**Quick Start Tutorial**](guides/quickstart.md) - Get productive in 5 minutes
  - Basic array operations
  - Performance comparison examples
  - Common usage patterns
- [**User Guide**](guides/USER_GUIDE.md) - Comprehensive usage documentation
  - Array fundamentals and concepts
  - Mathematical operations and functions
  - Statistical analysis capabilities  
  - Advanced manipulation techniques
  - Performance optimization strategies

### 📖 API Reference Documentation
Complete function and class reference with examples:

- [**Core Array Class**](api/array.md) - The Array class and all methods
  - Array properties (shape, size, ndim, dtype)
  - Indexing and slicing operations
  - Mathematical operator overloading
  - Method chaining and fluent interface
  - Memory management and views

- [**Array Creation Functions**](api/creation.md) - Functions for creating arrays
  - Basic creators: `zeros()`, `ones()`, `full()`, `empty()`
  - Range functions: `arange()`, `linspace()`, `logspace()`
  - Matrix functions: `eye()`, `identity()`
  - Advanced creation patterns

- [**Mathematical Functions**](api/math.md) - Element-wise mathematical operations
  - Trigonometric functions: `sin()`, `cos()`, `tan()`, `arcsin()`, etc.
  - Exponential/logarithmic: `exp()`, `log()`, `log10()`, `log2()`, `sqrt()`
  - Arithmetic operations: `power()`, `absolute()`, `sign()`, `floor_divide()`, `mod()`
  - Rounding functions: `floor()`, `ceil()`, `round()`, `trunc()`
  - Performance notes and error handling

- [**Statistical Functions**](api/statistics.md) - Data analysis and aggregation
  - Basic aggregations: `sum()`, `mean()`, `min()`, `max()`
  - Variability measures: `std()`, `var()`
  - Advanced statistics: `median()`, `percentile()`, `prod()`
  - Cumulative functions: `cumsum()`, `cumprod()`
  - Index functions: `argmin()`, `argmax()`
  - Real-world statistical analysis examples

- [**Array Manipulation**](api/manipulation.md) - Shape and structure manipulation
  - Shape operations: `reshape()`, `transpose()`, `squeeze()`, `expand_dims()`
  - Array joining: `concatenate()`, `stack()`, `vstack()`, `hstack()`
  - Array splitting: `split()`, `vsplit()`, `hsplit()`
  - Tiling and repetition: `tile()`, `repeat()`
  - Flipping and rotation: `flip()`, `fliplr()`, `flipud()`, `rot90()`
  - Utility functions: `flatten()`, `ravel()`

### 🏗️ Architecture and Design
- [**Architecture Overview**](guides/architecture.md) - Complete internal design documentation
  - High-level system architecture with diagrams
  - Hybrid backend system (C + Python)
  - Memory layout and optimization strategies
  - Module structure and import resolution
  - Performance optimization techniques
  - Extension architecture and C interface
  - Error handling and testing strategies
  - Build system and compilation pipeline
  - Debugging and profiling capabilities
  - Future architecture roadmap

### ⚡ Performance Documentation
- [**Performance Report**](../PERFORMANCE_REPORT.md) - Comprehensive benchmarking results
  - Array creation performance (4-5x faster with C)
  - Arithmetic operations (up to 170x speedup)
  - Statistical functions (20-50x improvement)
  - Memory usage optimization (60-70% reduction)
  - Scaling behavior analysis
  
- [**NumPy Comparison**](../NUMPY_COMPARISON_REPORT.md) - Head-to-head performance analysis
  - Feature parity assessment
  - Performance comparison across operations
  - Memory usage comparison
  - Use case recommendations
  
- [**C Extension Guide**](../C_EXTENSION_GUIDE.md) - Deep dive into C acceleration
  - C extension architecture
  - Compilation and optimization flags
  - SIMD vectorization details
  - OpenMP parallelization
  - Memory management strategies
  - Debugging C extensions

### 🔧 Development and Contributing
- [**Changelog**](CHANGELOG.md) - Complete version history and release notes
  - Version 0.1.0: Initial pure Python implementation
  - Version 0.2.0: Hybrid array system introduction
  - Version 0.3.0: C extensions and performance optimization
  - Breaking changes and migration guides
  
- [**Contributing Guide**](../CONTRIBUTING.md) - How to contribute to ArrPy
  - Code style guidelines
  - Testing requirements
  - Documentation standards
  - Pull request process
  - Issue reporting guidelines

## 🚀 Key Features

### Pure Python Implementation
- Educational and readable codebase
- No external dependencies
- Easy to understand and modify
- Great for learning array internals

### Optional C Acceleration
- 4-170x faster than pure Python
- Automatic backend selection
- Memory efficient
- Production-ready performance

### NumPy-Compatible API
- Familiar interface for NumPy users
- Easy migration path
- Subset of NumPy functionality
- Growing feature set

## 📊 Performance Highlights

With C extensions enabled:
- **Array Creation**: 4-5x faster than pure Python
- **Arithmetic**: Up to 170x faster
- **Aggregations**: Up to 48x faster
- **Memory**: 60-70% less usage

## 🎯 Use Cases

### Education
- Understanding array implementations
- Learning about Python C extensions
- Teaching numerical computing concepts
- Exploring optimization techniques

### Production
- Lightweight NumPy alternative
- Embedded systems
- Environments without NumPy
- Performance-critical applications

## 📖 Quick Example

```python
import arrpy as ap

# Create arrays
a = ap.Array([1, 2, 3, 4, 5])
b = ap.arange(5)

# Arithmetic operations
c = a + b * 2
print(f"Result: {c}")

# Aggregations
print(f"Sum: {c.sum()}")
print(f"Mean: {c.mean()}")

# 2D arrays
matrix = ap.Array([[1, 2], [3, 4]])
result = matrix.dot(matrix)
print(f"Matrix multiplication:\n{result}")

# Mathematical functions
angles = ap.linspace(0, ap.pi, 5)
sines = ap.sin(angles)
print(f"Sine values: {sines}")
```

## 🔧 Building C Extensions

For maximum performance:

```bash
# Build C extensions
python setup_c_ext.py build_ext --inplace

# Verify
python -c "from arrpy import Array; a = Array([1,2,3]); print('C backend:', hasattr(a, '_c_array'))"
```

## 📚 Recommended Learning Path

### For New Users
1. **Installation** → [Installation Guide](INSTALLATION.md)
2. **Quick Start** → [Quick Start Tutorial](guides/quickstart.md)  
3. **Core Concepts** → [User Guide](guides/USER_GUIDE.md)
4. **API Reference** → [API Documentation](api/)

### For Performance Users
1. **C Extensions** → [Installation Guide](INSTALLATION.md#c-extensions-installation)
2. **Benchmarks** → [Performance Report](../PERFORMANCE_REPORT.md)
3. **Architecture** → [Architecture Overview](guides/architecture.md)
4. **Optimization** → [C Extension Guide](../C_EXTENSION_GUIDE.md)

### For Contributors
1. **Architecture** → [Architecture Overview](guides/architecture.md)
2. **Contributing** → [Contributing Guide](../CONTRIBUTING.md)
3. **API Design** → [API Reference](api/)
4. **Changelog** → [Version History](CHANGELOG.md)

## 🤝 Community

- **GitHub**: [github.com/yourusername/ArrPy](https://github.com/yourusername/ArrPy)
- **Issues**: [Bug Reports & Features](https://github.com/yourusername/ArrPy/issues)
- **Discussions**: [Community Forum](https://github.com/yourusername/ArrPy/discussions)
- **Contributing**: [Contribution Guide](../CONTRIBUTING.md)

## 📄 License

ArrPy is open source software [licensed as MIT](../LICENSE).

---

*Last updated: January 31, 2024*