"""
Data type system for arrpy arrays.
"""

class DType:
    """Base class for data types."""
    
    def __init__(self, name, size, python_type):
        """
        Initialize a data type.
        
        Parameters
        ----------
        name : str
            Name of the data type (e.g., 'int32', 'float64')
        size : int
            Size in bytes
        python_type : type
            Corresponding Python type
        """
        self.name = name
        self.size = size
        self.python_type = python_type
    
    def __repr__(self):
        return f"dtype('{self.name}')"
    
    def __str__(self):
        return self.name


# Define common data types
int32 = DType('int32', 4, int)
int64 = DType('int64', 8, int)
float32 = DType('float32', 4, float)
float64 = DType('float64', 8, float)
bool_ = DType('bool', 1, bool)

# Default types
DEFAULT_INT_TYPE = int64
DEFAULT_FLOAT_TYPE = float64


def infer_dtype(data):
    """
    Infer the data type from input data.
    
    Parameters
    ----------
    data : array-like
        Input data
    
    Returns
    -------
    DType
        Inferred data type
    """
    if not data:
        return DEFAULT_FLOAT_TYPE
    
    # Check if all elements are booleans
    all_bool = True
    # Check if all elements are integers
    all_int = True
    # Check if any element is complex
    has_complex = False
    
    for item in data:
        if not isinstance(item, bool):
            all_bool = False
        if not isinstance(item, (bool, int)):
            all_int = False
        if isinstance(item, complex):
            has_complex = True
            break
    
    if has_complex:
        # Complex numbers not yet supported
        return DEFAULT_FLOAT_TYPE
    elif all_bool:
        return bool_
    elif all_int:
        return DEFAULT_INT_TYPE
    else:
        return DEFAULT_FLOAT_TYPE