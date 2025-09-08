# Multi-stage Docker build for ArrPy
# Supports development and production environments

# Stage 1: Build environment
FROM python:3.10-slim as builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    cmake \
    make \
    libblas-dev \
    liblapack-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /build

# Copy requirements first for better caching
COPY requirements.txt requirements-dev.txt ./
RUN pip install --upgrade pip wheel setuptools

# Install dependencies
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels -r requirements.txt
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels -r requirements-dev.txt

# Copy source code
COPY . .

# Build Cython extensions
RUN pip install cython numpy
RUN python setup.py build_ext --inplace

# Build C++ extensions (Linux only)
RUN python setup_cpp.py build_ext --inplace || echo "C++ build optional"

# Stage 2: Runtime environment
FROM python:3.10-slim as runtime

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libblas3 \
    liblapack3 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -s /bin/bash arrpy

# Set working directory
WORKDIR /app

# Copy wheels from builder
COPY --from=builder /build/wheels /wheels

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache /wheels/* && \
    rm -rf /wheels

# Copy built extensions and source
COPY --from=builder --chown=arrpy:arrpy /build/arrpy /app/arrpy
COPY --from=builder --chown=arrpy:arrpy /build/examples /app/examples
COPY --from=builder --chown=arrpy:arrpy /build/tutorials /app/tutorials
COPY --from=builder --chown=arrpy:arrpy /build/benchmarks /app/benchmarks
COPY --from=builder --chown=arrpy:arrpy /build/tests /app/tests
COPY --from=builder --chown=arrpy:arrpy /build/setup.py /app/
COPY --from=builder --chown=arrpy:arrpy /build/pyproject.toml /app/
COPY --from=builder --chown=arrpy:arrpy /build/README.md /app/

# Install ArrPy
RUN pip install -e .

# Switch to non-root user
USER arrpy

# Set environment variables
ENV PYTHONPATH=/app:$PYTHONPATH
ENV ARRPY_BACKEND=python

# Default command
CMD ["python", "-c", "import arrpy; print('ArrPy v1.0.0 ready!'); print('Backend:', arrpy.get_backend())"]

# Stage 3: Development environment
FROM runtime as development

USER root

# Install development tools
RUN pip install jupyter notebook ipython

# Create workspace
RUN mkdir -p /workspace && chown arrpy:arrpy /workspace
WORKDIR /workspace

USER arrpy

# Expose Jupyter port
EXPOSE 8888

# Development command
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--allow-root"]

# Stage 4: Testing environment
FROM runtime as testing

USER root

# Copy test requirements
COPY --from=builder /build/requirements-dev.txt /app/

# Install test dependencies
RUN pip install pytest pytest-cov pytest-benchmark

USER arrpy

# Run tests by default
CMD ["pytest", "tests/", "-v", "--cov=arrpy"]