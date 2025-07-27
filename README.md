# arrypy

A pure Python implementation that mimics the core functionality of NumPy's ndarray.

## Description

`arrypy` provides a lightweight, dependency-free alternative to NumPy arrays for basic array operations. It implements a pure Python Array class that supports multi-dimensional arrays, indexing, arithmetic operations, matrix operations, and more.

## Features

- **Multi-dimensional array support** with shape validation
- **Indexing and slicing** with tuple-based indexing
- **Element-wise arithmetic operations** (+, -, *, /)
- **Matrix operations** including transpose (T) and dot product
- **Array reshaping** with shape compatibility validation
- **Aggregation functions** (sum, mean)
- **Error handling** for shape mismatches and invalid operations
- **Pure Python implementation** - no external dependencies required

## Installation

### From source

Clone the repository and install:

```bash
git clone https://github.com/yourusername/arrypy.git
cd arrypy
pip install .
```

### Development installation

For development with testing dependencies:

```bash
pip install -e ".[dev]"
```

Or install testing dependencies separately:

```bash
pip install -r requirements.txt
```

## Usage

```python
from arrypy import Array

# Create arrays
a = Array([1, 2, 3])
b = Array([[1, 2], [3, 4]])

# Basic operations
print(a.shape)  # (3,)
print(b.shape)  # (2, 2)

# Indexing
print(a[0])     # 1
print(b[0, 1])  # 2

# Arithmetic operations
c = a + 10      # Element-wise addition with scalar
d = a + Array([4, 5, 6])  # Element-wise addition with another array

# Matrix operations
e = Array([[1, 2], [3, 4]])
f = Array([[5, 6], [7, 8]])
result = e.dot(f)  # Matrix multiplication

# Transpose
transposed = e.T

# Reshaping
reshaped = Array([1, 2, 3, 4, 5, 6]).reshape((2, 3))

# Aggregations
total = a.sum()
average = a.mean()
```

## Supported Operations

### Initialization
- Create arrays from nested lists
- Automatic shape detection
- Validation for ragged arrays

### Indexing
- Single element access: `arr[i]`
- Multi-dimensional indexing: `arr[i, j]`
- Element assignment: `arr[i, j] = value`

### Arithmetic Operations
- Addition: `arr + other`
- Subtraction: `arr - other`
- Multiplication: `arr * other`
- Division: `arr / other`

Works with both scalars and other Array instances of compatible shapes.

### Matrix Operations
- Transpose: `arr.T`
- Matrix multiplication: `arr.dot(other)`

### Shape Operations
- Reshape: `arr.reshape(new_shape)`
- Shape property: `arr.shape`

### Aggregations
- Sum: `arr.sum()`
- Mean: `arr.mean()`

## Testing

Run the test suite:

```bash
pytest
```

The test suite validates all functionality against NumPy's behavior to ensure compatibility and correctness.

## Development

### Project Structure

```
arrypy-project/
├── arrypy/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_array.py
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── setup.py
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Limitations

- This is a pure Python implementation and will be slower than NumPy for large arrays
- Limited to basic array operations compared to NumPy's extensive functionality
- No support for advanced NumPy features like broadcasting, fancy indexing, or specialized data types

## Requirements

- Python 3.6+
- No runtime dependencies
- Testing requires: pytest, numpy (for test validation)