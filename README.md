# ArrPy 🚀

<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.1-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
  <img src="https://img.shields.io/badge/status-Phase%201%20Complete-success.svg" alt="Status">
</p>

**ArrPy** is an educational recreation of NumPy built from scratch to understand the internals of numerical computing libraries. This project implements core NumPy functionality through three progressive versions, each with increasing performance optimizations.

## 📚 Table of Contents

- [Overview](#-overview)
- [Project Goals](#-project-goals)
- [Current Status](#-current-status)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Development](#-development)
- [Performance](#-performance)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Overview

ArrPy implements NumPy's core functionality in three progressive versions:

| Version | Implementation | Status | Purpose |
|---------|---------------|--------|---------|
| **v0.x** | Pure Python | 🚧 In Progress (Phase 1 ✅) | Learn algorithms & understand NumPy's design |
| **v1.x** | Cython | 📅 Planned | Learn compilation & type optimization |
| **v2.x** | C++ with PyBind11 | 📅 Planned | Learn low-level optimization & SIMD |

## 🎓 Project Goals

1. **Educational**: Understand how NumPy works internally by implementing it from scratch
2. **Progressive Optimization**: Learn different optimization techniques through three implementations
3. **Complete Implementation**: Implement all core NumPy features, not just a subset
4. **Well-Documented**: Every algorithm and design decision is documented for learning

## 📊 Current Status

### Version 0.1.1 - Phase 1 Complete ✅

- ✅ **Core Array Class**: N-dimensional array with shape, strides, and dtype
- ✅ **Array Creation**: zeros, ones, arange, linspace, eye, full, empty
- ✅ **Basic Indexing**: Integer and slice indexing for 1D/2D arrays
- ✅ **Data Types**: Type system with inference and conversion
- 🚧 **Operations**: Coming in Phase 2
- 🚧 **Broadcasting**: Coming in Phase 2
- 🚧 **Linear Algebra**: Coming in Phase 3

## 💻 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Development Installation

```bash
# Clone the repository
git clone https://github.com/abhiksark/ArrPy.git
cd ArrPy

# Install in development mode with all dependencies
pip install -e .[dev]

# Verify installation
python -c "import arrpy; print(arrpy.__version__)"
```

### Basic Installation

```bash
# Install without development dependencies
pip install -e .
```

## 🚀 Quick Start

```python
import arrpy as ap
import numpy as np  # for comparison

# Create arrays
a = ap.array([[1, 2, 3], [4, 5, 6]])
print(f"Array a:\n{a}")
print(f"Shape: {a.shape}, Size: {a.size}, Ndim: {a.ndim}")

# Array creation functions
zeros = ap.zeros((3, 4))
ones = ap.ones((2, 3), dtype=ap.int32)
range_arr = ap.arange(0, 10, 2)
linear = ap.linspace(0, 1, 5)
identity = ap.eye(3)

# Indexing and slicing
arr = ap.arange(12)
print(arr[5])        # Single element
print(arr[2:8])      # Slice
print(arr[::2])      # Strided slice

# 2D indexing
matrix = ap.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(matrix[0, :])  # First row
print(matrix[:, 1])  # Second column
print(matrix[1:, :2]) # Submatrix
```

## ✨ Features

### Currently Implemented (v0.1.1)

#### Core Array Structure
- N-dimensional arrays with efficient flattened storage
- Row-major (C-order) memory layout
- Strides for efficient multi-dimensional access
- Properties: shape, size, ndim, dtype, strides

#### Array Creation
```python
ap.zeros(shape)           # Zero-filled array
ap.ones(shape)            # One-filled array
ap.full(shape, value)     # Filled with specific value
ap.empty(shape)           # Uninitialized array
ap.arange(start, stop, step)  # Range of values
ap.linspace(start, stop, num) # Linearly spaced values
ap.eye(n, m)              # Identity matrix
ap.array(data)            # From list/nested lists
```

#### Data Types
- Supported types: int32, int64, float32, float64, bool
- Automatic type inference
- Type conversion and promotion

#### Indexing & Slicing
- Basic indexing: `arr[i]`, `arr[i, j]`
- Negative indexing: `arr[-1]`
- Slicing: `arr[start:stop:step]`
- Multi-dimensional slicing: `arr[:, 1:3]`
- Assignment: `arr[0] = 5`, `arr[1:3] = [7, 8]`

### Coming Soon

#### Phase 2 - Operations & Broadcasting (v0.2.x)
- Arithmetic operators (+, -, *, /, //, %, **)
- Broadcasting system
- Universal functions (ufuncs)
- Reductions (sum, mean, min, max)

#### Phase 3 - Advanced Features (v0.3.x)
- Advanced indexing (boolean, fancy)
- Array manipulation (reshape, transpose, concatenate)
- Linear algebra operations
- More ufuncs (trigonometric, exponential)

#### Phase 4 - Completion (v0.4.x)
- Random number generation
- Additional functions
- Performance optimizations
- Complete test coverage

## 📁 Project Structure

```
ArrPy/
├── arrpy/                  # Main package
│   ├── __init__.py        # Package initialization
│   ├── arrpy.py           # Core array class
│   ├── creation.py        # Array creation functions
│   ├── dtype.py           # Data type system
│   ├── indexing.py        # Advanced indexing logic
│   ├── ufuncs.py          # Universal functions
│   ├── broadcasting.py    # Broadcasting implementation
│   ├── linalg.py          # Linear algebra operations
│   ├── manipulation.py    # Shape manipulation
│   └── random.py          # Random number generation
├── tests/                  # Test suite
│   ├── test_arrpy.py      # Core array tests
│   ├── test_dtype.py      # Data type tests
│   └── ...
├── benchmarks/            # Performance benchmarks
│   ├── run_benchmarks.py  # Main benchmark runner
│   └── bench_*.py         # Specific benchmarks
├── docs/                  # Documentation
│   └── DEVELOPMENT_GUIDE.md
├── IMPLEMENTATION_PLAN.md # Detailed implementation plan
└── README.md             # This file
```

## 🛠️ Development

### Setup Development Environment

```bash
# Install development dependencies
make install-dev

# Run tests
make test

# Run tests with coverage
make test-cov

# Run benchmarks
make benchmark

# Run linting
make lint

# Format code
make format
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_arrpy.py

# Run with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=arrpy --cov-report=html
```

### Benchmarking

```bash
# Run all benchmarks
python benchmarks/run_benchmarks.py

# Compare with NumPy
python benchmarks/run_benchmarks.py --compare-numpy

# Run specific benchmark category
python benchmarks/run_benchmarks.py --category=creation
```

## 📈 Performance

Expected performance for Pure Python implementation (v0.x):

| Operation | ArrPy v0.x | NumPy | Ratio |
|-----------|------------|-------|-------|
| Array Creation | ~50-100x slower | Baseline | 🔴 |
| Element Access | ~20-50x slower | Baseline | 🟡 |
| Operations | ~100-500x slower | Baseline | 🔴 |
| Small Arrays | ~10-20x slower | Baseline | 🟡 |

*Note: v0.x focuses on correctness and clarity over performance. Versions 1.x (Cython) and 2.x (C++) will progressively improve performance.*

## 🗺️ Roadmap

### Phase Completion Timeline

| Phase | Version | Target Date | Status |
|-------|---------|------------|--------|
| Phase 1: Core Foundation | v0.1.x | Week 1 | ✅ Complete |
| Phase 2: Operations | v0.2.x | Week 2 | 🚧 In Progress |
| Phase 3: Advanced Features | v0.3.x | Week 3 | 📅 Planned |
| Phase 4: Completion | v0.4.x | Week 4 | 📅 Planned |
| **Pure Python Complete** | **v0.5.0** | Month 1 | 📅 Planned |
| **Cython Implementation** | **v1.0.0** | Month 2 | 📅 Planned |
| **C++ Implementation** | **v2.0.0** | Month 3 | 📅 Planned |

### Version History

- **v0.1.1** (Current) - Phase 1 Complete: Core array structure, creation, and indexing
- **v0.1.0** - Initial project structure

## 🤝 Contributing

This is an educational project and contributions are welcome! Areas where you can help:

1. **Implementation**: Help implement missing NumPy functions
2. **Testing**: Add more test cases and improve coverage
3. **Documentation**: Improve documentation and add examples
4. **Optimization**: Suggest optimizations (while keeping pure Python)
5. **Benchmarking**: Add more comprehensive benchmarks

### Guidelines

1. Follow the existing code style
2. Add tests for new features
3. Update documentation
4. Ensure all tests pass
5. Add benchmarks for new operations

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📚 Learning Resources

- [NumPy Documentation](https://numpy.org/doc/stable/)
- [From Python to NumPy](https://www.labri.fr/perso/nrougier/from-python-to-numpy/)
- [NumPy Internals](https://numpy.org/doc/stable/reference/internals.html)
- [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) - Detailed implementation guide

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **NumPy Team** - For creating an amazing library that serves as our reference
- **Python Community** - For excellent documentation and learning resources
- **Contributors** - Everyone who helps make this educational project better

## 📞 Contact

**Author**: Abhik Sarkar  
**Email**: abhiksark@gmail.com  
**GitHub**: [@abhiksark](https://github.com/abhiksark)  
**Repository**: [https://github.com/abhiksark/ArrPy](https://github.com/abhiksark/ArrPy)

---

<p align="center">
  Made with ❤️ for learning and education
</p>