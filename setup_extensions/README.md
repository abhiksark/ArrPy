# Setup Extensions

This directory contains specialized build scripts for ArrPy's C++ extensions.

## Available Setup Scripts

### setup_cpp.py
Original C++ backend build script. Compiles basic C++ operations.

### setup_buffer_cpp.py
Build script for buffer protocol implementation with zero-copy operations.
- Uses Python's buffer protocol for direct memory access
- Implements SIMD operations (AVX2/NEON)

### setup_optimized_cpp.py
Advanced optimizations build script.
- Aggressive compiler flags
- OpenMP support (if available)
- Loop unrolling and prefetching

### setup_cpp_fast.py
Experimental fast C++ backend with numpy-based zero-copy.

## Building Extensions

To build a specific extension:

```bash
# Basic C++ backend
python setup_extensions/setup_cpp.py build_ext --inplace

# Buffer protocol backend
python setup_extensions/setup_buffer_cpp.py build_ext --inplace

# Optimized backend (recommended)
python setup_extensions/setup_optimized_cpp.py build_ext --inplace
```

## Which to Use?

- **For production**: Use `setup_buffer_cpp.py` - stable and performant
- **For experimentation**: Use `setup_optimized_cpp.py` - cutting-edge optimizations
- **For debugging**: Use `setup_cpp.py` - simplest implementation