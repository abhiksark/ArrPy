"""
C backend array operations using buffer protocol for zero-copy operations.
This new implementation uses array.array's buffer_info() for direct pointer access.
"""

import array
import ctypes
from ctypes import POINTER, c_double, c_float, c_int32, c_int64, c_size_t

def _add_c(data1, data2, shape1, shape2):
    """C++ backend addition with zero-copy via buffer protocol."""
    try:
        # Try optimized path first
        if isinstance(data1, array.array) and isinstance(data2, array.array):
            # Get buffer info for direct pointer access
            ptr1, size1 = data1.buffer_info()
            ptr2, size2 = data2.buffer_info()
            
            # Ensure same size
            if size1 != size2:
                raise ValueError(f"Array sizes don't match: {size1} vs {size2}")
            
            # Try to use optimized C++ implementation
            try:
                from . import array_ops_buffer_cpp
                
                # Create result array
                result = array.array(data1.typecode, [0.0] * size1)
                ptr_result, _ = result.buffer_info()
                
                # Call optimized C++ function with direct pointers
                array_ops_buffer_cpp.add_buffer(ptr1, ptr2, ptr_result, size1)
                
                return result, shape1
                
            except ImportError:
                # C++ extension not compiled
                raise NotImplementedError(
                    "C++ backend not compiled. Run: make build-cpp\n"
                    "Available in: python, cython\n"
                    "Switch backends with: arrpy.set_backend('cython')"
                )
        else:
            # Fall back to original list-based implementation
            from . import array_ops
            return array_ops._add_c_original(data1, data2, shape1, shape2)
            
    except Exception as e:
        # Ultimate fallback to Python backend
        raise NotImplementedError(
            f"C++ backend encountered error: {e}\n"
            "Available in: python, cython\n"
            "Switch backends with: arrpy.set_backend('cython')"
        )


def _multiply_c(data1, data2, shape1, shape2):
    """C++ backend multiplication with zero-copy via buffer protocol."""
    try:
        if isinstance(data1, array.array):
            ptr1, size1 = data1.buffer_info()
            
            # Check if scalar multiplication
            if not isinstance(data2, (list, array.array)):
                scalar = float(data2)
                
                try:
                    from . import array_ops_buffer_cpp
                    
                    result = array.array(data1.typecode, [0.0] * size1)
                    ptr_result, _ = result.buffer_info()
                    
                    array_ops_buffer_cpp.multiply_scalar_buffer(ptr1, scalar, ptr_result, size1)
                    
                    return result, shape1
                    
                except ImportError:
                    # Fallback
                    result = array.array(data1.typecode)
                    for i in range(size1):
                        result.append(data1[i] * scalar)
                    return result, shape1
                    
            elif isinstance(data2, array.array):
                ptr2, size2 = data2.buffer_info()
                
                if size1 != size2:
                    raise ValueError(f"Array sizes don't match: {size1} vs {size2}")
                
                try:
                    from . import array_ops_buffer_cpp
                    
                    result = array.array(data1.typecode, [0.0] * size1)
                    ptr_result, _ = result.buffer_info()
                    
                    array_ops_buffer_cpp.multiply_buffer(ptr1, ptr2, ptr_result, size1)
                    
                    return result, shape1
                    
                except ImportError:
                    # C++ extension not compiled
                    raise NotImplementedError(
                        "C++ backend not compiled. Run: make build-cpp\n"
                        "Available in: python, cython\n"
                        "Switch backends with: arrpy.set_backend('cython')"
                    )
        
        # Fallback
        raise NotImplementedError(
            "C++ backend encountered error\n"
            "Available in: python, cython\n"
            "Switch backends with: arrpy.set_backend('cython')"
        )
        
    except Exception as e:
        raise NotImplementedError(
            f"C++ backend encountered error: {e}\n"
            "Available in: python, cython\n"
            "Switch backends with: arrpy.set_backend('cython')"
        )


def _subtract_c(data1, data2, shape1, shape2):
    """C++ backend subtraction with zero-copy via buffer protocol."""
    try:
        if isinstance(data1, array.array) and isinstance(data2, array.array):
            ptr1, size1 = data1.buffer_info()
            ptr2, size2 = data2.buffer_info()
            
            if size1 != size2:
                raise ValueError(f"Array sizes don't match: {size1} vs {size2}")
            
            try:
                from . import array_ops_buffer_cpp
                
                result = array.array(data1.typecode, [0.0] * size1)
                ptr_result, _ = result.buffer_info()
                
                array_ops_buffer_cpp.subtract_buffer(ptr1, ptr2, ptr_result, size1)
                
                return result, shape1
                
            except ImportError:
                # C++ extension not compiled
                raise NotImplementedError(
                    "C++ backend not compiled. Run: make build-cpp\n"
                    "Available in: python\n"
                    "Switch backends with: arrpy.set_backend('python')"
                )
        
        raise NotImplementedError(
            "C++ backend not compiled. Run: make build-cpp\n"
            "Available in: python\n"
            "Switch backends with: arrpy.set_backend('python')"
        )
        
    except Exception:
        raise NotImplementedError(
            "C++ backend not compiled. Run: make build-cpp\n"
            "Available in: python\n"
            "Switch backends with: arrpy.set_backend('python')"
        )


def _divide_c(data1, data2, shape1, shape2):
    """C++ backend division with zero-copy via buffer protocol."""
    try:
        if isinstance(data1, array.array) and isinstance(data2, array.array):
            ptr1, size1 = data1.buffer_info()
            ptr2, size2 = data2.buffer_info()
            
            if size1 != size2:
                raise ValueError(f"Array sizes don't match: {size1} vs {size2}")
            
            try:
                from . import array_ops_buffer_cpp
                
                result = array.array(data1.typecode, [0.0] * size1)
                ptr_result, _ = result.buffer_info()
                
                array_ops_buffer_cpp.divide_buffer(ptr1, ptr2, ptr_result, size1)
                
                return result, shape1
                
            except ImportError:
                # C++ extension not compiled
                raise NotImplementedError(
                    "C++ backend not compiled. Run: make build-cpp\n"
                    "Available in: python\n"
                    "Switch backends with: arrpy.set_backend('python')"
                )
        
        raise NotImplementedError(
            "C++ backend not compiled. Run: make build-cpp\n"
            "Available in: python\n"
            "Switch backends with: arrpy.set_backend('python')"
        )
        
    except Exception:
        raise NotImplementedError(
            "C++ backend not compiled. Run: make build-cpp\n"
            "Available in: python\n"
            "Switch backends with: arrpy.set_backend('python')"
        )