# ArrPy Scripts

This directory contains utility and automation scripts for ArrPy development and testing.

## Scripts

### check_features.py
Generates a feature implementation matrix showing which operations are available in each backend (Python, Cython, C++).

**Usage:**
```bash
python scripts/check_features.py              # Show feature matrix
python scripts/check_features.py --json       # Output as JSON
python scripts/check_features.py --detailed   # Show detailed matrix
python scripts/check_features.py --backend python  # Check specific backend
```

### run_ci_tests.py
Minimal CI test runner used by GitHub Actions for quick verification of the package.

**Usage:**
```bash
python scripts/run_ci_tests.py  # Run CI test suite
```

### run_experimental.py
Demonstrates experimental features including:
- Type-specific optimizations
- Memory pooling
- Alternative storage backends
- Zero-copy operations

**Usage:**
```bash
python scripts/run_experimental.py  # Run experimental demos
```

### test_skip_example.py
Example script showing how to skip tests when certain backends aren't available.

### pytest_skip_config.py
Configuration for pytest to handle backend-specific test skipping.

## Integration

These scripts are integrated with the Makefile:
- `make features` - Runs check_features.py
- `make experimental` - Runs run_experimental.py
- CI workflows use run_ci_tests.py for automated testing