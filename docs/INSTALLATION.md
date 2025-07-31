# ArrPy Installation Guide

## Table of Contents
- [Quick Start](#quick-start)
- [System Requirements](#system-requirements)
- [Installation Methods](#installation-methods)
  - [From Source (Recommended)](#from-source-recommended)
  - [Development Installation](#development-installation)
  - [C Extensions Installation](#c-extensions-installation)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Platform-Specific Instructions](#platform-specific-instructions)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/ArrPy.git
cd ArrPy

# Install in development mode
pip install -e .

# Optional: Build C extensions for better performance
python setup_c_ext.py build_ext --inplace
```

## System Requirements

### Minimum Requirements
- Python 3.7 or higher
- pip package manager
- 100 MB free disk space

### For C Extensions (Optional but Recommended)
- C compiler (GCC 7+ on Linux/Mac, MSVC on Windows)
- Python development headers
- NumPy (for building only, not runtime)
- OpenMP support (optional, for parallelization)

### Tested Platforms
- ✅ Ubuntu 20.04+ (x86_64, ARM64)
- ✅ macOS 11+ (Intel, Apple Silicon)
- ✅ Windows 10/11 (x64)
- ✅ CentOS/RHEL 8+
- ✅ Debian 10+

## Installation Methods

### From Source (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ArrPy.git
   cd ArrPy
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Linux/Mac:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install ArrPy**:
   ```bash
   pip install -e .
   ```

### Development Installation

For contributors and developers:

1. **Clone with full history**:
   ```bash
   git clone --recursive https://github.com/yourusername/ArrPy.git
   cd ArrPy
   ```

2. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

3. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

### C Extensions Installation

For maximum performance, build the C extensions:

1. **Install build dependencies**:
   
   **On Ubuntu/Debian**:
   ```bash
   sudo apt-get update
   sudo apt-get install build-essential python3-dev
   ```
   
   **On CentOS/RHEL/Fedora**:
   ```bash
   sudo yum groupinstall "Development Tools"
   sudo yum install python3-devel
   ```
   
   **On macOS**:
   ```bash
   # Install Xcode Command Line Tools
   xcode-select --install
   ```
   
   **On Windows**:
   - Install Visual Studio Build Tools or full Visual Studio
   - Ensure "Desktop development with C++" workload is selected

2. **Build C extensions**:
   ```bash
   python setup_c_ext.py build_ext --inplace
   ```

3. **Verify C extensions are loaded**:
   ```bash
   python -c "from arrpy import Array; a = Array([1,2,3]); print('C extensions:', hasattr(a, '_c_array'))"
   ```

## Verification

### Basic Verification

```python
# Test basic functionality
import arrpy as ap

# Create array
arr = ap.Array([1, 2, 3, 4, 5])
print("Array created:", arr)

# Test operations
print("Sum:", arr.sum())
print("Mean:", arr.mean())
print("Addition:", arr + 10)

# Check backend
from arrpy.core import HAS_C_EXTENSION
print("C extensions available:", HAS_C_EXTENSION)
```

### Performance Verification

```python
import time
import arrpy as ap

# Create large array
size = 1000000
data = list(range(size))

# Time array creation
start = time.time()
arr = ap.Array(data)
print(f"Array creation took: {time.time() - start:.4f}s")

# Time sum operation
start = time.time()
result = arr.sum()
print(f"Sum operation took: {time.time() - start:.4f}s")

# With C extensions, these should be significantly faster
```

### Run Test Suite

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=arrpy

# Run specific test categories
pytest tests/core/
pytest tests/math/
pytest tests/performance/
```

## Troubleshooting

### Common Issues

#### 1. ImportError: No module named 'arrpy'
**Solution**: Ensure you're in the correct directory and have installed ArrPy:
```bash
cd /path/to/ArrPy
pip install -e .
```

#### 2. C Extensions not building
**Error**: `error: Microsoft Visual C++ 14.0 or greater is required`

**Solution for Windows**:
- Download and install Visual Studio Build Tools
- Select "Desktop development with C++" workload
- Restart terminal and try again

**Solution for Linux/Mac**:
```bash
# Install compiler and Python headers
sudo apt-get install build-essential python3-dev  # Ubuntu/Debian
sudo yum install gcc python3-devel  # CentOS/RHEL
```

#### 3. OpenMP not found warning
**Warning**: `OpenMP not found, parallel operations will be slower`

**Solution**:
```bash
# Ubuntu/Debian
sudo apt-get install libomp-dev

# macOS
brew install libomp

# CentOS/RHEL
sudo yum install libomp-devel
```

#### 4. Permission denied during installation
**Solution**: Use `--user` flag or virtual environment:
```bash
pip install --user -e .
# OR
python -m venv venv && source venv/bin/activate
```

### Platform-Specific Instructions

#### Linux (Ubuntu/Debian)

```bash
# Complete installation script
sudo apt-get update
sudo apt-get install -y build-essential python3-dev python3-pip git

git clone https://github.com/yourusername/ArrPy.git
cd ArrPy
python3 -m venv venv
source venv/bin/activate
pip install -e .
python setup_c_ext.py build_ext --inplace
```

#### macOS

```bash
# Ensure Homebrew is installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python3 libomp

# Clone and install
git clone https://github.com/yourusername/ArrPy.git
cd ArrPy
python3 -m venv venv
source venv/bin/activate
pip install -e .
python setup_c_ext.py build_ext --inplace
```

#### Windows

1. Install Python from [python.org](https://python.org)
2. Install Git from [git-scm.com](https://git-scm.com)
3. Install Visual Studio Build Tools
4. Open Command Prompt or PowerShell:

```powershell
git clone https://github.com/yourusername/ArrPy.git
cd ArrPy
python -m venv venv
venv\Scripts\activate
pip install -e .
python setup_c_ext.py build_ext --inplace
```

### Docker Installation

```dockerfile
FROM python:3.9-slim

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clone and install ArrPy
RUN git clone https://github.com/yourusername/ArrPy.git /app
WORKDIR /app
RUN pip install -e . && \
    python setup_c_ext.py build_ext --inplace

# Verify installation
RUN python -c "import arrpy; print('ArrPy installed successfully')"
```

## Environment Variables

ArrPy supports several environment variables for configuration:

```bash
# Force pure Python mode (disable C extensions)
export ARRPY_FORCE_PYTHON=1

# Enable debug mode
export ARRPY_DEBUG=1

# Set number of threads for parallel operations
export ARRPY_NUM_THREADS=8
```

## Uninstallation

To remove ArrPy:

```bash
pip uninstall arrpy

# Clean build artifacts
rm -rf build/ dist/ *.egg-info
rm -f arrpy/c_src/*.so arrpy/c_src/*.pyd
```

## Next Steps

- Read the [User Guide](guides/USER_GUIDE.md)
- Check out [Examples](examples/)
- Explore the [API Documentation](api/)
- View [Performance Benchmarks](../PERFORMANCE_REPORT.md)

## Getting Help

- 📖 [Documentation](https://arrpy.readthedocs.io)
- 💬 [GitHub Discussions](https://github.com/yourusername/ArrPy/discussions)
- 🐛 [Issue Tracker](https://github.com/yourusername/ArrPy/issues)
- 📧 Email: support@arrpy.org