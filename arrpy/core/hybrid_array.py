"""
Hybrid Array implementation that uses C backend when available.

This module provides a transparent interface that automatically uses
the C-accelerated backend for performance when available, falling back
to pure Python implementation otherwise.
"""

import os
import warnings

# Try to import C extension
try:
    from ..c_src import c_array
    HAS_C_EXTENSION = True
    CArray = c_array.CArray
    c_zeros = c_array.zeros
    c_ones = c_array.ones
except ImportError:
    HAS_C_EXTENSION = False
    CArray = None
    c_zeros = None
    c_ones = None
    if os.environ.get('ARRPY_WARN_NO_C_EXT', '1') == '1':
        warnings.warn(
            "C extensions not available. Using pure Python implementation. "
            "Performance will be significantly reduced. "
            "To build C extensions, run: python setup_c_ext.py build_ext --inplace",
            RuntimeWarning,
            stacklevel=2
        )

from .array import Array as PythonArray


class HybridArray:
    """
    Hybrid array implementation that automatically uses C backend when available.
    
    This class provides the same interface as the pure Python Array class,
    but delegates operations to the C backend for improved performance when
    the C extension is available.
    """
    
    def __init__(self, data, _c_array=None):
        """
        Initialize a hybrid array.
        
        Parameters
        ----------
        data : list or CArray
            Input data as nested lists or existing C array
        _c_array : CArray, optional
            Pre-existing C array object (internal use)
        """
        if _c_array is not None:
            # Wrap existing C array
            self._c_array = _c_array
            self.__dict__['_python_array'] = None
            self._use_c = True
        elif HAS_C_EXTENSION and isinstance(data, list):
            # Try to create C array
            try:
                self._c_array = CArray(data)
                self.__dict__['_python_array'] = None
                self._use_c = True
            except Exception:
                # Fall back to Python implementation
                self._c_array = None
                self.__dict__['_python_array'] = PythonArray(data)
                self._use_c = False
        else:
            # Use Python implementation
            self._c_array = None
            self.__dict__['_python_array'] = PythonArray(data)
            self._use_c = False
    
    @property
    def _python_array(self):
        """Get Python array, creating it if necessary."""
        if self._use_c and self.__dict__.get('_python_array') is None:
            # Create Python array from C array data
            data = [self._c_array[i] for i in range(self._c_array.size)]
            temp_array = PythonArray(data)
            if self._c_array.ndim > 1:
                temp_array = temp_array.reshape(self._c_array.shape)
            return temp_array
        return self.__dict__.get('_python_array')
    
    @property
    def shape(self):
        """Return the shape of the array."""
        if self._use_c:
            return self._c_array.shape
        else:
            return self._python_array.shape
    
    @property
    def size(self):
        """Return the total number of elements."""
        if self._use_c:
            return self._c_array.size
        else:
            return self._python_array.size
    
    @property
    def ndim(self):
        """Return the number of dimensions."""
        if self._use_c:
            return self._c_array.ndim
        else:
            return self._python_array.ndim
    
    @property
    def _data(self):
        """Access to internal data for testing compatibility."""
        if self._use_c:
            # Convert C array data to Python list
            # For now, return a list representation
            # This is mainly for test compatibility
            size = self._c_array.size
            return [self._c_array[i] for i in range(size)]
        else:
            return self._python_array._data
    
    @property
    def _shape(self):
        """Access to internal shape for testing compatibility."""
        return self.shape
    
    def __getitem__(self, key):
        """Get array element(s) by index."""
        if self._use_c:
            return self._c_array[key]
        else:
            return self._python_array[key]
    
    def __setitem__(self, key, value):
        """Set array element(s) by index."""
        if self._use_c:
            self._c_array[key] = value
        else:
            self._python_array[key] = value
    
    def __repr__(self):
        """String representation of the array."""
        if self._use_c:
            # Convert C array representation to match Python format
            repr_str = repr(self._c_array)
            return repr_str.replace('CArray', 'Array')
        else:
            return repr(self._python_array)
    
    def __add__(self, other):
        """Element-wise addition."""
        if self._use_c:
            if isinstance(other, HybridArray) and other._use_c:
                result = self._c_array + other._c_array
            else:
                result = self._c_array + other
            return HybridArray([], _c_array=result)
        else:
            # Handle HybridArray in pure Python mode
            if isinstance(other, HybridArray):
                other = other._python_array
            result = self._python_array + other
            return HybridArray(result._data)
    
    def __sub__(self, other):
        """Element-wise subtraction."""
        if self._use_c:
            # C implementation for subtraction needs to be added
            # For now, fall back to Python
            pass
        
        # Use Python implementation
        if isinstance(other, HybridArray):
            other = other._python_array if hasattr(other, '_python_array') else other
        result = self._python_array - other
        return HybridArray(result._data)
    
    def __mul__(self, other):
        """Element-wise multiplication."""
        # For now, always use Python implementation for multiplication
        # C implementation needs to be added
        if isinstance(other, HybridArray):
            other = other._python_array if hasattr(other, '_python_array') else other
        result = self._python_array * other
        return HybridArray(result._data)
    
    def __truediv__(self, other):
        """Element-wise division."""
        if self._use_c:
            # C implementation for division needs to be added
            # For now, fall back to Python
            pass
        
        # Use Python implementation
        if isinstance(other, HybridArray):
            other = other._python_array if hasattr(other, '_python_array') else other
        result = self._python_array / other
        return HybridArray(result._data)
    
    def sum(self):
        """Calculate sum of array elements."""
        if self._use_c:
            return self._c_array.sum()
        else:
            return self._python_array.sum()
    
    def mean(self):
        """Calculate mean of array elements."""
        if self._use_c:
            return self._c_array.mean()
        else:
            return self._python_array.mean()
    
    def min(self):
        """Find minimum value in the array."""
        if self._use_c:
            # C implementation for min needs to be added
            pass
        return self._python_array.min()
    
    def max(self):
        """Find maximum value in the array."""
        if self._use_c:
            # C implementation for max needs to be added
            pass
        return self._python_array.max()
    
    def reshape(self, new_shape):
        """Give a new shape to the array."""
        # Get internal python array
        if self._use_c:
            # Convert to Python array first
            python_array = self._python_array
        else:
            python_array = self._python_array
        
        # Reshape using Python implementation
        result = python_array.reshape(new_shape)
        
        # Create new HybridArray preserving the shape
        new_hybrid = HybridArray(result._data)
        # Fix the shape by manually setting internal array's shape
        if hasattr(new_hybrid, '_python_array'):
            new_hybrid._python_array._shape = result._shape
        return new_hybrid
    
    @property
    def T(self):
        """Transpose the array."""
        # For now, use Python implementation
        result = self._python_array.T
        return HybridArray(result._data)
    
    def dot(self, other):
        """Matrix multiplication."""
        # For now, use Python implementation
        if isinstance(other, HybridArray):
            other = other._python_array
        result = self._python_array.dot(other)
        return HybridArray(result._data)
    
    # Add all other methods that delegate to appropriate backend
    def std(self, ddof=0):
        """Calculate standard deviation."""
        return self._python_array.std(ddof)
    
    def var(self, ddof=0):
        """Calculate variance."""
        return self._python_array.var(ddof)
    
    def median(self):
        """Calculate median."""
        return self._python_array.median()
    
    def percentile(self, q):
        """Calculate percentile."""
        return self._python_array.percentile(q)
    
    def sqrt(self):
        """Element-wise square root."""
        result = self._python_array.sqrt()
        return HybridArray(result._data)
    
    def sin(self):
        """Element-wise sine."""
        result = self._python_array.sin()
        return HybridArray(result._data)
    
    def cos(self):
        """Element-wise cosine."""
        result = self._python_array.cos()
        return HybridArray(result._data)
    
    def exp(self):
        """Element-wise exponential."""
        result = self._python_array.exp()
        return HybridArray(result._data)
    
    def log(self):
        """Element-wise natural logarithm."""
        result = self._python_array.log()
        return HybridArray(result._data)
    
    # Comparison operations
    def __eq__(self, other):
        """Element-wise equality comparison."""
        if isinstance(other, HybridArray):
            other = other._python_array
        result = self._python_array == other
        return HybridArray(result._data)
    
    def __ne__(self, other):
        """Element-wise inequality comparison."""
        if isinstance(other, HybridArray):
            other = other._python_array
        result = self._python_array != other
        return HybridArray(result._data)
    
    def __gt__(self, other):
        """Element-wise greater than comparison."""
        if isinstance(other, HybridArray):
            other = other._python_array
        result = self._python_array > other
        return HybridArray(result._data)
    
    def __lt__(self, other):
        """Element-wise less than comparison."""
        if isinstance(other, HybridArray):
            other = other._python_array
        result = self._python_array < other
        return HybridArray(result._data)
    
    def __ge__(self, other):
        """Element-wise greater or equal comparison."""
        if isinstance(other, HybridArray):
            other = other._python_array
        result = self._python_array >= other
        return HybridArray(result._data)
    
    def __le__(self, other):
        """Element-wise less or equal comparison."""
        if isinstance(other, HybridArray):
            other = other._python_array
        result = self._python_array <= other
        return HybridArray(result._data)
    
    # Logical operations
    def logical_and(self, other):
        """Element-wise logical AND."""
        if isinstance(other, HybridArray):
            other = other._python_array
        result = self._python_array.logical_and(other)
        return HybridArray(result._data)
    
    def logical_or(self, other):
        """Element-wise logical OR."""
        if isinstance(other, HybridArray):
            other = other._python_array
        result = self._python_array.logical_or(other)
        return HybridArray(result._data)
    
    def logical_not(self):
        """Element-wise logical NOT."""
        result = self._python_array.logical_not()
        return HybridArray(result._data)


# Factory functions that use C backend when available
def hybrid_zeros(shape):
    """Create array filled with zeros using C backend if available."""
    if HAS_C_EXTENSION:
        try:
            c_arr = c_zeros(shape)
            return HybridArray([], _c_array=c_arr)
        except Exception:
            pass
    
    # Fall back to Python implementation
    from ..creation.basic import zeros as py_zeros
    result = py_zeros(shape)
    return HybridArray(result._data)


def hybrid_ones(shape):
    """Create array filled with ones using C backend if available."""
    if HAS_C_EXTENSION:
        try:
            c_arr = c_ones(shape)
            return HybridArray([], _c_array=c_arr)
        except Exception:
            pass
    
    # Fall back to Python implementation
    from ..creation.basic import ones as py_ones
    result = py_ones(shape)
    return HybridArray(result._data)


# Export the appropriate Array class based on configuration
if os.environ.get('ARRPY_FORCE_PYTHON', '0') == '1':
    # Force pure Python implementation
    Array = PythonArray
    print("ArrPy: Using pure Python implementation (ARRPY_FORCE_PYTHON=1)")
else:
    # Use hybrid implementation by default
    Array = HybridArray
    if HAS_C_EXTENSION:
        print("ArrPy: C extensions loaded successfully! Performance mode enabled.")
    else:
        print("ArrPy: Using pure Python implementation (C extensions not available)")