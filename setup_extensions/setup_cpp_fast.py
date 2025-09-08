"""
Setup script for building fast C++ extensions with zero-copy numpy support.
"""

from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup
import pybind11
import numpy as np
import platform

# Determine compiler flags based on platform
extra_compile_args = []
extra_link_args = []

if platform.system() == "Windows":
    extra_compile_args = ["/O2", "/arch:AVX2", "/fp:fast"]
else:
    # Unix-like systems (Linux, macOS)
    extra_compile_args = [
        "-O3",
        "-ffast-math",
        "-funroll-loops",
        "-std=c++14",
        "-march=native",  # Enable all CPU features
        "-mtune=native",  # Optimize for current CPU
    ]
    
    # Try to enable OpenMP if available (mainly for Linux)
    if platform.system() == "Linux":
        extra_compile_args.extend(["-fopenmp", "-pthread"])
        extra_link_args.extend(["-fopenmp", "-pthread"])
    
    # Platform-specific optimizations
    machine = platform.machine().lower()
    
    if machine in ["x86_64", "amd64"]:
        # Enable AVX2 if available
        extra_compile_args.extend([
            "-mavx2",
            "-mfma",  # Fused multiply-add
        ])
    elif machine in ["aarch64", "arm64"]:
        # ARM optimizations (NEON is typically enabled with -march=native)
        pass

# Define the fast C++ extension
ext_modules = [
    Pybind11Extension(
        "arrpy.backends.c.array_ops_fast_cpp",
        ["arrpy/backends/c/array_ops_fast.cpp"],
        include_dirs=[
            pybind11.get_include(),
            np.get_include(),  # NumPy headers for array API
        ],
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
        cxx_std=14,
        language='c++',
    ),
]

setup(
    name="arrpy-cpp-fast",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)