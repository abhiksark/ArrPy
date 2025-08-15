# ArrPy Development Guide

## Getting Started

### Setup Development Environment
```bash
# Clone the repository
git clone https://github.com/yourusername/arrpy.git
cd arrpy

# Install in development mode with dependencies
make install-dev

# Verify installation
python -c "import arrpy; print(arrpy.__version__)"
```

### Development Workflow

#### 1. Test-Driven Development (TDD)
Always write tests first:

```python
# tests/test_feature.py
def test_new_feature():
    # Write expected behavior
    import numpy as np
    import arrpy as ap
    
    # NumPy reference
    np_result = np.some_operation()
    
    # ArrPy implementation (will fail initially)
    ap_result = ap.some_operation()
    
    # Compare results
    assert np.allclose(np_result, ap_result)
```

#### 2. Implement Feature
```python
# arrpy/module.py
def some_operation():
    """
    Implement to match NumPy behavior.
    """
    # Your implementation
    pass
```

#### 3. Run Tests
```bash
# Run specific test
make test-specific TEST=test_feature

# Run all tests
make test

# Run with coverage
make test-cov
```

#### 4. Benchmark Performance
```bash
# Run benchmarks
make benchmark

# Compare with NumPy
make benchmark-compare
```

---

## Code Style Guidelines

### Python Style
- Follow PEP 8
- Use descriptive variable names
- Add type hints where helpful
- Maximum line length: 88 characters (Black default)

### Documentation
Every function needs:
```python
def function_name(param1, param2):
    """
    Brief description of function.
    
    Parameters
    ----------
    param1 : type
        Description of param1
    param2 : type
        Description of param2
    
    Returns
    -------
    type
        Description of return value
    
    Examples
    --------
    >>> arrpy.function_name(1, 2)
    3
    """
```

### Testing Guidelines
1. **Compare with NumPy**: Every operation should match NumPy
2. **Edge Cases**: Test empty arrays, single elements, large arrays
3. **Properties**: Test mathematical properties (associativity, etc.)
4. **Errors**: Test error conditions match NumPy

Example test structure:
```python
class TestFeature:
    def test_basic_case(self):
        """Test basic functionality."""
        pass
    
    def test_edge_cases(self):
        """Test edge cases."""
        # Empty array
        # Single element
        # Very large array
        pass
    
    def test_properties(self):
        """Test mathematical properties."""
        # Associativity: (a + b) + c == a + (b + c)
        # Commutativity: a + b == b + a
        pass
    
    def test_errors(self):
        """Test error conditions."""
        with pytest.raises(ValueError):
            # Invalid operation
            pass
```

---

## Implementation Patterns

### Array Storage Pattern
```python
class arrpy:
    def __init__(self, data):
        # Flatten nested data
        self._data = self._flatten(data)
        # Store shape
        self._shape = self._get_shape(data)
        # Calculate strides
        self._strides = self._calculate_strides(self._shape)
```

### Broadcasting Pattern
```python
def broadcast_shapes(shape1, shape2):
    # Pad with 1s
    ndim = max(len(shape1), len(shape2))
    shape1 = (1,) * (ndim - len(shape1)) + shape1
    shape2 = (1,) * (ndim - len(shape2)) + shape2
    
    # Check compatibility and get result shape
    result = []
    for d1, d2 in zip(shape1, shape2):
        if d1 == d2:
            result.append(d1)
        elif d1 == 1:
            result.append(d2)
        elif d2 == 1:
            result.append(d1)
        else:
            raise ValueError("Shapes not compatible for broadcasting")
    
    return tuple(result)
```

### Indexing Pattern
```python
def __getitem__(self, key):
    # Normalize index
    if not isinstance(key, tuple):
        key = (key,)
    
    # Handle each index type
    result_data = self._data
    result_shape = self._shape
    
    for i, idx in enumerate(key):
        if isinstance(idx, int):
            # Integer indexing
            pass
        elif isinstance(idx, slice):
            # Slice indexing
            pass
        elif isinstance(idx, np.ndarray):
            # Fancy indexing
            pass
    
    return result
```

---

## Debugging Tips

### Common Issues

1. **Shape Mismatch**
   - Print shapes at each step
   - Check broadcasting rules
   - Verify stride calculations

2. **Indexing Errors**
   - Check negative index handling
   - Verify multi-dimensional access
   - Test slice boundaries

3. **Type Issues**
   - Check dtype preservation
   - Test type promotion rules
   - Verify casting behavior

### Debugging Tools
```python
# Add debug prints
def debug_array(arr):
    print(f"Shape: {arr.shape}")
    print(f"Strides: {arr.strides}")
    print(f"Data: {arr._data[:10]}...")  # First 10 elements

# Compare with NumPy step-by-step
np_arr = np.array(data)
ap_arr = ap.array(data)

print(f"NumPy shape: {np_arr.shape}")
print(f"ArrPy shape: {ap_arr.shape}")
```

---

## Performance Considerations

### Pure Python Optimization Tips
1. **List Comprehensions**: Faster than loops
2. **Local Variables**: Access is faster
3. **Avoid Function Calls**: In hot loops
4. **Preallocate Lists**: When size is known

```python
# Slow
result = []
for i in range(n):
    result.append(operation(i))

# Faster
result = [operation(i) for i in range(n)]

# Even faster (if possible)
result = [0] * n
for i in range(n):
    result[i] = operation(i)
```

### Memory Efficiency
```python
# Use views when possible
def transpose(self):
    # Don't copy data, just change strides
    new_strides = self._strides[::-1]
    new_shape = self._shape[::-1]
    return self._view(new_shape, new_strides)
```

---

## Testing Checklist

### For Each New Feature
- [ ] Unit tests written
- [ ] Compared with NumPy
- [ ] Edge cases tested
- [ ] Error cases tested
- [ ] Benchmarks added
- [ ] Documentation complete

### Before Committing
- [ ] All tests pass: `make test`
- [ ] Code formatted: `make format`
- [ ] No linting errors: `make lint`
- [ ] Coverage acceptable: `make test-cov`

---

## Common Patterns from NumPy

### Reduction Operations
```python
def reduce_operation(self, operation, axis=None):
    if axis is None:
        # Reduce over all elements
        return operation(self._data)
    else:
        # Reduce over specific axis
        # Reshape and apply operation
        pass
```

### Element-wise Operations
```python
def elementwise_operation(self, other, operation):
    # Handle scalar
    if np.isscalar(other):
        return operation(self, other)
    
    # Handle array with broadcasting
    broadcasted = broadcast_arrays(self, other)
    return operation(*broadcasted)
```

---

## Resources

### Essential Reading
- [NumPy Documentation](https://numpy.org/doc/stable/)
- [NumPy Enhancement Proposals (NEPs)](https://numpy.org/neps/)
- [From Python to NumPy](https://www.labri.fr/perso/nrougier/from-python-to-numpy/)

### Understanding NumPy Internals
- [NumPy Source Code](https://github.com/numpy/numpy)
- [100 NumPy Exercises](https://github.com/rougier/numpy-100)
- [NumPy Tutorial](https://numpy.org/doc/stable/user/tutorial.html)

### Testing Resources
- [NumPy Testing Guidelines](https://numpy.org/doc/stable/reference/testing.html)
- [Pytest Documentation](https://docs.pytest.org/)
- [Hypothesis for Property Testing](https://hypothesis.readthedocs.io/)