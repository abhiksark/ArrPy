# ArrPy API Reference

## Array Creation

```python
arrpy.array(data, dtype=None)          # Create array from data
arrpy.zeros(shape, dtype=None)         # Array of zeros
arrpy.ones(shape, dtype=None)          # Array of ones  
arrpy.full(shape, fill_value, dtype=None)  # Array filled with value
arrpy.arange(start, stop, step, dtype=None)  # Range of values
arrpy.linspace(start, stop, num=50)    # Evenly spaced values
arrpy.eye(N, M=None, k=0)              # Identity matrix
```

## Array Operations

### Basic Math
```python
a + b, a - b, a * b, a / b    # Element-wise operations
a ** b, a % b, a // b          # Power, modulo, floor division
arrpy.add(a, b)                # Explicit addition
arrpy.multiply(a, b)           # Explicit multiplication
```

### Universal Functions
```python
arrpy.sin(a), arrpy.cos(a), arrpy.tan(a)     # Trigonometric
arrpy.exp(a), arrpy.log(a), arrpy.log10(a)   # Exponential/logarithmic
arrpy.sqrt(a), arrpy.abs(a)                   # Square root, absolute
arrpy.maximum(a, b), arrpy.minimum(a, b)      # Element-wise min/max
```

### Reductions
```python
arrpy.sum(a, axis=None)         # Sum of elements
arrpy.mean(a, axis=None)        # Mean of elements
arrpy.std(a, axis=None)         # Standard deviation
arrpy.var(a, axis=None)         # Variance
arrpy.min(a), arrpy.max(a)      # Min/max values
arrpy.argmin(a), arrpy.argmax(a)  # Indices of min/max
```

### Linear Algebra
```python
arrpy.dot(a, b)                 # Dot product
arrpy.matmul(a, b)             # Matrix multiplication
arrpy.solve(A, b)              # Solve Ax = b
arrpy.det(a)                   # Determinant
arrpy.transpose(a)             # Transpose
```

### Array Manipulation
```python
a.reshape(shape)               # Reshape array
a.flatten()                    # Flatten to 1D
arrpy.concatenate([a, b])     # Join arrays
arrpy.stack([a, b])           # Stack arrays
arrpy.split(a, n)             # Split array
```

### Indexing & Slicing
```python
a[0]                          # Single element
a[1:5]                        # Slice
a[::2]                        # Strided slice
a[[0, 2, 4]]                  # Fancy indexing
a[(0, 2, 4)]                  # Tuple fancy indexing
```

## Backend Control

```python
arrpy.set_backend('python')   # Pure Python (default)
arrpy.set_backend('cython')   # Optimized Cython
arrpy.set_backend('c')        # C++ with SIMD
arrpy.get_backend()           # Get current backend
```

## Data Types

```python
arrpy.int32, arrpy.int64      # Integer types
arrpy.float32, arrpy.float64  # Float types
arrpy.bool_                   # Boolean type
```

## Array Attributes

```python
a.shape                       # Array dimensions
a.size                        # Total number of elements
a.ndim                        # Number of dimensions
a.dtype                       # Data type
a.T                          # Transpose