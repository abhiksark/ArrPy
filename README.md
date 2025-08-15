# ArrPy

Educational recreation of NumPy to understand its internals through progressive optimization.

## Overview

ArrPy is a learning project that implements NumPy's core functionality three times:
- **v0.x**: Pure Python implementation (current)
- **v1.x**: Cython optimization (future)
- **v2.x**: PyBind11 + Pure C (future)

## Installation

### Development Installation

```bash
git clone https://github.com/yourusername/arrpy.git
cd arrpy
pip install -e .[dev]
```

## Usage

```python
import arrpy as ap

# Create arrays
a = ap.zeros((3, 4))
b = ap.ones((3, 4))
c = ap.arange(12).reshape(3, 4)

# Operations
result = a + b * 2
dot_product = ap.linalg.dot(c, c.T)
```

## Development

### Running Tests

```bash
make test           # Run all tests
make test-cov      # Run with coverage
```

### Running Benchmarks

```bash
make benchmark     # Run benchmarks
make benchmark-compare  # Compare with NumPy
```

### Code Quality

```bash
make lint          # Run linting
make format        # Format code
```

## Project Structure

```
arrpy/
├── arrpy.py          # Main array class
├── dtype.py          # Data type system
├── ufuncs.py         # Universal functions
├── broadcasting.py   # Broadcasting implementation
├── linalg.py         # Linear algebra
├── random.py         # Random number generation
└── ...

tests/               # Comprehensive test suite
benchmarks/          # Performance benchmarks
```

## Features

- N-dimensional arrays with shape, dtype, strides
- Broadcasting system matching NumPy rules
- Universal functions for element-wise operations
- Basic linear algebra operations
- Array creation and manipulation functions
- Random number generation

## License

MIT License - See LICENSE file for details

## Contributing

This is an educational project. Contributions that improve clarity, add educational value, or enhance performance are welcome!

## Acknowledgments

Inspired by NumPy's excellent design and implementation.