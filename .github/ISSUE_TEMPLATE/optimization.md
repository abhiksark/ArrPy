---
name: Performance optimization
about: Propose a performance improvement for ArrPy
title: '[PERF] '
labels: performance
assignees: ''

---

## Optimization Target
Which operation(s) would be optimized?
- [ ] Array creation
- [ ] Arithmetic operations
- [ ] Linear algebra
- [ ] Reductions
- [ ] Universal functions
- [ ] Other: [please specify]

## Current Performance
Provide benchmark results for the current implementation:

```python
# Benchmarking code
import arrpy
import time

# Your benchmark here
```

Current results:
- Python backend: X ms
- Cython backend: X ms (if applicable)
- C++ backend: X ms (if applicable)

## Proposed Optimization
Describe your optimization approach:

### Technique
- [ ] Type optimization (Cython)
- [ ] SIMD vectorization
- [ ] Cache optimization
- [ ] Parallelization
- [ ] Algorithm improvement
- [ ] Memory pooling
- [ ] Other: [please describe]

### Implementation Details
```python
# or C/C++ code
# Show the optimized implementation
```

## Expected Performance Gain
- Estimated speedup: Xx
- Memory reduction: X%
- Theoretical limit: X

## Educational Value
How does this optimization teach important concepts?
- What technique does it demonstrate?
- What can users learn from this?

## Testing
How will you ensure correctness?
- [ ] Unit tests comparing with Python backend
- [ ] Numerical accuracy tests
- [ ] Edge case handling
- [ ] Performance regression tests

## Benchmarking Plan
```python
# How to measure the improvement
```

## Additional Context
Any additional information, research papers, or references.

## Checklist
- [ ] I have profiled the current implementation
- [ ] I have a working proof of concept
- [ ] The optimization maintains accuracy
- [ ] I've considered the educational aspect
- [ ] I'm willing to write tests and documentation