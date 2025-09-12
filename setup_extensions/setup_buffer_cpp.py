"""
Setup script for building the buffer protocol C++ extensions.
"""

from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup
import pybind11
import platform
import subprocess

# Determine compiler flags based on platform
extra_compile_args = []
extra_link_args = []
include_dirs = [pybind11.get_include()]

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
    
    # macOS-specific fixes
    if platform.system() == "Darwin":
        try:
            # Get the SDK path
            sdk_path = subprocess.check_output(["xcrun", "--show-sdk-path"]).decode().strip()
            # Add C++ standard library include path
            include_dirs.append(f"{sdk_path}/usr/include/c++/v1")
            # Ensure we use the SDK
            extra_compile_args.extend(["-isysroot", sdk_path])
            extra_link_args.extend(["-isysroot", sdk_path])
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fallback for older systems or if xcrun is not available
            pass
    
    # Platform-specific optimizations
    machine = platform.machine().lower()
    
    if machine in ["x86_64", "amd64"]:
        # Enable AVX2 if available on x86
        extra_compile_args.extend(["-mavx2", "-mfma"])
    elif machine in ["aarch64", "arm64"]:
        # ARM optimizations (NEON is typically enabled with -march=native)
        pass

# Define the C++ extension
ext_modules = [
    Pybind11Extension(
        "arrpy.backends.c.array_ops_buffer_cpp",
        ["arrpy/backends/c/array_ops_buffer.cpp"],
        include_dirs=include_dirs,
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
        cxx_std=14,
        language='c++',
    ),
]

setup(
    name="arrpy-buffer-cpp",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)