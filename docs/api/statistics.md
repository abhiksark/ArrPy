# Statistical Functions API Reference

Functions for statistical analysis and data aggregation.

## Basic Aggregation Functions

### `sum(arr, axis=None)`
Sum of array elements.

**Parameters:**
- `arr` : Array
  - Input array
- `axis` : int, optional
  - Axis along which to sum (not fully implemented)

**Returns:**
- `float` or `int` : Sum of all elements

**Examples:**
```python
import arrpy as ap

# 1D array
arr = ap.Array([1, 2, 3, 4, 5])
total = ap.sum(arr)  # 15

# Also available as method
total = arr.sum()  # 15

# 2D array
matrix = ap.Array([[1, 2, 3], [4, 5, 6]])
total = matrix.sum()  # 21
```

---

### `mean(arr, axis=None)`
Arithmetic mean of array elements.

**Parameters:**
- `arr` : Array
  - Input array
- `axis` : int, optional
  - Axis along which to compute mean (not fully implemented)

**Returns:**
- `float` : Arithmetic mean

**Examples:**
```python
arr = ap.Array([1, 2, 3, 4, 5])
average = ap.mean(arr)  # 3.0

# Method form
average = arr.mean()  # 3.0

# With decimals
arr = ap.Array([1.5, 2.5, 3.5])
average = arr.mean()  # 2.5
```

---

### `min(arr, axis=None)`
Minimum value in array.

**Parameters:**
- `arr` : Array
  - Input array
- `axis` : int, optional
  - Axis along which to find minimum (not fully implemented)

**Returns:**
- Minimum value

**Examples:**
```python
arr = ap.Array([3, 1, 4, 1, 5])
minimum = ap.min(arr)  # 1

# Method form
minimum = arr.min()  # 1

# With negative numbers
arr = ap.Array([-2, -1, 0, 1])
minimum = arr.min()  # -2
```

---

### `max(arr, axis=None)`
Maximum value in array.

**Parameters:**
- `arr` : Array
  - Input array
- `axis` : int, optional
  - Axis along which to find maximum (not fully implemented)

**Returns:**
- Maximum value

**Examples:**
```python
arr = ap.Array([3, 1, 4, 1, 5])
maximum = ap.max(arr)  # 5

# Method form
maximum = arr.max()  # 5
```

## Variance and Standard Deviation

### `var(arr, ddof=0)`
Variance of array elements.

**Parameters:**
- `arr` : Array
  - Input array
- `ddof` : int, optional
  - Delta degrees of freedom (default: 0)
  - Use ddof=1 for sample variance

**Returns:**
- `float` : Variance

**Examples:**
```python
arr = ap.Array([1, 2, 3, 4, 5])

# Population variance
pop_var = ap.var(arr)  # 2.0
pop_var = arr.var()    # Same result

# Sample variance
sample_var = arr.var(ddof=1)  # 2.5

# Manual calculation verification
mean_val = arr.mean()
manual_var = ap.sum((arr - mean_val) ** 2) / arr.size
```

---

### `std(arr, ddof=0)`
Standard deviation of array elements.

**Parameters:**
- `arr` : Array
  - Input array
- `ddof` : int, optional
  - Delta degrees of freedom (default: 0)

**Returns:**
- `float` : Standard deviation

**Examples:**
```python
arr = ap.Array([1, 2, 3, 4, 5])

# Population standard deviation
pop_std = ap.std(arr)  # 1.414...
pop_std = arr.std()    # Same result

# Sample standard deviation
sample_std = arr.std(ddof=1)  # 1.581...

# Relationship to variance
variance = arr.var()
std_dev = ap.sqrt(ap.Array([variance]))[0]
```

## Advanced Statistical Functions

### `prod(arr)`
Product of array elements.

**Parameters:**
- `arr` : Array
  - Input array

**Returns:**
- Product of all elements

**Examples:**
```python
arr = ap.Array([1, 2, 3, 4])
product = ap.prod(arr)  # 24

# Empty array
empty = ap.Array([])
product = ap.prod(empty)  # 1 (identity for multiplication)

# With zeros
arr = ap.Array([1, 2, 0, 4])
product = ap.prod(arr)  # 0
```

---

### `median(arr)`
Median value of array elements.

**Parameters:**
- `arr` : Array
  - Input array

**Returns:**
- `float` : Median value

**Examples:**
```python
# Odd number of elements
arr = ap.Array([1, 3, 2, 5, 4])
med = ap.median(arr)  # 3.0

# Even number of elements
arr = ap.Array([1, 2, 3, 4])
med = ap.median(arr)  # 2.5 (average of middle two)

# Already sorted
arr = ap.Array([1, 2, 3, 4, 5])
med = ap.median(arr)  # 3.0
```

---

### `percentile(arr, q)`
Percentile of array elements.

**Parameters:**
- `arr` : Array
  - Input array
- `q` : float
  - Percentile to compute (0-100)

**Returns:**
- `float` : Percentile value

**Examples:**
```python
arr = ap.Array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Common percentiles
q25 = ap.percentile(arr, 25)    # 3.25 (1st quartile)
q50 = ap.percentile(arr, 50)    # 5.5  (median)
q75 = ap.percentile(arr, 75)    # 7.75 (3rd quartile)

# Extreme percentiles
q10 = ap.percentile(arr, 10)    # 1.9
q90 = ap.percentile(arr, 90)    # 9.1
```

## Cumulative Functions

### `cumsum(arr)`
Cumulative sum of array elements.

**Parameters:**
- `arr` : Array
  - Input array

**Returns:**
- `Array` : Cumulative sum array

