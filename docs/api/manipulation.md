# Array Manipulation Functions API Reference

Functions for reshaping, transposing, concatenating, and manipulating array structure.

## Shape Manipulation

### `reshape(arr, new_shape)`
Give a new shape to an array without changing its data.

**Parameters:**
- `arr` : Array
  - Input array
- `new_shape` : int or tuple of ints
  - New shape compatible with original size

**Returns:**
- `Array` : Reshaped array (view when possible)

**Examples:**
```python
import arrpy as ap

# 1D to 2D
arr = ap.arange(12)
reshaped = ap.reshape(arr, (3, 4))
# Array([[0, 1, 2, 3],
#        [4, 5, 6, 7],
#        [8, 9, 10, 11]])

# Also available as method
reshaped = arr.reshape((3, 4))

# 1D to 3D
arr_3d = arr.reshape((2, 2, 3))
# Array([[[0, 1, 2],
#         [3, 4, 5]],
#        [[6, 7, 8],
#         [9, 10, 11]]])

# Automatic dimension (-1)
reshaped = arr.reshape((-1, 4))  # Infers first dimension as 3
```

---

### `transpose(arr, axes=None)`
Reverse or permute the axes of an array.

**Parameters:**
- `arr` : Array
  - Input array
- `axes` : None or tuple of ints, optional
  - Permutation of axes (default: reverse all axes)

**Returns:**
- `Array` : Transposed array

**Examples:**
```python
# 2D transpose
matrix = ap.Array([[1, 2, 3], [4, 5, 6]])
transposed = ap.transpose(matrix)
# Array([[1, 4],
#        [2, 5],
#        [3, 6]])

# Also available as method and property
transposed = matrix.transpose()
transposed = matrix.T

# 3D with specific axes
arr_3d = ap.arange(24).reshape((2, 3, 4))
# Shape: (2, 3, 4)
transposed = ap.transpose(arr_3d, (2, 0, 1))
# Shape: (4, 2, 3)
```

---

### `squeeze(arr, axis=None)`
Remove single-dimensional entries from the shape of an array.

**Parameters:**
- `arr` : Array
  - Input array
- `axis` : None or int, optional
  - Axis to squeeze (default: all single dimensions)

**Returns:**
- `Array` : Squeezed array

**Examples:**
```python
# Remove all single dimensions
arr = ap.ones((1, 3, 1, 4, 1))
squeezed = ap.squeeze(arr)
# Shape: (3, 4)

# Remove specific axis
arr = ap.ones((1, 3, 1, 4))
squeezed = ap.squeeze(arr, axis=0)
# Shape: (3, 1, 4)

# Method form
squeezed = arr.squeeze()
```

---

### `expand_dims(arr, axis)`
Expand the shape of an array by inserting new axes.

**Parameters:**
- `arr` : Array
  - Input array
- `axis` : int or tuple of ints
  - Position(s) in the expanded axes where new axis is placed

**Returns:**
- `Array` : Array with expanded dimensions

**Examples:**
```python
arr = ap.Array([1, 2, 3])  # Shape: (3,)

# Add axis at beginning
expanded = ap.expand_dims(arr, axis=0)
# Shape: (1, 3)

# Add axis at end
expanded = ap.expand_dims(arr, axis=1)
# Shape: (3, 1)

# Add multiple axes
expanded = ap.expand_dims(arr, axis=(0, 2))
# Shape: (1, 3, 1)
```

## Array Joining

### `concatenate(arrays, axis=0)`
Join arrays along an existing axis.

**Parameters:**
- `arrays` : sequence of Arrays
  - Arrays to concatenate
- `axis` : int, optional
  - Axis along which to concatenate (default: 0)

**Returns:**
- `Array` : Concatenated array

**Examples:**
```python
# 1D concatenation
a = ap.Array([1, 2, 3])
b = ap.Array([4, 5, 6])
result = ap.concatenate([a, b])
# Array([1, 2, 3, 4, 5, 6])

# 2D concatenation along axis 0
a = ap.Array([[1, 2], [3, 4]])
b = ap.Array([[5, 6], [7, 8]])
result = ap.concatenate([a, b], axis=0)
# Array([[1, 2],
#        [3, 4],
#        [5, 6],
#        [7, 8]])

# 2D concatenation along axis 1
result = ap.concatenate([a, b], axis=1)
# Array([[1, 2, 5, 6],
#        [3, 4, 7, 8]])

# Multiple arrays
c = ap.Array([[9, 10]])
result = ap.concatenate([a, b, c], axis=0)
```

---

### `stack(arrays, axis=0)`
Join arrays along a new axis.

