"""
Main arrpy array class - Pure Python implementation of NumPy-like arrays.
"""

from .dtype import infer_dtype, float64


class arrpy:
    """
    N-dimensional array class mimicking NumPy's ndarray.
    
    This is the pure Python implementation (v0.x) focusing on correctness
    over performance.
    """
    
    def __init__(self, data, dtype=None):
        """
        Initialize an arrpy array.
        
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
        """
        Determine the shape of nested data.
        
        Parameters
        ----------
        data : array-like
            Input data
        
        Returns
        -------
        tuple
            Shape of the data
        """
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
        """
        Flatten nested data into a 1D list.
        
        Parameters
        ----------
        data : array-like
            Nested input data
        
        Returns
        -------
        list
            Flattened data in row-major (C) order
        """
        if not isinstance(data, (list, tuple)):
            return [data]  # Scalar
        
        flat = []
        
        def flatten_recursive(item):
            if isinstance(item, (list, tuple)):
                for subitem in item:
                    flatten_recursive(subitem)
            else:
                flat.append(item)
        
        flatten_recursive(data)
        return flat
    
    def _convert_dtype(self, data, dtype):
        """
        Convert data to specified dtype.
        
        Parameters
        ----------
        data : list
            Input data
        dtype : DType
            Target data type
        
        Returns
        -------
        list
            Converted data
        """
        return [dtype.python_type(x) for x in data]
    
    def _calculate_strides(self, shape):
        """
        Calculate strides for given shape.
        
        Strides represent how many elements to skip to move
        along each dimension.
        
        Parameters
        ----------
        shape : tuple
            Array shape
        
        Returns
        -------
        tuple
            Strides for each dimension
        """
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
        """
        Calculate total number of elements.
        
        Parameters
        ----------
        shape : tuple
            Array shape
        
        Returns
        -------
        int
            Total number of elements
        """
        if len(shape) == 0:
            return 1
        
        size = 1
        for dim in shape:
            size *= dim
        return size
    
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
    
    def __repr__(self):
        """String representation of the array."""
        return f"arrpy(shape={self.shape}, dtype={self.dtype})"
    
    def __str__(self):
        """Pretty string representation."""
        if self.size == 0:
            return "arrpy([])"
        
        if self.ndim == 0:
            return str(self._data[0])
        
        if self.ndim == 1:
            return self._format_1d()
        
        if self.ndim == 2:
            return self._format_2d()
        
        # For higher dimensions, use compact representation
        return f"arrpy(shape={self.shape}, dtype={self.dtype})"
    
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
    
    def _get_flat_index(self, indices):
        """
        Convert multi-dimensional index to flat index.
        
        Parameters
        ----------
        indices : tuple
            Multi-dimensional indices
        
        Returns
        -------
        int
            Flat index into data array
        """
        flat_idx = 0
        for idx, stride in zip(indices, self._strides):
            flat_idx += idx * stride
        return flat_idx
    
    def _normalize_index(self, key):
        """
        Normalize and validate indices.
        
        Parameters
        ----------
        key : int, slice, tuple
            Index or indices
        
        Returns
        -------
        tuple
            Normalized indices
        """
        # Convert single index to tuple
        if not isinstance(key, tuple):
            key = (key,)
        
        # Check number of indices
        if len(key) > self.ndim:
            raise IndexError(f"Too many indices for array with {self.ndim} dimensions")
        
        # Pad with full slices if needed
        if len(key) < self.ndim:
            key = key + (slice(None),) * (self.ndim - len(key))
        
        # Normalize each index
        normalized = []
        for idx, dim_size in zip(key, self._shape):
            if isinstance(idx, int):
                # Handle negative indices
                if idx < 0:
                    idx = dim_size + idx
                # Check bounds
                if idx < 0 or idx >= dim_size:
                    raise IndexError(f"Index {idx} out of bounds for dimension with size {dim_size}")
                normalized.append(idx)
            elif isinstance(idx, slice):
                normalized.append(idx)
            else:
                raise TypeError(f"Invalid index type: {type(idx)}")
        
        return tuple(normalized)
    
    def __getitem__(self, key):
        """
        Get item(s) from array.
        
        Parameters
        ----------
        key : int, slice, tuple
            Index or indices
        
        Returns
        -------
        scalar or arrpy
            Selected element(s)
        """
        # Normalize indices
        indices = self._normalize_index(key)
        
        # Check if all indices are integers (single element access)
        if all(isinstance(idx, int) for idx in indices):
            flat_idx = self._get_flat_index(indices)
            return self._data[flat_idx]
        
        # Handle slicing
        # For now, implement basic slicing for 1D and 2D arrays
        if self.ndim == 1:
            idx = indices[0]
            if isinstance(idx, slice):
                start, stop, step = idx.indices(self._shape[0])
                new_data = self._data[start:stop:step]
                result = arrpy.__new__(arrpy)
                result._data = new_data
                result._shape = (len(new_data),)
                result._dtype = self._dtype
                result._size = len(new_data)
                result._strides = (1,)
                return result
        
        elif self.ndim == 2:
            row_idx, col_idx = indices
            rows, cols = self._shape
            
            # Determine new shape
            if isinstance(row_idx, int):
                # Single row selected
                if isinstance(col_idx, slice):
                    start, stop, step = col_idx.indices(cols)
                    new_data = []
                    row_start = row_idx * cols
                    for j in range(start, stop, step):
                        new_data.append(self._data[row_start + j])
                    
                    result = arrpy.__new__(arrpy)
                    result._data = new_data
                    result._shape = (len(new_data),)
                    result._dtype = self._dtype
                    result._size = len(new_data)
                    result._strides = (1,)
                    return result
            
            elif isinstance(row_idx, slice):
                r_start, r_stop, r_step = row_idx.indices(rows)
                
                if isinstance(col_idx, int):
                    # Single column selected
                    new_data = []
                    for i in range(r_start, r_stop, r_step):
                        new_data.append(self._data[i * cols + col_idx])
                    
                    result = arrpy.__new__(arrpy)
                    result._data = new_data
                    result._shape = (len(new_data),)
                    result._dtype = self._dtype
                    result._size = len(new_data)
                    result._strides = (1,)
                    return result
                    
                elif isinstance(col_idx, slice):
                    # Both are slices
                    c_start, c_stop, c_step = col_idx.indices(cols)
                    new_data = []
                    
                    for i in range(r_start, r_stop, r_step):
                        for j in range(c_start, c_stop, c_step):
                            new_data.append(self._data[i * cols + j])
                    
                    new_rows = len(range(r_start, r_stop, r_step))
                    new_cols = len(range(c_start, c_stop, c_step))
                    
                    result = arrpy.__new__(arrpy)
                    result._data = new_data
                    result._shape = (new_rows, new_cols)
                    result._dtype = self._dtype
                    result._size = new_rows * new_cols
                    result._strides = result._calculate_strides((new_rows, new_cols))
                    return result
        
        # For higher dimensions, raise NotImplementedError for now
        raise NotImplementedError(f"Slicing not yet implemented for {self.ndim}D arrays")
    
    def __setitem__(self, key, value):
        """
        Set item(s) in array.
        
        Parameters
        ----------
        key : int, slice, tuple
            Index or indices
        value : scalar or array-like
            Value(s) to set
        """
        # Normalize indices
        indices = self._normalize_index(key)
        
        # Check if all indices are integers (single element access)
        if all(isinstance(idx, int) for idx in indices):
            flat_idx = self._get_flat_index(indices)
            self._data[flat_idx] = self._dtype.python_type(value)
            return
        
        # Handle slicing for 1D arrays
        if self.ndim == 1:
            idx = indices[0]
            if isinstance(idx, slice):
                start, stop, step = idx.indices(self._shape[0])
                indices_to_set = list(range(start, stop, step))
                
                # Handle scalar value
                if not isinstance(value, (list, tuple)):
                    for i in indices_to_set:
                        self._data[i] = self._dtype.python_type(value)
                else:
                    # Handle array-like value
                    if len(value) != len(indices_to_set):
                        raise ValueError(f"Cannot assign {len(value)} values to {len(indices_to_set)} indices")
                    for i, v in zip(indices_to_set, value):
                        self._data[i] = self._dtype.python_type(v)
                return
        
        # For higher dimensions, raise NotImplementedError for now
        raise NotImplementedError(f"Slice assignment not yet implemented for {self.ndim}D arrays")