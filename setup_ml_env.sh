#!/bin/bash

# ArrPy ML Environment Setup Script
# This script activates the conda ml environment and sets up the proper paths

echo "🐍 Setting up ArrPy with Conda ML Environment"
echo "=============================================="

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "❌ Error: Conda is not available in PATH"
    echo "Please install conda or add it to your PATH"
    exit 1
fi

# Check if ml environment exists
if [ ! -d "/opt/miniconda3/envs/ml" ]; then
    echo "❌ Error: ML environment not found at /opt/miniconda3/envs/ml"
    echo "Please create the ml environment first:"
    echo "conda create -n ml python=3.10 numpy matplotlib pandas scipy -y"
    exit 1
fi

# Activate the ml environment
echo "🔄 Activating conda ml environment..."
source /opt/miniconda3/bin/activate ml

# Verify activation
if [[ "$CONDA_DEFAULT_ENV" == "ml" ]]; then
    echo "✅ Successfully activated ml environment"
else
    echo "❌ Failed to activate ml environment"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
echo "🐍 Python version: $PYTHON_VERSION"

# Check key packages
echo "📦 Checking key packages..."
python -c "
import sys
packages = ['numpy', 'matplotlib', 'pandas']
for pkg in packages:
    try:
        mod = __import__(pkg)
        version = getattr(mod, '__version__', 'unknown')
        print(f'✅ {pkg}: {version}')
    except ImportError:
        print(f'❌ {pkg}: not installed')
        sys.exit(1)
"

# Test ArrPy import
echo "🧮 Testing ArrPy import..."
python -c "
try:
    import arrpy as ap
    print(f'✅ ArrPy {ap.__version__} imported successfully')
    
    # Quick functionality test
    a = ap.Array([1, 2, 3])
    result = a.sum()
    print(f'✅ Basic functionality test passed (sum=[1,2,3] = {result})')
except Exception as e:
    print(f'❌ ArrPy import failed: {e}')
    exit(1)
"

echo ""
echo "🎉 ML Environment setup complete!"
echo ""
echo "Available commands:"
echo "  📊 Run benchmarks:           cd benchmarks && python scalability_test.py"
echo "  🧪 Run tests:                python -m pytest tests/ -v"  
echo "  📈 Performance comparison:   cd benchmarks && python performance_comparison.py"
echo "  📊 Generate plots:           cd benchmarks && python scalability_test.py"
echo ""
echo "💡 To manually activate this environment, run:"
echo "   source /opt/miniconda3/bin/activate ml"
echo ""

# Keep the environment activated for the current session
exec "$SHELL"