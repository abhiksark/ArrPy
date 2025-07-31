# Array Class API Reference

The `Array` class is the core data structure in ArrPy, representing n-dimensional arrays.

## Class Definition

```python
class Array:
    """
    N-dimensional array object for numerical computing.
    
    Parameters
    ----------
    data : array_like
        Input data as nested Python lists or sequences.
        
    Attributes
    ----------
    shape : tuple
        Dimensions of the array
    size : int
        Total number of elements
    ndim : int
        Number of dimensions
    """
```

## Constructor

### `Array(data)`

Create a new array from input data.

**Parameters:**
- `data` : list, tuple, or nested sequences
  - Input data to create array from

**Returns:**
- `Array` : New array object

**Examples:**
```python
# 1D array
arr1 = Array([1, 2, 3, 4, 5])

# 2D array
arr2 = Array([[1, 2, 3], 
              [4, 5, 6]])

# 3D array
arr3 = Array([[[1, 2], [3, 4]], 
              [[5, 6], [7, 8]]])
```

## Properties

### `shape`
Tuple of array dimensions.

```python
arr = Array([[1, 2, 3], [4, 5, 6]])
print(arr.shape)  # (2, 3)
```

### `size`
Total number of elements in the array.

```python
arr = Array([[1, 2, 3], [4, 5, 6]])
print(arr.size)  # 6
```

### `ndim`
Number of array dimensions.

```python
arr = Array([[1, 2, 3], [4, 5, 6]])
print(arr.ndim)  # 2
```

### `T`
Transposed array (2D only).

```python
arr = Array([[1, 2, 3], [4, 5, 6]])
print(arr.T)  # [[1, 4], [2, 5], [3, 6]]
```

## Indexing and Slicing

### `__getitem__(key)`
Access array elements using square bracket notation.

**1D Indexing:**
```python
arr = Array([1, 2, 3, 4, 5])
print(arr[0])    # 1
print(arr[-1])   # 5
print(arr[1:4])  # Array([2, 3, 4])
```

**2D Indexing:**
```python
arr = Array([[1, 2, 3], [4, 5, 6]])
print(arr[0, 1])    # 2
print(arr[1, :])    # Array([4, 5, 6])
print(arr[:, 2])    # Array([3, 6])
```

### `__setitem__(key, value)`
Set array elements.

```python
arr = Array([1, 2, 3])
arr[1] = 10
print(arr)  # Array([1, 10, 3])
```

## Arithmetic Operations

All arithmetic operations are element-wise.

### `__add__(other)` / `__radd__(other)`
Addition with scalar or array.

```python
arr = Array([1, 2, 3])
print(arr + 5)              # Array([6, 7, 8])
print(arr + Array([4, 5, 6]))  # Array([5, 7, 9])
```

### `__sub__(other)` / `__rsub__(other)`
Subtraction with scalar or array.

```python
arr = Array([5, 6, 7])
print(arr - 2)              # Array([3, 4, 5])
print(arr - Array([1, 2, 3]))  # Array([4, 4, 4])
```

### `__mul__(other)` / `__rmul__(other)`
Element-wise multiplication.

```python
arr = Array([2, 3, 4])
print(arr * 3)              # Array([6, 9, 12])
print(arr * Array([1, 2, 3]))  # Array([2, 6, 12])
```

### `__truediv__(other)` / `__rtruediv__(other)`
Element-wise division.

```python
arr = Array([6, 8, 10])
print(arr / 2)              # Array([3.0, 4.0, 5.0])
```

### `__pow__(other)`
Element-wise power.

```python
arr = Array([2, 3, 4])
print(arr ** 2)  # Array([4, 9, 16])
```

### `__neg__()`
Negation.

```python
arr = Array([1, -2, 3])
print(-arr)  # Array([-1, 2, -3])
```

## Comparison Operations

All comparison operations return boolean arrays.

### `__eq__(other)`
Element-wise equality.

```python
arr = Array([1, 2, 3])
print(arr == 2)  # Array([False, True, False])
```

### `__ne__(other)`
Element-wise inequality.

