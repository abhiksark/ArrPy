"""
Setup script for ArrPy package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

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
    classifiers=[
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
    install_requires=[],
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