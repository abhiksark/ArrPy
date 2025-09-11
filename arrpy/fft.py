"""
Fast Fourier Transform operations for ArrPy.

Note: FFT operations are not supported as they require complex number support,
which has been removed from ArrPy to focus on core numeric computing with real numbers only.
"""

from .backend_selector import get_backend, Backend
from .arrpy_backend import ArrPy


def fft(a):
    """
    Compute the one-dimensional discrete Fourier Transform.
    
    Parameters
    ----------
    a : ArrPy
        Input array
    
    Returns
    -------
    ArrPy
        Complex array containing FFT
    """
    raise NotImplementedError(
        "FFT operations require complex number support, which has been removed from ArrPy.\n"
        "FFT inherently produces complex-valued results and cannot be implemented with only real numbers."
    )


def ifft(a):
    """
    Compute the one-dimensional inverse discrete Fourier Transform.
    
    Parameters
    ----------
    a : ArrPy
        Input array (complex)
    
    Returns
    -------
    ArrPy
        Complex array containing inverse FFT
    """
    raise NotImplementedError(
        "FFT operations require complex number support, which has been removed from ArrPy.\n"
        "FFT inherently produces complex-valued results and cannot be implemented with only real numbers."
    )


def fft2(a):
    """
    Compute the 2-dimensional discrete Fourier Transform.
    
    Parameters
    ----------
    a : ArrPy
        Input array (must be 2D)
    
    Returns
    -------
    ArrPy
        Complex array containing 2D FFT
    """
    raise NotImplementedError(
        "FFT operations require complex number support, which has been removed from ArrPy.\n"
        "FFT inherently produces complex-valued results and cannot be implemented with only real numbers."
    )


def rfft(a):
    """
    Compute the one-dimensional FFT for real input.
    
    Parameters
    ----------
    a : ArrPy
        Real-valued input array
    
    Returns
    -------
    ArrPy
        Complex array of positive frequency terms
    """
    raise NotImplementedError(
        "FFT operations require complex number support, which has been removed from ArrPy.\n"
        "FFT inherently produces complex-valued results and cannot be implemented with only real numbers."
    )


def fftfreq(n, d=1.0):
    """
    Return the Discrete Fourier Transform sample frequencies.
    
    Parameters
    ----------
    n : int
        Window length
    d : float, optional
        Sample spacing (default: 1.0)
    
    Returns
    -------
    ArrPy
        Array of length n containing the sample frequencies
    """
    backend = get_backend()
    
    if backend == Backend.PYTHON:
        from .backends.python.fft_ops import _fftfreq_python
        result_data, shape = _fftfreq_python(n, d)
    else:
        from .backends.python.fft_ops import _fftfreq_python
        result_data, shape = _fftfreq_python(n, d)
    
    from .dtype import float64
    
    result = ArrPy.__new__(ArrPy)
    result._data = result_data
    result._shape = shape
    result._size = len(result_data)
    result._dtype = float64
    result._strides = result._calculate_strides(shape)
    
    return result


def fftshift(a):
    """
    Shift the zero-frequency component to the center of the spectrum.
    
    Parameters
    ----------
    a : ArrPy
        Input array
    
    Returns
    -------
    ArrPy
        Shifted array
    """
    backend = get_backend()
    
    if backend == Backend.PYTHON:
        from .backends.python.fft_ops import _fftshift_python
        result_data, shape = _fftshift_python(a._data, a._shape)
    else:
        from .backends.python.fft_ops import _fftshift_python
        result_data, shape = _fftshift_python(a._data, a._shape)
    
    result = ArrPy.__new__(ArrPy)
    result._data = result_data
    result._shape = shape
    result._size = len(result_data)
    result._dtype = a._dtype
    result._strides = result._calculate_strides(shape)
    
    return result


def convolve(a, v, mode='full'):
    """
    Convolve two arrays using FFT.
    
    Note: This implementation uses FFT internally which requires complex numbers.
    Since complex support has been removed, this function is not available.
    
    Parameters
    ----------
    a : ArrPy
        First input array
    v : ArrPy
        Second input array
    mode : {'full', 'same', 'valid'}, optional
        Output size mode
    
    Returns
    -------
    ArrPy
        Convolution result
    """
    raise NotImplementedError(
        "Convolution via FFT requires complex number support, which has been removed from ArrPy.\n"
        "Consider implementing direct convolution without FFT for real-valued arrays."
    )


def dct(a, type=2):
    """
    Discrete Cosine Transform.
    
    Parameters
    ----------
    a : ArrPy
        Input array
    type : int, optional
        DCT type (default: 2)
    
    Returns
    -------
    ArrPy
        DCT coefficients
    """
    backend = get_backend()
    
    if backend == Backend.PYTHON:
        from .backends.python.fft_ops import _dct_python
        result_data, shape = _dct_python(a._data, a._shape, type)
    else:
        from .backends.python.fft_ops import _dct_python
        result_data, shape = _dct_python(a._data, a._shape, type)
    
    result = ArrPy.__new__(ArrPy)
    result._data = result_data
    result._shape = shape
    result._size = len(result_data)
    result._dtype = a._dtype
    result._strides = result._calculate_strides(shape)
    
    return result


def idct(a, type=2):
    """
    Inverse Discrete Cosine Transform.
    
    Parameters
    ----------
    a : ArrPy
        DCT coefficients
    type : int, optional
        DCT type (default: 2)
    
    Returns
    -------
    ArrPy
        Reconstructed signal
    """
    backend = get_backend()
    
    if backend == Backend.PYTHON:
        from .backends.python.fft_ops import _idct_python
        result_data, shape = _idct_python(a._data, a._shape, type)
    else:
        from .backends.python.fft_ops import _idct_python
        result_data, shape = _idct_python(a._data, a._shape, type)
    
    result = ArrPy.__new__(ArrPy)
    result._data = result_data
    result._shape = shape
    result._size = len(result_data)
    result._dtype = a._dtype
    result._strides = result._calculate_strides(shape)
    
    return result