```python
arr = Array([1, 2, 3])
print(arr != 2)  # Array([True, False, True])
```

### `__lt__(other)`, `__le__(other)`, `__gt__(other)`, `__ge__(other)`
Element-wise comparisons.

```python
arr = Array([1, 2, 3])
print(arr > 2)   # Array([False, False, True])
print(arr <= 2)  # Array([True, True, False])
```

## Mathematical Methods

### `sum()`
Sum of array elements.

**Returns:**
- `float` or `int` : Sum of all elements

```python
arr = Array([1, 2, 3, 4])
print(arr.sum())  # 10
```

### `mean()`
Average of array elements.

**Returns:**
- `float` : Mean value

```python
arr = Array([1, 2, 3, 4])
print(arr.mean())  # 2.5
```

### `min()` / `max()`
Minimum/maximum element.

**Returns:**
- Minimum or maximum value

```python
arr = Array([3, 1, 4, 1, 5])
print(arr.min())  # 1
print(arr.max())  # 5
```

### `std(ddof=0)` / `var(ddof=0)`
Standard deviation and variance.

**Parameters:**
- `ddof` : int, optional
  - Delta degrees of freedom (default: 0)

**Returns:**
- `float` : Standard deviation or variance

```python
arr = Array([1, 2, 3, 4, 5])
print(arr.std())   # 1.414...
print(arr.var())   # 2.0
```

### `dot(other)`
Matrix multiplication.

**Parameters:**
- `other` : Array
  - Second array for multiplication

**Returns:**
- `Array` : Result of matrix multiplication

```python
A = Array([[1, 2], [3, 4]])
B = Array([[5, 6], [7, 8]])
print(A.dot(B))  # [[19, 22], [43, 50]]
```

### `reshape(new_shape)`
Return array with new shape.

**Parameters:**
- `new_shape` : tuple
  - New dimensions for the array

**Returns:**
- `Array` : Reshaped array

```python
arr = Array([1, 2, 3, 4, 5, 6])
reshaped = arr.reshape((2, 3))
# [[1, 2, 3],
#  [4, 5, 6]]
```

### `sqrt()`
Element-wise square root.

**Returns:**
- `Array` : Square root of each element

```python
arr = Array([1, 4, 9, 16])
print(arr.sqrt())  # Array([1.0, 2.0, 3.0, 4.0])
```

### `exp()` / `log()`
Element-wise exponential and natural logarithm.

```python
arr = Array([1, 2, 3])
print(arr.exp())  # Array([2.718..., 7.389..., 20.085...])
print(arr.log())  # Array([0, 0.693..., 1.098...])
```

### `sin()` / `cos()`
Element-wise trigonometric functions.

```python
import math
arr = Array([0, math.pi/2, math.pi])
print(arr.sin())  # Array([0, 1, 0])
print(arr.cos())  # Array([1, 0, -1])
```

## String Representation

### `__str__()` / `__repr__()`
String representation of the array.

```python
arr = Array([[1, 2], [3, 4]])
print(str(arr))
# [[1 2]
#  [3 4]]
```

## Type Conversion

### `__float__()` / `__int__()`
Convert single-element array to scalar.

```python
arr = Array([3.14])
print(float(arr))  # 3.14
print(int(arr))    # 3
```

## Special Methods

### `__len__()`
Length of the first dimension.

```python
arr = Array([[1, 2], [3, 4], [5, 6]])
print(len(arr))  # 3
```

### `__iter__()`
Iterate over first dimension.

```python
arr = Array([[1, 2], [3, 4]])
for row in arr:
    print(row)  # Array([1, 2]), then Array([3, 4])
```

### `__contains__(item)`
Check if item is in array.

```python
arr = Array([1, 2, 3, 4])
print(3 in arr)  # True
print(5 in arr)  # False
```

## Performance Notes

- With C extensions enabled, array operations are 4-170x faster
- Memory usage is optimized with contiguous storage
- Use vectorized operations instead of loops for best performance

## See Also

- [Array Creation Functions](creation.md)
- [Mathematical Functions](math.md)
- [Statistical Functions](statistics.md)