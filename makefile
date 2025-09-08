# ArrPy Development Makefile with ASCII Banner
# Simplifies common development tasks

# Colors for terminal output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
MAGENTA := \033[0;35m
CYAN := \033[0;36m
WHITE := \033[0;37m
RESET := \033[0m

# ASCII Art Banner
define ARRPY_BANNER
$(CYAN)
     ___                  ____          
    /   |  _____  _____  / __ \__  __   
   / /| | / ___/ / ___/ / /_/ / / / /   
  / ___ |/ /    / /    / ____/ /_/ /    
 /_/  |_/_/    /_/    /_/    \__, /     
                            /____/      
$(RESET)
$(YELLOW) 🚀 Educational NumPy Recreation$(RESET)
$(GREEN) 📚 Learn by Building | v0.1.0$(RESET)
$(BLUE)════════════════════════════════════════$(RESET)
endef
export ARRPY_BANNER

# Default target shows banner and help
.DEFAULT_GOAL := banner-help

.PHONY: banner banner-help help install dev test bench clean build docs \
        test-python test-cython test-c bench-python bench-cython bench-c \
        build-cython build-cpp status

# Show banner only
banner:
	@echo "$$ARRPY_BANNER"

# Show banner with help (default)
banner-help: banner
	@echo "$(WHITE)Available Commands:$(RESET)"
	@echo "$(CYAN)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"
	@echo "$(GREEN)make install$(RESET)    - Install ArrPy in production mode"
	@echo "$(GREEN)make dev$(RESET)        - Install ArrPy in development mode"
	@echo "$(GREEN)make test$(RESET)       - Run all tests"
	@echo "$(GREEN)make bench$(RESET)      - Run benchmarks"
	@echo "$(GREEN)make clean$(RESET)      - Clean build artifacts"
	@echo "$(GREEN)make build$(RESET)      - Build all extensions"
	@echo "$(GREEN)make status$(RESET)     - Show backend status"
	@echo ""
	@echo "$(WHITE)Backend-specific commands:$(RESET)"
	@echo "$(CYAN)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"
	@echo "$(YELLOW)make test-python$(RESET)  - Test Python backend"
	@echo "$(YELLOW)make test-cython$(RESET)  - Test Cython backend"
	@echo "$(YELLOW)make test-c$(RESET)       - Test C++ backend"
	@echo "$(YELLOW)make bench-compare$(RESET) - Compare all backends"
	@echo ""
	@echo "$(WHITE)Build commands:$(RESET)"
	@echo "$(CYAN)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"
	@echo "$(MAGENTA)make build-cython$(RESET) - Build Cython extensions"
	@echo "$(MAGENTA)make build-cpp$(RESET)    - Build C++ extensions"
	@echo ""

# Shorter help without banner
help:
	@echo "$(WHITE)ArrPy Commands:$(RESET)"
	@echo "  install    - Install in production mode"
	@echo "  dev        - Install in development mode"
	@echo "  test       - Run all tests"
	@echo "  bench      - Run benchmarks"
	@echo "  clean      - Clean build artifacts"
	@echo "  build      - Build all extensions"
	@echo "  status     - Show backend status"

# Installation targets with banner
install: banner
	@echo "$(GREEN)Installing ArrPy...$(RESET)"
	pip install .
	@echo "$(GREEN)✓ Installation complete!$(RESET)"

dev: banner
	@echo "$(GREEN)Installing ArrPy in development mode...$(RESET)"
	pip install -e .
	pip install -r requirements-dev.txt
	@echo "$(GREEN)✓ Development setup complete!$(RESET)"

# Testing targets with banner
test: banner
	@echo "$(CYAN)Running all tests...$(RESET)"
	pytest tests/ -v
	@echo "$(GREEN)✓ Tests complete!$(RESET)"

test-python:
	@echo "$(YELLOW)Testing Python backend...$(RESET)"
	ARRPY_BACKEND=python pytest tests/ -v

test-cython:
	@echo "$(YELLOW)Testing Cython backend...$(RESET)"
	ARRPY_BACKEND=cython pytest tests/ -v

test-c:
	@echo "$(YELLOW)Testing C++ backend...$(RESET)"
	ARRPY_BACKEND=c pytest tests/ -v

test-coverage: banner
	@echo "$(CYAN)Running tests with coverage...$(RESET)"
	pytest tests/ --cov=arrpy --cov-report=html --cov-report=term
	@echo "$(GREEN)✓ Coverage report generated!$(RESET)"

# Benchmark targets with banner
bench: banner
	@echo "$(MAGENTA)Running benchmarks...$(RESET)"
	python benchmarks/benchmark_v1.py

bench-python:
	@echo "$(YELLOW)Benchmarking Python backend...$(RESET)"
	ARRPY_BACKEND=python python benchmarks/bench_core.py

bench-cython:
	@echo "$(YELLOW)Benchmarking Cython backend...$(RESET)"
	ARRPY_BACKEND=cython python benchmarks/bench_core.py

bench-c:
	@echo "$(YELLOW)Benchmarking C++ backend...$(RESET)"
	ARRPY_BACKEND=c python benchmarks/bench_core.py

bench-compare: banner
	@echo "$(MAGENTA)Comparing all backends...$(RESET)"
	python benchmarks/compare_backends.py
	@echo "$(GREEN)✓ Comparison complete!$(RESET)"

bench-vs-numpy: banner
	@echo "$(MAGENTA)Benchmarking against NumPy...$(RESET)"
	python benchmarks/benchmark_vs_numpy.py

# Build targets with banner
build: banner build-cython build-cpp
	@echo "$(GREEN)✓ All extensions built successfully!$(RESET)"

build-cython:
	@echo "$(CYAN)Building Cython extensions...$(RESET)"
	python setup.py build_ext --inplace
	@echo "$(GREEN)✓ Cython build complete!$(RESET)"

build-cpp:
	@echo "$(CYAN)Building C++ extensions...$(RESET)"
	python setup_extensions/setup_buffer_cpp.py build_ext --inplace
	@echo "$(GREEN)✓ C++ build complete!$(RESET)"

build-cpp-optimized:
	@echo "$(CYAN)Building optimized C++ extensions...$(RESET)"
	python setup_extensions/setup_optimized_cpp.py build_ext --inplace
	@echo "$(GREEN)✓ Optimized C++ build complete!$(RESET)"

# Clean target with banner
clean: banner
	@echo "$(RED)Cleaning build artifacts...$(RESET)"
	rm -rf build/
	rm -rf *.egg-info
	rm -rf dist/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.so" -delete
	find . -type f -name "*.c" -path "*/cython/*" -delete
	find . -type f -name "*.cpp" -path "*/cython/*" -delete
	@echo "$(GREEN)✓ Cleanup complete!$(RESET)"

# Status command to show backend availability
status: banner
	@echo "$(WHITE)Backend Status:$(RESET)"
	@echo "$(CYAN)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"
	@python scripts/check_backends.py 2>/dev/null || python -c "import arrpy; print('✓ Python backend: Available')"
	@echo "$(CYAN)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"

# Quick start guide
quickstart: banner
	@echo "$(WHITE)Quick Start Guide:$(RESET)"
	@echo "$(CYAN)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"
	@echo "1. $(GREEN)make dev$(RESET)         # Set up development environment"
	@echo "2. $(GREEN)make build$(RESET)       # Build all extensions"
	@echo "3. $(GREEN)make test$(RESET)        # Run tests"
	@echo "4. $(GREEN)make bench$(RESET)       # Run benchmarks"
	@echo "5. $(GREEN)make status$(RESET)      # Check backend availability"
	@echo "$(CYAN)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"

# Interactive demo
demo: banner
	@echo "$(MAGENTA)Starting ArrPy interactive demo...$(RESET)"
	@python -c "import arrpy; \
		print('Creating arrays...'); \
		a = arrpy.arange(10); \
		b = arrpy.ones(10); \
		print(f'a = {a}'); \
		print(f'b = {b}'); \
		c = a + b; \
		print(f'a + b = {c}'); \
		print(f'Sum: {c.sum()}'); \
		print(''); \
		print('Try different backends:'); \
		print('  arrpy.set_backend(\"python\")'); \
		print('  arrpy.set_backend(\"cython\")'); \
		print('  arrpy.set_backend(\"c\")')"

# Development workflow
workflow: banner
	@echo "$(WHITE)Development Workflow:$(RESET)"
	@echo "$(CYAN)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"
	@echo "$(YELLOW)1. Code Development:$(RESET)"
	@echo "   Edit files → $(GREEN)make build$(RESET) → $(GREEN)make test$(RESET)"
	@echo ""
	@echo "$(YELLOW)2. Performance Testing:$(RESET)"
	@echo "   $(GREEN)make bench-compare$(RESET) → Analyze results"
	@echo ""
	@echo "$(YELLOW)3. Backend Development:$(RESET)"
	@echo "   Python: Edit → Test immediately"
	@echo "   Cython: Edit → $(GREEN)make build-cython$(RESET) → Test"
	@echo "   C++: Edit → $(GREEN)make build-cpp$(RESET) → Test"
	@echo "$(CYAN)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"

.PHONY: banner banner-help quickstart demo workflow status