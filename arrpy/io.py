"""
Input/Output operations for ArrPy arrays.
"""

import json
import struct
from .arrpy_backend import ArrPy
from .creation import array


def save(filename, arr):
    """
    Save an array to a binary file in ArrPy format.
    
    Parameters
    ----------
    filename : str
        File path to save to
    arr : ArrPy
        Array to save
    """
    if not filename.endswith('.apy'):
        filename += '.apy'
    
    with open(filename, 'wb') as f:
        # Write magic number
        f.write(b'ARRPY001')
        
        # Write metadata as JSON
        metadata = {
            'shape': arr._shape,
            'dtype': str(arr._dtype),
            'size': arr._size
        }
        metadata_json = json.dumps(metadata).encode('utf-8')
        
        # Write metadata length and metadata
        f.write(struct.pack('I', len(metadata_json)))
        f.write(metadata_json)
        
        # Write data based on dtype
        dtype_str = str(arr._dtype)
        
        if 'int' in dtype_str:
            # Integer data
            fmt = 'q' if '64' in dtype_str else 'i'  # long long or int
            for val in arr._data:
                f.write(struct.pack(fmt, int(val)))
        
        elif 'float' in dtype_str:
            # Float data
            fmt = 'd' if '64' in dtype_str else 'f'  # double or float
            for val in arr._data:
                f.write(struct.pack(fmt, float(val)))
        
        elif 'complex' in dtype_str:
            # Complex data - store as pairs of floats
            fmt = 'd' if '128' in dtype_str else 'f'
            for i in range(0, len(arr._data), 2):
                real = arr._data[i] if i < len(arr._data) else 0.0
                imag = arr._data[i + 1] if i + 1 < len(arr._data) else 0.0
                f.write(struct.pack(fmt, float(real)))
                f.write(struct.pack(fmt, float(imag)))
        
        elif 'bool' in dtype_str:
            # Boolean data
            for val in arr._data:
                f.write(struct.pack('?', bool(val)))
        
        else:
            # Default to float64
            for val in arr._data:
                f.write(struct.pack('d', float(val)))


