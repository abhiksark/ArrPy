# ArrPy - Cython-Optimized NumPy-like Arrays

A **Cython-optimized** implementation that mimics the core functionality of NumPy's ndarray with significant performance improvements.

## 🚀 Performance Highlights

- **6-9x faster** array creation than pure Python
- **2-3x faster** arithmetic operations  
- **3-4x faster** mathematical functions
- **C-level optimized** aggregation operations
- **Automatic fallback** to pure Python when Cython unavailable

## 📊 Quick Performance Comparison

| Operation | ArrPy vs Pure Python | ArrPy vs NumPy |
|-----------|---------------------|----------------|
| **Array Creation** | 6.83x faster | 2.78-7.58x faster |
| **Arithmetic Ops** | 3.33x faster | 3-4x slower (small arrays) |
| **Math Functions** | 3.34x faster | 2-9x slower |
| **Aggregations** | Up to 6x faster | Competitive (small arrays) |

*Note: Performance varies by array size. ArrPy excels with small-medium arrays, NumPy dominates large arrays.*

## 🔧 Description

ArrPy provides a **Cython-accelerated**, lightweight alternative to NumPy arrays for educational and specialized use cases. It features:

- **Dual Implementation**: Cython-optimized with Python fallback
- **Educational Value**: Clear, readable implementation showing optimization techniques  
- **Production Ready**: Comprehensive testing with 157 test cases
- **NumPy Compatible**: API designed to match NumPy behavior

## ✨ Features

### Core Functionality
- **Multi-dimensional array support** with shape validation
- **Indexing and slicing** with tuple-based indexing
- **Element-wise arithmetic operations** (+, -, *, /)
- **Matrix operations** including transpose (T) and dot product
- **Array reshaping** with shape compatibility validation

### Cython-Optimized Operations
- **Fast creation functions** (zeros, ones, eye, arange, linspace)
- **C-level aggregations** (sum_fast, mean_fast, min, max, std, var, median, percentile)
- **Optimized math functions** (sqrt_fast, sin_fast, cos_fast, exp_fast, log_fast)
- **Efficient comparisons** (==, !=, >, <, >=, <=)
- **Logical operations** (logical_and, logical_or, logical_not)

### Advanced Features
- **Array concatenation** (concatenate, vstack, hstack)
- **Comprehensive error handling** with clear error messages
- **Memory efficient** operations with minimal overhead
- **Fallback system** ensuring compatibility across environments

## 🛠 Installation

### Quick Installation

```bash
git clone https://github.com/yourusername/arrpy.git
cd arrpy
pip install -e .
```

### Building Cython Extensions

**Automatic (Recommended):**
```bash
make build
# or
python setup.py build_ext --inplace
```

**Manual Dependencies:**
```bash
pip install cython numpy
python setup.py build_ext --inplace
```

### Development Installation

```bash
pip install -e ".[dev]"
```

### Requirements
- **Runtime**: Python 3.7+, Cython ≥0.29.0, NumPy ≥1.19.0
- **Development**: pytest, additional testing dependencies
- **Optional**: matplotlib (for benchmarking)

## 🚀 Usage

### Basic Operations

```python
from arrpy import Array, zeros, ones, eye

# Array creation - Cython optimized!
a = Array([1, 2, 3])              # From list
b = Array([[1, 2], [3, 4]])       # Multi-dimensional
zeros_arr = zeros((2, 3))          # 2x3 zeros (fast)
ones_arr = ones(5)                 # 1D ones (fast)
identity = eye(3)                  # 3x3 identity (fast)

# Fast arithmetic
c = a + 10                         # Cython-optimized
d = a * Array([2, 3, 4])          # Element-wise

# High-performance aggregations
total = a.sum()                    # Regular sum
fast_total = a.sum_fast()          # C-level sum (faster)
fast_mean = a.mean_fast()          # C-level mean (faster)

# Optimized math functions
sqrt_result = a.sqrt_fast()        # C math sqrt
sin_result = a.sin_fast()          # C math sine
exp_result = a.exp_fast()          # C math exponential
```

### Matrix Operations

```python
# Matrix operations
e = Array([[1, 2], [3, 4]])
f = Array([[5, 6], [7, 8]])

# Matrix multiplication
result = e.dot(f)

# Transpose
transposed = e.T

# Reshaping
reshaped = Array([1, 2, 3, 4, 5, 6]).reshape((2, 3))
```

### Advanced Features

```python
from arrpy.creation import arange, linspace
from arrpy.math import power, absolute
from arrpy.manipulation.joining import concatenate, vstack

# Range creation
range_arr = arange(0, 10, 2)       # [0, 2, 4, 6, 8]
linear = linspace(0, 1, 11)        # 11 evenly spaced values

# Mathematical functions
powered = power(a, 2)              # Element-wise power
abs_vals = absolute(Array([-1, 2, -3]))  # Absolute values

# Array joining
arr1 = Array([1, 2])
arr2 = Array([3, 4])
joined = concatenate([arr1, arr2])  # [1, 2, 3, 4]
```

## 🧪 Testing

### Run All Tests (157 test cases)

```bash
# Quick test
pytest

# Comprehensive test suite
python run_comprehensive_tests.py

# Specific test categories
pytest tests/test_cython_implementation.py  # Cython-specific tests
pytest tests/test_performance_regression.py  # Performance tests
pytest tests/test_build_system.py          # Build system tests
```

### Test Categories
- **89 original functionality tests** - Core array operations
- **30 Cython implementation tests** - Cython-specific features
- **19 performance regression tests** - Performance monitoring
- **19 build system tests** - Installation and build verification

