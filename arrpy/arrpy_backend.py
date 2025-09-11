"""
Main ArrPy array class with backend system support.

This is the new version that delegates operations to the selected backend.
Now uses array.array for efficient storage and zero-copy C++ operations.
"""

import array
from .dtype import infer_dtype, float64
from .backend_selector import get_backend, Backend


class ArrPy:
    """
    N-dimensional array class with pluggable backend system.
    
    Supports switching between Pure Python, Cython, and C backends at runtime.
    """
    
    def __init__(self, data, dtype=None):
        """
        Initialize an ArrPy array.
        
        Parameters
        ----------
        data : array-like
            Input data (list, tuple, or nested sequences)
        dtype : dtype, optional
            Desired data type for the array
        """
        # Get shape from nested structure
        self._shape = self._get_shape(data)
        
        # Flatten data for storage (row-major/C-order)
        self._data = self._flatten_data(data)
        
        # Set or infer dtype
        if dtype is None:
            self._dtype = infer_dtype(self._data)
        else:
            self._dtype = dtype
            # Convert data to specified dtype
            self._data = self._convert_dtype(self._data, dtype)
        
        # Calculate strides (in elements, not bytes for simplicity)
        self._strides = self._calculate_strides(self._shape)
        
        # Calculate total size
        self._size = self._calculate_size(self._shape)
    
    def _get_shape(self, data):
        """Determine the shape of nested data."""
        if not isinstance(data, (list, tuple)):
            return ()  # Scalar
        
        shape = []
        current = data
        while isinstance(current, (list, tuple)):
            shape.append(len(current))
            if len(current) == 0:
                break
            current = current[0]
        
        return tuple(shape)
    
    def _flatten_data(self, data):
        """Flatten nested data into a 1D array.array for efficient storage."""
        if not isinstance(data, (list, tuple)):
            # Scalar - return as array.array
            return array.array('d', [float(data)])
        
        flat = []
        
        def flatten_recursive(item):
            if isinstance(item, (list, tuple)):
                for subitem in item:
                    flatten_recursive(subitem)
            else:
                flat.append(float(item))
        
        flatten_recursive(data)
        # Return as array.array instead of list
        return array.array('d', flat)
    
    def _convert_dtype(self, data, dtype):
        """Convert data to specified dtype."""
        # Convert array.array to appropriate type
        if dtype.name == 'float64':
            return array.array('d', [float(x) for x in data])
        elif dtype.name == 'float32':
            return array.array('f', [float(x) for x in data])
        elif dtype.name == 'int32':
            return array.array('i', [int(x) for x in data])
        else:
            # Default to double
            return array.array('d', [dtype.python_type(x) for x in data])
    
    def _calculate_strides(self, shape):
        """Calculate strides for given shape."""
        if len(shape) == 0:
            return ()
        
        strides = []
        stride = 1
        for dim in reversed(shape[1:]):
            strides.append(stride)
            stride *= dim
        strides.append(stride)
        
        return tuple(reversed(strides))
    
    def _calculate_size(self, shape):
        """Calculate total number of elements."""
        if len(shape) == 0:
            return 1
        
        size = 1
        for dim in shape:
            size *= dim
        return size
    
    def _create_from_data(self, data, shape):
        """Create a new ArrPy array from raw data and shape."""
        result = ArrPy.__new__(ArrPy)
        # Ensure data is array.array
        if isinstance(data, array.array):
            result._data = data
        elif isinstance(data, list):
            result._data = array.array('d', data)
        else:
            result._data = data  # Already processed
        result._shape = shape
        result._size = self._calculate_size(shape)
        result._dtype = self._dtype
        result._strides = self._calculate_strides(shape)
        return result
    
    @property
    def shape(self):
        """Get the shape of the array."""
        return self._shape
    
    @property
    def size(self):
        """Get the total number of elements."""
        return self._size
    
    @property
    def ndim(self):
        """Get the number of dimensions."""
        return len(self._shape)
    
    @property
    def dtype(self):
        """Get the data type."""
        return self._dtype
    
    @property
    def strides(self):
        """Get the strides of the array."""
        return self._strides
    
    def get_buffer_info(self):
        """Get buffer info for C/C++ interop (pointer and size)."""
        if isinstance(self._data, array.array):
            return self._data.buffer_info()
        else:
            # Fallback for compatibility
            return (id(self._data), len(self._data))
    
    def to_memoryview(self):
        """Get memoryview for zero-copy operations with Cython."""
        if isinstance(self._data, array.array):
            return memoryview(self._data)
        else:
            # Convert to array first
            temp_array = array.array('d', self._data)
            return memoryview(temp_array)
    
    def tolist(self):
        """Convert to Python list for backward compatibility."""
        if isinstance(self._data, array.array):
            return self._data.tolist()
        else:
            return list(self._data)
    
    def __repr__(self):
        """String representation of the array."""
        return f"ArrPy(shape={self.shape}, dtype={self.dtype})"
    
    def __str__(self):
        """Pretty string representation."""
        if self.size == 0:
            return "ArrPy([])"
        
        if self.ndim == 0:
            return str(self._data[0])
        
        if self.ndim == 1:
            return self._format_1d()
        
        if self.ndim == 2:
            return self._format_2d()
        
        # For higher dimensions, use compact representation
        return f"ArrPy(shape={self.shape}, dtype={self.dtype})"
    
    def _format_1d(self):
        """Format 1D array for display."""
        if self.size > 10:
            # Show first 3 and last 3 elements
            elements = [str(self._data[i]) for i in range(3)]
            elements.append("...")
            elements.extend([str(self._data[i]) for i in range(-3, 0)])
            return "[" + " ".join(elements) + "]"
        else:
            return "[" + " ".join(str(x) for x in self._data) + "]"
    
    def _format_2d(self):
        """Format 2D array for display."""
        rows, cols = self.shape
        lines = []
        
        for i in range(min(rows, 6)):  # Show max 6 rows
            if i == 3 and rows > 6:
                lines.append(" ...")
                continue
            
            row_start = i * cols
            row_data = self._data[row_start:row_start + cols]
            
            if cols > 6:
                # Show first 3 and last 3 columns
                row_str = " ".join(str(x) for x in row_data[:3])
                row_str += " ... "
                row_str += " ".join(str(x) for x in row_data[-3:])
            else:
                row_str = " ".join(str(x) for x in row_data)
            
            if i == 0:
                lines.append("[" + "[" + row_str + "]")
            elif i == rows - 1 or (i == 5 and rows > 6):
                lines.append(" [" + row_str + "]" + "]")
            else:
                lines.append(" [" + row_str + "]")
        
        return "\n".join(lines)
    
    # ============================================================
    # Arithmetic operators using backend system
    # ============================================================
    
    def __add__(self, other):
        """Element-wise addition using backend."""
        backend = get_backend()
        
        # Convert scalar to array if needed
        if not isinstance(other, ArrPy):
            other = ArrPy([other] * self.size)
            other._shape = self._shape
        
        if backend == Backend.PYTHON:
            from .backends.python.array_ops import _add_python
            result_data, result_shape = _add_python(
                self._data, other._data, self._shape, other._shape
            )
        elif backend == Backend.CYTHON:
            from .backends.cython import _add_cython
            result_data, result_shape = _add_cython(
                self._data, other._data, self._shape, other._shape
            )
        elif backend == Backend.C:
            from .backends.c.array_ops import _add_c
            result_data, result_shape = _add_c(
                self._data, other._data, self._shape, other._shape
            )
        
        return self._create_from_data(result_data, result_shape)
    
    def __radd__(self, other):
        """Right addition."""
        return self.__add__(other)
    
    def __sub__(self, other):
        """Element-wise subtraction using backend."""
        backend = get_backend()
        
        if not isinstance(other, ArrPy):
            other = ArrPy([other] * self.size)
            other._shape = self._shape
        
        if backend == Backend.PYTHON:
            from .backends.python.array_ops import _subtract_python
            result_data, result_shape = _subtract_python(
                self._data, other._data, self._shape, other._shape
            )
        elif backend == Backend.CYTHON:
            from .backends.cython import _subtract_cython
            result_data, result_shape = _subtract_cython(
                self._data, other._data, self._shape, other._shape
            )
        elif backend == Backend.C:
            from .backends.c.array_ops import _subtract_c
            result_data, result_shape = _subtract_c(
                self._data, other._data, self._shape, other._shape
            )
        
        return self._create_from_data(result_data, result_shape)
    
    def __rsub__(self, other):
        """Right subtraction."""
        if not isinstance(other, ArrPy):
            other = ArrPy([other] * self.size)
            other._shape = self._shape
        return other.__sub__(self)
    
    def __mul__(self, other):
        """Element-wise multiplication using backend."""
        backend = get_backend()
        
        if not isinstance(other, ArrPy):
            other = ArrPy([other] * self.size)
            other._shape = self._shape
        
        if backend == Backend.PYTHON:
            from .backends.python.array_ops import _multiply_python
            result_data, result_shape = _multiply_python(
                self._data, other._data, self._shape, other._shape
            )
        elif backend == Backend.CYTHON:
            from .backends.cython import _multiply_cython
            result_data, result_shape = _multiply_cython(
                self._data, other._data, self._shape, other._shape
            )
        elif backend == Backend.C:
            from .backends.c.array_ops import _multiply_c
            result_data, result_shape = _multiply_c(
                self._data, other._data, self._shape, other._shape
            )
        
        return self._create_from_data(result_data, result_shape)
    
    def __rmul__(self, other):
        """Right multiplication."""
        return self.__mul__(other)
    
    def __truediv__(self, other):
        """Element-wise division using backend."""
        backend = get_backend()
        
        if not isinstance(other, ArrPy):
            other = ArrPy([other] * self.size)
            other._shape = self._shape
        
        if backend == Backend.PYTHON:
            from .backends.python.array_ops import _divide_python
            result_data, result_shape = _divide_python(
                self._data, other._data, self._shape, other._shape
            )
        elif backend == Backend.CYTHON:
            from .backends.cython import _divide_cython
            result_data, result_shape = _divide_cython(
                self._data, other._data, self._shape, other._shape
            )
        elif backend == Backend.C:
            from .backends.c.array_ops import _divide_c
            result_data, result_shape = _divide_c(
                self._data, other._data, self._shape, other._shape
            )
        
        return self._create_from_data(result_data, result_shape)
    
    def __rtruediv__(self, other):
        """Right division."""
        if not isinstance(other, ArrPy):
            other = ArrPy([other] * self.size)
            other._shape = self._shape
        return other.__truediv__(self)
    
    def __neg__(self):
        """Unary negation using backend."""
        backend = get_backend()
        
        if backend == Backend.PYTHON:
            from .backends.python.array_ops import _negative_python
            result_data, result_shape = _negative_python(self._data, self._shape)
        elif backend == Backend.CYTHON:
            # Not implemented in Cython yet
            from .backends.python.array_ops import _negative_python
            result_data, result_shape = _negative_python(self._data, self._shape)
        elif backend == Backend.C:
            # Not implemented in C yet
            from .backends.python.array_ops import _negative_python
            result_data, result_shape = _negative_python(self._data, self._shape)
        
        return self._create_from_data(result_data, result_shape)
    
    def __abs__(self):
        """Absolute value using backend."""
        backend = get_backend()
        
        if backend == Backend.PYTHON:
            from .backends.python.array_ops import _absolute_python
            result_data, result_shape = _absolute_python(self._data, self._shape)
        elif backend == Backend.CYTHON:
            # Not implemented in Cython yet
            from .backends.python.array_ops import _absolute_python
            result_data, result_shape = _absolute_python(self._data, self._shape)
        elif backend == Backend.C:
            # Not implemented in C yet
            from .backends.python.array_ops import _absolute_python
            result_data, result_shape = _absolute_python(self._data, self._shape)
        
        return self._create_from_data(result_data, result_shape)
    
    def __matmul__(self, other):
        """Matrix multiplication using @ operator."""
        from . import matmul
        return matmul(self, other)
    
    def __rmatmul__(self, other):
        """Right matrix multiplication using @ operator."""
        from . import matmul
        return matmul(other, self)
    
    # ============================================================
    # Comparison operators
    # ============================================================
    
    def __eq__(self, other):
        """Element-wise equality comparison."""
        if not isinstance(other, ArrPy):
            other = ArrPy([other])
            from .broadcasting import broadcast_arrays
            self_b, other_b = broadcast_arrays(self, other)
        else:
            from .broadcasting import broadcast_arrays
            self_b, other_b = broadcast_arrays(self, other)
        
        result_data = [self_b._data[i] == other_b._data[i] for i in range(self_b._size)]
        
        result = self._create_from_data(result_data, self_b._shape)
        from .dtype import bool_
        result._dtype = bool_
        return result
    
    def __ne__(self, other):
        """Element-wise inequality comparison."""
        if not isinstance(other, ArrPy):
            other = ArrPy([other])
            from .broadcasting import broadcast_arrays
            self_b, other_b = broadcast_arrays(self, other)
        else:
            from .broadcasting import broadcast_arrays
            self_b, other_b = broadcast_arrays(self, other)
        
        result_data = [self_b._data[i] != other_b._data[i] for i in range(self_b._size)]
        
        result = self._create_from_data(result_data, self_b._shape)
        from .dtype import bool_
        result._dtype = bool_
        return result
    
    def __lt__(self, other):
        """Element-wise less than comparison."""
        if not isinstance(other, ArrPy):
            other = ArrPy([other])
            from .broadcasting import broadcast_arrays
            self_b, other_b = broadcast_arrays(self, other)
        else:
            from .broadcasting import broadcast_arrays
            self_b, other_b = broadcast_arrays(self, other)
        
        result_data = [self_b._data[i] < other_b._data[i] for i in range(self_b._size)]
        
        result = self._create_from_data(result_data, self_b._shape)
        from .dtype import bool_
        result._dtype = bool_
        return result
    
    def __le__(self, other):
        """Element-wise less than or equal comparison."""
        if not isinstance(other, ArrPy):
            other = ArrPy([other])
            from .broadcasting import broadcast_arrays
            self_b, other_b = broadcast_arrays(self, other)
        else:
            from .broadcasting import broadcast_arrays
            self_b, other_b = broadcast_arrays(self, other)
        
        result_data = [self_b._data[i] <= other_b._data[i] for i in range(self_b._size)]
        
        result = self._create_from_data(result_data, self_b._shape)
        from .dtype import bool_
        result._dtype = bool_
        return result
    
    def __gt__(self, other):
        """Element-wise greater than comparison."""
        if not isinstance(other, ArrPy):
            other = ArrPy([other])
            from .broadcasting import broadcast_arrays
            self_b, other_b = broadcast_arrays(self, other)
        else:
            from .broadcasting import broadcast_arrays
            self_b, other_b = broadcast_arrays(self, other)
        
        result_data = [self_b._data[i] > other_b._data[i] for i in range(self_b._size)]
        
        result = self._create_from_data(result_data, self_b._shape)
        from .dtype import bool_
        result._dtype = bool_
        return result
    
    def __ge__(self, other):
        """Element-wise greater than or equal comparison."""
        if not isinstance(other, ArrPy):
            other = ArrPy([other])
            from .broadcasting import broadcast_arrays
            self_b, other_b = broadcast_arrays(self, other)
        else:
            from .broadcasting import broadcast_arrays
            self_b, other_b = broadcast_arrays(self, other)
        
        result_data = [self_b._data[i] >= other_b._data[i] for i in range(self_b._size)]
        
        result = self._create_from_data(result_data, self_b._shape)
        from .dtype import bool_
        result._dtype = bool_
        return result
    
    # ============================================================
    # Indexing and slicing
    # ============================================================
    
    def __getitem__(self, key):
        """Get item(s) from array using indexing."""
        # Handle single integer index for 1D arrays
        if isinstance(key, int):
            if self.ndim == 1:
                # Handle negative indexing
                if key < 0:
                    key = self._size + key
                if key < 0 or key >= self._size:
                    raise IndexError(f"Index {key} out of bounds for array of size {self._size}")
                return self._data[key]
            else:
                # For multi-dimensional arrays, integer index selects a sub-array
                raise NotImplementedError("Integer indexing for multi-dimensional arrays not yet implemented")
        
        # Handle list/tuple of indices (fancy indexing)
        if isinstance(key, (list, tuple)):
            # Check if this looks like fancy indexing (all elements are integers)
            # vs multi-dimensional indexing (would have slices, etc)
            if all(isinstance(k, int) for k in key):
                # This is fancy indexing - treat as array of indices
                from .indexing import fancy_index
                from .creation import array
                return fancy_index(self, array(key))
            elif self.ndim == 1 and len(key) > 1:
                # Multiple indices for 1D array that aren't all integers
                raise IndexError(f"Too many indices for array: array is 1-dimensional, but {len(key)} were indexed")
            elif self.ndim > 1:
                # Multi-dimensional indexing
                raise NotImplementedError("Multi-dimensional indexing not yet implemented")
        
        # Handle slicing for 1D arrays
        if isinstance(key, slice):
            if self.ndim != 1:
                raise NotImplementedError("Slicing for multi-dimensional arrays not yet implemented")
            
            # Extract sliced data - pass slice directly to handle negative steps correctly
            sliced_data = self._data[key]
            
            # Create new array with sliced data
            from .creation import array
            return array(list(sliced_data))
        
        # Handle boolean array indexing
        if isinstance(key, ArrPy):
            from .dtype import bool_
            if key._dtype == bool_:
                from .indexing import boolean_index
                return boolean_index(self, key)
            else:
                # Fancy indexing with integer array
                from .indexing import fancy_index
                return fancy_index(self, key)
        
        
        raise TypeError(f"Invalid index type: {type(key)}")
    
    def __setitem__(self, key, value):
        """Set item(s) in array using indexing."""
        # Handle single integer index for 1D arrays
        if isinstance(key, int):
            if self.ndim == 1:
                # Handle negative indexing
                if key < 0:
                    key = self._size + key
                if key < 0 or key >= self._size:
                    raise IndexError(f"Index {key} out of bounds for array of size {self._size}")
                self._data[key] = value
                return
            else:
                raise NotImplementedError("Integer indexing for multi-dimensional arrays not yet implemented")
        
        # Handle tuple of indices for multi-dimensional arrays
        if isinstance(key, tuple):
            if self.ndim == 1:
                raise IndexError("Too many indices for 1D array")
            
            # Convert multi-dimensional index to flat index
            if len(key) != self.ndim:
                raise IndexError(f"Expected {self.ndim} indices, got {len(key)}")
            
            # Calculate flat index from multi-dimensional indices
            flat_idx = 0
            for i, (idx, dim_size) in enumerate(zip(key, self._shape)):
                if isinstance(idx, int):
                    # Handle negative indexing
                    if idx < 0:
                        idx = dim_size + idx
                    if idx < 0 or idx >= dim_size:
                        raise IndexError(f"Index {idx} out of bounds for axis {i} with size {dim_size}")
                    
                    # Calculate offset for this dimension
                    stride = 1
                    for j in range(i + 1, self.ndim):
                        stride *= self._shape[j]
                    flat_idx += idx * stride
                else:
                    raise NotImplementedError("Only integer indexing currently supported")
            
            self._data[flat_idx] = value
            return
        
        # Handle slicing for 1D arrays
        if isinstance(key, slice):
            if self.ndim != 1:
                raise NotImplementedError("Slicing for multi-dimensional arrays not yet implemented")
            
            # Get slice indices
            start, stop, step = key.indices(self._size)
            
            # Convert value to list if it's an array
            if isinstance(value, ArrPy):
                value = list(value._data)
            elif not isinstance(value, (list, tuple)):
                # Broadcast single value
                value = [value] * len(range(start, stop, step))
            
            # Set sliced data
            for i, idx in enumerate(range(start, stop, step)):
                self._data[idx] = value[i] if i < len(value) else value[-1]
            return
        
        # Handle boolean array indexing
        if isinstance(key, ArrPy):
            from .dtype import bool_
            if key._dtype == bool_:
                # Boolean indexing - set values where mask is True
                if key._size != self._size:
                    raise ValueError("Boolean index size must match array size")
                
                # Convert value to list if needed
                if isinstance(value, ArrPy):
                    value_list = list(value._data)
                elif not isinstance(value, (list, tuple)):
                    value_list = [value]
                else:
                    value_list = value
                
                # Set values where mask is True
                value_idx = 0
                for i in range(self._size):
                    if key._data[i]:
                        self._data[i] = value_list[value_idx % len(value_list)]
                        value_idx += 1
                return
        
        raise TypeError(f"Invalid index type for setitem: {type(key)}")
    
    # ============================================================
    # Reduction methods using backend system
    # ============================================================
    
    def sum(self, axis=None, keepdims=False):
        """Sum using backend."""
        backend = get_backend()
        
        if backend == Backend.PYTHON:
            from .backends.python.reduction_ops import _sum_python
            result_data, result_shape = _sum_python(
                self._data, self._shape, axis, keepdims
            )
        elif backend == Backend.CYTHON:
            from .backends.cython.reduction_ops import _sum_cython
            result_data, result_shape = _sum_cython(
                self._data, self._shape, axis, keepdims
            )
        elif backend == Backend.C:
            from .backends.c.reduction_ops import _sum_c
            result_data, result_shape = _sum_c(
                self._data, self._shape, axis, keepdims
            )
        
        if result_shape == ():
            # Scalar result
            return result_data[0]
        return self._create_from_data(result_data, result_shape)
    
    def mean(self, axis=None, keepdims=False):
        """Mean using backend."""
        backend = get_backend()
        
        if backend == Backend.PYTHON:
            from .backends.python.reduction_ops import _mean_python
            result_data, result_shape = _mean_python(
                self._data, self._shape, axis, keepdims
            )
        elif backend == Backend.CYTHON:
            from .backends.cython.reduction_ops import _mean_cython
            result_data, result_shape = _mean_cython(
                self._data, self._shape, axis, keepdims
            )
        elif backend == Backend.C:
            from .backends.c.reduction_ops import _mean_c
            result_data, result_shape = _mean_c(
                self._data, self._shape, axis, keepdims
            )
        
        if result_shape == ():
            # Scalar result
            return result_data[0]
        return self._create_from_data(result_data, result_shape)
    
    def min(self, axis=None, keepdims=False):
        """Minimum using backend."""
        backend = get_backend()
        
        if backend == Backend.PYTHON:
            from .backends.python.reduction_ops import _min_python
            result_data, result_shape = _min_python(
                self._data, self._shape, axis, keepdims
            )
        else:
            # Not implemented in other backends yet
            from .backends.python.reduction_ops import _min_python
            result_data, result_shape = _min_python(
                self._data, self._shape, axis, keepdims
            )
        
        if result_shape == ():
            # Scalar result
            return result_data[0]
        return self._create_from_data(result_data, result_shape)
    
    def max(self, axis=None, keepdims=False):
        """Maximum using backend."""
        backend = get_backend()
        
        if backend == Backend.PYTHON:
            from .backends.python.reduction_ops import _max_python
            result_data, result_shape = _max_python(
                self._data, self._shape, axis, keepdims
            )
        else:
            # Not implemented in other backends yet
            from .backends.python.reduction_ops import _max_python
            result_data, result_shape = _max_python(
                self._data, self._shape, axis, keepdims
            )
        
        if result_shape == ():
            # Scalar result
            return result_data[0]
        return self._create_from_data(result_data, result_shape)
    
    def argmin(self, axis=None):
        """Return indices of minimum values along an axis."""
        if axis is not None:
            raise NotImplementedError("axis parameter not yet supported for argmin")
        
        # For 1D or flattened array, find index of minimum
        min_val = float('inf')
        min_idx = 0
        for i, val in enumerate(self._data):
            if val < min_val:
                min_val = val
                min_idx = i
        return min_idx
    
    def argmax(self, axis=None):
        """Return indices of maximum values along an axis."""
        if axis is not None:
            raise NotImplementedError("axis parameter not yet supported for argmax")
        
        # For 1D or flattened array, find index of maximum
        max_val = float('-inf')
        max_idx = 0
        for i, val in enumerate(self._data):
            if val > max_val:
                max_val = val
                max_idx = i
        return max_idx
    
    # ============================================================
    # Shape manipulation (doesn't need backend)
    # ============================================================
    
    def reshape(self, *shape):
        """Return array with new shape."""
        # Handle different input formats
        if len(shape) == 1 and isinstance(shape[0], (tuple, list)):
            new_shape = tuple(shape[0])
        else:
            new_shape = shape
        
        # Convert -1 to inferred dimension
        if -1 in new_shape:
            # Calculate size for -1 dimension
            known_size = 1
            minus_one_count = 0
            for dim in new_shape:
                if dim == -1:
                    minus_one_count += 1
                else:
                    known_size *= dim
            
            if minus_one_count > 1:
                raise ValueError("Can only specify one unknown dimension")
            
            if self.size % known_size != 0:
                raise ValueError(f"Cannot reshape array of size {self.size} into shape {new_shape}")
            
            inferred_dim = self.size // known_size
            new_shape = tuple(inferred_dim if dim == -1 else dim for dim in new_shape)
        
        # Check size compatibility
        new_size = 1
        for dim in new_shape:
            new_size *= dim
        
        if new_size != self.size:
            raise ValueError(f"Cannot reshape array of size {self.size} into shape {new_shape}")
        
        # Create reshaped array
        result = ArrPy.__new__(ArrPy)
        # Properly copy array.array
        import array
        if isinstance(self._data, array.array):
            result._data = array.array(self._data.typecode, self._data)
        else:
            result._data = list(self._data)
        result._shape = new_shape
        result._size = self._size
        result._dtype = self._dtype
        result._strides = result._calculate_strides(new_shape)
        
        return result
    
    def flatten(self):
        """Return a flattened copy of the array."""
        return self.reshape(-1)
    
    @property
    def T(self):
        """Transpose of the array."""
        return self.transpose()
    
    def transpose(self, *axes):
        """Return array with axes transposed."""
        # Handle no arguments - reverse all axes
        if len(axes) == 0:
            axes = tuple(reversed(range(self.ndim)))
        elif len(axes) == 1 and axes[0] is None:
            axes = tuple(reversed(range(self.ndim)))
        elif len(axes) == 1 and isinstance(axes[0], (tuple, list)):
            axes = tuple(axes[0])
        
        # For 2D, simple transpose
        if self.ndim == 2 and axes == (1, 0):
            rows, cols = self._shape
            new_data = []
            for j in range(cols):
                for i in range(rows):
                    new_data.append(self._data[i * cols + j])
            
            result = ArrPy.__new__(ArrPy)
            result._data = new_data
            result._shape = (cols, rows)
            result._size = self._size
            result._dtype = self._dtype
            result._strides = result._calculate_strides(result._shape)
            return result
        
        # For other cases, not fully implemented
        raise NotImplementedError(f"Transpose with axes {axes} not fully implemented")