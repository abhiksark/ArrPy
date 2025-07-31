# Mathematical Functions API Reference

Mathematical functions that operate element-wise on arrays.

## Trigonometric Functions

### `sin(arr)`
Element-wise sine function.

**Parameters:**
- `arr` : Array
  - Input array in radians

**Returns:**
- `Array` : Sine of each element

**Examples:**
```python
import arrpy as ap
import math

angles = ap.Array([0, math.pi/6, math.pi/4, math.pi/2])
result = ap.sin(angles)
# Array([0, 0.5, 0.707, 1.0])

# Also available as method
result = angles.sin()
```

---

### `cos(arr)`
Element-wise cosine function.

**Parameters:**
- `arr` : Array
  - Input array in radians

**Returns:**
- `Array` : Cosine of each element

**Examples:**
```python
angles = ap.Array([0, math.pi/3, math.pi/2, math.pi])
result = ap.cos(angles)
# Array([1.0, 0.5, 0, -1.0])
```

---

### `tan(arr)`
Element-wise tangent function.

**Parameters:**
- `arr` : Array
  - Input array in radians

**Returns:**
- `Array` : Tangent of each element

**Examples:**
```python
angles = ap.Array([0, math.pi/4, math.pi/3])
result = ap.tan(angles)
# Array([0, 1.0, 1.732])
```

## Inverse Trigonometric Functions

### `arcsin(arr)`
Element-wise inverse sine (arcsine).

**Parameters:**
- `arr` : Array
  - Input array with values in [-1, 1]

**Returns:**
- `Array` : Arcsine in radians, values in [-π/2, π/2]

**Examples:**
```python
values = ap.Array([-1, -0.5, 0, 0.5, 1])
result = ap.arcsin(values)
# Array([-1.571, -0.524, 0, 0.524, 1.571])
```

---

### `arccos(arr)`
Element-wise inverse cosine (arccosine).

**Parameters:**
- `arr` : Array
  - Input array with values in [-1, 1]

**Returns:**
- `Array` : Arccosine in radians, values in [0, π]

**Examples:**
```python
values = ap.Array([-1, 0, 1])
result = ap.arccos(values)
# Array([3.142, 1.571, 0])
```

---

### `arctan(arr)`
Element-wise inverse tangent (arctangent).

**Parameters:**
- `arr` : Array
  - Input array

**Returns:**
- `Array` : Arctangent in radians, values in [-π/2, π/2]

**Examples:**
```python
values = ap.Array([-1, 0, 1, float('inf')])
result = ap.arctan(values)
# Array([-0.785, 0, 0.785, 1.571])
```

## Exponential and Logarithmic Functions

### `exp(arr)`
Element-wise exponential function (e^x).

**Parameters:**
- `arr` : Array
  - Input array

**Returns:**
- `Array` : Exponential of each element

**Examples:**
```python
x = ap.Array([0, 1, 2, 3])
result = ap.exp(x)
# Array([1.0, 2.718, 7.389, 20.086])

# Also available as method
result = x.exp()
```

---

### `log(arr)`
Element-wise natural logarithm.

**Parameters:**
- `arr` : Array
  - Input array with positive values

**Returns:**
- `Array` : Natural logarithm of each element

**Examples:**
```python
x = ap.Array([1, 2, math.e, 10])
result = ap.log(x)
# Array([0, 0.693, 1.0, 2.303])

# Also available as method
result = x.log()
```

---

### `log10(arr)`
Element-wise base-10 logarithm.

**Parameters:**
- `arr` : Array
  - Input array with positive values

**Returns:**
- `Array` : Base-10 logarithm of each element

**Examples:**
```python
x = ap.Array([1, 10, 100, 1000])
result = ap.log10(x)
# Array([0, 1, 2, 3])
```

---

### `log2(arr)`
Element-wise base-2 logarithm.

**Parameters:**
- `arr` : Array
  - Input array with positive values

**Returns:**
- `Array` : Base-2 logarithm of each element

**Examples:**
```python
x = ap.Array([1, 2, 4, 8, 16])
result = ap.log2(x)
# Array([0, 1, 2, 3, 4])
```

---

### `sqrt(arr)`
Element-wise square root.

**Parameters:**
- `arr` : Array
  - Input array with non-negative values

**Returns:**
- `Array` : Square root of each element

**Examples:**
```python
x = ap.Array([0, 1, 4, 9, 16, 25])
result = ap.sqrt(x)
# Array([0, 1, 2, 3, 4, 5])

# Also available as method
result = x.sqrt()
```

## Arithmetic Functions

### `power(arr1, arr2)`
Element-wise power function.

**Parameters:**
- `arr1` : Array
  - Base array
- `arr2` : Array or scalar
  - Exponent array or scalar

**Returns:**
- `Array` : arr1 raised to the power of arr2

