"""
Sorting and searching operations for Python backend.
Educational implementations of various sorting algorithms.
"""


def _sort_python(data, shape, axis=-1, kind='quicksort'):
    """
    Sort an array along the given axis.
    
    Educational implementation showing different sorting algorithms.
    """
    import copy
    
    # Convert to nested lists for easier manipulation
    def to_nested(flat_data, shape):
        if len(shape) == 1:
            return flat_data[:]
        
        size = 1
        for dim in shape[1:]:
            size *= dim
        
        nested = []
        for i in range(shape[0]):
            nested.append(to_nested(flat_data[i*size:(i+1)*size], shape[1:]))
        return nested
    
    def from_nested(nested, shape):
        if len(shape) == 1:
            return nested[:]
        
        flat = []
        for item in nested:
            flat.extend(from_nested(item, shape[1:]))
        return flat
    
    # Handle negative axis
    if axis < 0:
        axis = len(shape) + axis
    
    if axis < 0 or axis >= len(shape):
        raise ValueError(f"axis {axis} is out of bounds for array of dimension {len(shape)}")
    
    # For 1D arrays, just sort directly
    if len(shape) == 1:
        sorted_data = sorted(data)
        return sorted_data, shape
    
    # Convert to nested structure
    nested = to_nested(data, shape)
    
    # Sort along the specified axis
    def sort_recursive(arr, current_axis, target_axis):
        if current_axis == target_axis:
            # Sort this level
            if isinstance(arr[0], list):
                # Need to transpose, sort, then transpose back
                transposed = list(zip(*arr))
                sorted_transposed = [sorted(row) for row in transposed]
                return list(map(list, zip(*sorted_transposed)))
            else:
                return sorted(arr)
        else:
            # Recurse deeper
            return [sort_recursive(item, current_axis + 1, target_axis) for item in arr]
    
    sorted_nested = sort_recursive(nested, 0, axis)
    
    # Convert back to flat
    sorted_data = from_nested(sorted_nested, shape)
    
    return sorted_data, shape


def _argsort_python(data, shape, axis=-1, kind='quicksort'):
    """
    Return the indices that would sort an array.
    
    Educational implementation showing index tracking during sort.
    """
    # Handle negative axis
    if axis < 0:
        axis = len(shape) + axis
    
    if axis < 0 or axis >= len(shape):
        raise ValueError(f"axis {axis} is out of bounds for array of dimension {len(shape)}")
    
    # For 1D arrays
    if len(shape) == 1:
        # Create pairs of (value, index)
        indexed_data = [(data[i], i) for i in range(len(data))]
        # Sort by value
        indexed_data.sort(key=lambda x: x[0])
        # Extract indices
        indices = [x[1] for x in indexed_data]
        return indices, shape
    
    # For multi-dimensional arrays, we need to handle axis properly
    # This is a simplified implementation for 2D arrays
    if len(shape) == 2 and axis == 1:
        indices_data = []
        rows, cols = shape
        
        for row in range(rows):
            row_data = data[row * cols:(row + 1) * cols]
            indexed = [(row_data[i], i) for i in range(cols)]
            indexed.sort(key=lambda x: x[0])
            row_indices = [x[1] for x in indexed]
            indices_data.extend(row_indices)
        
        return indices_data, shape
    
    elif len(shape) == 2 and axis == 0:
        indices_data = []
        rows, cols = shape
        
        # Process each column
        for col in range(cols):
            col_data = [data[row * cols + col] for row in range(rows)]
            indexed = [(col_data[i], i) for i in range(rows)]
            indexed.sort(key=lambda x: x[0])
            col_indices = [x[1] for x in indexed]
            
            # Place indices in correct positions
            for row, idx in enumerate(col_indices):
                if row == 0:
                    indices_data.append(idx)
                else:
                    # Insert at correct position
                    pos = row * cols + col
                    while len(indices_data) <= pos:
                        indices_data.append(0)
                    indices_data[pos] = idx
        
        return indices_data, shape
    
    # Fallback for higher dimensions
    raise NotImplementedError(f"argsort for {len(shape)}D arrays on axis {axis} not yet implemented")


def _searchsorted_python(a_data, a_shape, v_data, v_shape, side='left'):
    """
    Find indices where elements should be inserted to maintain order.
    
    Educational implementation of binary search.
    """
    # Assume a_data is sorted and 1D for simplicity
    if len(a_shape) != 1:
        raise ValueError("searchsorted requires 1D sorted array")
    
    def binary_search(arr, val, side='left'):
        """Binary search implementation."""
        left, right = 0, len(arr)
        
        if side == 'left':
            # Find leftmost position
            while left < right:
                mid = (left + right) // 2
                if arr[mid] < val:
                    left = mid + 1
                else:
                    right = mid
        else:  # side == 'right'
            # Find rightmost position
            while left < right:
                mid = (left + right) // 2
                if arr[mid] <= val:
                    left = mid + 1
                else:
                    right = mid
        
        return left
    
    # Process each value in v_data
    result = []
    for val in v_data:
        idx = binary_search(a_data, val, side)
        result.append(idx)
    
    return result, v_shape


