"""
Fast Fourier Transform operations for Python backend.
Educational implementation of FFT algorithms.
"""

import math
import cmath


def _fft_python(data, shape, inverse=False):
    """
    Compute 1D FFT using Cooley-Tukey algorithm.
    
    Educational recursive implementation showing the divide-and-conquer approach.
    """
    n = shape[0] if len(shape) == 1 else shape[0] * shape[1]
    
    # Convert to complex numbers
    if all(isinstance(x, (int, float)) for x in data):
        x = [complex(val) for val in data[:n]]
    else:
        x = data[:n]
    
    # Compute FFT
    result = _fft_recursive(x, inverse)
    
    # Convert back to flat list format (real and imaginary parts interleaved)
    result_flat = []
    for val in result:
        result_flat.append(val.real)
        result_flat.append(val.imag)
    
    return result_flat, (len(result), 2)  # Shape is (n, 2) for complex


def _fft_recursive(x, inverse=False):
    """
    Recursive Cooley-Tukey FFT algorithm.
    
    This is the classic divide-and-conquer FFT algorithm.
    """
    n = len(x)
    
    # Base case
    if n <= 1:
        return x
    
    # Pad to nearest power of 2 if necessary
    if n & (n - 1):  # Not a power of 2
        # Find next power of 2
        next_pow2 = 1
        while next_pow2 < n:
            next_pow2 <<= 1
        # Pad with zeros
        x = x + [0] * (next_pow2 - n)
        n = next_pow2
    
    # Divide
    even = _fft_recursive([x[i] for i in range(0, n, 2)], inverse)
    odd = _fft_recursive([x[i] for i in range(1, n, 2)], inverse)
    
    # Conquer
    T = []
    for k in range(n // 2):
        # Twiddle factor
        angle = -2 * math.pi * k / n
        if inverse:
            angle = -angle
        w = cmath.exp(1j * angle)
        
        t = w * odd[k]
        T.append(t)
    
    # Combine
    result = [0] * n
    for k in range(n // 2):
        result[k] = even[k] + T[k]
        result[k + n // 2] = even[k] - T[k]
    
    # Normalize for inverse transform
    if inverse:
        result = [val / 2 for val in result]
    
    return result


def _fft2_python(data, shape):
    """
    Compute 2D FFT using row-column decomposition.
    
    Applies 1D FFT to rows, then to columns.
    """
    rows, cols = shape
    
    # Convert flat data to 2D complex array
    data_2d = []
    for i in range(rows):
        row = []
        for j in range(cols):
            idx = i * cols + j
            if idx < len(data):
                row.append(complex(data[idx]))
            else:
                row.append(0j)
        data_2d.append(row)
    
    # FFT on rows
    for i in range(rows):
        data_2d[i] = _fft_recursive(data_2d[i], False)
    
    # Transpose
    data_transposed = [[data_2d[i][j] for i in range(rows)] for j in range(cols)]
    
    # FFT on columns (now rows after transpose)
    for j in range(cols):
        data_transposed[j] = _fft_recursive(data_transposed[j], False)
    
    # Transpose back
    result_2d = [[data_transposed[j][i] for j in range(cols)] for i in range(rows)]
    
    # Flatten to interleaved real/imaginary format
    result_flat = []
    for row in result_2d:
        for val in row:
            result_flat.append(val.real)
            result_flat.append(val.imag)
    
    return result_flat, (rows, cols, 2)


def _ifft_python(data, shape):
    """
    Compute inverse FFT.
    
    Uses the property that IFFT(x) = conj(FFT(conj(x))) / N
    """
    # Extract complex values from interleaved format
    n = shape[0]
    complex_data = []
    for i in range(0, len(data), 2):
        real = data[i] if i < len(data) else 0
        imag = data[i + 1] if i + 1 < len(data) else 0
        complex_data.append(complex(real, imag))
    
    # Compute inverse FFT
    result = _fft_recursive(complex_data, inverse=True)
    
    # Normalize
    result = [val * 2 / n for val in result]  # Compensate for recursive normalization
    
    # Convert back to flat format
    result_flat = []
    for val in result:
        result_flat.append(val.real)
        result_flat.append(val.imag)
    
    return result_flat, (len(result), 2)


def _rfft_python(data, shape):
    """
    Compute real FFT (FFT of real-valued signal).
    
    Returns only the positive frequency components.
    """
    n = shape[0] if len(shape) == 1 else shape[0] * shape[1]
    
    # Convert to complex
    x = [complex(data[i]) if i < len(data) else 0j for i in range(n)]
    
    # Compute full FFT
    result = _fft_recursive(x, False)
    
    # Return only positive frequencies (first half + 1)
    n_out = n // 2 + 1
    result_flat = []
    for i in range(n_out):
        result_flat.append(result[i].real)
        result_flat.append(result[i].imag)
    
    return result_flat, (n_out, 2)


def _fftfreq_python(n, d=1.0):
    """
    Return the Discrete Fourier Transform sample frequencies.
    
    The returned frequencies are in cycles per unit of the sample spacing.
    """
    val = 1.0 / (n * d)
    results = []
    N = (n - 1) // 2 + 1
    
    # Positive frequencies
    for i in range(N):
        results.append(i * val)
    
    # Negative frequencies
    for i in range(-(n // 2), 0):
        results.append(i * val)
    
    return results, (n,)


def _fftshift_python(data, shape):
    """
    Shift the zero-frequency component to the center of the spectrum.
    
    Swaps half-spaces for all axes.
    """
    if len(shape) == 1:
        n = shape[0]
        mid = n // 2
        
        # Swap halves
        result = data[mid:] + data[:mid]
        return result, shape
    
    elif len(shape) == 2:
        rows, cols = shape
        mid_row = rows // 2
        mid_col = cols // 2
        
        # Create 2D array
        data_2d = [[data[i * cols + j] for j in range(cols)] for i in range(rows)]
        
        # Swap quadrants
        result_2d = [[0] * cols for _ in range(rows)]
        
        # Top-left -> bottom-right
        for i in range(mid_row):
            for j in range(mid_col):
                result_2d[i + mid_row][j + mid_col] = data_2d[i][j]
        
        # Top-right -> bottom-left
        for i in range(mid_row):
            for j in range(mid_col, cols):
                result_2d[i + mid_row][j - mid_col] = data_2d[i][j]
        
        # Bottom-left -> top-right
        for i in range(mid_row, rows):
            for j in range(mid_col):
                result_2d[i - mid_row][j + mid_col] = data_2d[i][j]
        
        # Bottom-right -> top-left
        for i in range(mid_row, rows):
            for j in range(mid_col, cols):
                result_2d[i - mid_row][j - mid_col] = data_2d[i][j]
        
        # Flatten
        result = [val for row in result_2d for val in row]
        return result, shape
    
    else:
        raise NotImplementedError(f"fftshift for {len(shape)}D arrays not implemented")


def _convolve_fft_python(data1, shape1, data2, shape2, mode='full'):
    """
    Convolve two arrays using FFT.
    
    Efficient convolution using the convolution theorem:
    conv(f, g) = ifft(fft(f) * fft(g))
    """
    n1 = shape1[0] if len(shape1) == 1 else shape1[0] * shape1[1]
    n2 = shape2[0] if len(shape2) == 1 else shape2[0] * shape2[1]
    
    # Determine output size
    if mode == 'full':
        n_out = n1 + n2 - 1
    elif mode == 'same':
        n_out = n1
    elif mode == 'valid':
        n_out = max(n1 - n2 + 1, 0)
    else:
        raise ValueError(f"Unknown mode: {mode}")
    
    # Pad to next power of 2 for efficiency
    n_fft = 1
    while n_fft < n_out:
        n_fft <<= 1
    
    # Pad inputs
    x1 = [complex(data1[i]) if i < n1 else 0j for i in range(n_fft)]
    x2 = [complex(data2[i]) if i < n2 else 0j for i in range(n_fft)]
    
    # Compute FFTs
    X1 = _fft_recursive(x1, False)
    X2 = _fft_recursive(x2, False)
    
    # Multiply in frequency domain
    Y = [X1[i] * X2[i] for i in range(n_fft)]
    
    # Inverse FFT
    y = _fft_recursive(Y, inverse=True)
    
    # Normalize and extract result
    y = [val.real * n_fft / 2 for val in y]  # Compensate for recursive normalization
    
    if mode == 'full':
        result = y[:n_out]
    elif mode == 'same':
        start = (n2 - 1) // 2
        result = y[start:start + n1]
    else:  # valid
        result = y[n2 - 1:n2 - 1 + n_out] if n_out > 0 else []
    
    return result, (len(result),)


def _dct_python(data, shape, type=2):
    """
    Discrete Cosine Transform.
    
    Type II DCT (most common, used in JPEG).
    """
    n = shape[0] if len(shape) == 1 else shape[0] * shape[1]
    x = data[:n]
    
    if type == 2:
        # Type II DCT
        result = []
        for k in range(n):
            sum_val = 0
            for i in range(n):
                angle = math.pi * k * (2 * i + 1) / (2 * n)
                sum_val += x[i] * math.cos(angle)
            
            # Normalization
            if k == 0:
                sum_val *= math.sqrt(1 / n)
            else:
                sum_val *= math.sqrt(2 / n)
            
            result.append(sum_val)
        
        return result, shape
    
    else:
        raise NotImplementedError(f"DCT type {type} not implemented")


def _idct_python(data, shape, type=2):
    """
    Inverse Discrete Cosine Transform.
    
    Type II IDCT (actually Type III DCT).
    """
    n = shape[0] if len(shape) == 1 else shape[0] * shape[1]
    x = data[:n]
    
    if type == 2:
        # Type III DCT (inverse of Type II)
        result = []
        for i in range(n):
            sum_val = x[0] * math.sqrt(1 / n)  # DC component
            
            for k in range(1, n):
                angle = math.pi * k * (2 * i + 1) / (2 * n)
                sum_val += x[k] * math.sqrt(2 / n) * math.cos(angle)
            
            result.append(sum_val)
        
        return result, shape
    
    else:
        raise NotImplementedError(f"IDCT type {type} not implemented")