**Parameters:**
- `arrays` : sequence of Arrays
  - Arrays to stack (must have same shape)
- `axis` : int, optional
  - Axis along which to stack (default: 0)

**Returns:**
- `Array` : Stacked array with one more dimension

**Examples:**
```python
# Stack 1D arrays
a = ap.Array([1, 2, 3])
b = ap.Array([4, 5, 6])
result = ap.stack([a, b])
# Array([[1, 2, 3],
#        [4, 5, 6]])

# Stack along axis 1
result = ap.stack([a, b], axis=1)
# Array([[1, 4],
#        [2, 5],
#        [3, 6]])

# Stack 2D arrays
a = ap.Array([[1, 2], [3, 4]])
b = ap.Array([[5, 6], [7, 8]])
result = ap.stack([a, b])
# Array([[[1, 2],
#         [3, 4]],
#        [[5, 6],
#         [7, 8]]])
```

---

### `vstack(arrays)`
Stack arrays vertically (row-wise).

**Parameters:**
- `arrays` : sequence of Arrays
  - Arrays to stack vertically

**Returns:**
- `Array` : Vertically stacked array

**Examples:**
```python
a = ap.Array([1, 2, 3])
b = ap.Array([4, 5, 6])
result = ap.vstack([a, b])
# Array([[1, 2, 3],
#        [4, 5, 6]])

# 2D arrays
a = ap.Array([[1, 2], [3, 4]])
b = ap.Array([[5, 6]])
result = ap.vstack([a, b])
# Array([[1, 2],
#        [3, 4],
#        [5, 6]])
```

---

### `hstack(arrays)`
Stack arrays horizontally (column-wise).

**Parameters:**
- `arrays` : sequence of Arrays
  - Arrays to stack horizontally

**Returns:**
- `Array` : Horizontally stacked array

**Examples:**
```python
a = ap.Array([1, 2, 3])
b = ap.Array([4, 5, 6])
result = ap.hstack([a, b])
# Array([1, 2, 3, 4, 5, 6])

# 2D arrays
a = ap.Array([[1, 2], [3, 4]])
b = ap.Array([[5], [6]])
result = ap.hstack([a, b])
# Array([[1, 2, 5],
#        [3, 4, 6]])
```

## Array Splitting

### `split(arr, indices_or_sections, axis=0)`
Split an array into multiple sub-arrays.

**Parameters:**
- `arr` : Array
  - Input array
- `indices_or_sections` : int or sequence of ints
  - If int: number of equal sections
  - If sequence: indices where to split
- `axis` : int, optional
  - Axis along which to split (default: 0)

**Returns:**
- `list of Arrays` : List of sub-arrays

**Examples:**
```python
arr = ap.arange(9)
# Array([0, 1, 2, 3, 4, 5, 6, 7, 8])

# Split into 3 equal sections
result = ap.split(arr, 3)
# [Array([0, 1, 2]), Array([3, 4, 5]), Array([6, 7, 8])]

# Split at specific indices
result = ap.split(arr, [2, 5])
# [Array([0, 1]), Array([2, 3, 4]), Array([5, 6, 7, 8])]

# 2D split
matrix = ap.arange(12).reshape((4, 3))
result = ap.split(matrix, 2, axis=0)
# [Array([[0, 1, 2], [3, 4, 5]]), Array([[6, 7, 8], [9, 10, 11]])]
```

---

### `vsplit(arr, indices_or_sections)`
Split array vertically (row-wise).

**Parameters:**
- `arr` : Array
  - Input array (must be at least 2D)
- `indices_or_sections` : int or sequence
  - Split specification

**Returns:**
- `list of Arrays` : Vertically split arrays

**Examples:**
```python
matrix = ap.arange(12).reshape((4, 3))
result = ap.vsplit(matrix, 2)
# [Array([[0, 1, 2], [3, 4, 5]]), Array([[6, 7, 8], [9, 10, 11]])]

# Split at specific rows
result = ap.vsplit(matrix, [1, 3])
# [Array([[0, 1, 2]]), Array([[3, 4, 5], [6, 7, 8]]), Array([[9, 10, 11]])]
```

---

### `hsplit(arr, indices_or_sections)`
Split array horizontally (column-wise).

**Parameters:**
- `arr` : Array
  - Input array
- `indices_or_sections` : int or sequence
  - Split specification

**Returns:**
- `list of Arrays` : Horizontally split arrays