## 📈 Benchmarking

### Quick Performance Check

```bash
python benchmark_cython.py
```

### Comprehensive ArrPy vs NumPy Benchmark

```bash
python benchmark_vs_numpy.py
```

### Available Benchmarks
- `benchmark_cython.py` - ArrPy Python vs Cython comparison
- `benchmark_vs_numpy.py` - ArrPy vs NumPy comprehensive comparison
- `benchmarks/performance_comparison.py` - Legacy benchmarks
- `tests/test_performance_regression.py` - Automated performance tests

## 🏗 Development

### Project Structure

```
arrpy/
├── arrpy/
│   ├── core/
│   │   ├── array.py              # Pure Python implementation
│   │   ├── array_cython.pyx      # Cython optimized implementation
│   │   ├── array_cython.pxd      # Cython header file
│   │   └── __init__.py           # Auto-import with fallback
│   ├── math/
│   │   ├── arithmetic.py         # Pure Python math functions
│   │   ├── arithmetic_cython.pyx # Cython optimized math
│   │   └── __init__.py           # Auto-import with fallback
│   ├── creation/
│   │   ├── basic.py              # Pure Python creation
│   │   ├── basic_cython.pyx      # Cython optimized creation
│   │   └── __init__.py           # Auto-import with fallback
│   └── manipulation/             # Array manipulation operations
├── tests/
│   ├── test_array.py             # Original functionality tests
│   ├── test_cython_implementation.py  # Cython-specific tests
│   ├── test_performance_regression.py # Performance monitoring
│   └── test_build_system.py      # Build system validation
├── benchmarks/                   # Legacy benchmarking
├── examples/                     # Usage examples
├── setup.py                      # Cython build configuration
├── pyproject.toml               # Modern Python packaging
├── Makefile                     # Development commands
└── README.md
```

### Build Commands

```bash
# Build Cython extensions
make build

# Clean build artifacts  
make clean

# Run tests
make test

# Run benchmarks
make benchmark

# Development installation
make install

# Verify installation
make check
```

### Implementation Details

**Cython Optimizations:**
- `cdef` variables for C-level performance
- `boundscheck=False` for loop optimization
- Direct C math function calls (`libc.math`)
- Memory-efficient array operations
- Type-specific optimizations

**Fallback System:**
- Automatic detection of Cython availability
- Graceful degradation to pure Python
- Identical API regardless of implementation
- Zero user code changes required

## 🎯 Performance Guide

### When ArrPy Excels
- **Array creation from Python data** (2-7x faster than NumPy)
- **Small array operations** (<1000 elements)
- **Educational/prototyping** use cases
- **Custom mathematical operations**

### When to Use NumPy
- **Large array operations** (>10,000 elements)  
- **Production applications** requiring maximum performance
- **Complex mathematical operations**
- **Ecosystem integration** (SciPy, Pandas, etc.)

### Optimization Tips
```python
# Use fast methods when available
arr.sum_fast()    # instead of arr.sum()
arr.mean_fast()   # instead of arr.mean()
arr.sqrt_fast()   # instead of arr.sqrt()

# Check for Cython availability
from arrpy.core import _using_cython
print(f"Using Cython: {_using_cython}")
```

## 🧬 Technical Highlights

### Cython Implementation Features
- **1,222 lines** of optimized Cython code
- **C-level variable declarations** with `cdef`
- **Direct math library calls** for mathematical functions
- **Optimized memory access patterns**
- **Compiler directive optimization** (`boundscheck=False`, `wraparound=False`)

### Quality Assurance
- **157 comprehensive tests** with 100% pass rate
- **Performance regression monitoring**
- **Build system validation**
- **Cross-platform compatibility testing**
- **Memory safety verification**

## 🔍 Limitations

### Performance Limitations
- **Large arrays**: NumPy is 10-50x faster for arrays >10K elements
- **Complex operations**: Limited vectorization compared to NumPy
- **Memory allocation**: Less optimized than NumPy's C implementation

### Feature Limitations  
- **Broadcasting**: Limited compared to NumPy
- **Data types**: Primarily supports Python numeric types
- **Advanced indexing**: No fancy indexing support
- **Ecosystem**: Limited integration with other scientific libraries

## 🆘 Troubleshooting

### Build Issues

**Cython not found:**
```bash
pip install cython numpy
python setup.py build_ext --inplace
```

**Compilation errors:**
```bash
# Clean and rebuild
make clean
make build
```

**Import errors:**
```bash
# Verify installation
python -c "from arrpy.core import Array; print('✅ Working')"
```

### Performance Issues

**Check implementation:**
```python
from arrpy.core import Array
arr = Array([1, 2, 3])
print(f"Implementation: {type(arr).__module__}")
print(f"Has fast methods: {hasattr(arr, 'sum_fast')}")
```

**Force Python fallback (for debugging):**
```bash
# Temporarily rename Cython extensions
mv arrpy/core/*.so backup/
python your_script.py  # Will use Python fallback
```

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch  
3. Add tests for new functionality
4. Ensure all tests pass: `python run_comprehensive_tests.py`
5. Submit a pull request

## 🎓 Educational Value

ArrPy serves as an excellent **learning platform** for understanding:
- **Cython optimization techniques**
- **NumPy-style array implementations**  
- **Performance optimization strategies**
- **C-Python integration patterns**
- **Scientific computing fundamentals**

Perfect for **students**, **educators**, and **developers** interested in high-performance Python programming!