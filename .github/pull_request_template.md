## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Performance improvement (optimization that improves speed/memory)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Code refactoring

## Backend Impact
Which backends does this PR affect?
- [ ] Python backend
- [ ] Cython backend
- [ ] C++ backend
- [ ] Backend-agnostic (affects all)

## Implementation Details
Describe your implementation approach:

### Changes Made
- List the main changes
- Highlight any important design decisions
- Mention any algorithms used

### Performance Impact
If this is a performance PR:
```
Operation: [name]
Python backend: before Xms → after Xms (Xx speedup)
Cython backend: before Xms → after Xms (Xx speedup)
C++ backend: before Xms → after Xms (Xx speedup)
```

## Testing
- [ ] Tests pass locally (`make test`)
- [ ] Added new tests for this feature/fix
- [ ] All backends produce consistent results
- [ ] Benchmarks show expected performance

### Test Coverage
```bash
# Include coverage report for changed files
pytest tests/ --cov=arrpy --cov-report=term
```

## Documentation
- [ ] Docstrings added/updated
- [ ] README updated (if needed)
- [ ] CHANGELOG entry added
- [ ] Tutorial/example updated (if applicable)

## Educational Value
How does this PR contribute to ArrPy's educational mission?
- [ ] Demonstrates important concepts
- [ ] Improves code clarity
- [ ] Adds helpful comments
- [ ] Shows optimization techniques

## Benchmarks
```python
# Include benchmark results if applicable
python benchmarks/benchmark_v1.py
```

## Related Issues
Closes #[issue_number]

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

## Screenshots (if applicable)
Add screenshots to help explain your changes.

## Additional Notes
Any additional information that reviewers should know.