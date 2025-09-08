"""
Backend selection system for ArrPy.
Allows switching between Python, Cython, and C backends at runtime.
"""

from enum import Enum
from typing import Optional, Dict, List, Union


class Backend(Enum):
    """Available backends for ArrPy operations."""
    PYTHON = 'python'
    CYTHON = 'cython'
    C = 'c'


# Global backend setting
_backend = Backend.PYTHON


def set_backend(backend: Union[str, Backend]) -> None:
    """
    Set the global backend for ArrPy operations.
    
    Parameters
    ----------
    backend : str or Backend
        Backend to use ('python', 'cython', or 'c')
        
    Raises
    ------
    ValueError
        If backend is not recognized
        
    Examples
    --------
    >>> import arrpy
    >>> arrpy.set_backend('python')
    >>> arrpy.set_backend(Backend.CYTHON)
    """
    global _backend
    
    if isinstance(backend, str):
        try:
            backend = Backend(backend.lower())
        except ValueError:
            valid = [b.value for b in Backend]
            raise ValueError(
                f"Unknown backend: '{backend}'. "
                f"Valid options are: {valid}"
            )
    
    _backend = backend


def get_backend() -> Backend:
    """
    Get the currently active backend.
    
    Returns
    -------
    Backend
        The current backend enum value
    """
    return _backend


def get_backend_capabilities(backend: Optional[Backend] = None) -> Dict:
    """
    Get the operations implemented in each backend.
    
    Parameters
    ----------
    backend : Backend, optional
        Specific backend to query. If None, returns all backends.
        
    Returns
    -------
    dict
        Dictionary of implemented operations for each backend
        
    Examples
    --------
    >>> capabilities = get_backend_capabilities()
    >>> capabilities[Backend.PYTHON]['add']  # True
    >>> capabilities[Backend.C]['add']  # False (not implemented yet)
    """
    # This will be populated as we implement operations
    capabilities = {
        Backend.PYTHON: {
            # Basic operations
            'add': True,
            'subtract': True,
            'multiply': True,
            'divide': True,
            'floor_divide': True,
            'mod': True,
            'power': True,
            
            # Linear algebra
            'matmul': True,
            'dot': True,
            'inner': True,
            'outer': True,
            'solve': True,
            'inv': True,
            'det': True,
            
            # Universal functions
            'sin': True,
            'cos': True,
            'tan': True,
            'exp': True,
            'log': True,
            'sqrt': True,
            'absolute': True,
            
            # Reductions
            'sum': True,
            'mean': True,
            'min': True,
            'max': True,
            'prod': True,
            'std': True,
            'var': True,
            
            # Array creation
            'zeros': True,
            'ones': True,
            'arange': True,
            'linspace': True,
            'eye': True,
            
            # Array manipulation
            'reshape': True,
            'transpose': True,
            'flatten': True,
            'concatenate': True,
            'stack': True,
            'split': True,
        },
        Backend.CYTHON: {
            # Start with just a few optimized operations
            'add': True,
            'multiply': True,
            'matmul': True,
            'sum': True,
            'sqrt': True,
            
            # Everything else not implemented yet
            'subtract': False,
            'divide': False,
            'sin': False,
            'cos': False,
            'mean': False,
            # ... etc
        },
        Backend.C: {
            # Only the most critical operations
            'matmul': True,
            'dot': True,
            
            # Everything else not implemented
            'add': False,
            'multiply': False,
            'sum': False,
            # ... etc
        }
    }
    
    if backend:
        return capabilities.get(backend, {})
    return capabilities


def show_backend_status() -> None:
    """
    Print a table showing which operations are implemented in each backend.
    
    Examples
    --------
    >>> show_backend_status()
    Backend Implementation Status
    ==============================
    Operation    Python  Cython  C
    ------------------------------
    add          ✓       ✓       ✗
    multiply     ✓       ✓       ✗
    matmul       ✓       ✓       ✓
    ...
    """
    capabilities = get_backend_capabilities()
    
    # Get all unique operations
    all_ops = set()
    for backend_caps in capabilities.values():
        all_ops.update(backend_caps.keys())
    
    # Print header
    print("\nBackend Implementation Status")
    print("=" * 40)
    print(f"{'Operation':<15} {'Python':<8} {'Cython':<8} {'C':<8}")
    print("-" * 40)
    
    # Print each operation
    for op in sorted(all_ops):
        row = f"{op:<15}"
        for backend in Backend:
            implemented = capabilities[backend].get(op, False)
            symbol = "✓" if implemented else "✗"
            row += f" {symbol:<8}"
        print(row)
    
    # Print summary
    print("-" * 40)
    print("\nCurrent backend:", get_backend().value)
    
    # Count implementations
    for backend in Backend:
        count = sum(1 for v in capabilities[backend].values() if v)
        total = len(capabilities[backend])
        print(f"{backend.value}: {count}/{total} operations implemented")


def check_backend_has_operation(operation: str, backend: Optional[Backend] = None) -> bool:
    """
    Check if a specific operation is implemented in a backend.
    
    Parameters
    ----------
    operation : str
        Name of the operation to check
    backend : Backend, optional
        Backend to check. If None, uses current backend.
        
    Returns
    -------
    bool
        True if operation is implemented, False otherwise
    """
    if backend is None:
        backend = get_backend()
    
    capabilities = get_backend_capabilities(backend)
    return capabilities.get(operation, False)


def get_available_backends_for_operation(operation: str) -> List[Backend]:
    """
    Get list of backends that implement a specific operation.
    
    Parameters
    ----------
    operation : str
        Name of the operation
        
    Returns
    -------
    list of Backend
        Backends that implement this operation
        
    Examples
    --------
    >>> get_available_backends_for_operation('matmul')
    [<Backend.PYTHON>, <Backend.CYTHON>, <Backend.C>]
    >>> get_available_backends_for_operation('sin')
    [<Backend.PYTHON>]
    """
    available = []
    capabilities = get_backend_capabilities()
    
    for backend in Backend:
        if capabilities[backend].get(operation, False):
            available.append(backend)
    
    return available