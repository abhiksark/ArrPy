# Examples

This directory contains comprehensive examples demonstrating the full capabilities of the **Cython-Optimized ArrPy** library, showcasing all 75+ implemented features with performance improvements.

## Example Files

### Core Examples

#### 1. `basic_usage.py`
**Demonstrates fundamental Cython-optimized ArrPy operations:**
- **Cython-accelerated** array creation (1D, 2D, 3D) using Array constructor
- **6-9x faster** creation methods: zeros, ones, full, arange
- Indexing and element access
- **2-3x faster** arithmetic operations (addition, subtraction, multiplication, division)
- Comparison and logical operations (==, >, <, logical_and, logical_or, logical_not)
- Matrix operations (transpose, dot product)
- Reshape functionality
- **C-level optimized** aggregation functions (sum, mean, sum_fast, mean_fast)

**Run with:**
```bash
cd examples
python basic_usage.py
```

#### 2. `matrix_operations.py`
**Advanced matrix and linear algebra operations:**
- Matrix multiplication and properties
- Chaining matrix operations
- Identity matrix operations and eye function
- Matrix powers using repeated multiplication
- Vector operations (dot product, outer product)
- 2D transformation matrices (scaling, rotation, reflection)
- System of equations representation
- Matrix construction with zeros, ones, and eye
- Matrix concatenation and stacking (hstack, vstack)
- Block matrix operations

**Run with:**
```bash
cd examples
python matrix_operations.py
```

#### 3. `data_analysis.py`
**Real-world data analysis scenarios:**
- Statistical analysis of test scores
- Grade matrix analysis (students × subjects)
- Sales data analysis with monthly and product breakdowns
- Financial portfolio calculations
- Growth trend analysis with percentage calculations
- Advanced statistical functions (min, max, std, var, median, percentile)
- Time series data concatenation

**Run with:**
```bash
cd examples
python data_analysis.py
```

#### 4. `error_handling.py`
**Comprehensive error handling demonstrations:**
- Initialization errors (ragged arrays, invalid types)
- Indexing errors (out of bounds, wrong dimensions)
- Arithmetic operation errors (shape mismatches)
- Reshape errors (incompatible sizes)
- Transpose errors (invalid dimensions)
- Dot product errors (incompatible shapes, wrong types)
- Aggregation errors (empty arrays)
- Mathematical function errors (domain errors)
- Concatenation errors (shape mismatches)
- Defensive programming patterns

**Run with:**
```bash
cd examples
python error_handling.py
```

### Comprehensive Feature Examples

#### 5. `array_creation_examples.py`
**Complete array creation function showcase (300+ lines):**
- Basic creation: Array(), array()
- Special arrays: zeros(), ones(), empty(), full()
- Identity matrices: eye(), identity() with offsets
- Range-based: arange(), linspace(), logspace()
- Multi-dimensional shapes and memory efficiency
- Performance tips and best practices

**Run with:**
```bash
cd examples
python array_creation_examples.py
```

#### 6. `mathematical_functions_examples.py`
**Complete mathematical function library (400+ lines):**
- **Trigonometric:** sin, cos, tan, arcsin, arccos, arctan
- **Logarithmic:** exp, log, log10, log2, sqrt
- **Arithmetic:** power, absolute, sign, floor_divide, mod
- **Rounding:** floor, ceil, round, trunc
- Method vs function call patterns
- Scientific calculations and error handling
- Performance optimization tips

**Run with:**
```bash
cd examples
python mathematical_functions_examples.py
```

#### 7. `statistical_analysis_examples.py`
**Extended statistical capabilities (500+ lines):**
- **Basic statistics:** sum, mean, min, max, std, var
- **Distribution analysis:** median, percentile, quartiles
- **Advanced functions:** prod, cumsum, cumprod, argmin, argmax
- Central tendency and variability measures
- Time series analysis and comparative statistics
- Outlier detection using statistical methods
- Data quality assessment

**Run with:**
```bash
cd examples
python statistical_analysis_examples.py
```

#### 8. `array_manipulation_examples.py`
**Complete manipulation operations (400+ lines):**
- **Concatenation:** concatenate() with axis control
- **Stacking:** stack(), vstack(), hstack()
- **Reshaping:** reshape() and transpose operations
- **Dimension manipulation:** squeeze(), expand_dims()
- Practical examples: dataset building, matrix operations
- Performance tips and error handling

**Run with:**
```bash
cd examples
python array_manipulation_examples.py
```

#### 9. `comparison_and_logical_examples.py`
**Complete comparison and logical operations (350+ lines):**
- **Element-wise comparisons:** ==, !=, >, <, >=, <=
- **Scalar comparisons** and filtering
- **Logical operations:** logical_and, logical_or, logical_not
- Complex logical expressions and data filtering
- Matrix comparison operations
- Range and boundary checking
- Performance optimization and error handling