def _partition_python(data, shape, kth, axis=-1):
    """
    Partition array so that element at kth position is in its sorted position.
    
    Educational implementation of quickselect algorithm.
    """
    import copy
    
    # Handle negative axis
    if axis < 0:
        axis = len(shape) + axis
    
    if axis < 0 or axis >= len(shape):
        raise ValueError(f"axis {axis} is out of bounds for array of dimension {len(shape)}")
    
    # Make a copy of the data
    result_data = copy.copy(data)
    
    # For 1D arrays
    if len(shape) == 1:
        n = len(data)
        
        # Convert kth to list if scalar
        if isinstance(kth, int):
            kth = [kth]
        
        def partition_1d(arr, left, right, k):
            """Partition around kth element using quickselect."""
            if left == right:
                return
            
            # Choose pivot
            pivot_idx = (left + right) // 2
            pivot_val = arr[pivot_idx]
            
            # Move pivot to end
            arr[pivot_idx], arr[right] = arr[right], arr[pivot_idx]
            
            # Partition
            store_idx = left
            for i in range(left, right):
                if arr[i] < pivot_val:
                    arr[store_idx], arr[i] = arr[i], arr[store_idx]
                    store_idx += 1
            
            # Move pivot to final position
            arr[right], arr[store_idx] = arr[store_idx], arr[right]
            
            # Recurse on the part containing k
            if k < store_idx:
                partition_1d(arr, left, store_idx - 1, k)
            elif k > store_idx:
                partition_1d(arr, store_idx + 1, right, k)
        
        # Partition for each kth value
        for k in sorted(kth):
            if k < 0:
                k = n + k
            if k < 0 or k >= n:
                raise ValueError(f"kth value {k} is out of bounds")
            partition_1d(result_data, 0, n - 1, k)
        
        return result_data, shape
    
    # For multi-dimensional arrays
    # Simplified implementation for 2D arrays
    if len(shape) == 2:
        rows, cols = shape
        
        if axis == 1:
            # Partition each row
            for row in range(rows):
                row_start = row * cols
                row_data = result_data[row_start:row_start + cols]
                
                # Convert kth to list if scalar
                if isinstance(kth, int):
                    kth_list = [kth]
                else:
                    kth_list = list(kth)
                
                # Apply quickselect to this row
                def partition_1d(arr, left, right, k):
                    if left >= right:
                        return
                    
                    pivot_idx = (left + right) // 2
                    pivot_val = arr[pivot_idx]
                    arr[pivot_idx], arr[right] = arr[right], arr[pivot_idx]
                    
                    store_idx = left
                    for i in range(left, right):
                        if arr[i] < pivot_val:
                            arr[store_idx], arr[i] = arr[i], arr[store_idx]
                            store_idx += 1
                    
                    arr[right], arr[store_idx] = arr[store_idx], arr[right]
                    
                    if k < store_idx:
                        partition_1d(arr, left, store_idx - 1, k)
                    elif k > store_idx:
                        partition_1d(arr, store_idx + 1, right, k)
                
                for k in sorted(kth_list):
                    if k < 0:
                        k = cols + k
                    if k < 0 or k >= cols:
                        raise ValueError(f"kth value {k} is out of bounds")
                    partition_1d(row_data, 0, cols - 1, k)
                
                # Copy back
                for i, val in enumerate(row_data):
                    result_data[row_start + i] = val
        
        elif axis == 0:
            # Partition each column - more complex, skipping for now
            raise NotImplementedError("Partition along axis 0 for 2D arrays not yet implemented")
    
    else:
        raise NotImplementedError(f"Partition for {len(shape)}D arrays not yet implemented")
    
    return result_data, shape


def _unique_python(data, shape, return_index=False, return_inverse=False, return_counts=False):
    """
    Find the unique elements of an array.
    
    Educational implementation showing how to track unique elements.
    """
    # Flatten the data
    flat_data = data[:]
    
    # Track unique elements and their info
    seen = {}  # value -> first_index
    unique_vals = []
    indices = []
    
    for i, val in enumerate(flat_data):
        if val not in seen:
            seen[val] = len(unique_vals)
            unique_vals.append(val)
            indices.append(i)
    
    # Sort unique values
    sorted_pairs = sorted(zip(unique_vals, indices))
    unique_vals = [p[0] for p in sorted_pairs]
    first_indices = [p[1] for p in sorted_pairs]
    
    # Build return values
    results = [unique_vals, (len(unique_vals),)]
    
    if return_index:
        results.extend([first_indices, (len(first_indices),)])
    
    if return_inverse:
        # Create mapping from original to unique
        val_to_idx = {val: i for i, val in enumerate(unique_vals)}
        inverse = [val_to_idx[val] for val in flat_data]
        results.extend([inverse, shape])
    
    if return_counts:
        # Count occurrences
        counts = [0] * len(unique_vals)
        for val in flat_data:
            idx = val_to_idx[val] if return_inverse else seen[val]
            counts[idx] += 1
        results.extend([counts, (len(counts),)])
    
    return results