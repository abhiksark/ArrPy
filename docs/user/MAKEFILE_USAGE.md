# Makefile Usage Guide for ArrPy

## Quick Start

```bash
# 1. Build the Cython extensions (REQUIRED FIRST!)
make build

# 2. Run the demo to see backends in action
make demo

# 3. Run benchmarks to compare performance
make bench-quick
```

## Common Commands

### Building & Installation

| Command | Description |
|---------|-------------|
| `make build` | Build Cython extensions (.pyx → .so) |
| `make install` | Install ArrPy package with all backends |
| `make install-dev` | Install with development dependencies |
| `make clean` | Remove all build artifacts and compiled files |

### Testing

| Command | Description |
|---------|-------------|
| `make test` | Run all tests |
| `make test-python` | Test Python backend only |
| `make test-cython` | Test Cython backend only |
| `make test-c` | Test C backend only |
| `make test-cov` | Run tests with coverage report |

### Benchmarking

| Command | Description |
|---------|-------------|
| `make bench` | Run complete benchmark suite |
| `make bench-quick` | Quick benchmark (small arrays) |
| `make bench-ops` | Benchmark basic operations |
| `make bench-linalg` | Benchmark linear algebra |
| `make benchmark-compare` | Compare with NumPy |

### Development

| Command | Description |
|---------|-------------|
| `make demo` | Run backend system demonstration |
| `make lint` | Run code linting with ruff |
| `make format` | Format code with black and ruff |

## Typical Workflows

### First Time Setup
```bash
# Clean any previous builds
make clean

# Build Cython extensions
make build

# Install in development mode
make install-dev

# Run demo to verify everything works
make demo
```

### After Code Changes
```bash
# If you modified Cython files (.pyx)
make clean
make build

# Run tests
make test

# Check performance
make bench-quick
```

### Benchmark Workflow
```bash
# Build first
make build

# Run quick benchmarks
make bench-quick

# For detailed benchmarks
make bench

# Compare specific operations
make bench-ops     # Basic ops
make bench-linalg   # Linear algebra
```

### Development Workflow
```bash
# Format your code
make format

# Run linting
make lint

# Test specific backend
make test-python   # or test-cython, test-c

# Run demo
make demo
```

## What Each Command Does

### `make build`
- Compiles `.pyx` files to `.c`
- Compiles `.c` files to `.so` (shared objects)
- Places compiled extensions in `arrpy/backends/cython/`
- Uses optimization flags: `-O3 -ffast-math`

### `make clean`
- Removes `build/` and `dist/` directories
- Deletes `.so`, `.pyd`, `.pyc` files
- Removes generated `.c` files from Cython
- Cleans `__pycache__` directories

### `make demo`
- Builds Cython extensions first
- Runs `test_backend_system.py`
- Shows backend switching
- Demonstrates performance differences
- Tests NO fallback behavior

### `make bench-quick`
- Builds extensions
- Runs benchmarks with small arrays (100, 1000)
- Compares Python vs Cython vs C backends
- Shows speedup ratios

## Troubleshooting

### "No module named 'arrpy.backends.cython.array_ops'"
**Solution:** Run `make build` first

### "ImportError: cannot import name '_add_cython'"
**Solution:** 
```bash
make clean
make build
```

### Benchmarks show Python faster than Cython
**Expected for small arrays** - Cython has overhead from type conversion. Benefits show with:
- Larger arrays (>10,000 elements)
- Complex algorithms
- Tight loops

### Build warnings about NumPy API
**Normal** - These are deprecation warnings from NumPy, not errors

## Notes

- Always run `make build` after cloning or pulling changes
- Cython extensions are platform-specific (.so files)
- The C backend currently has placeholder implementations
- Benchmarks may vary based on array size and system specs