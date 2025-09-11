# Contributing to ArrPy

Thank you for your interest in contributing to ArrPy! This educational project welcomes contributions that enhance learning and demonstrate optimization techniques.

## 🎯 Project Mission

ArrPy is an educational library that demonstrates the journey from simple Python to highly-optimized C++. Contributions should maintain this educational focus while improving performance or functionality.

## 🚀 Getting Started

### Development Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/yourusername/arrpy.git
   cd arrpy
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies:**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Build extensions:**
   ```bash
   # Cython extensions
   python setup.py build_ext --inplace
   
   # C++ extensions (Linux only)
   python setup_cpp.py build_ext --inplace
   ```

5. **Run tests to verify setup:**
   ```bash
   pytest tests/
   ```

## 📝 Contribution Guidelines

### Types of Contributions

#### 1. Backend Implementations
- **Python Backend**: Clear, educational implementations
- **Cython Backend**: Type-optimized versions of hot paths
- **C++ Backend**: SIMD-vectorized critical operations

#### 2. New Operations
- Must be implemented in Python backend first
- Should follow NumPy API conventions
- Include comprehensive tests

#### 3. Performance Optimizations
- Must include benchmarks showing improvement
- Should not sacrifice code clarity in Python backend
- Document optimization techniques used

#### 4. Documentation
- Code examples and tutorials
- Performance analysis
- Algorithm explanations

### Code Style

#### Python Code
```python
# Good: Clear variable names and algorithm steps
def matrix_multiply_naive(A, B):
    """Educational matrix multiplication showing O(n³) complexity."""
    m, k = len(A), len(A[0])
    k2, n = len(B), len(B[0])
    
    assert k == k2, "Inner dimensions must match"
    
    result = [[0 for _ in range(n)] for _ in range(m)]
    
    # Triple nested loop - clearly shows O(n³)
    for i in range(m):
        for j in range(n):
            for l in range(k):
                result[i][j] += A[i][l] * B[l][j]
    
    return result
```

#### Cython Code
```cython
# Good: Type annotations and optimization directives
@cython.boundscheck(False)
@cython.wraparound(False)
def matrix_multiply_cython(double[:, :] A, double[:, :] B):
    """Optimized matrix multiplication with Cython."""
    cdef int m = A.shape[0]
    cdef int k = A.shape[1]
    cdef int n = B.shape[1]
    cdef double[:, :] result = np.zeros((m, n))
    cdef int i, j, l
    cdef double sum_val
    
    for i in range(m):
        for j in range(n):
            sum_val = 0
            for l in range(k):
                sum_val += A[i, l] * B[l, j]
            result[i, j] = sum_val
    
    return np.asarray(result)
```

#### C++ Code
```cpp
// Good: SIMD optimization with clear intent
void matrix_multiply_simd(const double* A, const double* B, double* C,
                          int m, int k, int n) {
    // Cache blocking parameters
    const int BLOCK_SIZE = 64;
    
    #pragma omp parallel for
    for (int ii = 0; ii < m; ii += BLOCK_SIZE) {
        for (int jj = 0; jj < n; jj += BLOCK_SIZE) {
            for (int kk = 0; kk < k; kk += BLOCK_SIZE) {
                // Process blocks with SIMD
                for (int i = ii; i < std::min(ii + BLOCK_SIZE, m); i++) {
                    for (int j = jj; j < std::min(jj + BLOCK_SIZE, n); j++) {
                        __m256d sum = _mm256_setzero_pd();
                        // SIMD inner loop...
                    }
                }
            }
        }
    }
}
```

### Testing Requirements

All contributions must include tests:

```python
# tests/test_your_feature.py
import pytest
import arrpy
from arrpy import Backend

class TestYourFeature:
    @pytest.mark.parametrize("backend", [Backend.PYTHON, Backend.CYTHON])
    def test_correctness(self, backend):
        """Test that operation produces correct results."""
        arrpy.set_backend(backend)
        # Your test here
    
    def test_consistency(self):
        """Test that all backends produce identical results."""
        data = create_test_data()
        results = {}
        
        for backend in [Backend.PYTHON, Backend.CYTHON]:
            arrpy.set_backend(backend)
            results[backend] = your_operation(data)
        
        assert_allclose(results[Backend.PYTHON], results[Backend.CYTHON])
```

