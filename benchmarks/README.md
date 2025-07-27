# 🚀 ArrPy Benchmark Suite

A comprehensive, colorful, and interactive benchmark suite for comparing ArrPy's performance against NumPy across all major array operations with beautiful visualizations and detailed analysis.

## ✨ New Features Added

### 🎨 **Beautiful Colorized Output**
- **ANSI color support** with automatic terminal detection
- **Progress bars** and real-time status updates  
- **Color-coded performance indicators** (🟢 competitive, 🟡 moderate, 🔴 high gaps)
- **Styled headers, tables, and charts** for easy reading

### 📊 **Multiple Visualization Options**
- **ASCII Charts** - Terminal-based charts that work anywhere
- **HTML Reports** - Beautiful, responsive web reports
- **Performance Matrices** - Detailed breakdowns by operation and size
- **Interactive Demonstrations** - Guided tours of all features

### 🔧 **Expanded Test Coverage**
- **50+ new benchmark tests** across 8 major categories
- **All new ArrPy features** including array creation, math functions, comparisons
- **Multiple array sizes** (small, medium, large) for each operation
- **Statistical analysis** with multiple iterations and error handling

## 📋 Enhanced Test Categories

| Category | Tests | New Features |
|----------|-------|-------------|
| 🏗️ **Array Creation** | 21 tests | `zeros`, `ones`, `eye`, `arange`, `linspace` |
| ➕ **Arithmetic Operations** | 12 tests | Element-wise `+`, `-`, `*`, `/` with scalars and arrays |
| 🔢 **Matrix Operations** | 8 tests | Matrix multiplication, transpose, dot products |
| 📈 **Extended Aggregations** | 18 tests | `sum`, `mean`, `min`, `max`, `std`, `var`, `median`, `percentile` |
| 📐 **Mathematical Functions** | 15 tests | `sqrt`, `sin`, `cos`, `exp`, `log` |
| ⚖️ **Comparison Operations** | 15 tests | `==`, `!=`, `>`, `<`, `>=`, `<=` |
| 🔗 **Logical Operations** | 9 tests | `logical_and`, `logical_or`, `logical_not` |
| 🔗 **Concatenation** | 12 tests | `concatenate`, `vstack`, `hstack` |

## 📁 Enhanced File Structure

```
benchmarks/
├── 🎨 colors.py              # Color utilities and formatting
├── 🚀 performance_comparison.py # Main benchmark suite (ENHANCED)
├── 🔬 micro_benchmarks.py    # Detailed micro-benchmarks (ENHANCED)
├── 📈 scalability_test.py    # Scalability analysis (ENHANCED)
├── 📊 ascii_charts.py        # Terminal-based visualization (NEW)
├── 📄 html_report.py         # HTML report generation (NEW)
├── 🎬 sample_visualizations.py # Interactive demos (NEW)
├── 🖼️ visualization.py       # Advanced plotting (matplotlib support)
└── 📖 README.md              # This enhanced documentation
```

## 🚀 Quick Start

### Run Enhanced Benchmarks
```bash
# Comprehensive benchmark suite with colorized output
python performance_comparison.py

# Detailed micro-benchmarks with beautiful formatting
python micro_benchmarks.py

# Scalability analysis with new features
python scalability_test.py
```

### Generate Visualizations
```bash
# ASCII charts and terminal visualization
python ascii_charts.py

# HTML report generation
python html_report.py

# Interactive demonstration of all features
python sample_visualizations.py
```

## 📊 Sample Enhanced Output

### Colorized Terminal Output
```
    ╔═══════════════════════════════════════╗
    ║  █████╗ ██████╗ ██████╗ ██████╗ ██╗   ██╗  ║
    ║  ██╔══██╗██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝  ║
    ║  ███████║██████╔╝██████╔╝██████╔╝ ╚████╔╝   ║
    ║  ██╔══██║██╔══██╗██╔══██╗██╔═══╝   ╚██╔╝    ║
    ║  ██║  ██║██║  ██║██║  ██║██║        ██║     ║
    ║  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝     ║
    ║                                           ║
    ║         Pure Python NumPy Alternative         ║
    ║              Performance Benchmarks              ║
    ╚═══════════════════════════════════════╝

════════════════════════════════════════════════════════════════════════════════
                     📊 NumPy Speedup by Operation Category                      
════════════════════════════════════════════════════════════════════════════════

Array Creation            │░░░░░░░░░                          2.50x 🟡
Matrix Operations         │████████████████████████████████  15.20x 🔴
Math Functions            │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  8.70x 🔴
```

