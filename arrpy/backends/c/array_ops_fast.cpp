/**
 * High-performance array operations using C++ and SIMD with zero-copy numpy arrays.
 * Cross-platform support for ARM (NEON), x86/x64 (AVX2), and scalar fallback.
 */

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <algorithm>
#include <cstring>

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
 * Optimized addition using platform-specific SIMD with zero-copy numpy arrays.
 */
py::array_t<double> add_simd(
    py::array_t<double, py::array::c_style | py::array::forcecast> data1,
    py::array_t<double, py::array::c_style | py::array::forcecast> data2) {
    
    // Get direct pointer access - no copy!
    auto buf1 = data1.unchecked<1>();
    auto buf2 = data2.unchecked<1>();
    
    size_t n = buf1.shape(0);
    
    // Allocate result array
    py::array_t<double> result(n);
    auto res_buf = result.mutable_unchecked<1>();
    
    // Get raw pointers for SIMD operations
    const double* ptr1 = buf1.data(0);
    const double* ptr2 = buf2.data(0);
    double* res_ptr = res_buf.mutable_data(0);
    
    #if USE_AVX2
    // x86/x64 with AVX2: Process 4 doubles at a time
    size_t simd_end = n - (n % 4);
    
    for (size_t i = 0; i < simd_end; i += 4) {
        __m256d a = _mm256_loadu_pd(ptr1 + i);
        __m256d b = _mm256_loadu_pd(ptr2 + i);
        __m256d c = _mm256_add_pd(a, b);
        _mm256_storeu_pd(res_ptr + i, c);
    }
    
    // Handle remaining elements
    for (size_t i = simd_end; i < n; ++i) {
        res_ptr[i] = ptr1[i] + ptr2[i];
    }
    
    #elif USE_NEON
    // ARM with NEON: Process 2 doubles at a time
    size_t simd_end = n - (n % 2);
    
    for (size_t i = 0; i < simd_end; i += 2) {
        float64x2_t a = vld1q_f64(ptr1 + i);
        float64x2_t b = vld1q_f64(ptr2 + i);
        float64x2_t c = vaddq_f64(a, b);
        vst1q_f64(res_ptr + i, c);
    }
    
    // Handle remaining elements
    for (size_t i = simd_end; i < n; ++i) {
        res_ptr[i] = ptr1[i] + ptr2[i];
    }
    
    #else
    // Scalar fallback with loop unrolling
    size_t unroll_end = n - (n % 4);
    
    for (size_t i = 0; i < unroll_end; i += 4) {
        res_ptr[i] = ptr1[i] + ptr2[i];
        res_ptr[i+1] = ptr1[i+1] + ptr2[i+1];
        res_ptr[i+2] = ptr1[i+2] + ptr2[i+2];
        res_ptr[i+3] = ptr1[i+3] + ptr2[i+3];
    }
    
    for (size_t i = unroll_end; i < n; ++i) {
        res_ptr[i] = ptr1[i] + ptr2[i];
    }
    #endif
    
    return result;
}

/**
 * Optimized subtraction using platform-specific SIMD with zero-copy numpy arrays.
 */
py::array_t<double> subtract_simd(
    py::array_t<double, py::array::c_style | py::array::forcecast> data1,
    py::array_t<double, py::array::c_style | py::array::forcecast> data2) {
    
    auto buf1 = data1.unchecked<1>();
    auto buf2 = data2.unchecked<1>();
    
    size_t n = buf1.shape(0);
    py::array_t<double> result(n);
    auto res_buf = result.mutable_unchecked<1>();
    
    const double* ptr1 = buf1.data(0);
    const double* ptr2 = buf2.data(0);
    double* res_ptr = res_buf.mutable_data(0);
    
    #if USE_AVX2
    size_t simd_end = n - (n % 4);
    
    for (size_t i = 0; i < simd_end; i += 4) {
        __m256d a = _mm256_loadu_pd(ptr1 + i);
        __m256d b = _mm256_loadu_pd(ptr2 + i);
        __m256d c = _mm256_sub_pd(a, b);
        _mm256_storeu_pd(res_ptr + i, c);
    }
    
    for (size_t i = simd_end; i < n; ++i) {
        res_ptr[i] = ptr1[i] - ptr2[i];
    }
    
    #elif USE_NEON
    size_t simd_end = n - (n % 2);
    
    for (size_t i = 0; i < simd_end; i += 2) {
        float64x2_t a = vld1q_f64(ptr1 + i);
        float64x2_t b = vld1q_f64(ptr2 + i);
        float64x2_t c = vsubq_f64(a, b);
        vst1q_f64(res_ptr + i, c);
    }
    
    for (size_t i = simd_end; i < n; ++i) {
        res_ptr[i] = ptr1[i] - ptr2[i];
    }
    
    #else
    size_t unroll_end = n - (n % 4);
    
    for (size_t i = 0; i < unroll_end; i += 4) {
        res_ptr[i] = ptr1[i] - ptr2[i];
        res_ptr[i+1] = ptr1[i+1] - ptr2[i+1];
        res_ptr[i+2] = ptr1[i+2] - ptr2[i+2];
        res_ptr[i+3] = ptr1[i+3] - ptr2[i+3];
    }
    
    for (size_t i = unroll_end; i < n; ++i) {
        res_ptr[i] = ptr1[i] - ptr2[i];
    }
    #endif
    
    return result;
}

