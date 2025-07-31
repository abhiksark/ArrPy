# Array Creation Functions API Reference

Functions for creating arrays with specific values or patterns.

## Basic Creation Functions

### `zeros(shape)`
Create an array filled with zeros.

**Parameters:**
- `shape` : int or tuple of ints
  - Shape of the new array

**Returns:**
- `Array` : Array of zeros with given shape

**Examples:**
```python
# 1D array
zeros(5)  # Array([0, 0, 0, 0, 0])

# 2D array
zeros((2, 3))  # Array([[0, 0, 0], [0, 0, 0]])

# 3D array
zeros((2, 2, 2))  # 2x2x2 array of zeros
```

---

### `ones(shape)`
Create an array filled with ones.

**Parameters:**
- `shape` : int or tuple of ints
  - Shape of the new array

**Returns:**
- `Array` : Array of ones with given shape

**Examples:**
```python
# 1D array
ones(4)  # Array([1, 1, 1, 1])

# 2D array
ones((3, 2))  # Array([[1, 1], [1, 1], [1, 1]])
```

---

### `empty(shape)`
Create an uninitialized array.

**Parameters:**
- `shape` : int or tuple of ints
  - Shape of the new array

**Returns:**
- `Array` : Uninitialized array (contains zeros in current implementation)

**Notes:**
- In ArrPy, `empty()` returns zeros for safety
- Use when you'll immediately fill the array with values

**Examples:**
```python
arr = empty((2, 3))  # 2x3 uninitialized array
```

---

### `full(shape, fill_value)`
Create an array filled with a specific value.

**Parameters:**
- `shape` : int or tuple of ints
  - Shape of the new array
- `fill_value` : scalar
  - Value to fill the array with

**Returns:**
- `Array` : Array filled with fill_value

**Examples:**
```python
# Fill with integer
full(5, 7)  # Array([7, 7, 7, 7, 7])

# Fill with float
full((2, 3), 3.14)  # Array([[3.14, 3.14, 3.14], [3.14, 3.14, 3.14]])

# Fill with boolean
full((2, 2), True)  # Array([[True, True], [True, True]])
```

## Range Functions

### `arange(start, stop=None, step=1)`
Create an array with evenly spaced values within a given range.

**Parameters:**
- `start` : number
  - Start of interval (inclusive)
- `stop` : number, optional
  - End of interval (exclusive)
- `step` : number, optional
  - Spacing between values (default: 1)

**Returns:**
- `Array` : Array of evenly spaced values

**Notes:**
- If only one argument is provided, it's treated as `stop` with `start=0`
- Similar to Python's built-in `range()`

**Examples:**
```python
# Single argument (stop)
arange(5)  # Array([0, 1, 2, 3, 4])

# Start and stop
arange(2, 8)  # Array([2, 3, 4, 5, 6, 7])

# With step
arange(0, 10, 2)  # Array([0, 2, 4, 6, 8])

# Negative step
arange(10, 0, -2)  # Array([10, 8, 6, 4, 2])

# Float values
arange(0, 1, 0.2)  # Array([0, 0.2, 0.4, 0.6, 0.8])
```

---

### `linspace(start, stop, num=50)`
Create an array with evenly spaced values over a specified interval.

**Parameters:**
- `start` : number
  - Start of interval
- `stop` : number
  - End of interval (inclusive)
- `num` : int, optional
  - Number of samples (default: 50)

**Returns:**
- `Array` : Array of evenly spaced values

**Notes:**
- Unlike `arange()`, `stop` is inclusive
- Guarantees exactly `num` points

**Examples:**
```python
# Default 50 points
linspace(0, 1)  # 50 evenly spaced points from 0 to 1

# Specify number of points
linspace(0, 10, 11)  # Array([0, 1, 2, ..., 9, 10])

# Float interval
linspace(-1, 1, 5)  # Array([-1, -0.5, 0, 0.5, 1])

# For plotting
x = linspace(0, 2*pi, 100)  # 100 points for smooth curves
```

---

### `logspace(start, stop, num=50, base=10)`
Create an array with values spaced evenly on a log scale.

**Parameters:**
- `start` : float
  - Starting exponent (base^start)
- `stop` : float
  - Ending exponent (base^stop)
- `num` : int, optional
  - Number of samples (default: 50)
- `base` : float, optional
  - Base of the logarithm (default: 10)

**Returns:**
- `Array` : Array of values logarithmically spaced

**Examples:**
```python
# Powers of 10 from 10^0 to 10^2
logspace(0, 2, 5)  # Array([1, 3.16, 10, 31.6, 100])

# Powers of 2
logspace(0, 4, 5, base=2)  # Array([1, 2, 4, 8, 16])

# Fractional exponents
logspace(0, 1, 3)  # Array([1, 3.16, 10])
```

## Matrix Creation Functions

### `eye(n, m=None, k=0)`
Create a 2D array with ones on the diagonal and zeros elsewhere.

**Parameters:**
- `n` : int
  - Number of rows
- `m` : int, optional
  - Number of columns (default: n)
- `k` : int, optional
  - Diagonal offset (default: 0)
    - k > 0: diagonal above main
    - k < 0: diagonal below main

**Returns:**
- `Array` : 2D array with ones on k-th diagonal

**Examples:**
```python
# Square identity matrix
eye(3)
# Array([[1, 0, 0],
#        [0, 1, 0],
#        [0, 0, 1]])

# Rectangular matrix
eye(2, 4)
# Array([[1, 0, 0, 0],
#        [0, 1, 0, 0]])

# Offset diagonal
eye(3, k=1)
# Array([[0, 1, 0],
#        [0, 0, 1],
#        [0, 0, 0]])

eye(3, k=-1)
# Array([[0, 0, 0],
#        [1, 0, 0],
#        [0, 1, 0]])
```

---

### `identity(n)`
Create a square identity matrix.

**Parameters:**
- `n` : int
  - Number of rows and columns

**Returns:**
- `Array` : n x n identity matrix

**Notes:**
- Equivalent to `eye(n)`
- Always returns a square matrix

**Examples:**
```python
identity(3)
# Array([[1, 0, 0],
#        [0, 1, 0],
#        [0, 0, 1]])

identity(1)  # Array([[1]])
```

## Advanced Creation

### `array(data)`
Convenience function equivalent to `Array(data)`.

**Parameters:**
- `data` : array_like
  - Input data

**Returns:**
- `Array` : New array from data

**Examples:**
```python
# Same as Array() constructor
array([1, 2, 3])  # Array([1, 2, 3])
array([[1, 2], [3, 4]])  # 2D array
```

## Performance Considerations

- All creation functions are optimized with C backend
- For large arrays, creation is 4-5x faster with C extensions
- Memory is allocated contiguously for efficiency

## Common Patterns

```python
# Create coordinate grids
x = linspace(-1, 1, 100)
y = linspace(-1, 1, 100)

# Initialize before filling
result = zeros((100, 100))
for i in range(100):
    for j in range(100):
        result[i, j] = compute_value(i, j)

# Create test data
test_matrix = eye(5) * 2  # Diagonal matrix with 2s
random_like = ones((3, 3)) * random.random()  # Random values
```

## See Also

- [Array Class](array.md)
- [Array Manipulation](manipulation.md)
- [Mathematical Functions](math.md)