**Run with:**
```bash
cd examples
python comparison_and_logical_examples.py
```

## Running All Examples

### Core Examples
```bash
cd examples
python basic_usage.py
python matrix_operations.py
python data_analysis.py
python error_handling.py
```

### Comprehensive Feature Examples
```bash
cd examples
python array_creation_examples.py
python mathematical_functions_examples.py
python statistical_analysis_examples.py
python array_manipulation_examples.py
python comparison_and_logical_examples.py
```

### Run All Examples Script
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

## Complete Feature Coverage

### 75+ Features Demonstrated

#### Array Creation (11 functions)
- `Array()`, `array()`, `zeros()`, `ones()`, `empty()`, `full()`
- `eye()`, `identity()`, `arange()`, `linspace()`, `logspace()`

#### Mathematical Functions (15 functions)
- **Trigonometric:** `sin`, `cos`, `tan`, `arcsin`, `arccos`, `arctan`
- **Logarithmic:** `exp`, `log`, `log10`, `log2`, `sqrt`
- **Arithmetic:** `power`, `absolute`, `sign`, `floor_divide`, `mod`
- **Rounding:** `floor`, `ceil`, `round`, `trunc`

#### Statistical Functions (11 functions)
- **Basic:** `sum`, `mean`, `min`, `max`, `std`, `var`
- **Distribution:** `median`, `percentile`
- **Advanced:** `prod`, `cumsum`, `cumprod`, `argmin`, `argmax`

#### Array Manipulation (8 functions)
- **Shape:** `reshape`, `transpose`, `squeeze`, `expand_dims`
- **Joining:** `concatenate`, `stack`, `vstack`, `hstack`

#### Comparison & Logical Operations (12 operators)
- **Comparisons:** `==`, `!=`, `>`, `<`, `>=`, `<=`
- **Logical:** `logical_and`, `logical_or`, `logical_not`
- **Broadcasting:** scalar and array comparisons

#### Core Array Operations (18+ methods)
- Indexing, slicing, arithmetic operations, matrix multiplication
- Properties: `shape`, `size`, `ndim`, `T`
- Methods: `dot()`, `mean()`, `sum()`, etc.

## Learning Path

### Beginner Path
1. **`basic_usage.py`** - Core concepts and operations
2. **`array_creation_examples.py`** - All creation methods
3. **`matrix_operations.py`** - Matrix mathematics

### Intermediate Path
4. **`data_analysis.py`** - Practical applications
5. **`statistical_analysis_examples.py`** - Statistical computing
6. **`mathematical_functions_examples.py`** - Scientific computing

### Advanced Path
7. **`array_manipulation_examples.py`** - Complex data reshaping
8. **`comparison_and_logical_examples.py`** - Data filtering
9. **`error_handling.py`** - Robust programming

## Key Concepts Demonstrated

### Array Operations
- Creating arrays from nested lists and specialized functions
- Shape validation and multi-dimensional indexing
- Element-wise operations and broadcasting
- Memory-efficient array creation patterns

### Mathematical Computing
- Complete trigonometric and logarithmic function library
- Arithmetic operations with proper error handling
- Scientific calculations and performance optimization
- Method vs function calling patterns

### Statistical Analysis
- Comprehensive statistical function library
- Distribution analysis and percentile calculations
- Time series analysis and data quality assessment
- Outlier detection and comparative statistics

### Data Manipulation
- Advanced concatenation and stacking operations
- Flexible reshaping and dimension manipulation
- Block matrix construction and practical applications
- Performance-optimized manipulation patterns

### Logical Operations
- Complete comparison operator support
- Boolean logic with logical_and, logical_or, logical_not
- Data filtering and conditional operations
- Complex logical expressions for data analysis

### Error Handling
- Comprehensive input validation and domain checking
- Shape compatibility verification
- Graceful error recovery patterns
- Defensive programming best practices

## Performance Notes

- All examples include performance tips and optimization suggestions
- Vectorized operations are demonstrated as preferred approaches
- Memory-efficient patterns are highlighted throughout
- Error handling approaches balance safety with performance

## Notes for Learning

- **Progressive Complexity:** Examples build from basic to advanced concepts
- **Complete Coverage:** All 75+ features are demonstrated with practical examples
- **Real-world Applications:** Examples show practical use cases for each feature
- **Error Awareness:** Common mistakes and proper error handling are emphasized
- **Performance Conscious:** Best practices for efficient array operations

## Extending the Examples

These examples provide a solid foundation for:
- Building custom data analysis workflows
- Implementing scientific computing applications
- Creating educational tools for numerical computing
- Developing NumPy-compatible libraries
- Understanding array programming concepts

Each example file is thoroughly documented and can serve as both reference material and starting point for your own ArrPy-based projects.