"""
Setup script for building the highly optimized C++ extensions.
Includes aggressive compiler optimizations and OpenMP support.
"""

from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup
import pybind11
import platform
import os

# Determine compiler flags based on platform
extra_compile_args = []
extra_link_args = []

if platform.system() == "Windows":
    extra_compile_args = [
        "/O2",           # Maximum optimization
        "/arch:AVX2",    # Enable AVX2
        "/fp:fast",      # Fast floating point
        "/openmp",       # OpenMP support
        "/GL",           # Whole program optimization
    ]
    extra_link_args = ["/LTCG"]  # Link time code generation
else:
    # Unix-like systems (Linux, macOS)
    extra_compile_args = [
        "-O3",                    # Maximum optimization
        "-ffast-math",            # Fast floating point
        "-funroll-loops",         # Loop unrolling
        "-ftree-vectorize",       # Auto-vectorization
        "-std=c++14",
        "-march=native",          # Enable all CPU features
        "-mtune=native",          # Optimize for current CPU
        "-fomit-frame-pointer",   # Remove frame pointer
        "-finline-functions",     # Inline functions
    ]
    
    # Add LTO only on Linux (not supported well on macOS clang)
    if platform.system() == "Linux":
        extra_compile_args.extend([
            "-flto",              # Link-time optimization
            "-fopt-info-vec",     # Report vectorization
            "-fprefetch-loop-arrays", # Prefetch arrays in loops
        ])
        extra_link_args = ["-flto"]  # Link-time optimization
    else:
        extra_link_args = []  # No special link flags for macOS
    
    # Platform-specific optimizations
    machine = platform.machine().lower()
    
    if machine in ["x86_64", "amd64"]:
        # Enable AVX2 if available on x86
        extra_compile_args.extend([
            "-mavx2",
            "-mfma",
            "-mavx",
            "-msse4.2",
        ])
    elif machine in ["aarch64", "arm64"]:
        # ARM optimizations (NEON is typically enabled with -march=native)
        pass
    
    # Add OpenMP support
    if platform.system() == "Darwin":  # macOS
        # macOS uses libomp from Homebrew
        if os.path.exists("/opt/homebrew/opt/libomp"):
            # Apple Silicon Mac
            extra_compile_args.extend([
                "-Xpreprocessor", "-fopenmp",
                "-I/opt/homebrew/opt/libomp/include"
            ])
            extra_link_args.extend([
                "-L/opt/homebrew/opt/libomp/lib",
                "-lomp"
            ])
        elif os.path.exists("/usr/local/opt/libomp"):
            # Intel Mac
            extra_compile_args.extend([
                "-Xpreprocessor", "-fopenmp",
                "-I/usr/local/opt/libomp/include"
            ])
            extra_link_args.extend([
                "-L/usr/local/opt/libomp/lib",
                "-lomp"
            ])
        else:
            print("Warning: OpenMP not found. Install with: brew install libomp")
    else:
        # Linux
        extra_compile_args.append("-fopenmp")
        extra_link_args.append("-fopenmp")

# Define the C++ extension
ext_modules = [
    Pybind11Extension(
        "arrpy.backends.c.array_ops_optimized_cpp",
        ["arrpy/backends/c/array_ops_optimized.cpp"],
        include_dirs=[pybind11.get_include()],
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
        cxx_std=14,
        language='c++',
    ),
]

setup(
    name="arrpy-optimized-cpp",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)

print("\nOptimization flags enabled:")
print(f"Compile args: {' '.join(extra_compile_args)}")
print(f"Link args: {' '.join(extra_link_args)}")