"""
Test configuration for ArrPy.

This file configures pytest to handle both pure Python and C-accelerated
implementations transparently.
"""

import os
import pytest
import warnings

# Suppress C extension warnings during tests
os.environ['ARRPY_WARN_NO_C_EXT'] = '0'

# Configure warning filters
warnings.filterwarnings("ignore", category=RuntimeWarning, module="arrpy.core")


@pytest.fixture(scope="session", autouse=True)
def configure_test_environment():
    """Configure test environment for both backends."""
    print("\nTest Configuration:")
    
    # Check if we can import the C extension
    try:
        import arrpy
        if arrpy.core.HAS_C_EXTENSION:
            print("  ✓ Testing with C extensions enabled")
        else:
            print("  ✓ Testing with pure Python implementation")
    except Exception as e:
        print(f"  ⚠ Warning: {e}")
    
    yield
    
    # Cleanup if needed
    pass


@pytest.fixture
def use_python_backend():
    """Force use of Python backend for specific tests."""
    original = os.environ.get('ARRPY_FORCE_PYTHON', '0')
    os.environ['ARRPY_FORCE_PYTHON'] = '1'
    
    # Clear any cached imports
    import sys
    modules_to_clear = [m for m in sys.modules if m.startswith('arrpy')]
    for module in modules_to_clear:
        del sys.modules[module]
    
    yield
    
    # Restore original setting
    os.environ['ARRPY_FORCE_PYTHON'] = original
    
    # Clear imports again
    modules_to_clear = [m for m in sys.modules if m.startswith('arrpy')]
    for module in modules_to_clear:
        del sys.modules[module]


@pytest.fixture
def use_c_backend():
    """Force use of C backend for specific tests (if available)."""
    original = os.environ.get('ARRPY_FORCE_PYTHON', '0')
    os.environ['ARRPY_FORCE_PYTHON'] = '0'
    
    # Clear any cached imports
    import sys
    modules_to_clear = [m for m in sys.modules if m.startswith('arrpy')]
    for module in modules_to_clear:
        del sys.modules[module]
    
    yield
    
    # Restore original setting
    os.environ['ARRPY_FORCE_PYTHON'] = original
    
    # Clear imports again
    modules_to_clear = [m for m in sys.modules if m.startswith('arrpy')]
    for module in modules_to_clear:
        del sys.modules[module]