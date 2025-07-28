"""
Core Array class implementation for ArrPy.

This module contains the fundamental Array class that provides the foundation
for all array operations in ArrPy, similar to numpy.ndarray.
"""


class Array:
    """
    ArrPy's fundamental array class.
    
    An Array object represents a multi-dimensional array with a fixed data type.
    It provides the foundation for all numerical operations in ArrPy.
    
    Parameters
    ----------
    data : list
        Input data as nested lists. Must have consistent dimensions.
    
    Attributes
    ----------
    shape : tuple
        The dimensions of the array.
    """
    
    def __init__(self, data):
        if not isinstance(data, list):
            raise TypeError("Data must be a list")
        
        if not data:
            self._data = []
            self._shape = (0,)
            return
        
        # Check if it's a nested list and validate shape consistency
        self._shape = self._get_shape(data)
        self._data = self._flatten(data)
        
        # Validate that the data is not ragged
        expected_size = 1
        for dim in self._shape:
            expected_size *= dim
        
        if len(self._data) != expected_size:
            raise ValueError("Input data is ragged (inconsistent dimensions)")
    
    def _get_shape(self, data):
        """Determine the shape of nested list data."""
        shape = []
        current = data
        
        while isinstance(current, list):
            if not current:
                break
            shape.append(len(current))
            current = current[0]
        
        return tuple(shape)
    
    def _flatten(self, data):
        """Flatten nested list data into a 1D list."""
        if not isinstance(data, list):
            return [data]
        
        result = []
        for item in data:
            if isinstance(item, list):
                result.extend(self._flatten(item))
            else:
                result.append(item)
        
        return result
    
    def _validate_shape_consistency(self, data, expected_shape, current_dim=0):
        """Validate that nested list data has consistent shape."""
        if current_dim >= len(expected_shape):
            return not isinstance(data, list)
        
        if not isinstance(data, list) or len(data) != expected_shape[current_dim]:
            return False
        
        for item in data:
            if not self._validate_shape_consistency(item, expected_shape, current_dim + 1):
                return False
        
        return True
    
    @property
    def shape(self):
        """Return the shape of the array."""
        return self._shape
    
    @property
    def size(self):
        """Return the total number of elements in the array."""
        return len(self._data)
    
    @property
    def ndim(self):
        """Return the number of dimensions of the array."""
        return len(self._shape)
    
    def __getitem__(self, key):
        """Get array element(s) by index."""
        if isinstance(key, tuple):
            # Handle partial indexing for multi-dimensional arrays
            if len(key) > len(self._shape):
                raise IndexError("Too many indices for array")
            
            if len(key) == len(self._shape):
                # Full indexing - return single element
                # Convert multi-dimensional index to flat index
                flat_index = 0
                multiplier = 1
                
                for i in range(len(self._shape) - 1, -1, -1):
                    idx = key[i]
                    # Handle negative indexing
                    if idx < 0:
                        idx += self._shape[i]
                    if idx < 0 or idx >= self._shape[i]:
                        raise IndexError("Index out of bounds")
                    flat_index += idx * multiplier
                    multiplier *= self._shape[i]
                
                return self._data[flat_index]
            else:
                # Partial indexing - return sub-array
                # Apply the given indices and return array with remaining dimensions
                current_shape = list(self._shape)
                current_data = self._data
                
                for i, idx in enumerate(key):
                    # Handle negative indexing
                    if idx < 0:
                        idx += current_shape[0]
                    if idx < 0 or idx >= current_shape[0]:
                        raise IndexError("Index out of bounds")
                    
                    # Calculate sub-array size and extract data
                    sub_size = len(current_data) // current_shape[0]
                    start_idx = idx * sub_size
                    end_idx = start_idx + sub_size
                    
                    current_data = current_data[start_idx:end_idx]
                    current_shape = current_shape[1:]
                
                # Create new Array with sub-data that shares reference to original data
                new_array = Array([])
                new_array._data = current_data
                new_array._shape = tuple(current_shape)
                new_array._parent = self  # Keep reference to parent for shared data
                new_array._parent_offset = self._data.index(current_data[0]) if current_data else 0
                
                return new_array
        else:
            # Single index
            if len(self._shape) == 1:
                # Handle negative indexing for 1D
                if key < 0:
                    key += len(self._data)
                if key < 0 or key >= len(self._data):
                    raise IndexError("Index out of bounds")
                return self._data[key]
            else:
                # Return a sub-array
                # Handle negative indexing
                if key < 0:
                    key += self._shape[0]
                if key < 0 or key >= self._shape[0]:
                    raise IndexError("Index out of bounds")
                
                sub_size = len(self._data) // self._shape[0]
                start_idx = key * sub_size
                end_idx = start_idx + sub_size
                
                sub_data = self._data[start_idx:end_idx]
                sub_shape = self._shape[1:]
                
                # Create new Array with sub-data that shares reference to original data
                new_array = Array([])
                new_array._data = sub_data
                new_array._shape = sub_shape
                new_array._parent = self  # Keep reference to parent for shared data
                new_array._parent_offset = start_idx
                
                return new_array
    
    def __setitem__(self, key, value):
        """Set array element(s) by index."""
        if isinstance(key, tuple):
            if len(key) != len(self._shape):
                raise IndexError("Number of indices must match number of dimensions")
            
            # Convert multi-dimensional index to flat index
            flat_index = 0
            multiplier = 1
            
            for i in range(len(self._shape) - 1, -1, -1):
                idx = key[i]
                # Handle negative indexing
                if idx < 0:
                    idx += self._shape[i]
                if idx < 0 or idx >= self._shape[i]:
                    raise IndexError("Index out of bounds")
                flat_index += idx * multiplier
                multiplier *= self._shape[i]
            
            # If this is a subarray, update parent's data
            if hasattr(self, '_parent') and self._parent is not None:
                self._parent._data[self._parent_offset + flat_index] = value
            else:
                self._data[flat_index] = value
        else:
            # Single index
            if len(self._shape) == 1:
                # Handle negative indexing
                if key < 0:
                    key += len(self._data)
                if key < 0 or key >= len(self._data):
                    raise IndexError("Index out of bounds")
                
                # If this is a subarray, update parent's data
                if hasattr(self, '_parent') and self._parent is not None:
                    self._parent._data[self._parent_offset + key] = value
                else:
                    self._data[key] = value
            else:
                raise ValueError("Cannot assign to sub-array with single index")
    
    def __repr__(self):
        """Return string representation of the array."""
        if not self._data:
            return "Array([])"
        
        def format_data(data, shape, start_idx=0):
            if len(shape) == 1:
                return str(data[start_idx:start_idx + shape[0]])
            else:
                result = "["
                sub_size = 1
                for dim in shape[1:]:
                    sub_size *= dim
                
                for i in range(shape[0]):
                    if i > 0:
                        result += ",\n "
                    sub_start = start_idx + i * sub_size
                    result += format_data(data, shape[1:], sub_start)
                
                result += "]"
                return result
        
        return f"Array({format_data(self._data, self._shape)})"
    
    def _check_compatible_shape(self, other):
        """Check if another array or scalar is compatible for element-wise operations."""
        if isinstance(other, Array):
            if self._shape != other._shape:
                raise ValueError(f"Shape mismatch: {self._shape} vs {other._shape}")
            return other._data
        else:
            # Scalar - broadcast to all elements
            return [other] * len(self._data)
    
    def _create_result_array(self, result_data):
        """Create a new Array instance with the same shape but different data."""
        new_array = Array([])
        new_array._data = result_data
        new_array._shape = self._shape
        return new_array
    
    # Basic arithmetic operations
    def __add__(self, other):
        """Element-wise addition."""
        other_data = self._check_compatible_shape(other)
        result_data = [a + b for a, b in zip(self._data, other_data)]
        return self._create_result_array(result_data)
    
    def __sub__(self, other):
        """Element-wise subtraction."""
        other_data = self._check_compatible_shape(other)
        result_data = [a - b for a, b in zip(self._data, other_data)]
        return self._create_result_array(result_data)
    
    def __mul__(self, other):
        """Element-wise multiplication."""
        other_data = self._check_compatible_shape(other)
        result_data = [a * b for a, b in zip(self._data, other_data)]
        return self._create_result_array(result_data)
    
    def __truediv__(self, other):
        """Element-wise division."""
        other_data = self._check_compatible_shape(other)
        result_data = [a / b for a, b in zip(self._data, other_data)]
        return self._create_result_array(result_data)
    
    # Comparison operations
    def __eq__(self, other):
        """Element-wise equality comparison."""
        other_data = self._check_compatible_shape(other)
        result_data = [a == b for a, b in zip(self._data, other_data)]
        return self._create_result_array(result_data)
    
    def __ne__(self, other):
        """Element-wise not equal comparison."""
        other_data = self._check_compatible_shape(other)
        result_data = [a != b for a, b in zip(self._data, other_data)]
        return self._create_result_array(result_data)
    
    def __gt__(self, other):
        """Element-wise greater than comparison."""
        other_data = self._check_compatible_shape(other)
        result_data = [a > b for a, b in zip(self._data, other_data)]
        return self._create_result_array(result_data)
    
    def __lt__(self, other):
        """Element-wise less than comparison."""
        other_data = self._check_compatible_shape(other)
        result_data = [a < b for a, b in zip(self._data, other_data)]
        return self._create_result_array(result_data)
    
    def __ge__(self, other):
        """Element-wise greater than or equal comparison."""
        other_data = self._check_compatible_shape(other)
        result_data = [a >= b for a, b in zip(self._data, other_data)]
        return self._create_result_array(result_data)
    
    def __le__(self, other):
        """Element-wise less than or equal comparison."""
        other_data = self._check_compatible_shape(other)
        result_data = [a <= b for a, b in zip(self._data, other_data)]
        return self._create_result_array(result_data)
    
    # Array methods that operate on the array data
    def sum(self):
        """Calculate sum of array elements."""
        return sum(self._data)
    
    def mean(self):
        """Calculate arithmetic mean of array elements."""
        if not self._data:
            raise ValueError("Cannot calculate mean of empty array")
        return sum(self._data) / len(self._data)
    
    def min(self):
        """Find minimum value in the array."""
        if not self._data:
            raise ValueError("Cannot calculate min of empty array")
        return min(self._data)
    
    def max(self):
        """Find maximum value in the array."""
        if not self._data:
            raise ValueError("Cannot calculate max of empty array")
        return max(self._data)
    
    def std(self, ddof=0):
        """Calculate standard deviation of array elements."""
        if not self._data:
            raise ValueError("Cannot calculate std of empty array")
        mean_val = self.mean()
        variance = sum((x - mean_val) ** 2 for x in self._data) / (len(self._data) - ddof)
        return variance ** 0.5
    
    def var(self, ddof=0):
        """Calculate variance of array elements."""
        if not self._data:
            raise ValueError("Cannot calculate var of empty array")
        mean_val = self.mean()
        return sum((x - mean_val) ** 2 for x in self._data) / (len(self._data) - ddof)
    
    def median(self):
        """Calculate median of array elements."""
        if not self._data:
            raise ValueError("Cannot calculate median of empty array")
        sorted_data = sorted(self._data)
        n = len(sorted_data)
        if n % 2 == 0:
            return (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
        else:
            return sorted_data[n//2]
    
    def percentile(self, q):
        """Calculate q-th percentile of array elements."""
        if not self._data:
            raise ValueError("Cannot calculate percentile of empty array")
        if not 0 <= q <= 100:
            raise ValueError("Percentile must be between 0 and 100")
        
        sorted_data = sorted(self._data)
        if q == 0:
            return sorted_data[0]
        if q == 100:
            return sorted_data[-1]
        
        index = (len(sorted_data) - 1) * q / 100
        lower = int(index)
        upper = lower + 1
        
        if upper >= len(sorted_data):
            return sorted_data[lower]
        
        weight = index - lower
        return sorted_data[lower] * (1 - weight) + sorted_data[upper] * weight
    
    def reshape(self, new_shape):
        """Give a new shape to the array without changing its data."""
        if isinstance(new_shape, int):
            new_shape = (new_shape,)
        
        # Calculate total elements
        new_size = 1
        for dim in new_shape:
            new_size *= dim
        
        if new_size != len(self._data):
            raise ValueError(f"Cannot reshape array of size {len(self._data)} into shape {new_shape}")
        
        new_array = Array([])
        new_array._data = self._data.copy()
        new_array._shape = new_shape
        return new_array
    
    @property
    def T(self):
        """Transpose the array."""
        if len(self._shape) == 1:
            # 1D array transpose is itself
            return Array(self._data.copy())
        elif len(self._shape) == 2:
            # 2D transpose
            rows, cols = self._shape
            transposed_data = []
            
            for j in range(cols):
                for i in range(rows):
                    transposed_data.append(self._data[i * cols + j])
            
            new_array = Array([])
            new_array._data = transposed_data
            new_array._shape = (cols, rows)
            return new_array
        else:
            raise NotImplementedError("Transpose for >2D arrays not yet implemented")
    
    def dot(self, other):
        """Matrix multiplication."""
        if not isinstance(other, Array):
            raise TypeError("Dot product requires another Array")
        
        if len(self._shape) != 2 or len(other._shape) != 2:
            raise ValueError("Dot product requires 2D arrays")
        
        rows_a, cols_a = self._shape
        rows_b, cols_b = other._shape
        
        if cols_a != rows_b:
            raise ValueError(f"Cannot multiply arrays with shapes {self._shape} and {other._shape}")
        
        result_data = []
        
        for i in range(rows_a):
            for j in range(cols_b):
                dot_product = 0
                for k in range(cols_a):
                    a_val = self._data[i * cols_a + k]
                    b_val = other._data[k * cols_b + j]
                    dot_product += a_val * b_val
                result_data.append(dot_product)
        
        new_array = Array([])
        new_array._data = result_data
        new_array._shape = (rows_a, cols_b)
        return new_array
    
    # Mathematical functions as methods
    def sqrt(self):
        """Element-wise square root."""
        import math
        result_data = [math.sqrt(x) for x in self._data]
        return self._create_result_array(result_data)
    
    def sin(self):
        """Element-wise sine."""
        import math
        result_data = [math.sin(x) for x in self._data]
        return self._create_result_array(result_data)
    
    def cos(self):
        """Element-wise cosine."""
        import math
        result_data = [math.cos(x) for x in self._data]
        return self._create_result_array(result_data)
    
    def exp(self):
        """Element-wise exponential."""
        import math
        result_data = [math.exp(x) for x in self._data]
        return self._create_result_array(result_data)
    
    def log(self):
        """Element-wise natural logarithm."""
        import math
        result_data = [math.log(x) for x in self._data]
        return self._create_result_array(result_data)
    
    # Logical operations
    def logical_and(self, other):
        """Element-wise logical AND."""
        if not isinstance(other, Array):
            raise TypeError("logical_and requires another Array")
        if self._shape != other._shape:
            raise ValueError(f"Shape mismatch: {self._shape} vs {other._shape}")
        
        result_data = [bool(a) and bool(b) for a, b in zip(self._data, other._data)]
        return self._create_result_array(result_data)
    
    def logical_or(self, other):
        """Element-wise logical OR."""
        if not isinstance(other, Array):
            raise TypeError("logical_or requires another Array")
        if self._shape != other._shape:
            raise ValueError(f"Shape mismatch: {self._shape} vs {other._shape}")
        
        result_data = [bool(a) or bool(b) for a, b in zip(self._data, other._data)]
        return self._create_result_array(result_data)
    
    def logical_not(self):
        """Element-wise logical NOT."""
        result_data = [not bool(x) for x in self._data]
        return self._create_result_array(result_data)