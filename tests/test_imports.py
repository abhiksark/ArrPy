"""
Centralized imports for tests to handle hybrid array compatibility.
"""

import sys
import os

# Add parent directory to path so we can import arrpy
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Array class (which could be HybridArray or pure Python Array)
from arrpy import Array

# For tests that need to check isinstance, we need to handle both cases
import arrpy



# Get the actual Array type being used
# The Array imported from arrpy could be HybridArray or pure Python Array
# Check what type it actually is
if hasattr(arrpy.core, 'hybrid_array'):
    # We're using the hybrid implementation
    from arrpy.core.hybrid_array import HybridArray
    from arrpy.core.array import Array as PythonArray
    ArrayType = (PythonArray, HybridArray)
else:
    # Pure Python only
    ArrayType = arrpy.core.array.Array

# Helper function for type checking in tests
def is_array(obj):
    """Check if object is an Array (works with both implementations)."""
    return isinstance(obj, ArrayType)