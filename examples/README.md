# Examples

This directory contains comprehensive examples demonstrating the capabilities of the arrypy library.

## Example Files

### 1. `basic_usage.py`
**Demonstrates fundamental arrypy operations:**
- Array creation (1D, 2D, 3D)
- Indexing and element access
- Basic arithmetic operations (addition, subtraction, multiplication, division)
- Matrix operations (transpose, dot product)
- Reshape functionality
- Aggregation functions (sum, mean)

**Run with:**
```bash
cd examples
python basic_usage.py
```

### 2. `matrix_operations.py`
**Advanced matrix and linear algebra operations:**
- Matrix multiplication and properties
- Chaining matrix operations
- Identity matrix operations
- Matrix powers using repeated multiplication
- Vector operations (dot product, outer product)
- 2D transformation matrices (scaling, rotation, reflection)
- System of equations representation

**Run with:**
```bash
cd examples
python matrix_operations.py
```

### 3. `data_analysis.py`
**Real-world data analysis scenarios:**
- Statistical analysis of test scores
- Grade matrix analysis (students × subjects)
- Sales data analysis with monthly and product breakdowns
- Financial portfolio calculations
- Growth trend analysis with percentage calculations

**Run with:**
```bash
cd examples
python data_analysis.py
```

### 4. `error_handling.py`
**Comprehensive error handling demonstrations:**
- Initialization errors (ragged arrays, invalid types)
- Indexing errors (out of bounds, wrong dimensions)
- Arithmetic operation errors (shape mismatches)
- Reshape errors (incompatible sizes)
- Transpose errors (invalid dimensions)
- Dot product errors (incompatible shapes, wrong types)
- Aggregation errors (empty arrays)
- Defensive programming patterns

**Run with:**
```bash
cd examples
python error_handling.py
```

## Running All Examples

To run all examples sequentially:

```bash
cd examples
python basic_usage.py
python matrix_operations.py
python data_analysis.py
python error_handling.py
```

Or create a simple script to run them all:

```bash
# Run from the examples directory
for script in *.py; do
    if [ "$script" != "__init__.py" ]; then
        echo "=== Running $script ==="
        python "$script"
        echo
    fi
done
```

## Learning Path

1. **Start with `basic_usage.py`** to understand fundamental operations
2. **Move to `matrix_operations.py`** for advanced mathematical operations
3. **Explore `data_analysis.py`** for practical applications
4. **Study `error_handling.py`** to understand robust programming practices

## Key Concepts Demonstrated

### Array Operations
- Creating arrays from nested lists
- Shape validation and error handling
- Multi-dimensional indexing
- Element-wise arithmetic operations

### Matrix Mathematics
- Matrix multiplication (dot product)
- Transpose operations
- Linear algebra concepts
- Transformation matrices

### Data Analysis
- Statistical calculations (mean, sum)
- Multi-dimensional data processing
- Financial calculations
- Trend analysis

### Error Handling
- Input validation
- Shape compatibility checking
- Graceful error recovery
- Defensive programming patterns

## Notes for Learning

- Each example file is self-contained and can be run independently
- Examples progress from simple to complex concepts
- Error handling examples show both correct usage and common mistakes
- Comments throughout the code explain the mathematical and programming concepts
- Real-world scenarios demonstrate practical applications

## Extending the Examples

Feel free to modify these examples to:
- Test different data sets
- Explore edge cases
- Combine operations in new ways
- Add your own error handling scenarios
- Create new analysis workflows

These examples serve as both documentation and starting points for your own arrypy-based projects.