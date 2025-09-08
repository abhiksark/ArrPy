/**
 * Optimized C++ functions that work directly with buffer pointers.
 * Designed for zero-copy operations with Python's array.array via buffer protocol.
 */

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <cstring>
#include <cmath>
#include <algorithm>

// Platform-specific SIMD headers
#if defined(__x86_64__) || defined(_M_X64) || defined(__i386__) || defined(_M_IX86)
    #ifdef __AVX2__
        #include <immintrin.h>
        #define USE_AVX2 1
    #else
        #define USE_AVX2 0
    #endif
    #define USE_NEON 0
#elif defined(__aarch64__) || defined(__ARM_NEON) || defined(_M_ARM64)
    #include <arm_neon.h>
    #define USE_NEON 1
    #define USE_AVX2 0
#else
    #define USE_AVX2 0
    #define USE_NEON 0
#endif

namespace py = pybind11;

/**
 * Add two arrays using buffer pointers with SIMD optimization.
 */
void add_buffer(uintptr_t ptr1, uintptr_t ptr2, uintptr_t ptr_result, size_t size) {
    double* data1 = reinterpret_cast<double*>(ptr1);
    double* data2 = reinterpret_cast<double*>(ptr2);
    double* result = reinterpret_cast<double*>(ptr_result);
    
    #if USE_AVX2
    // Process 4 doubles at a time with AVX2
    size_t simd_end = size - (size % 4);
    for (size_t i = 0; i < simd_end; i += 4) {
        __m256d a = _mm256_loadu_pd(data1 + i);
        __m256d b = _mm256_loadu_pd(data2 + i);
        __m256d c = _mm256_add_pd(a, b);
        _mm256_storeu_pd(result + i, c);
    }
    // Handle remaining elements
    for (size_t i = simd_end; i < size; ++i) {
        result[i] = data1[i] + data2[i];
    }
    
    #elif USE_NEON
    // Process 2 doubles at a time with NEON
    size_t simd_end = size - (size % 2);
    for (size_t i = 0; i < simd_end; i += 2) {
        float64x2_t a = vld1q_f64(data1 + i);
        float64x2_t b = vld1q_f64(data2 + i);
        float64x2_t c = vaddq_f64(a, b);
        vst1q_f64(result + i, c);
    }
    // Handle remaining elements
    for (size_t i = simd_end; i < size; ++i) {
        result[i] = data1[i] + data2[i];
    }
    
    #else
    // Scalar fallback with loop unrolling
    size_t i = 0;
    for (; i + 4 <= size; i += 4) {
        result[i] = data1[i] + data2[i];
        result[i+1] = data1[i+1] + data2[i+1];
        result[i+2] = data1[i+2] + data2[i+2];
        result[i+3] = data1[i+3] + data2[i+3];
    }
    for (; i < size; ++i) {
        result[i] = data1[i] + data2[i];
    }
    #endif
}

/**
 * Subtract two arrays using buffer pointers with SIMD.
 */
void subtract_buffer(uintptr_t ptr1, uintptr_t ptr2, uintptr_t ptr_result, size_t size) {
    double* data1 = reinterpret_cast<double*>(ptr1);
    double* data2 = reinterpret_cast<double*>(ptr2);
    double* result = reinterpret_cast<double*>(ptr_result);
    
    #if USE_AVX2
    size_t simd_end = size - (size % 4);
    for (size_t i = 0; i < simd_end; i += 4) {
        __m256d a = _mm256_loadu_pd(data1 + i);
        __m256d b = _mm256_loadu_pd(data2 + i);
        __m256d c = _mm256_sub_pd(a, b);
        _mm256_storeu_pd(result + i, c);
    }
    for (size_t i = simd_end; i < size; ++i) {
        result[i] = data1[i] - data2[i];
    }
    
    #elif USE_NEON
    size_t simd_end = size - (size % 2);
    for (size_t i = 0; i < simd_end; i += 2) {
        float64x2_t a = vld1q_f64(data1 + i);
        float64x2_t b = vld1q_f64(data2 + i);
        float64x2_t c = vsubq_f64(a, b);
        vst1q_f64(result + i, c);
    }
    for (size_t i = simd_end; i < size; ++i) {
        result[i] = data1[i] - data2[i];
    }
    
    #else
    for (size_t i = 0; i < size; ++i) {
        result[i] = data1[i] - data2[i];
    }
    #endif
}

/**
 * Multiply two arrays using buffer pointers with SIMD.
 */
