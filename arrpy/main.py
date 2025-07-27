class Array:
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
        shape = []
        current = data
        
        while isinstance(current, list):
            if not current:
                break
            shape.append(len(current))
            current = current[0]
        
        return tuple(shape)
    
    def _flatten(self, data):
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
        return self._shape
    
    def __getitem__(self, key):
        if isinstance(key, tuple):
            if len(key) != len(self._shape):
                raise IndexError("Number of indices must match number of dimensions")
            
            # Convert multi-dimensional index to flat index
            flat_index = 0
            multiplier = 1
            
            for i in range(len(self._shape) - 1, -1, -1):
                if key[i] < 0 or key[i] >= self._shape[i]:
                    raise IndexError("Index out of bounds")
                flat_index += key[i] * multiplier
                multiplier *= self._shape[i]
            
            return self._data[flat_index]
        else:
            # Single index
            if len(self._shape) == 1:
                return self._data[key]
            else:
                # Return a sub-array
                if key < 0 or key >= self._shape[0]:
                    raise IndexError("Index out of bounds")
                
                sub_size = len(self._data) // self._shape[0]
                start_idx = key * sub_size
                end_idx = start_idx + sub_size
                
                sub_data = self._data[start_idx:end_idx]
                sub_shape = self._shape[1:]
                
                # Create new Array with sub-data
                new_array = Array([])
                new_array._data = sub_data
                new_array._shape = sub_shape
                
                return new_array
    
    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            if len(key) != len(self._shape):
                raise IndexError("Number of indices must match number of dimensions")
            
            # Convert multi-dimensional index to flat index
            flat_index = 0
            multiplier = 1
            
            for i in range(len(self._shape) - 1, -1, -1):
                if key[i] < 0 or key[i] >= self._shape[i]:
                    raise IndexError("Index out of bounds")
                flat_index += key[i] * multiplier
                multiplier *= self._shape[i]
            
            self._data[flat_index] = value
        else:
            # Single index
            if len(self._shape) == 1:
                self._data[key] = value
            else:
                raise ValueError("Cannot assign to sub-array with single index")
    
    def __repr__(self):
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
        if isinstance(other, Array):
            if self._shape != other._shape:
                raise ValueError(f"Shape mismatch: {self._shape} vs {other._shape}")
            return other._data
        else:
            # Scalar
            return [other] * len(self._data)
    
    def __add__(self, other):
        other_data = self._check_compatible_shape(other)
        result_data = [a + b for a, b in zip(self._data, other_data)]
        
        new_array = Array([])
        new_array._data = result_data
        new_array._shape = self._shape
        return new_array
    
    def __sub__(self, other):
        other_data = self._check_compatible_shape(other)
        result_data = [a - b for a, b in zip(self._data, other_data)]
        
        new_array = Array([])
        new_array._data = result_data
        new_array._shape = self._shape
        return new_array
    
    def __mul__(self, other):
        other_data = self._check_compatible_shape(other)
        result_data = [a * b for a, b in zip(self._data, other_data)]
        
        new_array = Array([])
        new_array._data = result_data
        new_array._shape = self._shape
        return new_array
    
    def __truediv__(self, other):
        other_data = self._check_compatible_shape(other)
        result_data = [a / b for a, b in zip(self._data, other_data)]
        
        new_array = Array([])
        new_array._data = result_data
        new_array._shape = self._shape
        return new_array
    
    def reshape(self, new_shape):
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
        if len(self._shape) != 2:
            raise ValueError("Transpose is only supported for 2D arrays")
        
        rows, cols = self._shape
        transposed_data = []
        
        for j in range(cols):
            for i in range(rows):
                transposed_data.append(self._data[i * cols + j])
        
        new_array = Array([])
        new_array._data = transposed_data
        new_array._shape = (cols, rows)
        return new_array
    
    def dot(self, other):
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
    
    def sum(self):
        return sum(self._data)
    
    def mean(self):
        if not self._data:
            raise ValueError("Cannot calculate mean of empty array")
        return sum(self._data) / len(self._data)
    
    def min(self):
        if not self._data:
            raise ValueError("Cannot calculate min of empty array")
        return min(self._data)
    
    def max(self):
        if not self._data:
            raise ValueError("Cannot calculate max of empty array")
        return max(self._data)
    
    def std(self):
        if not self._data:
            raise ValueError("Cannot calculate std of empty array")
        mean_val = self.mean()
        variance = sum((x - mean_val) ** 2 for x in self._data) / len(self._data)
        return variance ** 0.5
    
    def var(self):
        if not self._data:
            raise ValueError("Cannot calculate var of empty array")
        mean_val = self.mean()
        return sum((x - mean_val) ** 2 for x in self._data) / len(self._data)
    
    def sqrt(self):
        """Element-wise square root"""
        import math
        result_data = [math.sqrt(x) for x in self._data]
        new_array = Array([])
        new_array._data = result_data
        new_array._shape = self._shape
        return new_array
    
    def sin(self):
        """Element-wise sine"""
        import math
        result_data = [math.sin(x) for x in self._data]
        new_array = Array([])
        new_array._data = result_data
        new_array._shape = self._shape
        return new_array
    
    def cos(self):
        """Element-wise cosine"""
        import math
        result_data = [math.cos(x) for x in self._data]
        new_array = Array([])
        new_array._data = result_data
        new_array._shape = self._shape
        return new_array
    
    def exp(self):
        """Element-wise exponential"""
        import math
        result_data = [math.exp(x) for x in self._data]
        new_array = Array([])
        new_array._data = result_data
        new_array._shape = self._shape
        return new_array
    
    def log(self):
        """Element-wise natural logarithm"""
        import math
        result_data = [math.log(x) for x in self._data]
        new_array = Array([])
        new_array._data = result_data
        new_array._shape = self._shape
        return new_array
    
    def median(self):
        """Calculate median of the array"""
        if not self._data:
            raise ValueError("Cannot calculate median of empty array")
        sorted_data = sorted(self._data)
        n = len(sorted_data)
        if n % 2 == 0:
            return (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
        else:
            return sorted_data[n//2]
    
    def percentile(self, q):
        """Calculate percentile of the array"""
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
    
    def __eq__(self, other):
        """Element-wise equality comparison"""
        other_data = self._check_compatible_shape(other)
        result_data = [a == b for a, b in zip(self._data, other_data)]
        new_array = Array([])
        new_array._data = result_data
        new_array._shape = self._shape
        return new_array
    
    def __ne__(self, other):
        """Element-wise not equal comparison"""
        other_data = self._check_compatible_shape(other)
        result_data = [a != b for a, b in zip(self._data, other_data)]
        new_array = Array([])
        new_array._data = result_data
        new_array._shape = self._shape
        return new_array
    
    def __gt__(self, other):
        """Element-wise greater than comparison"""
        other_data = self._check_compatible_shape(other)
        result_data = [a > b for a, b in zip(self._data, other_data)]
        new_array = Array([])
        new_array._data = result_data
        new_array._shape = self._shape
        return new_array
    
    def __lt__(self, other):
        """Element-wise less than comparison"""
        other_data = self._check_compatible_shape(other)
        result_data = [a < b for a, b in zip(self._data, other_data)]
        new_array = Array([])
        new_array._data = result_data
        new_array._shape = self._shape
        return new_array
    
    def __ge__(self, other):
        """Element-wise greater than or equal comparison"""
        other_data = self._check_compatible_shape(other)
        result_data = [a >= b for a, b in zip(self._data, other_data)]
        new_array = Array([])
        new_array._data = result_data
        new_array._shape = self._shape
        return new_array
    
    def __le__(self, other):
        """Element-wise less than or equal comparison"""
        other_data = self._check_compatible_shape(other)
        result_data = [a <= b for a, b in zip(self._data, other_data)]
        new_array = Array([])
        new_array._data = result_data
        new_array._shape = self._shape
        return new_array
    
    def logical_and(self, other):
        """Element-wise logical AND"""
        if not isinstance(other, Array):
            raise TypeError("logical_and requires another Array")
        if self._shape != other._shape:
            raise ValueError(f"Shape mismatch: {self._shape} vs {other._shape}")
        
        result_data = [bool(a) and bool(b) for a, b in zip(self._data, other._data)]
        new_array = Array([])
        new_array._data = result_data
        new_array._shape = self._shape
        return new_array
    
    def logical_or(self, other):
        """Element-wise logical OR"""
        if not isinstance(other, Array):
            raise TypeError("logical_or requires another Array")
        if self._shape != other._shape:
            raise ValueError(f"Shape mismatch: {self._shape} vs {other._shape}")
        
        result_data = [bool(a) or bool(b) for a, b in zip(self._data, other._data)]
        new_array = Array([])
        new_array._data = result_data
        new_array._shape = self._shape
        return new_array
    
    def logical_not(self):
        """Element-wise logical NOT"""
        result_data = [not bool(x) for x in self._data]
        new_array = Array([])
        new_array._data = result_data
        new_array._shape = self._shape
        return new_array


def zeros(shape):
    """Create an array filled with zeros"""
    if isinstance(shape, int):
        shape = (shape,)
    
    total_size = 1
    for dim in shape:
        total_size *= dim
    
    data = [0] * total_size
    arr = Array([])
    arr._data = data
    arr._shape = shape
    return arr


def ones(shape):
    """Create an array filled with ones"""
    if isinstance(shape, int):
        shape = (shape,)
    
    total_size = 1
    for dim in shape:
        total_size *= dim
    
    data = [1] * total_size
    arr = Array([])
    arr._data = data
    arr._shape = shape
    return arr


def eye(n, m=None):
    """Create an identity matrix"""
    if m is None:
        m = n
    
    data = []
    for i in range(n):
        for j in range(m):
            if i == j:
                data.append(1)
            else:
                data.append(0)
    
    arr = Array([])
    arr._data = data
    arr._shape = (n, m)
    return arr


def arange(start, stop=None, step=1):
    """Create an array with evenly spaced values within a given interval"""
    if stop is None:
        stop = start
        start = 0
    
    data = []
    current = start
    while current < stop:
        data.append(current)
        current += step
    
    return Array(data)


def linspace(start, stop, num=50):
    """Create an array with evenly spaced numbers over a specified interval"""
    if num <= 0:
        raise ValueError("Number of samples must be positive")
    
    if num == 1:
        return Array([start])
    
    step = (stop - start) / (num - 1)
    data = [start + i * step for i in range(num)]
    return Array(data)


def concatenate(arrays, axis=0):
    """Join arrays along an existing axis"""
    if not arrays:
        raise ValueError("Need at least one array to concatenate")
    
    if not all(isinstance(arr, Array) for arr in arrays):
        raise TypeError("All inputs must be Array instances")
    
    first_array = arrays[0]
    
    # Check shape compatibility
    for arr in arrays[1:]:
        if len(arr.shape) != len(first_array.shape):
            raise ValueError("All arrays must have the same number of dimensions")
        
        for i, (dim1, dim2) in enumerate(zip(first_array.shape, arr.shape)):
            if i != axis and dim1 != dim2:
                raise ValueError(f"All arrays must have the same shape except on axis {axis}")
    
    if axis < 0 or axis >= len(first_array.shape):
        raise ValueError(f"axis {axis} is out of bounds for array of dimension {len(first_array.shape)}")
    
    # Calculate new shape
    new_shape = list(first_array.shape)
    new_shape[axis] = sum(arr.shape[axis] for arr in arrays)
    new_shape = tuple(new_shape)
    
    # Concatenate data
    result_data = []
    
    if len(first_array.shape) == 1:
        # 1D case is simple
        for arr in arrays:
            result_data.extend(arr._data)
    else:
        # Multi-dimensional case
        # Calculate strides for each dimension
        strides = []
        stride = 1
        for dim in reversed(first_array.shape):
            strides.append(stride)
            stride *= dim
        strides.reverse()
        
        # For 2D case (most common)
        if len(first_array.shape) == 2 and axis == 0:
            # Concatenate rows
            for arr in arrays:
                result_data.extend(arr._data)
        elif len(first_array.shape) == 2 and axis == 1:
            # Concatenate columns
            rows = first_array.shape[0]
            cols = first_array.shape[1]
            
            for row in range(rows):
                for arr in arrays:
                    arr_cols = arr.shape[1]
                    start_idx = row * arr_cols
                    end_idx = start_idx + arr_cols
                    result_data.extend(arr._data[start_idx:end_idx])
    
    new_array = Array([])
    new_array._data = result_data
    new_array._shape = new_shape
    return new_array


def vstack(arrays):
    """Stack arrays vertically (row-wise)"""
    return concatenate(arrays, axis=0)


def hstack(arrays):
    """Stack arrays horizontally (column-wise)"""
    # For 1D arrays, hstack is just concatenation
    if all(len(arr.shape) == 1 for arr in arrays):
        return concatenate(arrays, axis=0)
    else:
        return concatenate(arrays, axis=1)