/**
 * Optimized multiplication using platform-specific SIMD with zero-copy numpy arrays.
 */
py::array_t<double> multiply_simd(
    py::array_t<double, py::array::c_style | py::array::forcecast> data1,
    py::array_t<double, py::array::c_style | py::array::forcecast> data2) {
    
    auto buf1 = data1.unchecked<1>();
    auto buf2 = data2.unchecked<1>();
    
    size_t n = buf1.shape(0);
    py::array_t<double> result(n);
    auto res_buf = result.mutable_unchecked<1>();
    
    const double* ptr1 = buf1.data(0);
    const double* ptr2 = buf2.data(0);
    double* res_ptr = res_buf.mutable_data(0);
    
    #if USE_AVX2
    size_t simd_end = n - (n % 4);
    
    for (size_t i = 0; i < simd_end; i += 4) {
        __m256d a = _mm256_loadu_pd(ptr1 + i);
        __m256d b = _mm256_loadu_pd(ptr2 + i);
        __m256d c = _mm256_mul_pd(a, b);
        _mm256_storeu_pd(res_ptr + i, c);
    }
    
    for (size_t i = simd_end; i < n; ++i) {
        res_ptr[i] = ptr1[i] * ptr2[i];
    }
    
    #elif USE_NEON
    size_t simd_end = n - (n % 2);
    
    for (size_t i = 0; i < simd_end; i += 2) {
        float64x2_t a = vld1q_f64(ptr1 + i);
        float64x2_t b = vld1q_f64(ptr2 + i);
        float64x2_t c = vmulq_f64(a, b);
        vst1q_f64(res_ptr + i, c);
    }
    
    for (size_t i = simd_end; i < n; ++i) {
        res_ptr[i] = ptr1[i] * ptr2[i];
    }
    
    #else
    size_t unroll_end = n - (n % 4);
    
    for (size_t i = 0; i < unroll_end; i += 4) {
        res_ptr[i] = ptr1[i] * ptr2[i];
        res_ptr[i+1] = ptr1[i+1] * ptr2[i+1];
        res_ptr[i+2] = ptr1[i+2] * ptr2[i+2];
        res_ptr[i+3] = ptr1[i+3] * ptr2[i+3];
    }
    
    for (size_t i = unroll_end; i < n; ++i) {
        res_ptr[i] = ptr1[i] * ptr2[i];
    }
    #endif
    
    return result;
}

/**
 * Optimized division using platform-specific SIMD with zero-copy numpy arrays.
 */
py::array_t<double> divide_simd(
    py::array_t<double, py::array::c_style | py::array::forcecast> data1,
    py::array_t<double, py::array::c_style | py::array::forcecast> data2) {
    
    auto buf1 = data1.unchecked<1>();
    auto buf2 = data2.unchecked<1>();
    
    size_t n = buf1.shape(0);
    py::array_t<double> result(n);
    auto res_buf = result.mutable_unchecked<1>();
    
    const double* ptr1 = buf1.data(0);
    const double* ptr2 = buf2.data(0);
    double* res_ptr = res_buf.mutable_data(0);
    
    #if USE_AVX2
    size_t simd_end = n - (n % 4);
    
    for (size_t i = 0; i < simd_end; i += 4) {
        __m256d a = _mm256_loadu_pd(ptr1 + i);
        __m256d b = _mm256_loadu_pd(ptr2 + i);
        __m256d c = _mm256_div_pd(a, b);
        _mm256_storeu_pd(res_ptr + i, c);
    }
    
    for (size_t i = simd_end; i < n; ++i) {
        res_ptr[i] = ptr1[i] / ptr2[i];
    }
    
    #elif USE_NEON
    size_t simd_end = n - (n % 2);
    
    for (size_t i = 0; i < simd_end; i += 2) {
        float64x2_t a = vld1q_f64(ptr1 + i);
        float64x2_t b = vld1q_f64(ptr2 + i);
        float64x2_t c = vdivq_f64(a, b);
        vst1q_f64(res_ptr + i, c);
    }
    
    for (size_t i = simd_end; i < n; ++i) {
        res_ptr[i] = ptr1[i] / ptr2[i];
    }
    
    #else
    size_t unroll_end = n - (n % 4);
    
    for (size_t i = 0; i < unroll_end; i += 4) {
        res_ptr[i] = ptr1[i] / ptr2[i];
        res_ptr[i+1] = ptr1[i+1] / ptr2[i+1];
        res_ptr[i+2] = ptr1[i+2] / ptr2[i+2];
        res_ptr[i+3] = ptr1[i+3] / ptr2[i+3];
    }
    
    for (size_t i = unroll_end; i < n; ++i) {
        res_ptr[i] = ptr1[i] / ptr2[i];
    }
    #endif
    
    return result;
}