void multiply_buffer(uintptr_t ptr1, uintptr_t ptr2, uintptr_t ptr_result, size_t size) {
    double* data1 = reinterpret_cast<double*>(ptr1);
    double* data2 = reinterpret_cast<double*>(ptr2);
    double* result = reinterpret_cast<double*>(ptr_result);
    
    #if USE_AVX2
    size_t simd_end = size - (size % 4);
    for (size_t i = 0; i < simd_end; i += 4) {
        __m256d a = _mm256_loadu_pd(data1 + i);
        __m256d b = _mm256_loadu_pd(data2 + i);
        __m256d c = _mm256_mul_pd(a, b);
        _mm256_storeu_pd(result + i, c);
    }
    for (size_t i = simd_end; i < size; ++i) {
        result[i] = data1[i] * data2[i];
    }
    
    #elif USE_NEON
    size_t simd_end = size - (size % 2);
    for (size_t i = 0; i < simd_end; i += 2) {
        float64x2_t a = vld1q_f64(data1 + i);
        float64x2_t b = vld1q_f64(data2 + i);
        float64x2_t c = vmulq_f64(a, b);
        vst1q_f64(result + i, c);
    }
    for (size_t i = simd_end; i < size; ++i) {
        result[i] = data1[i] * data2[i];
    }
    
    #else
    for (size_t i = 0; i < size; ++i) {
        result[i] = data1[i] * data2[i];
    }
    #endif
}

/**
 * Multiply array by scalar using buffer pointer with SIMD.
 */
void multiply_scalar_buffer(uintptr_t ptr1, double scalar, uintptr_t ptr_result, size_t size) {
    double* data1 = reinterpret_cast<double*>(ptr1);
    double* result = reinterpret_cast<double*>(ptr_result);
    
    #if USE_AVX2
    __m256d scalar_vec = _mm256_set1_pd(scalar);
    size_t simd_end = size - (size % 4);
    for (size_t i = 0; i < simd_end; i += 4) {
        __m256d a = _mm256_loadu_pd(data1 + i);
        __m256d c = _mm256_mul_pd(a, scalar_vec);
        _mm256_storeu_pd(result + i, c);
    }
    for (size_t i = simd_end; i < size; ++i) {
        result[i] = data1[i] * scalar;
    }
    
    #elif USE_NEON
    float64x2_t scalar_vec = vdupq_n_f64(scalar);
    size_t simd_end = size - (size % 2);
    for (size_t i = 0; i < simd_end; i += 2) {
        float64x2_t a = vld1q_f64(data1 + i);
        float64x2_t c = vmulq_f64(a, scalar_vec);
        vst1q_f64(result + i, c);
    }
    for (size_t i = simd_end; i < size; ++i) {
        result[i] = data1[i] * scalar;
    }
    
    #else
    for (size_t i = 0; i < size; ++i) {
        result[i] = data1[i] * scalar;
    }
    #endif
}

/**
 * Divide two arrays using buffer pointers.
 */
void divide_buffer(uintptr_t ptr1, uintptr_t ptr2, uintptr_t ptr_result, size_t size) {
    double* data1 = reinterpret_cast<double*>(ptr1);
    double* data2 = reinterpret_cast<double*>(ptr2);
    double* result = reinterpret_cast<double*>(ptr_result);
    
    #if USE_AVX2
    size_t simd_end = size - (size % 4);
    for (size_t i = 0; i < simd_end; i += 4) {
        __m256d a = _mm256_loadu_pd(data1 + i);
        __m256d b = _mm256_loadu_pd(data2 + i);
        __m256d c = _mm256_div_pd(a, b);
        _mm256_storeu_pd(result + i, c);
    }
    for (size_t i = simd_end; i < size; ++i) {
        result[i] = data1[i] / data2[i];
    }
    
    #elif USE_NEON
    size_t simd_end = size - (size % 2);
    for (size_t i = 0; i < simd_end; i += 2) {
        float64x2_t a = vld1q_f64(data1 + i);
        float64x2_t b = vld1q_f64(data2 + i);
        float64x2_t c = vdivq_f64(a, b);
        vst1q_f64(result + i, c);
    }
    for (size_t i = simd_end; i < size; ++i) {
        result[i] = data1[i] / data2[i];
    }
    
    #else
    for (size_t i = 0; i < size; ++i) {
        if (data2[i] != 0.0) {
            result[i] = data1[i] / data2[i];
        } else {
            if (data1[i] > 0) {
                result[i] = INFINITY;
            } else if (data1[i] < 0) {
                result[i] = -INFINITY;
            } else {
                result[i] = NAN;
            }
        }
    }
    #endif
}

PYBIND11_MODULE(array_ops_buffer_cpp, m) {
    m.doc() = "Optimized array operations with buffer protocol support";
    
    m.def("add_buffer", &add_buffer, 
          "Add two arrays using buffer pointers",
          py::arg("ptr1"), py::arg("ptr2"), py::arg("ptr_result"), py::arg("size"));
    
    m.def("subtract_buffer", &subtract_buffer,
          "Subtract two arrays using buffer pointers",
          py::arg("ptr1"), py::arg("ptr2"), py::arg("ptr_result"), py::arg("size"));
    
    m.def("multiply_buffer", &multiply_buffer,
          "Multiply two arrays using buffer pointers",
          py::arg("ptr1"), py::arg("ptr2"), py::arg("ptr_result"), py::arg("size"));
    
    m.def("multiply_scalar_buffer", &multiply_scalar_buffer,
          "Multiply array by scalar using buffer pointer",
          py::arg("ptr1"), py::arg("scalar"), py::arg("ptr_result"), py::arg("size"));
    
    m.def("divide_buffer", &divide_buffer,
          "Divide two arrays using buffer pointers",
          py::arg("ptr1"), py::arg("ptr2"), py::arg("ptr_result"), py::arg("size"));
}