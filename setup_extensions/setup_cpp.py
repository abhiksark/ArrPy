"""
Setup script for building C++ extensions with PyBind11.
"""

from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup, find_packages
import pybind11
import platform

# Determine compiler flags based on platform
extra_compile_args = []
extra_link_args = []

if platform.system() == "Windows":
    extra_compile_args = ["/O2", "/arch:AVX2"]
else:
    # Unix-like systems (Linux, macOS)
    extra_compile_args = [
        "-O3",
        "-ffast-math",
        "-funroll-loops",
        "-std=c++14",
    ]
    
    # Try to enable OpenMP if available (mainly for Linux)
    if platform.system() == "Linux":
        extra_compile_args.append("-fopenmp")
        extra_link_args.append("-fopenmp")
    else:
        extra_link_args = []
    
    # Platform-specific optimizations
    machine = platform.machine().lower()
    
    if machine in ["x86_64", "amd64"]:
        # x86/x64 processors
        extra_compile_args.append("-march=native")
        # Let compiler detect AVX2/SSE support
    elif machine in ["aarch64", "arm64"]:
        # ARM processors (Apple Silicon, etc.)
        extra_compile_args.append("-march=native")
        # NEON is typically enabled by default on ARM64
    else:
        # Generic fallback
        extra_compile_args.append("-O3")

# Define C++ extensions
ext_modules = [
    Pybind11Extension(
        "arrpy.backends.c.array_ops_cpp",
        ["arrpy/backends/c/array_ops.cpp"],
        include_dirs=[pybind11.get_include()],
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
        cxx_std=14,
    ),
    Pybind11Extension(
        "arrpy.backends.c.linalg_ops_cpp",
        ["arrpy/backends/c/linalg_ops.cpp"],
        include_dirs=[pybind11.get_include()],
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
        cxx_std=14,
    ),
    Pybind11Extension(
        "arrpy.backends.c.reduction_ops_cpp",
        ["arrpy/backends/c/reduction_ops.cpp"],
        include_dirs=[pybind11.get_include()],
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
        cxx_std=14,
    ),
    Pybind11Extension(
        "arrpy.backends.c.ufuncs_ops_cpp",
        ["arrpy/backends/c/ufuncs_ops.cpp"],
        include_dirs=[pybind11.get_include()],
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
        cxx_std=14,
    ),
]

setup(
    name="arrpy-cpp",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)