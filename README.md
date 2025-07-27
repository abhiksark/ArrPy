# arrpy

A pure Python implementation that mimics the core functionality of NumPy's ndarray.

## Description

`arrpy` provides a lightweight, dependency-free alternative to NumPy arrays for basic array operations. It implements a pure Python Array class that supports multi-dimensional arrays, indexing, arithmetic operations, matrix operations, and more.

## Features

- **Multi-dimensional array support** with shape validation
- **Indexing and slicing** with tuple-based indexing
- **Element-wise arithmetic operations** (+, -, *, /)
- **Matrix operations** including transpose (T) and dot product
- **Array reshaping** with shape compatibility validation
- **Array creation functions** (zeros, ones, eye, arange, linspace)
- **Aggregation functions** (sum, mean, min, max, std, var, median, percentile)
- **Mathematical functions** (sqrt, sin, cos, exp, log)
- **Comparison operations** (==, !=, >, <, >=, <=)
- **Logical operations** (logical_and, logical_or, logical_not)
- **Array concatenation and stacking** (concatenate, vstack, hstack)
- **Error handling** for shape mismatches and invalid operations
- **Pure Python implementation** - no external dependencies required

## Installation

### From source

Clone the repository and install:

```bash
git clone https://github.com/yourusername/arrpy.git
cd arrpy
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
from arrpy import Array, zeros, ones, eye, arange, linspace, concatenate, vstack, hstack

# Create arrays
a = Array([1, 2, 3])
b = Array([[1, 2], [3, 4]])

# Array creation functions
zeros_arr = zeros((2, 3))        # 2x3 array of zeros
ones_arr = ones(5)               # 1D array of ones
identity = eye(3)                # 3x3 identity matrix
range_arr = arange(0, 10, 2)     # [0, 2, 4, 6, 8]
linear = linspace(0, 1, 11)      # 11 evenly spaced values from 0 to 1

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
minimum = a.min()
maximum = a.max()
std_dev = a.std()
variance = a.var()
med = a.median()
p90 = a.percentile(90)

# Mathematical functions
sqrt_arr = a.sqrt()     # Element-wise square root
sin_arr = a.sin()       # Element-wise sine
exp_arr = a.exp()       # Element-wise exponential

# Comparison operations
greater = a > 2         # Element-wise comparison
equal = a == Array([1, 2, 4])  # Element-wise equality

# Logical operations
bool_arr1 = Array([True, False, True])
bool_arr2 = Array([False, False, True])
and_result = bool_arr1.logical_and(bool_arr2)
or_result = bool_arr1.logical_or(bool_arr2)
not_result = bool_arr1.logical_not()

# Array concatenation and stacking
arr1 = Array([1, 2])
arr2 = Array([3, 4])
concatenated = concatenate([arr1, arr2])  # [1, 2, 3, 4]

mat1 = Array([[1, 2]])
mat2 = Array([[3, 4]])
vstacked = vstack([mat1, mat2])           # [[1, 2], [3, 4]]
hstacked = hstack([mat1.T, mat2.T])       # [[1, 3], [2, 4]]
```

## Supported Operations

### Array Creation
- `zeros(shape)`: Create array filled with zeros
- `ones(shape)`: Create array filled with ones  
- `eye(n, m=None)`: Create identity matrix
- `arange(start, stop=None, step=1)`: Create array with evenly spaced values
- `linspace(start, stop, num=50)`: Create array with linearly spaced values

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
- Min/Max: `arr.min()`, `arr.max()`
- Standard deviation: `arr.std()`
- Variance: `arr.var()`
- Median: `arr.median()`
- Percentile: `arr.percentile(q)`

### Mathematical Functions
- Square root: `arr.sqrt()`
- Trigonometric: `arr.sin()`, `arr.cos()`
- Exponential: `arr.exp()`
- Natural logarithm: `arr.log()`

### Comparison Operations
- Element-wise comparisons: `==`, `!=`, `>`, `<`, `>=`, `<=`
- Works with both arrays and scalars

### Logical Operations
- Logical AND: `arr1.logical_and(arr2)`
- Logical OR: `arr1.logical_or(arr2)`
- Logical NOT: `arr.logical_not()`

### Array Concatenation and Stacking
- Concatenate: `concatenate([arr1, arr2], axis=0)`
- Vertical stack: `vstack([arr1, arr2])`
- Horizontal stack: `hstack([arr1, arr2])`

## Testing

Run the test suite:

```bash
pytest
```

The test suite validates all functionality against NumPy's behavior to ensure compatibility and correctness.

## Development

### Project Structure

```
arrpy-project/
├── arrpy/
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