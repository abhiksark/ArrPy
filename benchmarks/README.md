# Performance Benchmarks

This directory contains comprehensive performance benchmarks comparing arrypy with numpy across all supported functionalities.

## Benchmark Files

### 1. `performance_comparison.py`
**Comprehensive performance comparison across all operations:**
- Array initialization (various sizes)
- Indexing operations (single element, row access)
- Arithmetic operations (addition, multiplication, division)
- Matrix operations (transpose, dot product)
- Reshape operations
- Aggregation functions (sum, mean)
- Memory usage comparison

**Features:**
- Multiple iterations for statistical accuracy
- Garbage collection before timing
- Detailed speedup analysis
- Summary report generation

**Run with:**
```bash
cd benchmarks
python performance_comparison.py
```

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
- `arrypy` - the package being benchmarked

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

**arrypy characteristics:**
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

### When to Use arrypy
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
        lambda: arrypy_operation(test_data),
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
        arrypy_func,
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
        lambda size: arrypy_func(size),
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
Operation Name                     | numpy speedup | arrypy time | numpy time
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
Estimated complexity - arrypy: O(n^2.1), numpy: O(n^2.0)
```

- Shows theoretical performance scaling
- arrypy may have higher complexity due to Python overhead
- Matrix operations should show O(n³) for both implementations

## Troubleshooting

### Common Issues

1. **Inconsistent results**: Ensure system is not under load during benchmarking
2. **Import errors**: Verify arrypy package is properly installed
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

The benchmark suite helps users understand the performance trade-offs between arrypy and numpy across different use cases and array sizes.