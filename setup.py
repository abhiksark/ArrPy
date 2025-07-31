from setuptools import setup, find_packages, Extension
import os
import sys

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Check if we should build C extensions
BUILD_C_EXT = os.environ.get('ARRPY_BUILD_C_EXT', '0') == '1'

ext_modules = []
if BUILD_C_EXT:
    try:
        import numpy as np
        # Define C extension
        c_array_module = Extension(
            'arrpy.c_src.c_array',
            sources=['arrpy/c_src/c_array.c'],
            include_dirs=[np.get_include()],
            extra_compile_args=['-O3', '-march=native', '-ffast-math'],
        )
        ext_modules = [c_array_module]
        print("Building with C extensions enabled")
    except ImportError:
        print("NumPy not found, skipping C extension build")
        BUILD_C_EXT = False

setup(
    name="arrpy",
    version="0.2.0",
    author="ArrPy Contributors",
    author_email="your.email@example.com",
    description="A pure Python implementation mimicking NumPy's ndarray functionality with optional C acceleration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/arrpy",
    packages=find_packages(),
    ext_modules=ext_modules,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: C",
    ],
    python_requires=">=3.6",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "numpy>=1.19.0",
        ],
        "c-ext": [
            "numpy>=1.19.0",  # Required for building C extensions
        ],
    },
)