### Benchmarking

Performance improvements must include benchmarks:

```python
# benchmarks/bench_your_feature.py
from bench_core import Benchmark

def benchmark_your_feature():
    bench = Benchmark("YourFeature")
    bench.run(lambda a: your_operation(a))
    bench.report()
    
    # Should show improvement
    assert bench.speedup(Backend.CYTHON, Backend.PYTHON) > 2.0
```

## 🔄 Pull Request Process

### 1. Choose an Issue
- Check existing issues or create a new one
- Comment to claim the issue
- Reference issue number in PR

### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 3. Implement Your Changes
- Follow code style guidelines
- Add tests for new functionality
- Update documentation as needed
- Run tests locally: `pytest tests/`

### 4. Commit Your Changes
```bash
# Use descriptive commit messages
git commit -m "feat: Add SIMD optimization for reduction operations"
git commit -m "fix: Correct broadcasting for edge case"
git commit -m "docs: Add tutorial for backend system"
```

### 5. Push and Create PR
```bash
git push origin feature/your-feature-name
```

Then create a pull request with:
- Clear description of changes
- Benchmark results if applicable
- Reference to related issue
- Screenshots/examples if relevant

### PR Checklist
- [ ] Tests pass locally
- [ ] Code follows project style
- [ ] Documentation updated
- [ ] Benchmarks show improvement (if performance PR)
- [ ] Commit messages are descriptive
- [ ] PR description is comprehensive

## 📊 Backend Implementation Guide

### Adding a New Operation

#### Step 1: Python Implementation
```python
# arrpy/backends/python/your_ops.py
def _your_operation_python(data, shape, **kwargs):
    """
    Clear, educational implementation.
    Document the algorithm and complexity.
    """
    # Your implementation
    return result, result_shape
```

#### Step 2: Integration
```python
# arrpy/arrpy.py
def your_operation(self, **kwargs):
    backend = get_backend()
    
    if backend == Backend.PYTHON:
        from .backends.python.your_ops import _your_operation_python
        result = _your_operation_python(self._data, self._shape, **kwargs)
    elif backend == Backend.CYTHON:
        raise NotImplementedError("Not yet in Cython backend")
    elif backend == Backend.C:
        raise NotImplementedError("Not yet in C backend")
    
    return self._create_from_data(*result)
```

#### Step 3: Cython Optimization (Optional)
```cython
# arrpy/backends/cython/your_ops.pyx
def _your_operation_cython(data, shape, **kwargs):
    """Optimized version with type annotations."""
    # Cython implementation
```

#### Step 4: Update Implementation Matrix
Update `CLAUDE.md` with your implementation status:
```markdown
| your_operation | ✅ | ❌ | ❌ | Notes on performance |
```

## 🐛 Bug Reports

### Creating a Bug Report

Include:
1. **Description**: Clear explanation of the bug
2. **Reproduction**: Minimal code to reproduce
3. **Expected behavior**: What should happen
4. **Actual behavior**: What actually happens
5. **Environment**: Python version, OS, backend used

Example:
```python
# Reproduction code
import arrpy
arrpy.set_backend('cython')

a = arrpy.array([1, 2, 3])
b = arrpy.array([4, 5, 6])
result = a + b  # Error occurs here

# Expected: [5, 7, 9]
# Actual: SegmentationFault
```

## 💡 Feature Requests

### Proposing New Features

1. **Check existing issues** first
2. **Describe the feature** clearly
3. **Explain the use case**
4. **Consider educational value**
5. **Suggest implementation approach**

## 🎓 Educational Contributions

We especially welcome:
- **Tutorials**: Step-by-step guides for concepts
- **Visualizations**: Performance comparisons
- **Algorithm explanations**: Comments and documentation
- **Optimization case studies**: Before/after analysis

## 📧 Communication

- **Issues**: Bug reports and feature requests
- **Discussions**: General questions and ideas
- **Pull Requests**: Code contributions

## 🙏 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in relevant documentation

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make ArrPy a better learning resource! 🚀