def load(filename):
    """
    Load an array from a binary file in ArrPy format.
    
    Parameters
    ----------
    filename : str
        File path to load from
    
    Returns
    -------
    ArrPy
        Loaded array
    """
    if not filename.endswith('.apy'):
        filename += '.apy'
    
    with open(filename, 'rb') as f:
        # Read and verify magic number
        magic = f.read(8)
        if magic != b'ARRPY001':
            raise ValueError("Not a valid ArrPy file")
        
        # Read metadata length and metadata
        metadata_len = struct.unpack('I', f.read(4))[0]
        metadata_json = f.read(metadata_len).decode('utf-8')
        metadata = json.loads(metadata_json)
        
        shape = tuple(metadata['shape'])
        dtype_str = metadata['dtype']
        size = metadata['size']
        
        # Read data based on dtype
        data = []
        
        if 'int' in dtype_str:
            # Integer data
            fmt = 'q' if '64' in dtype_str else 'i'
            fmt_size = 8 if '64' in dtype_str else 4
            
            for _ in range(size):
                val = struct.unpack(fmt, f.read(fmt_size))[0]
                data.append(val)
        
        elif 'float' in dtype_str:
            # Float data
            fmt = 'd' if '64' in dtype_str else 'f'
            fmt_size = 8 if '64' in dtype_str else 4
            
            for _ in range(size):
                val = struct.unpack(fmt, f.read(fmt_size))[0]
                data.append(val)
        
        elif 'complex' in dtype_str:
            # Complex data
            fmt = 'd' if '128' in dtype_str else 'f'
            fmt_size = 8 if '128' in dtype_str else 4
            
            # Complex arrays store real/imag interleaved
            for _ in range(size // 2):  # size includes both real and imag
                real = struct.unpack(fmt, f.read(fmt_size))[0]
                imag = struct.unpack(fmt, f.read(fmt_size))[0]
                data.append(real)
                data.append(imag)
        
        elif 'bool' in dtype_str:
            # Boolean data
            for _ in range(size):
                val = struct.unpack('?', f.read(1))[0]
                data.append(val)
        
        else:
            # Default to float64
            for _ in range(size):
                val = struct.unpack('d', f.read(8))[0]
                data.append(val)
    
    # Create array
    result = ArrPy.__new__(ArrPy)
    result._data = data
    result._shape = shape
    result._size = size
    
    # Set dtype
    from .dtype import (int32, int64, float32, float64, 
                        bool_, complex64, complex128)
    
    dtype_map = {
        'int32': int32,
        'int64': int64,
        'float32': float32,
        'float64': float64,
        'bool': bool_,
        'complex64': complex64,
        'complex128': complex128
    }
    
    result._dtype = dtype_map.get(dtype_str, float64)
    result._strides = result._calculate_strides(shape)
    
    return result


def savetxt(filename, arr, delimiter=',', fmt='%.18e'):
    """
    Save an array to a text file.
    
    Parameters
    ----------
    filename : str
        File path to save to
    arr : ArrPy
        Array to save (1D or 2D)
    delimiter : str, optional
        String to separate values
    fmt : str, optional
        Format string for values
    """
    with open(filename, 'w') as f:
        if arr.ndim == 1:
            # 1D array - write as single row
            values = []
            for val in arr._data:
                if isinstance(val, bool):
                    values.append(str(val))
                elif isinstance(val, int):
                    values.append(str(val))
                else:
                    values.append(fmt % val)
            f.write(delimiter.join(values) + '\n')
        
        elif arr.ndim == 2:
            # 2D array - write row by row
            rows, cols = arr.shape
            for i in range(rows):
                values = []
                for j in range(cols):
                    val = arr._data[i * cols + j]
                    if isinstance(val, bool):
                        values.append(str(val))
                    elif isinstance(val, int):
                        values.append(str(val))
                    else:
                        values.append(fmt % val)
                f.write(delimiter.join(values) + '\n')
        
        else:
            raise ValueError("savetxt only supports 1D and 2D arrays")


def loadtxt(filename, delimiter=',', dtype=None):
    """
    Load data from a text file.
    
    Parameters
    ----------
    filename : str
        File path to load from
    delimiter : str, optional
        String separating values
    dtype : DType, optional
        Data type of the resulting array
    
    Returns
    -------
    ArrPy
        Data read from text file
    """
    data = []
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Split by delimiter
            if delimiter:
                values = line.split(delimiter)
            else:
                values = line.split()
            
            # Convert values
            row = []
            for val in values:
                val = val.strip()
                if not val:
                    continue
                
                # Try to convert to number
                try:
                    # Try int first
                    if '.' not in val and 'e' not in val.lower():
                        row.append(int(val))
                    else:
                        row.append(float(val))
                except ValueError:
                    # Keep as string or convert to boolean
                    if val.lower() == 'true':
                        row.append(True)
                    elif val.lower() == 'false':
                        row.append(False)
                    else:
                        row.append(val)
            
            if row:
                data.append(row)
    
    if not data:
        raise ValueError("No data found in file")
    
    # Check if all rows have same length
    first_len = len(data[0])
    if all(len(row) == first_len for row in data):
        # 2D array
        flat_data = [val for row in data for val in row]
        shape = (len(data), first_len)
    else:
        # Ragged array - flatten to 1D
        flat_data = [val for row in data for val in row]
        shape = (len(flat_data),)
    
    # Create array
    result = array(flat_data)
    result._shape = shape
    result._strides = result._calculate_strides(shape)
    
    # Set dtype if specified
    if dtype is not None:
        result._dtype = dtype
    
    return result


def savez(filename, **arrays):
    """
    Save multiple arrays to a compressed archive.
    
    Parameters
    ----------
    filename : str
        File path to save to
    **arrays : ArrPy
        Arrays to save with their names as keys
    """
    import zipfile
    import tempfile
    import os
    
    if not filename.endswith('.apz'):
        filename += '.apz'
    
    with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Save each array to a temporary file and add to zip
        for name, arr in arrays.items():
            with tempfile.NamedTemporaryFile(delete=False, suffix='.apy') as tmp:
                tmp_name = tmp.name
            
            try:
                save(tmp_name, arr)
                zf.write(tmp_name, f"{name}.apy")
            finally:
                os.unlink(tmp_name)


def loadz(filename):
    """
    Load arrays from a compressed archive.
    
    Parameters
    ----------
    filename : str
        File path to load from
    
    Returns
    -------
    dict
        Dictionary of arrays with their names as keys
    """
    import zipfile
    import tempfile
    import os
    
    if not filename.endswith('.apz'):
        filename += '.apz'
    
    arrays = {}
    
    with zipfile.ZipFile(filename, 'r') as zf:
        for info in zf.filelist:
            if info.filename.endswith('.apy'):
                # Extract to temporary file and load
                with tempfile.NamedTemporaryFile(delete=False, suffix='.apy') as tmp:
                    tmp.write(zf.read(info.filename))
                    tmp_name = tmp.name
                
                try:
                    name = info.filename[:-4]  # Remove .apy extension
                    arrays[name] = load(tmp_name)
                finally:
                    os.unlink(tmp_name)
    
    return arrays