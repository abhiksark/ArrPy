"""
Setup script for building Cython extensions.
Configuration is in pyproject.toml - this file only handles extension building.
"""

from setuptools import setup, Extension
import numpy as np

# Try to use Cython if available
try:
    from Cython.Build import cythonize
    USE_CYTHON = True
except ImportError:
    USE_CYTHON = False
    print("Warning: Cython not available, building without Cython extensions")

# Define Cython extensions if available
ext_modules = []
if USE_CYTHON:
    extensions = [
        Extension(
            "arrpy.backends.cython.array_ops",
            ["arrpy/backends/cython/array_ops.pyx"],
            include_dirs=[np.get_include()],
            extra_compile_args=["-O3", "-ffast-math"],
        ),
        Extension(
            "arrpy.backends.cython.linalg_ops",
            ["arrpy/backends/cython/linalg_ops.pyx"],
            include_dirs=[np.get_include()],
            extra_compile_args=["-O3", "-ffast-math"],
        ),
        Extension(
            "arrpy.backends.cython.reduction_ops",
            ["arrpy/backends/cython/reduction_ops.pyx"],
            include_dirs=[np.get_include()],
            extra_compile_args=["-O3", "-ffast-math"],
        ),
        Extension(
            "arrpy.backends.cython.ufuncs_ops",
            ["arrpy/backends/cython/ufuncs_ops.pyx"],
            include_dirs=[np.get_include()],
            extra_compile_args=["-O3"],  # Removed -ffast-math to avoid vectorization issues
            libraries=["m"],  # Link with math library
        ),
        # Note: Experimental modules have been moved to experimental_archive
    ]
    ext_modules = cythonize(
        extensions,
        compiler_directives={
            'language_level': "3",
            'boundscheck': False,
            'wraparound': False,
        }
    )

# Configuration is now in pyproject.toml
# This setup.py is only for building Cython extensions
setup(
    ext_modules=ext_modules,
)