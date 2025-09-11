"""
Setup script for ArrPy package with Cython extensions.
"""

from setuptools import setup, find_packages, Extension
import numpy as np

# Try to use Cython if available
try:
    from Cython.Build import cythonize
    USE_CYTHON = True
except ImportError:
    USE_CYTHON = False
    print("Warning: Cython not available, building without Cython extensions")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

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
            "arrpy.backends.cython.array_ops_new",
            ["arrpy/backends/cython/array_ops_new.pyx"],
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
            extra_compile_args=["-O3", "-ffast-math"],
        ),
        # Experimental modules (only compile standalone modules)
        Extension(
            "arrpy.backends.cython.experimental.typed_ops",
            ["arrpy/backends/cython/experimental/typed_ops.pyx"],
            include_dirs=[np.get_include()],
            extra_compile_args=["-O3", "-ffast-math"],
        ),
    ]
    ext_modules = cythonize(
        extensions,
        compiler_directives={
            'language_level': "3",
            'boundscheck': False,
            'wraparound': False,
        }
    )

setup(
    name="arrpy",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Educational NumPy recreation for learning internals",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/arrpy",
    packages=find_packages(),
    ext_modules=ext_modules,
    classifiers=[
        "Programming Language :: Cython",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",  # Required for Cython extensions
    ],
    setup_requires=[
        "numpy>=1.20.0",
        "cython>=0.29.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-benchmark>=4.0.0",
            "numpy>=1.20.0",  # For testing comparison
            "ruff>=0.1.0",
            "black>=23.0.0",
        ],
    },
)