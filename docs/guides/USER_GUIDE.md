# ArrPy User Guide

A comprehensive guide to using ArrPy for numerical computing.

## Table of Contents

1. [Introduction](#introduction)
2. [Core Concepts](#core-concepts)
3. [Array Creation](#array-creation)
4. [Array Operations](#array-operations)
5. [Mathematical Functions](#mathematical-functions)
6. [Statistical Functions](#statistical-functions)
7. [Array Manipulation](#array-manipulation)
8. [Performance Optimization](#performance-optimization)
9. [Advanced Topics](#advanced-topics)
10. [Best Practices](#best-practices)

## Introduction

ArrPy is a lightweight numerical computing library that provides NumPy-like functionality with optional C acceleration. It's designed to be:

- **Educational**: Clear, readable implementation
- **Performant**: Optional C backend for speed
- **Compatible**: NumPy-like API
- **Lightweight**: Minimal dependencies

### When to Use ArrPy

- Learning about array implementations
- Environments where NumPy isn't available
- Teaching numerical computing
- Lightweight numerical applications
- Understanding Python C extensions

## Core Concepts

### The Array Object

The fundamental object in ArrPy is the `Array`:

```python
import arrpy as ap

# Create an array
arr = ap.Array([1, 2, 3, 4, 5])

# Key properties
print(f"Data: {arr}")           # Array([1, 2, 3, 4, 5])
print(f"Shape: {arr.shape}")    # (5,)
print(f"Size: {arr.size}")      # 5
print(f"Dimensions: {arr.ndim}") # 1
```

### Multi-dimensional Arrays

ArrPy supports N-dimensional arrays:

```python
# 2D array (matrix)
matrix = ap.Array([[1, 2, 3],
                   [4, 5, 6]])
print(f"Shape: {matrix.shape}")  # (2, 3)
print(f"Dimensions: {matrix.ndim}") # 2

# 3D array
tensor = ap.Array([[[1, 2], [3, 4]],
                   [[5, 6], [7, 8]]])
print(f"Shape: {tensor.shape}")  # (2, 2, 2)
```

### Memory Layout

Arrays are stored in row-major (C-style) order:

```python
arr = ap.Array([[1, 2, 3],
                [4, 5, 6]])
# Memory: [1, 2, 3, 4, 5, 6]
```

## Array Creation

### From Python Sequences

```python
# From list
arr1 = ap.Array([1, 2, 3, 4, 5])

# From nested lists (2D)
arr2 = ap.Array([[1, 2], [3, 4]])

# From range
arr3 = ap.Array(range(10))
```

### Creation Functions

#### Zeros and Ones

```python
# 1D arrays
zeros_1d = ap.zeros(5)          # [0, 0, 0, 0, 0]
ones_1d = ap.ones(5)            # [1, 1, 1, 1, 1]

# 2D arrays
zeros_2d = ap.zeros((3, 4))     # 3x4 matrix of zeros
ones_2d = ap.ones((2, 3))       # 2x3 matrix of ones

# 3D arrays
zeros_3d = ap.zeros((2, 3, 4))  # 2x3x4 tensor of zeros
```

#### Ranges and Sequences

```python
# arange - similar to Python's range
arr1 = ap.arange(10)           # [0, 1, 2, ..., 9]
arr2 = ap.arange(1, 10)        # [1, 2, 3, ..., 9]
arr3 = ap.arange(0, 10, 2)     # [0, 2, 4, 6, 8]

# linspace - evenly spaced values
arr4 = ap.linspace(0, 1, 5)    # [0, 0.25, 0.5, 0.75, 1.0]
arr5 = ap.linspace(-1, 1, 11)  # 11 points from -1 to 1

# logspace - logarithmically spaced
arr6 = ap.logspace(0, 2, 5)    # [1, 3.16, 10, 31.6, 100]
```

#### Special Arrays

```python
# Identity matrix
identity = ap.identity(3)
# [[1, 0, 0],
#  [0, 1, 0],
#  [0, 0, 1]]

# Eye matrix (with offset)
eye1 = ap.eye(3)        # Same as identity
eye2 = ap.eye(3, 4)     # 3x4 with diagonal ones
eye3 = ap.eye(3, k=1)   # Diagonal offset by 1

# Full array (filled with value)
full1 = ap.full(5, 7)          # [7, 7, 7, 7, 7]
full2 = ap.full((2, 3), 3.14)  # 2x3 filled with 3.14

# Empty array (uninitialized)
empty = ap.empty((3, 3))  # 3x3 uninitialized
```

## Array Operations

### Arithmetic Operations

All arithmetic operations are element-wise:

```python
a = ap.Array([1, 2, 3, 4])
b = ap.Array([5, 6, 7, 8])

# Basic arithmetic
addition = a + b        # [6, 8, 10, 12]
subtraction = a - b     # [-4, -4, -4, -4]
multiplication = a * b  # [5, 12, 21, 32]
division = a / b        # [0.2, 0.33, 0.43, 0.5]

# Scalar operations
scalar_add = a + 10     # [11, 12, 13, 14]
scalar_mult = a * 2     # [2, 4, 6, 8]
scalar_pow = a ** 2     # [1, 4, 9, 16]
```

### Comparison Operations

```python
a = ap.Array([1, 2, 3, 4])
b = ap.Array([2, 2, 4, 3])

# Element-wise comparisons return boolean arrays
equal = a == b          # [False, True, False, False]
not_equal = a != b      # [True, False, True, True]
greater = a > b         # [False, False, False, True]
less_equal = a <= b     # [True, True, True, False]

# Scalar comparisons
above_2 = a > 2         # [False, False, True, True]
```

### Matrix Operations

```python
# Matrix multiplication
A = ap.Array([[1, 2], [3, 4]])
B = ap.Array([[5, 6], [7, 8]])

C = A.dot(B)  # Matrix multiplication
# [[19, 22],
#  [43, 50]]

# Transpose
A_T = A.T
# [[1, 3],
#  [2, 4]]

# Matrix-vector multiplication
v = ap.Array([1, 2])
result = A.dot(v)  # [5, 11]
```

## Mathematical Functions

### Trigonometric Functions

```python
angles = ap.linspace(0, 2 * ap.pi, 5)

# Basic trig
sines = ap.sin(angles)
cosines = ap.cos(angles)
tangents = ap.tan(angles)

# Inverse trig
values = ap.Array([0, 0.5, 1])
arcsines = ap.arcsin(values)
arccosines = ap.arccos(values)
arctangents = ap.arctan(values)
```

### Exponential and Logarithmic

```python
x = ap.Array([1, 2, 3, 4, 5])

# Exponential
exp_x = ap.exp(x)          # e^x
exp_x_method = x.exp()     # Same result

# Logarithms
log_x = ap.log(x)          # Natural log
log10_x = ap.log10(x)      # Base-10 log
log2_x = ap.log2(x)        # Base-2 log

# Square root
sqrt_x = ap.sqrt(x)
sqrt_method = x.sqrt()     # Same result
```

### Other Mathematical Functions

```python
a = ap.Array([-2, -1, 0, 1, 2])

# Absolute value
abs_a = ap.absolute(a)     # [2, 1, 0, 1, 2]

# Sign function
sign_a = ap.sign(a)        # [-1, -1, 0, 1, 1]

# Power function
powered = ap.power(a, 3)   # Cube each element

# Modulo and floor division
b = ap.Array([5, 6, 7, 8, 9])
mod = ap.mod(b, 3)         # [2, 0, 1, 2, 0]
floor_div = ap.floor_divide(b, 3)  # [1, 2, 2, 2, 3]
```

### Rounding Functions

```python
x = ap.Array([1.2, 2.7, -1.5, 3.1])

# Different rounding methods
rounded = ap.round(x)      # [1, 3, -2, 3]
floored = ap.floor(x)      # [1, 2, -2, 3]
ceiled = ap.ceil(x)        # [2, 3, -1, 4]
truncated = ap.trunc(x)    # [1, 2, -1, 3]
```

## Statistical Functions

### Basic Statistics

```python
data = ap.Array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Aggregations
total = data.sum()         # 55
average = data.mean()      # 5.5
minimum = data.min()       # 1
maximum = data.max()       # 10

# Variance and standard deviation
variance = data.var()      # 8.25
std_dev = data.std()       # 2.87

# With degrees of freedom
variance_ddof1 = data.var(ddof=1)  # 9.17
std_ddof1 = data.std(ddof=1)       # 3.03
```

### Advanced Statistics

```python
# Product of elements
product = ap.prod(data)    # 3628800

# Cumulative operations
cumsum = ap.cumsum(data)   # [1, 3, 6, 10, 15, ...]
cumprod = ap.cumprod(data) # [1, 2, 6, 24, 120, ...]

# Median and percentiles
median = ap.median(data)   # 5.5
percentile_25 = ap.percentile(data, 25)  # 3.25
percentile_75 = ap.percentile(data, 75)  # 7.75

# Argument functions
min_index = ap.argmin(data)  # 0
max_index = ap.argmax(data)  # 9
```

### Axis-based Operations

```python
# 2D array statistics
matrix = ap.Array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

# Sum along axes
sum_all = matrix.sum()      # 45
sum_rows = matrix.sum(axis=0)  # [12, 15, 18]
sum_cols = matrix.sum(axis=1)  # [6, 15, 24]

# Mean along axes
mean_rows = matrix.mean(axis=0)  # [4, 5, 6]
mean_cols = matrix.mean(axis=1)  # [2, 5, 8]
```

## Array Manipulation

### Reshaping

```python
# Basic reshape
arr = ap.arange(12)
reshaped = arr.reshape((3, 4))
# [[0, 1, 2, 3],
#  [4, 5, 6, 7],
#  [8, 9, 10, 11]]

# Multiple dimensions
reshaped_3d = arr.reshape((2, 2, 3))

# Automatic dimension calculation
auto_dim = arr.reshape((3, -1))  # -1 means "infer this dimension"
```

### Dimension Manipulation

```python
# Squeeze - remove dimensions of size 1
arr = ap.Array([[[1], [2], [3]]])  # Shape: (1, 3, 1)
squeezed = ap.squeeze(arr)         # Shape: (3,)

# Expand dimensions
arr = ap.Array([1, 2, 3])          # Shape: (3,)
expanded = ap.expand_dims(arr, axis=0)  # Shape: (1, 3)
expanded2 = ap.expand_dims(arr, axis=1) # Shape: (3, 1)
```

### Joining Arrays

```python
a = ap.Array([1, 2, 3])
b = ap.Array([4, 5, 6])

# Concatenate
concat = ap.concatenate([a, b])    # [1, 2, 3, 4, 5, 6]

# Stack - creates new dimension
stacked = ap.stack([a, b])         # [[1, 2, 3], [4, 5, 6]]
vstacked = ap.vstack([a, b])       # Same as stack
hstacked = ap.hstack([a, b])       # [1, 2, 3, 4, 5, 6]

# 2D concatenation
A = ap.Array([[1, 2], [3, 4]])
B = ap.Array([[5, 6], [7, 8]])

concat_axis0 = ap.concatenate([A, B], axis=0)
# [[1, 2],
#  [3, 4],
#  [5, 6],
#  [7, 8]]

concat_axis1 = ap.concatenate([A, B], axis=1)
# [[1, 2, 5, 6],
#  [3, 4, 7, 8]]
```

## Performance Optimization

### Enable C Extensions

```python
# Check if C extensions are available
from arrpy.core import HAS_C_EXTENSION
print(f"C extensions: {HAS_C_EXTENSION}")

# Build C extensions if not available
# Run in terminal: python setup_c_ext.py build_ext --inplace
```

### Performance Tips

1. **Use Vectorized Operations**
   ```python
   # Good - vectorized
   result = arr * 2 + 3
   
   # Bad - loop
   result = ap.Array([x * 2 + 3 for x in arr])
   ```

2. **Preallocate Arrays**
   ```python
   # Good - preallocate
   result = ap.zeros(1000)
   for i in range(1000):
       result[i] = compute_value(i)
   
   # Bad - growing list
   result = []
   for i in range(1000):
       result.append(compute_value(i))
   result = ap.Array(result)
   ```

3. **Use Built-in Functions**
   ```python
   # Good - built-in
   mean = arr.mean()
   
   # Bad - manual
   mean = arr.sum() / arr.size
   ```

4. **Minimize Copies**
   ```python
   # In-place operations when possible
   arr += 5  # Modifies arr in place
   # vs
   arr = arr + 5  # Creates new array
   ```

### Performance Comparison

With C extensions enabled:
- Array creation: 4-5x faster
- Arithmetic: 30-170x faster
- Aggregations: 17-48x faster
- Memory: 60-70% less usage

## Advanced Topics

### Broadcasting (Limited)

ArrPy supports basic broadcasting:

```python
# Scalar broadcasting
arr = ap.Array([[1, 2, 3],
                [4, 5, 6]])
result = arr + 10  # Adds 10 to each element

# Row/column operations (limited)
row = ap.Array([1, 2, 3])
# Some broadcasting operations may not be supported
```

### Memory Views and Efficiency

```python
# Views vs copies
arr = ap.arange(10)
view = arr[2:8]  # This may be a copy in ArrPy
view[0] = 100    # May not affect original array

# Always verify behavior for your use case
```

### Error Handling

```python
try:
    # Invalid operation
    result = ap.Array([1, 2]) + ap.Array([1, 2, 3])
except ValueError as e:
    print(f"Shape mismatch: {e}")

try:
    # Invalid reshape
    arr = ap.arange(10)
    reshaped = arr.reshape((3, 4))  # 10 elements can't reshape to 3x4
except ValueError as e:
    print(f"Cannot reshape: {e}")
```

## Best Practices

### 1. Import Convention

```python
import arrpy as ap  # Standard alias
```

### 2. Type Consistency

```python
# Be consistent with numeric types
floats = ap.Array([1.0, 2.0, 3.0])  # Float array
ints = ap.Array([1, 2, 3])          # Integer array
```

### 3. Shape Awareness

```python
# Always check shapes before operations
assert a.shape == b.shape, "Shape mismatch"
result = a + b
```

### 4. Use Appropriate Functions

```python
# Use specialized functions when available
identity_matrix = ap.identity(5)  # Better than creating manually
```

### 5. Documentation

```python
def process_data(arr):
    """
    Process array data.
    
    Parameters
    ----------
    arr : Array
        Input array of shape (n,) or (n, m)
        
    Returns
    -------
    Array
        Processed array of same shape
    """
    return arr * 2 + 1
```

## Migrating from NumPy

If you're coming from NumPy:

```python
# NumPy -> ArrPy equivalents
# np.array() -> ap.Array()
# np.zeros() -> ap.zeros()
# np.dot() -> arr.dot()
# np.sum() -> ap.sum() or arr.sum()

# Key differences:
# 1. Limited broadcasting
# 2. No complex dtypes
# 3. Subset of functions
# 4. Different performance characteristics
```

## Troubleshooting

### Common Issues

1. **Import Error**
   ```python
   # Make sure ArrPy is installed
   pip install -e /path/to/ArrPy
   ```

2. **Performance Issues**
   ```python
   # Enable C extensions
   python setup_c_ext.py build_ext --inplace
   ```

3. **Shape Mismatches**
   ```python
   # Always verify shapes
   print(f"Shape A: {a.shape}, Shape B: {b.shape}")
   ```

## Further Reading

- [API Reference](../api/) - Complete function reference
- [Examples](../examples/) - Real-world examples
- [Performance Guide](performance.md) - Optimization tips
- [Contributing](../../CONTRIBUTING.md) - How to contribute

Happy computing with ArrPy! 🚀