/**
 * Optimized scalar multiplication with SIMD and zero-copy.
 */
py::array_t<double> multiply_scalar_simd(
    py::array_t<double, py::array::c_style | py::array::forcecast> data,
    double scalar) {
    
    auto buf = data.unchecked<1>();
    size_t n = buf.shape(0);
    py::array_t<double> result(n);
    auto res_buf = result.mutable_unchecked<1>();
    
    const double* ptr = buf.data(0);
    double* res_ptr = res_buf.mutable_data(0);
    
    #if USE_AVX2
    __m256d scalar_vec = _mm256_set1_pd(scalar);
    size_t simd_end = n - (n % 4);
    
    for (size_t i = 0; i < simd_end; i += 4) {
        __m256d a = _mm256_loadu_pd(ptr + i);
        __m256d c = _mm256_mul_pd(a, scalar_vec);
        _mm256_storeu_pd(res_ptr + i, c);
    }
    
    for (size_t i = simd_end; i < n; ++i) {
        res_ptr[i] = ptr[i] * scalar;
    }
    
    #elif USE_NEON
    float64x2_t scalar_vec = vdupq_n_f64(scalar);
    size_t simd_end = n - (n % 2);
    
    for (size_t i = 0; i < simd_end; i += 2) {
        float64x2_t a = vld1q_f64(ptr + i);
        float64x2_t c = vmulq_f64(a, scalar_vec);
        vst1q_f64(res_ptr + i, c);
    }
    
    for (size_t i = simd_end; i < n; ++i) {
        res_ptr[i] = ptr[i] * scalar;
    }
    
    #else
    size_t unroll_end = n - (n % 4);
    
    for (size_t i = 0; i < unroll_end; i += 4) {
        res_ptr[i] = ptr[i] * scalar;
        res_ptr[i+1] = ptr[i+1] * scalar;
        res_ptr[i+2] = ptr[i+2] * scalar;
        res_ptr[i+3] = ptr[i+3] * scalar;
    }
    
    for (size_t i = unroll_end; i < n; ++i) {
        res_ptr[i] = ptr[i] * scalar;
    }
    #endif
    
    return result;
}

// Python module definition
PYBIND11_MODULE(array_ops_fast_cpp, m) {
    m.doc() = "Fast SIMD-optimized array operations with zero-copy numpy arrays";
    
    m.def("add", &add_simd, "SIMD-optimized addition with zero-copy",
          py::arg("data1").noconvert(), py::arg("data2").noconvert());
    
    m.def("subtract", &subtract_simd, "SIMD-optimized subtraction with zero-copy",
          py::arg("data1").noconvert(), py::arg("data2").noconvert());
    
    m.def("multiply", &multiply_simd, "SIMD-optimized multiplication with zero-copy",
          py::arg("data1").noconvert(), py::arg("data2").noconvert());
    
    m.def("divide", &divide_simd, "SIMD-optimized division with zero-copy",
          py::arg("data1").noconvert(), py::arg("data2").noconvert());
    
    m.def("multiply_scalar", &multiply_scalar_simd, "SIMD-optimized scalar multiplication",
          py::arg("data").noconvert(), py::arg("scalar"));
    
    // Platform detection attributes
    #if USE_AVX2
    m.attr("simd_type") = "AVX2";
    m.attr("has_avx2") = true;
    m.attr("has_neon") = false;
    #elif USE_NEON
    m.attr("simd_type") = "NEON";
    m.attr("has_avx2") = false;
    m.attr("has_neon") = true;
    #else
    m.attr("simd_type") = "scalar";
    m.attr("has_avx2") = false;
    m.attr("has_neon") = false;
    #endif
}