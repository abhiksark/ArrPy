from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import numpy as np

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Define Cython extensions with OpenMP support
import os

# OpenMP flags for different platforms
openmp_compile_args = []
openmp_link_args = []

if os.name == 'posix':  # Unix/Linux/macOS
    # Try to detect if we have OpenMP support
    try:
        import subprocess
        result = subprocess.run(['gcc', '--version'], capture_output=True, text=True)
        if 'gcc' in result.stdout.lower():
            openmp_compile_args = ['-fopenmp']
            openmp_link_args = ['-fopenmp']
        else:
            # Clang on macOS might need different flags
            openmp_compile_args = ['-Xpreprocessor', '-fopenmp']
            openmp_link_args = ['-lomp']
    except:
        pass  # No OpenMP support
elif os.name == 'nt':  # Windows
    openmp_compile_args = ['/openmp']

extensions = [
    Extension(
        "arrpy.core.array_cython",
        ["arrpy/core/array_cython.pyx"],
        include_dirs=[np.get_include()],
        extra_compile_args=openmp_compile_args,
        extra_link_args=openmp_link_args,
    ),
    Extension(
        "arrpy.math.arithmetic_cython",
        ["arrpy/math/arithmetic_cython.pyx"],
        include_dirs=[np.get_include()],
        extra_compile_args=openmp_compile_args,
        extra_link_args=openmp_link_args,
    ),
    Extension(
        "arrpy.creation.basic_cython",
        ["arrpy/creation/basic_cython.pyx"],
        include_dirs=[np.get_include()],
        extra_compile_args=openmp_compile_args,
        extra_link_args=openmp_link_args,
    ),
]

setup(
    name="arrpy",
    version="0.2.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Cython-optimized implementation mimicking NumPy's ndarray functionality",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/arrpy",
    packages=find_packages(),
    ext_modules=cythonize(extensions, compiler_directives={'boundscheck': False, 'wraparound': False, 'language_level': 3}),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=[
        "cython>=0.29.0",
        "numpy>=1.19.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
        ],
    },
    zip_safe=False,
)