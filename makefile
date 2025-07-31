# Makefile for ArrPy - Cython optimized version

.PHONY: clean build install test benchmark cython

# Default target
all: build

# Build Cython extensions
build:
	python setup.py build_ext --inplace

# Install in development mode
install:
	pip install -e .

# Build Cython extensions
cython:
	python setup.py build_ext --inplace

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -name "*.c" -delete
	find . -name "*.so" -delete
	find . -name "*.pyd" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete

# Run tests
test:
	python -m pytest tests/ -v

# Run benchmarks
benchmark:
	python benchmarks/performance_comparison.py

# Run micro benchmarks
micro-benchmark:
	python benchmarks/micro_benchmarks.py

# Check if Cython extensions are properly built
check:
	python -c "from arrpy.core import Array; print('Core Array imported successfully')"
	python -c "from arrpy.math import power; print('Math functions imported successfully')"
	python -c "from arrpy.creation import zeros; print('Creation functions imported successfully')"

# Help
help:
	@echo "Available targets:"
	@echo "  build          - Build Cython extensions"
	@echo "  install        - Install in development mode"
	@echo "  cython         - Build Cython extensions (alias for build)"
	@echo "  clean          - Clean build artifacts"
	@echo "  test           - Run tests"
	@echo "  benchmark      - Run performance benchmarks"
	@echo "  micro-benchmark- Run micro benchmarks"
	@echo "  check          - Verify Cython extensions are working"
	@echo "  help           - Show this help message"