### ASCII Performance Matrix
```
🎯 Performance Matrix: NumPy Speedup by Operation & Size

Operation                      Small      Medium       Large
────────────────────────────────────────────────────────────
Array Creation                  1.20x       2.10x       4.50x
Arithmetic                      1.50x       2.80x       6.20x
Matrix Ops                      5.20x      12.10x      25.80x
Aggregations                    2.10x       3.40x       7.80x
Math Functions                  3.20x       6.70x      12.30x
```

### Progress Indicators with Colors
```
ℹ Running benchmark... (5 iterations)
[████████████████████████████████████████████████████] 100.0%

✓ Array Creation (1000 elements)     │ arrpy: 123.45μs │ numpy: 45.23μs │ speedup: 2.73x 🟡
```

## 📈 Performance Insights

### Key Findings from Enhanced Testing
- **🟢 Competitive Areas**: Array creation for small arrays, simple indexing
- **🟡 Moderate Gaps**: Arithmetic operations, aggregations (2-5x slower)
- **🔴 Large Gaps**: Matrix operations, mathematical functions (5-25x slower)

### Enhanced Scalability Patterns
- **Linear Operations**: ArrPy shows O(n) scaling similar to NumPy but with higher constants
- **Matrix Operations**: O(n³) complexity shows dramatic differences due to optimization
- **Memory Usage**: ArrPy uses 2-3x more memory due to Python object overhead

### Updated Recommendations
| Use Case | Recommended Library | Why |
|----------|-------------------|-----|
| 🎓 **Learning** | ArrPy | Pure Python, easy to understand implementation |
| 🧪 **Prototyping** | ArrPy | Quick setup, no dependencies |
| 📊 **Small Data** | ArrPy | Competitive performance, simpler deployment |
| 🚀 **Production** | NumPy | Optimized performance, mature ecosystem |
| 🔢 **Large Arrays** | NumPy | Significant performance advantages |
| 🧮 **Heavy Math** | NumPy | Optimized mathematical operations |

### 1. `performance_comparison.py` (ENHANCED)
**Comprehensive performance comparison with beautiful output:**
- **All original tests** plus 50+ new benchmarks
- **New categories**: Array creation, math functions, comparisons, logical ops, concatenation
- **Colorized output** with progress bars and status indicators
- **Enhanced reporting** with category summaries and insights

### 2. `micro_benchmarks.py`
**Detailed micro-benchmarks for specific operation patterns:**
- Array creation patterns (different sizes and shapes)
- Arithmetic operation patterns (various combinations)
- Indexing patterns (single access, multiple access, row access)
- Matrix operation patterns (multiplication, transpose, chaining)
- Aggregation patterns (1D and 2D arrays)
- Reshape patterns (different size transformations)

**Features:**
- High iteration counts for precise measurements
- Statistical analysis (mean, standard deviation)
- Detailed performance reports by category
- Error handling and reproducible results

**Run with:**
```bash
cd benchmarks
python micro_benchmarks.py
```

### 3. `scalability_test.py`
**Scalability analysis showing how performance changes with array size:**
- Array creation scalability (1D and 2D)
- Arithmetic operations scalability
- Matrix operations scalability (critical for O(n³) operations)
- Aggregation operations scalability
- Indexing operations scalability
- Reshape operations scalability

**Features:**
- Computational complexity analysis
- Growth ratio calculations
- Optional matplotlib plots (if available)
- Performance scaling insights

**Run with:**
```bash
cd benchmarks
python scalability_test.py
```

## Running All Benchmarks

To run all benchmarks sequentially:

```bash
cd benchmarks
python performance_comparison.py
python micro_benchmarks.py
python scalability_test.py
```

Or use a script to run them all:

```bash
# Run from the benchmarks directory
for script in performance_comparison.py micro_benchmarks.py scalability_test.py; do
    echo "=== Running $script ==="
    python "$script"
    echo
done
```

## Dependencies

**Required:**
- `numpy` - for comparison baseline
- `arrpy` - the package being benchmarked

**Optional:**
- `matplotlib` - for generating scalability plots (only in scalability_test.py)

Install dependencies:
```bash
pip install numpy matplotlib
```

## Expected Results

### Performance Characteristics