**Examples:**
```python
base = ap.Array([2, 3, 4])
exponent = ap.Array([2, 3, 2])
result = ap.power(base, exponent)
# Array([4, 27, 16])

# Scalar exponent
result = ap.power(base, 3)
# Array([8, 27, 64])
```

---

### `absolute(arr)`
Element-wise absolute value.

**Parameters:**
- `arr` : Array
  - Input array

**Returns:**
- `Array` : Absolute value of each element

**Examples:**
```python
x = ap.Array([-3, -1, 0, 1, 3])
result = ap.absolute(x)
# Array([3, 1, 0, 1, 3])

# Also works with alias
result = ap.abs(x)
```

---

### `sign(arr)`
Element-wise sign function.

**Parameters:**
- `arr` : Array
  - Input array

**Returns:**
- `Array` : Sign of each element (-1, 0, or 1)

**Examples:**
```python
x = ap.Array([-5, -0.1, 0, 0.1, 5])
result = ap.sign(x)
# Array([-1, -1, 0, 1, 1])
```

---

### `floor_divide(arr1, arr2)`
Element-wise floor division.

**Parameters:**
- `arr1` : Array
  - Dividend array
- `arr2` : Array or scalar
  - Divisor array or scalar

**Returns:**
- `Array` : Floor division result

**Examples:**
```python
dividend = ap.Array([7, 8, 9, 10])
divisor = ap.Array([2, 3, 2, 3])
result = ap.floor_divide(dividend, divisor)
# Array([3, 2, 4, 3])

# Scalar divisor
result = ap.floor_divide(dividend, 3)
# Array([2, 2, 3, 3])
```

---

### `mod(arr1, arr2)`
Element-wise modulo operation.

**Parameters:**
- `arr1` : Array
  - Dividend array
- `arr2` : Array or scalar
  - Divisor array or scalar

**Returns:**
- `Array` : Remainder of division

**Examples:**
```python
dividend = ap.Array([7, 8, 9, 10])
divisor = ap.Array([3, 3, 4, 3])
result = ap.mod(dividend, divisor)
# Array([1, 2, 1, 1])

# Scalar divisor
result = ap.mod(dividend, 3)
# Array([1, 2, 0, 1])
```

## Rounding Functions

### `floor(arr)`
Element-wise floor function.

**Parameters:**
- `arr` : Array
  - Input array

**Returns:**
- `Array` : Largest integer less than or equal to each element

**Examples:**
```python
x = ap.Array([1.2, 2.7, -1.5, -2.3])
result = ap.floor(x)
# Array([1, 2, -2, -3])
```

---

### `ceil(arr)`
Element-wise ceiling function.

**Parameters:**
- `arr` : Array
  - Input array

**Returns:**
- `Array` : Smallest integer greater than or equal to each element

**Examples:**
```python
x = ap.Array([1.2, 2.7, -1.5, -2.3])
result = ap.ceil(x)
# Array([2, 3, -1, -2])
```

---

### `round(arr)`
Element-wise rounding function.

**Parameters:**
- `arr` : Array
  - Input array

**Returns:**
- `Array` : Rounded values to nearest integer

**Examples:**
```python
x = ap.Array([1.2, 1.5, 1.7, 2.5])
result = ap.round(x)
# Array([1, 2, 2, 2])  # Note: rounds 0.5 to nearest even
```

---

### `trunc(arr)`
Element-wise truncation function.

**Parameters:**
- `arr` : Array
  - Input array

**Returns:**
- `Array` : Truncated values (toward zero)

**Examples:**
```python
x = ap.Array([1.7, -1.7, 2.3, -2.3])
result = ap.trunc(x)
# Array([1, -1, 2, -2])
```

## Function vs Method Usage

Most mathematical functions are available both as standalone functions and as array methods:

```python
# Function syntax
result = ap.sin(arr)
result = ap.exp(arr)
result = ap.sqrt(arr)

# Method syntax (when available)
result = arr.sin()
result = arr.exp()
result = arr.sqrt()

# Both produce identical results
```

## Performance Notes

- All functions are optimized with C backend when available
- With C extensions: 10-50x faster than pure Python
- Functions operate element-wise in vectorized fashion
- Memory usage is optimized for large arrays

## Error Handling

```python
# Domain errors
try:
    result = ap.sqrt(ap.Array([-1, 4]))  # Negative square root
except ValueError as e:
    print(f"Domain error: {e}")

try:
    result = ap.log(ap.Array([0, 1]))  # Log of zero
except ValueError as e:
    print(f"Domain error: {e}")

# Input validation
try:
    result = ap.sin("not_an_array")
except TypeError as e:
    print(f"Type error: {e}")
```

## Constants

Common mathematical constants are available:

```python
# Access through math module or define
import math
pi = math.pi
e = math.e

# Use in computations
angles = ap.linspace(0, 2*pi, 100)
sine_wave = ap.sin(angles)
```

## See Also

- [Array Class](array.md) - For array methods
- [Statistical Functions](statistics.md) - For statistical operations
- [Array Creation](creation.md) - For creating test arrays