**Examples:**
```python
matrix = ap.arange(12).reshape((3, 4))
result = ap.hsplit(matrix, 2)
# [Array([[0, 1], [4, 5], [8, 9]]), Array([[2, 3], [6, 7], [10, 11]])]

# Split at specific columns
result = ap.hsplit(matrix, [1, 3])
# [Array([[0], [4], [8]]), Array([[1, 2], [5, 6], [9, 10]]), Array([[3], [7], [11]])]
```

## Array Tiling and Repeating

### `tile(arr, reps)`
Construct an array by repeating arr the number of times given by reps.

**Parameters:**
- `arr` : Array
  - Input array
- `reps` : int or tuple of ints
  - Number of repetitions along each axis

**Returns:**
- `Array` : Tiled array

**Examples:**
```python
arr = ap.Array([1, 2])

# Repeat along 1D
result = ap.tile(arr, 3)
# Array([1, 2, 1, 2, 1, 2])

# Repeat in 2D
result = ap.tile(arr, (2, 3))
# Array([[1, 2, 1, 2, 1, 2],
#        [1, 2, 1, 2, 1, 2]])

# 2D input
arr = ap.Array([[1, 2], [3, 4]])
result = ap.tile(arr, (2, 1))
# Array([[1, 2],
#        [3, 4],
#        [1, 2],
#        [3, 4]])
```

---

### `repeat(arr, repeats, axis=None)`
Repeat elements of an array.

**Parameters:**
- `arr` : Array
  - Input array
- `repeats` : int or array of ints
  - Number of repetitions for each element
- `axis` : int, optional
  - Axis along which to repeat (default: flatten then repeat)

**Returns:**
- `Array` : Array with repeated elements

**Examples:**
```python
arr = ap.Array([1, 2, 3])

# Repeat each element
result = ap.repeat(arr, 2)
# Array([1, 1, 2, 2, 3, 3])

# Different repetitions per element
result = ap.repeat(arr, [2, 1, 3])
# Array([1, 1, 2, 3, 3, 3])

# 2D repeat along axis
arr = ap.Array([[1, 2], [3, 4]])
result = ap.repeat(arr, 2, axis=0)
# Array([[1, 2],
#        [1, 2],
#        [3, 4],
#        [3, 4]])

result = ap.repeat(arr, 2, axis=1)
# Array([[1, 1, 2, 2],
#        [3, 3, 4, 4]])
```

## Flipping and Rotating

### `flip(arr, axis=None)`
Reverse the order of elements along given axis.

**Parameters:**
- `arr` : Array
  - Input array
- `axis` : None, int, or tuple of ints, optional
  - Axis or axes to flip (default: all axes)

**Returns:**
- `Array` : Flipped array

**Examples:**
```python
arr = ap.Array([1, 2, 3, 4])
result = ap.flip(arr)
# Array([4, 3, 2, 1])

# 2D flip
matrix = ap.Array([[1, 2, 3], [4, 5, 6]])

# Flip rows
result = ap.flip(matrix, axis=0)
# Array([[4, 5, 6],
#        [1, 2, 3]])

# Flip columns
result = ap.flip(matrix, axis=1)
# Array([[3, 2, 1],
#        [6, 5, 4]])

# Flip both axes
result = ap.flip(matrix)
# Array([[6, 5, 4],
#        [3, 2, 1]])
```

---

### `fliplr(arr)`
Flip array left to right (horizontally).

**Parameters:**
- `arr` : Array
  - Input array (must be at least 2D)

**Returns:**
- `Array` : Horizontally flipped array

**Examples:**
```python
matrix = ap.Array([[1, 2, 3], [4, 5, 6]])
result = ap.fliplr(matrix)
# Array([[3, 2, 1],
#        [6, 5, 4]])
```

---

### `flipud(arr)`
Flip array up to down (vertically).

**Parameters:**
- `arr` : Array
  - Input array (must be at least 1D)

**Returns:**
- `Array` : Vertically flipped array

**Examples:**
```python
matrix = ap.Array([[1, 2, 3], [4, 5, 6]])
result = ap.flipud(matrix)
# Array([[4, 5, 6],
#        [1, 2, 3]])
```

---

### `rot90(arr, k=1, axes=(0, 1))`
Rotate array by 90 degrees in the plane specified by axes.

**Parameters:**
- `arr` : Array
  - Input array
- `k` : int, optional
  - Number of 90-degree rotations (default: 1)
- `axes` : tuple of 2 ints, optional
  - Plane of rotation (default: (0, 1))

**Returns:**
- `Array` : Rotated array

