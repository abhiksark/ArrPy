# Makefile for ArrPy development

.PHONY: help install install-dev test test-cov test-specific benchmark benchmark-compare lint format clean

help:
	@echo "Available commands:"
	@echo "  make install        Install ArrPy package"
	@echo "  make install-dev    Install with development dependencies"
	@echo "  make test          Run all tests"
	@echo "  make test-cov      Run tests with coverage report"
	@echo "  make test-specific  Run specific test file (use TEST=filename)"
	@echo "  make benchmark     Run performance benchmarks"
	@echo "  make benchmark-compare  Compare performance with NumPy"
	@echo "  make lint          Run code linting with ruff"
	@echo "  make format        Format code with black and ruff"
	@echo "  make clean         Clean build artifacts"

install:
	pip install -e .

install-dev:
	pip install -e .[dev]

test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=arrpy --cov-report=html --cov-report=term

test-specific:
	@if [ -z "$(TEST)" ]; then \
		echo "Usage: make test-specific TEST=test_arrpy"; \
		exit 1; \
	fi
	pytest tests/$(TEST).py -v

benchmark:
	python benchmarks/run_benchmarks.py

benchmark-compare:
	python benchmarks/run_benchmarks.py --compare-numpy

lint:
	ruff check arrpy/ tests/

format:
	black arrpy/ tests/ benchmarks/
	ruff check --fix arrpy/ tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete