"""
Data type dispatching system for ArrPy.
Routes operations to type-specific implementations for optimal performance.
"""

from enum import Enum
from typing import Callable, Dict, Any, Optional, Tuple
import numpy as np


class DTypeCode(Enum):
    """Data type codes for type dispatching in ArrPy."""
    INT32 = 'int32'
    INT64 = 'int64'
    FLOAT32 = 'float32'
    FLOAT64 = 'float64'
    BOOL = 'bool'
    OBJECT = 'object'
    
    @classmethod
    def from_data(cls, data):
        """Infer dtype from data."""
        if not data:
            return cls.FLOAT64
        
        # Check first element
        first = data[0]
        
        if isinstance(first, bool):
            return cls.BOOL
        elif isinstance(first, int):
            # Check if all values fit in int32
            max_val = max(data)
            min_val = min(data)
            if -2147483648 <= min_val and max_val <= 2147483647:
                return cls.INT32
            else:
                return cls.INT64
        elif isinstance(first, float):
            return cls.FLOAT64
        else:
            return cls.OBJECT
    
    @classmethod
    def from_numpy_dtype(cls, np_dtype):
        """Convert numpy dtype to ArrPy DTypeCode."""
        dtype_map = {
            np.int32: cls.INT32,
            np.int64: cls.INT64,
            np.float32: cls.FLOAT32,
            np.float64: cls.FLOAT64,
            np.bool_: cls.BOOL,
        }
        return dtype_map.get(np_dtype, cls.OBJECT)


class DTypeDispatcher:
    """
    Dispatches operations to type-specific implementations.
    """
    
    def __init__(self):
        self._registry: Dict[Tuple[str, DTypeCode], Callable] = {}
        self._fallbacks: Dict[str, Callable] = {}
    
    def register(self, operation: str, dtype: DTypeCode, implementation: Callable):
        """Register a type-specific implementation."""
        self._registry[(operation, dtype)] = implementation
    
    def register_fallback(self, operation: str, implementation: Callable):
        """Register a fallback implementation for an operation."""
        self._fallbacks[operation] = implementation
    
    def dispatch(self, operation: str, dtype: DTypeCode, *args, **kwargs):
        """
        Dispatch to the appropriate implementation.
        Falls back to generic implementation if type-specific not available.
        """
        # Try type-specific implementation
        key = (operation, dtype)
        if key in self._registry:
            return self._registry[key](*args, **kwargs)
        
        # Try fallback
        if operation in self._fallbacks:
            return self._fallbacks[operation](*args, **kwargs)
        
        # No implementation found
        raise NotImplementedError(
            f"Operation '{operation}' not implemented for dtype {dtype.value}"
        )
    
    def has_implementation(self, operation: str, dtype: Optional[DType] = None) -> bool:
        """Check if an implementation exists."""
        if dtype:
            return (operation, dtype) in self._registry
        return operation in self._fallbacks
    
    def get_supported_dtypes(self, operation: str) -> list:
        """Get list of dtypes that have specific implementations."""
        return [dtype for op, dtype in self._registry.keys() if op == operation]


# Global dispatcher instance
_dispatcher = DTypeDispatcher()


def get_dispatcher() -> DTypeDispatcher:
    """Get the global dtype dispatcher."""
    return _dispatcher


def register_typed_operation(operation: str, dtype: DTypeCode):
    """Decorator to register a type-specific operation."""
    def decorator(func):
        _dispatcher.register(operation, dtype, func)
        return func
    return decorator


def register_fallback_operation(operation: str):
    """Decorator to register a fallback operation."""
    def decorator(func):
        _dispatcher.register_fallback(operation, func)
        return func
    return decorator


# Register Cython implementations if available
def register_cython_operations():
    """Register all available Cython type-specific operations."""
    try:
        from .backends.cython import typed_ops
        
        # Register float64 operations
        _dispatcher.register('add', DTypeCodeCode.FLOAT64, typed_ops._add_float64)
        _dispatcher.register('multiply', DTypeCodeCode.FLOAT64, typed_ops._multiply_float64)
        _dispatcher.register('subtract', DTypeCodeCode.FLOAT64, typed_ops._subtract_float64)
        _dispatcher.register('divide', DTypeCodeCode.FLOAT64, typed_ops._divide_float64)
        
        # Register float32 operations
        _dispatcher.register('add', DTypeCodeCode.FLOAT32, typed_ops._add_float32)
        
        # Register int64 operations
        _dispatcher.register('add', DTypeCodeCode.INT64, typed_ops._add_int64)
        
        # Register int32 operations
        _dispatcher.register('add', DTypeCodeCode.INT32, typed_ops._add_int32)
        
        # Register vectorized operations
        _dispatcher.register('add_vectorized', DTypeCodeCode.FLOAT64, typed_ops._add_float64_vectorized)
        
        return True
    except ImportError:
        return False


# Utility functions for dtype conversion
def cast_to_dtype(data, dtype: DTypeCode):
    """Cast data to specified dtype."""
    if dtype == DTypeCode.INT32:
        return [np.int32(x) for x in data]
    elif dtype == DTypeCode.INT64:
        return [np.int64(x) for x in data]
    elif dtype == DTypeCode.FLOAT32:
        return [np.float32(x) for x in data]
    elif dtype == DTypeCode.FLOAT64:
        return [np.float64(x) for x in data]
    elif dtype == DTypeCode.BOOL:
        return [bool(x) for x in data]
    else:
        return list(data)


def get_dtype_info(dtype: DTypeCode) -> dict:
    """Get information about a dtype."""
    info = {
        DTypeCode.INT32: {
            'bits': 32,
            'min': -2147483648,
            'max': 2147483647,
            'numpy_type': np.int32,
            'c_type': 'int'
        },
        DTypeCode.INT64: {
            'bits': 64,
            'min': -9223372036854775808,
            'max': 9223372036854775807,
            'numpy_type': np.int64,
            'c_type': 'long'
        },
        DTypeCode.FLOAT32: {
            'bits': 32,
            'min': np.finfo(np.float32).min,
            'max': np.finfo(np.float32).max,
            'numpy_type': np.float32,
            'c_type': 'float'
        },
        DTypeCode.FLOAT64: {
            'bits': 64,
            'min': np.finfo(np.float64).min,
            'max': np.finfo(np.float64).max,
            'numpy_type': np.float64,
            'c_type': 'double'
        },
        DTypeCode.BOOL: {
            'bits': 8,
            'min': False,
            'max': True,
            'numpy_type': np.bool_,
            'c_type': 'bool'
        },
        DTypeCode.OBJECT: {
            'bits': None,
            'min': None,
            'max': None,
            'numpy_type': object,
            'c_type': 'PyObject*'
        }
    }
    return info.get(dtype, {})