**Examples:**
```python
matrix = ap.Array([[1, 2], [3, 4]])

# 90 degrees counterclockwise
result = ap.rot90(matrix)
# Array([[2, 4],
#        [1, 3]])

# 180 degrees
result = ap.rot90(matrix, k=2)
# Array([[4, 3],
#        [2, 1]])

# 270 degrees (or -90 degrees)
result = ap.rot90(matrix, k=3)
# Array([[3, 1],
#        [4, 2]])
```

## Reshaping Utilities

### `flatten(arr)`
Return a copy of the array collapsed into one dimension.

**Parameters:**
- `arr` : Array
  - Input array

**Returns:**
- `Array` : 1D copy of the input

**Examples:**
```python
matrix = ap.Array([[1, 2, 3], [4, 5, 6]])
result = ap.flatten(matrix)
# Array([1, 2, 3, 4, 5, 6])

# Also available as method
result = matrix.flatten()
```

---

### `ravel(arr)`
Return a flattened array (view when possible).

**Parameters:**
- `arr` : Array
  - Input array

**Returns:**
- `Array` : 1D view or copy of the input

**Examples:**
```python
matrix = ap.Array([[1, 2, 3], [4, 5, 6]])
result = ap.ravel(matrix)
# Array([1, 2, 3, 4, 5, 6])

# Modifications affect original when possible
result[0] = 99
# matrix is now [[99, 2, 3], [4, 5, 6]]
```

## Manipulation Examples

### Complex Reshaping Operations

```python
# Create test data
data = ap.arange(24).reshape((2, 3, 4))
print(f"Original shape: {data.shape}")  # (2, 3, 4)

# Transpose to move last axis first
transposed = data.transpose((2, 0, 1))
print(f"Transposed shape: {transposed.shape}")  # (4, 2, 3)

# Flatten and reshape differently
flattened = data.flatten()
reshaped = flattened.reshape((4, 6))
print(f"New shape: {reshaped.shape}")  # (4, 6)
```

### Array Assembly

```python
# Create building blocks
block1 = ap.ones((2, 2))
block2 = ap.zeros((2, 2))
block3 = ap.eye(2)

# Horizontal assembly
top_row = ap.hstack([block1, block2])
bottom_row = ap.hstack([block3, block1])

# Vertical assembly
assembled = ap.vstack([top_row, bottom_row])
print(f"Assembled matrix:\n{assembled}")
```

### Data Preparation

```python
# Prepare time series data
time_series = ap.arange(100)

# Split into training/test sets
train_data, test_data = ap.split(time_series, [80])
print(f"Training: {len(train_data[0])}, Test: {len(train_data[1])}")

# Reshape for batch processing
batched = train_data[0].reshape((-1, 10))  # 10-sample batches
print(f"Batch shape: {batched.shape}")
```

## Performance Notes

- Reshaping operations return views when possible (no data copying)
- C extensions provide 3-10x speedup for manipulation functions
- Memory layout optimizations for cache efficiency
- Large array operations are optimized with SIMD instructions

## Function Availability

| Function | Standalone | Method | Notes |
|----------|------------|--------|-------|
| reshape | ✓ | ✓ | `ap.reshape(arr, shape)` or `arr.reshape(shape)` |
| transpose | ✓ | ✓ | `ap.transpose(arr)`, `arr.transpose()`, or `arr.T` |
| squeeze | ✓ | ✓ | `ap.squeeze(arr)` or `arr.squeeze()` |
| flatten | ✓ | ✓ | `ap.flatten(arr)` or `arr.flatten()` |
| concatenate | ✓ | ✗ | Only `ap.concatenate(arrays, axis)` |
| stack | ✓ | ✗ | Only `ap.stack(arrays, axis)` |
| split | ✓ | ✗ | Only `ap.split(arr, sections, axis)` |

## Error Handling

```python
# Shape compatibility errors
try:
    arr = ap.arange(10)
    result = arr.reshape((3, 4))  # 10 elements can't fit in 3x4
except ValueError as e:
    print(f"Reshape error: {e}")

# Axis out of bounds
try:
    arr = ap.Array([1, 2, 3])
    result = ap.split(arr, 2, axis=1)  # 1D array has no axis 1
except IndexError as e:
    print(f"Axis error: {e}")

# Incompatible arrays for concatenation
try:
    a = ap.Array([[1, 2]])     # Shape: (1, 2)
    b = ap.Array([[1, 2, 3]])  # Shape: (1, 3)
    result = ap.concatenate([a, b], axis=0)
except ValueError as e:
    print(f"Concatenation error: {e}")
```

## See Also

- [Array Class](array.md) - For array methods
- [Array Creation](creation.md) - For creating arrays
- [Mathematical Functions](math.md) - For element-wise operations
- [Statistical Functions](statistics.md) - For data analysis