**numpy advantages:**
- Consistently faster across all operations (typically 2x-100x+)
- Optimized C implementation
- Efficient memory layout
- SIMD and vectorization optimizations
- Mature, highly optimized algorithms

**arrpy characteristics:**
- Pure Python implementation
- Readable and educational code
- Similar API to numpy
- Good for learning and prototyping
- Suitable for small-medium datasets

### Typical Speedup Ranges

| Operation Category | Expected numpy Speedup |
|-------------------|------------------------|
| Array Creation    | 2x - 10x              |
| Simple Indexing   | 1.5x - 5x             |
| Arithmetic Ops    | 5x - 25x              |
| Matrix Multiply   | 20x - 200x+           |
| Aggregations      | 10x - 50x             |
| Reshape           | 3x - 15x              |

### Scalability Patterns

- **Linear operations** (sum, mean): Performance gap increases linearly
- **Quadratic operations** (matrix ops): Performance gap increases quadratically
- **Matrix multiplication**: Shows the largest performance differences
- **Memory-bound operations**: Smaller relative differences

## Benchmark Insights

### When to Use arrpy
- Educational purposes and learning NumPy concepts
- Small datasets (< 1000 elements)
- Prototyping and algorithm development
- When NumPy dependencies are not allowed
- Understanding array operation implementations

### When to Use numpy
- Production applications
- Large datasets (> 10,000 elements)
- Performance-critical code
- Scientific computing
- Machine learning applications

## Customizing Benchmarks

### Adding New Tests

1. **For performance_comparison.py:**
```python
def your_new_benchmark():
    benchmark = PerformanceBenchmark()
    
    # Setup test data
    test_data = [your_test_data]
    
    benchmark.run_benchmark(
        "Your Test Name",
        lambda: arrpy_operation(test_data),
        lambda: numpy_operation(test_data)
    )
    
    return benchmark
```

2. **For micro_benchmarks.py:**
```python
def benchmark_your_operation():
    benchmark = MicroBenchmark(iterations=1000)
    
    # Your test setup
    benchmark.compare_operations(
        "Your Operation Name",
        arrpy_func,
        numpy_func,
        *args
    )
    
    return benchmark
```

3. **For scalability_test.py:**
```python
def test_your_scaling():
    benchmark = ScalabilityBenchmark()
    
    sizes = [10, 50, 100, 500]
    
    benchmark.test_scaling(
        "Your Operation",
        sizes,
        lambda size: arrpy_func(size),
        lambda size: numpy_func(size)
    )
    
    return benchmark
```

### Modifying Test Parameters

- **Iteration counts**: Adjust for accuracy vs. speed trade-off
- **Array sizes**: Test different size ranges relevant to your use case
- **Data types**: Test with different numeric types
- **Operation combinations**: Test realistic usage patterns

## Understanding Results

### Reading Performance Reports

```
Operation Name                     | numpy speedup | arrpy time | numpy time
Array Creation (100x100)          | 15.32x faster | 0.012000s   | 0.000783s
```

- **Higher speedup** = larger performance gap
- **Lower speedup** = more competitive performance
- **Times** = actual execution time in seconds

### Statistical Significance

- Benchmarks use multiple iterations for accuracy
- Standard deviation shows measurement consistency
- Outliers are handled through averaging
- Garbage collection ensures clean measurements

### Interpreting Complexity Analysis

```
Estimated complexity - arrpy: O(n^2.1), numpy: O(n^2.0)
```

- Shows theoretical performance scaling
- arrpy may have higher complexity due to Python overhead
- Matrix operations should show O(n³) for both implementations

## Troubleshooting

### Common Issues

1. **Inconsistent results**: Ensure system is not under load during benchmarking
2. **Import errors**: Verify arrpy package is properly installed
3. **Memory errors**: Reduce array sizes for large-scale tests
4. **Plot generation fails**: Install matplotlib or skip plotting

### Performance Tips

- Close other applications during benchmarking
- Use a dedicated Python environment
- Run benchmarks multiple times for consistency
- Consider system thermal throttling for long tests

## Contributing

When adding new benchmarks:

1. Follow existing patterns and naming conventions
2. Include proper error handling
3. Add documentation for new test categories
4. Consider both small and large scale tests
5. Include statistical analysis where appropriate

The benchmark suite helps users understand the performance trade-offs between arrpy and numpy across different use cases and array sizes.