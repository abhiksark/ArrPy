# ArrPy Quick Start Guide

Get started with ArrPy in just 5 minutes! This guide covers the essentials to begin using ArrPy for numerical computing.

## Installation (1 minute)

```bash
# Clone and install
git clone https://github.com/yourusername/ArrPy.git
cd ArrPy
pip install -e .

# Optional: Build C extensions for 4-170x speedup
python setup_c_ext.py build_ext --inplace
```

## Your First ArrPy Program (2 minutes)

```python
import arrpy as ap

# Create arrays - just like NumPy!
arr = ap.Array([1, 2, 3, 4, 5])
print(f"Array: {arr}")
print(f"Shape: {arr.shape}")
print(f"Size: {arr.size}")

# Basic operations
doubled = arr * 2
print(f"Doubled: {doubled}")

squared = arr ** 2
print(f"Squared: {squared}")

# Aggregations
print(f"Sum: {arr.sum()}")
print(f"Mean: {arr.mean()}")
print(f"Max: {arr.max()}")
```

## Common Array Operations (2 minutes)

### Creating Arrays

```python
# Different ways to create arrays
zeros = ap.zeros(5)                    # [0, 0, 0, 0, 0]
ones = ap.ones((2, 3))                 # [[1, 1, 1], [1, 1, 1]]
range_arr = ap.arange(0, 10, 2)       # [0, 2, 4, 6, 8]
linspace = ap.linspace(0, 1, 5)       # [0, 0.25, 0.5, 0.75, 1.0]
```

### 2D Arrays and Matrix Operations

```python
# Create 2D array
matrix = ap.Array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

# Access elements
print(matrix[1, 2])  # 6

# Transpose
transposed = matrix.T

# Matrix multiplication
result = matrix.dot(transposed)
```

### Mathematical Functions

```python
# Trigonometric
angles = ap.Array([0, ap.pi/4, ap.pi/2])
sines = ap.sin(angles)
cosines = ap.cos(angles)

# Exponential and logarithmic
data = ap.Array([1, 2, 3])
exp_data = ap.exp(data)
log_data = ap.log(data)

# Square root
values = ap.Array([1, 4, 9, 16])
roots = ap.sqrt(values)  # [1, 2, 3, 4]
```

### Array Manipulation

```python
# Reshape
arr = ap.arange(12)
reshaped = arr.reshape((3, 4))

# Concatenate
a = ap.Array([1, 2, 3])
b = ap.Array([4, 5, 6])
combined = ap.concatenate([a, b])  # [1, 2, 3, 4, 5, 6]

# Stack
stacked = ap.stack([a, b])  # [[1, 2, 3], [4, 5, 6]]
```

## Performance Tips

### 1. Use C Extensions
```python
# Check if C extensions are loaded
from arrpy.core import HAS_C_EXTENSION
print(f"C extensions enabled: {HAS_C_EXTENSION}")

# C extensions provide 4-170x speedup!
```

### 2. Vectorize Operations
```python
# Good - vectorized
result = arr * 2 + 3

# Avoid - loop
result = ap.Array([x * 2 + 3 for x in arr])
```

### 3. Use Built-in Functions
```python
# Good - built-in sum
total = arr.sum()

# Avoid - manual loop
total = sum(arr[i] for i in range(len(arr)))
```

## Real-World Example: Data Analysis

```python
import arrpy as ap

# Simulate temperature readings (Celsius)
days = 30
temperatures = ap.Array([20 + 10 * ap.sin(2 * ap.pi * i / 30) 
                        for i in range(days)])

# Convert to Fahrenheit
fahrenheit = temperatures * 9/5 + 32

# Statistics
print(f"Average temperature: {temperatures.mean():.1f}°C")
print(f"Hottest day: {temperatures.max():.1f}°C")
print(f"Coldest day: {temperatures.min():.1f}°C")
print(f"Temperature range: {temperatures.max() - temperatures.min():.1f}°C")

# Find days above 25°C
hot_days = temperatures > 25
print(f"Days above 25°C: {hot_days.sum()}")
```

## Differences from NumPy

While ArrPy aims for NumPy compatibility, there are some differences:

1. **Subset of Features**: ArrPy implements core functionality
2. **Type System**: ArrPy uses Python's native types
3. **Broadcasting**: Limited compared to NumPy
4. **Performance**: With C extensions, 75-500% of NumPy's speed

## Next Steps

✅ **You've learned the basics!** Here's where to go next:

1. 📖 Read the [User Guide](USER_GUIDE.md) for in-depth coverage
2. 🔬 Explore [Examples](../examples/) for more use cases
3. 📚 Check the [API Reference](../api/) for all functions
4. 🚀 Learn about [Performance Optimization](performance.md)
5. 🤝 [Contribute](../../CONTRIBUTING.md) to the project

## Quick Reference Card

```python
# Creation
ap.Array([1, 2, 3])          # From list
ap.zeros(shape)              # Zeros
ap.ones(shape)               # Ones
ap.arange(start, stop, step) # Range
ap.linspace(start, stop, n)  # Linear space

# Operations
a + b, a - b, a * b, a / b  # Arithmetic
a ** 2                       # Power
a.dot(b)                     # Matrix multiply

# Math
ap.sin(a), ap.cos(a)         # Trigonometric
ap.exp(a), ap.log(a)         # Exponential
ap.sqrt(a)                   # Square root

# Statistics
a.sum(), a.mean()            # Aggregation
a.min(), a.max()             # Extremes
a.std(), a.var()             # Variance

# Manipulation
a.reshape(shape)             # Reshape
a.T                          # Transpose
ap.concatenate([a, b])       # Join
```

Happy computing with ArrPy! 🚀