**Examples:**
```python
arr = ap.Array([1, 2, 3, 4, 5])
cum_sum = ap.cumsum(arr)
# Array([1, 3, 6, 10, 15])

# 2D array (flattened)
matrix = ap.Array([[1, 2], [3, 4]])
cum_sum = ap.cumsum(matrix)
# Array([1, 3, 6, 10])
```

---

### `cumprod(arr)`
Cumulative product of array elements.

**Parameters:**
- `arr` : Array
  - Input array

**Returns:**
- `Array` : Cumulative product array

**Examples:**
```python
arr = ap.Array([1, 2, 3, 4])
cum_prod = ap.cumprod(arr)
# Array([1, 2, 6, 24])

# With fractions
arr = ap.Array([2, 0.5, 3, 0.25])
cum_prod = ap.cumprod(arr)
# Array([2, 1.0, 3.0, 0.75])
```

## Index Functions

### `argmin(arr)`
Indices of minimum values.

**Parameters:**
- `arr` : Array
  - Input array

**Returns:**
- `int` : Index of minimum value

**Examples:**
```python
arr = ap.Array([3, 1, 4, 1, 5])
min_idx = ap.argmin(arr)  # 1 (first occurrence)

# 2D array (returns flat index)
matrix = ap.Array([[3, 1], [4, 0]])
min_idx = ap.argmin(matrix)  # 3 (index in flattened array)
```

---

### `argmax(arr)`
Indices of maximum values.

**Parameters:**
- `arr` : Array
  - Input array

**Returns:**
- `int` : Index of maximum value

**Examples:**
```python
arr = ap.Array([3, 1, 4, 1, 5])
max_idx = ap.argmax(arr)  # 4

# With ties (returns first occurrence)
arr = ap.Array([5, 1, 5, 1, 3])
max_idx = ap.argmax(arr)  # 0
```

## Statistical Analysis Examples

### Descriptive Statistics

```python
# Generate sample data
data = ap.Array([12, 15, 18, 22, 25, 28, 30, 35, 40, 45])

# Basic statistics
print(f"Count: {data.size}")
print(f"Mean: {data.mean():.2f}")
print(f"Median: {ap.median(data):.2f}")
print(f"Min: {data.min()}")
print(f"Max: {data.max()}")
print(f"Range: {data.max() - data.min()}")

# Variability
print(f"Variance: {data.var():.2f}")
print(f"Std Dev: {data.std():.2f}")

# Quartiles
print(f"Q1: {ap.percentile(data, 25):.2f}")
print(f"Q3: {ap.percentile(data, 75):.2f}")
print(f"IQR: {ap.percentile(data, 75) - ap.percentile(data, 25):.2f}")
```

### Data Distribution Analysis

```python
# Analyze distribution shape
def analyze_distribution(data):
    mean_val = data.mean()
    median_val = ap.median(data)
    
    print(f"Mean: {mean_val:.2f}")
    print(f"Median: {median_val:.2f}")
    
    if abs(mean_val - median_val) < 0.1:
        print("Distribution appears symmetric")
    elif mean_val > median_val:
        print("Distribution appears right-skewed")
    else:
        print("Distribution appears left-skewed")

# Example usage
data = ap.Array([1, 2, 2, 3, 3, 3, 4, 4, 5])
analyze_distribution(data)
```

### Moving Statistics

```python
def moving_average(data, window_size):
    """Calculate moving average."""
    if window_size > data.size:
        return data.mean()
    
    result = []
    for i in range(data.size - window_size + 1):
        window = data[i:i+window_size]
        result.append(window.mean())
    
    return ap.Array(result)

# Example
time_series = ap.Array([1, 3, 2, 4, 3, 5, 4, 6, 5, 7])
ma_3 = moving_average(time_series, 3)
print(f"3-period moving average: {ma_3}")
```

## Performance Notes

- All statistical functions are optimized with C backend
- Aggregation functions are 20-50x faster with C extensions
- Memory usage is optimized for large datasets
- Functions handle edge cases (empty arrays, single elements)

## Function vs Method Availability

| Function | Standalone | Method | Notes |
|----------|------------|--------|-------|
| sum | ✓ | ✓ | `ap.sum(arr)` or `arr.sum()` |
| mean | ✓ | ✓ | `ap.mean(arr)` or `arr.mean()` |
| min | ✓ | ✓ | `ap.min(arr)` or `arr.min()` |
| max | ✓ | ✓ | `ap.max(arr)` or `arr.max()` |
| std | ✓ | ✓ | `ap.std(arr)` or `arr.std()` |
| var | ✓ | ✓ | `ap.var(arr)` or `arr.var()` |
| median | ✓ | ✓ | `ap.median(arr)` or `arr.median()` |
| prod | ✓ | ✗ | Only `ap.prod(arr)` |
| cumsum | ✓ | ✗ | Only `ap.cumsum(arr)` |
| argmin | ✓ | ✗ | Only `ap.argmin(arr)` |

## Error Handling

```python
# Empty array handling
empty = ap.Array([])
try:
    result = empty.mean()  # Returns NaN or raises error
except ValueError as e:
    print(f"Cannot compute mean of empty array: {e}")

# Invalid percentile
try:
    result = ap.percentile(arr, 150)  # Invalid percentile
except ValueError as e:
    print(f"Invalid percentile: {e}")

# Type validation
try:
    result = ap.sum("not_an_array")
except TypeError as e:
    print(f"Type error: {e}")
```

## See Also

- [Array Class](array.md) - For array methods
- [Mathematical Functions](math.md) - For element-wise operations
- [Array Creation](creation.md) - For creating test data