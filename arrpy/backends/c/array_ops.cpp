/**
 * High-performance array operations using C++ and SIMD.
 * Cross-platform support for ARM (NEON), x86/x64 (AVX2), and scalar fallback.
 */

#include <vector>
#include <algorithm>
#include <cstring>
#include <cstdlib>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

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

// Cross-platform aligned allocation
inline double* aligned_alloc_double(size_t n) {
    void* ptr = nullptr;
    size_t alignment = 32;  // 32-byte alignment for SIMD
    
    #ifdef _WIN32
        ptr = _aligned_malloc(n * sizeof(double), alignment);
    #elif defined(__APPLE__) || defined(__linux__)
        if (posix_memalign(&ptr, alignment, n * sizeof(double)) != 0) {
            ptr = nullptr;
        }
    #else
        // Fallback to standard malloc
        ptr = std::malloc(n * sizeof(double));
    #endif
    
    return static_cast<double*>(ptr);
}

inline void aligned_free(void* ptr) {
    #ifdef _WIN32
        _aligned_free(ptr);
    #else
        std::free(ptr);
    #endif
}

/**
 * Optimized addition using platform-specific SIMD.
 */
std::pair<std::vector<double>, std::pair<size_t, size_t>> 
add_simd(const std::vector<double>& data1, 
         const std::vector<double>& data2,
         const std::pair<size_t, size_t>& shape1,
         const std::pair<size_t, size_t>& shape2) {
    
    size_t n = data1.size();
    std::vector<double> result(n);
    
    #if USE_AVX2
    // x86/x64 with AVX2: Process 4 doubles at a time
    size_t simd_end = n - (n % 4);
    
    for (size_t i = 0; i < simd_end; i += 4) {
        __m256d a = _mm256_loadu_pd(&data1[i]);
        __m256d b = _mm256_loadu_pd(&data2[i]);
        __m256d c = _mm256_add_pd(a, b);
        _mm256_storeu_pd(&result[i], c);
    }
    
    // Handle remaining elements
    for (size_t i = simd_end; i < n; ++i) {
        result[i] = data1[i] + data2[i];
    }
    
    #elif USE_NEON
    // ARM with NEON: Process 2 doubles at a time
    size_t simd_end = n - (n % 2);
    
    for (size_t i = 0; i < simd_end; i += 2) {
        float64x2_t a = vld1q_f64(&data1[i]);
        float64x2_t b = vld1q_f64(&data2[i]);
        float64x2_t c = vaddq_f64(a, b);
        vst1q_f64(&result[i], c);
    }
    
    // Handle remaining elements
    for (size_t i = simd_end; i < n; ++i) {
        result[i] = data1[i] + data2[i];
    }
    
    #else
    // Scalar fallback with loop unrolling
    size_t unroll_end = n - (n % 4);
    
    for (size_t i = 0; i < unroll_end; i += 4) {
        result[i] = data1[i] + data2[i];
        result[i+1] = data1[i+1] + data2[i+1];
        result[i+2] = data1[i+2] + data2[i+2];
        result[i+3] = data1[i+3] + data2[i+3];
    }
    
    for (size_t i = unroll_end; i < n; ++i) {
        result[i] = data1[i] + data2[i];
    }
    #endif
    
    return {result, shape1};
}

/**
 * Optimized subtraction using platform-specific SIMD.
 */
std::pair<std::vector<double>, std::pair<size_t, size_t>> 
subtract_simd(const std::vector<double>& data1, 
              const std::vector<double>& data2,
              const std::pair<size_t, size_t>& shape1,
              const std::pair<size_t, size_t>& shape2) {
    
    size_t n = data1.size();
    std::vector<double> result(n);
    
    #if USE_AVX2
    size_t simd_end = n - (n % 4);
    
    for (size_t i = 0; i < simd_end; i += 4) {
        __m256d a = _mm256_loadu_pd(&data1[i]);
        __m256d b = _mm256_loadu_pd(&data2[i]);
        __m256d c = _mm256_sub_pd(a, b);
        _mm256_storeu_pd(&result[i], c);
    }
    
    for (size_t i = simd_end; i < n; ++i) {
        result[i] = data1[i] - data2[i];
    }
    
    #elif USE_NEON
    size_t simd_end = n - (n % 2);
    
    for (size_t i = 0; i < simd_end; i += 2) {
        float64x2_t a = vld1q_f64(&data1[i]);
        float64x2_t b = vld1q_f64(&data2[i]);
        float64x2_t c = vsubq_f64(a, b);
        vst1q_f64(&result[i], c);
    }
    
    for (size_t i = simd_end; i < n; ++i) {
        result[i] = data1[i] - data2[i];
    }
    
    #else
    size_t unroll_end = n - (n % 4);
    
    for (size_t i = 0; i < unroll_end; i += 4) {
        result[i] = data1[i] - data2[i];
        result[i+1] = data1[i+1] - data2[i+1];
        result[i+2] = data1[i+2] - data2[i+2];
        result[i+3] = data1[i+3] - data2[i+3];
    }
    
    for (size_t i = unroll_end; i < n; ++i) {
        result[i] = data1[i] - data2[i];
    }
    #endif
    
    return {result, shape1};
}

/**
 * Optimized multiplication using platform-specific SIMD.
 */
std::pair<std::vector<double>, std::pair<size_t, size_t>> 
multiply_simd(const std::vector<double>& data1, 
              const std::vector<double>& data2,
              const std::pair<size_t, size_t>& shape1,
              const std::pair<size_t, size_t>& shape2) {
    
    size_t n = data1.size();
    std::vector<double> result(n);
    
    #if USE_AVX2
    size_t simd_end = n - (n % 4);
    
    for (size_t i = 0; i < simd_end; i += 4) {
        __m256d a = _mm256_loadu_pd(&data1[i]);
        __m256d b = _mm256_loadu_pd(&data2[i]);
        __m256d c = _mm256_mul_pd(a, b);
        _mm256_storeu_pd(&result[i], c);
    }
    
    for (size_t i = simd_end; i < n; ++i) {
        result[i] = data1[i] * data2[i];
    }
    
    #elif USE_NEON
    size_t simd_end = n - (n % 2);
    
    for (size_t i = 0; i < simd_end; i += 2) {
        float64x2_t a = vld1q_f64(&data1[i]);
        float64x2_t b = vld1q_f64(&data2[i]);
        float64x2_t c = vmulq_f64(a, b);
        vst1q_f64(&result[i], c);
    }
    
    for (size_t i = simd_end; i < n; ++i) {
        result[i] = data1[i] * data2[i];
    }
    
    #else
    size_t unroll_end = n - (n % 4);
    
    for (size_t i = 0; i < unroll_end; i += 4) {
        result[i] = data1[i] * data2[i];
        result[i+1] = data1[i+1] * data2[i+1];
        result[i+2] = data1[i+2] * data2[i+2];
        result[i+3] = data1[i+3] * data2[i+3];
    }
    
    for (size_t i = unroll_end; i < n; ++i) {
        result[i] = data1[i] * data2[i];
    }
    #endif
    
    return {result, shape1};
}

/**
 * Optimized division using platform-specific SIMD.
 */
std::pair<std::vector<double>, std::pair<size_t, size_t>> 
divide_simd(const std::vector<double>& data1, 
            const std::vector<double>& data2,
            const std::pair<size_t, size_t>& shape1,
            const std::pair<size_t, size_t>& shape2) {
    
    size_t n = data1.size();
    std::vector<double> result(n);
    
    #if USE_AVX2
    size_t simd_end = n - (n % 4);
    
    for (size_t i = 0; i < simd_end; i += 4) {
        __m256d a = _mm256_loadu_pd(&data1[i]);
        __m256d b = _mm256_loadu_pd(&data2[i]);
        __m256d c = _mm256_div_pd(a, b);
        _mm256_storeu_pd(&result[i], c);
    }
    
    for (size_t i = simd_end; i < n; ++i) {
        result[i] = data1[i] / data2[i];
    }
    
    #elif USE_NEON
    size_t simd_end = n - (n % 2);
    
    for (size_t i = 0; i < simd_end; i += 2) {
        float64x2_t a = vld1q_f64(&data1[i]);
        float64x2_t b = vld1q_f64(&data2[i]);
        float64x2_t c = vdivq_f64(a, b);
        vst1q_f64(&result[i], c);
    }
    
    for (size_t i = simd_end; i < n; ++i) {
        result[i] = data1[i] / data2[i];
    }
    
    #else
    for (size_t i = 0; i < n; ++i) {
        result[i] = data1[i] / data2[i];
    }
    #endif
    
    return {result, shape1};
}

/**
 * Scalar multiplication optimized with platform-specific SIMD.
 */
std::pair<std::vector<double>, std::pair<size_t, size_t>> 
multiply_scalar_simd(const std::vector<double>& data, 
                     double scalar,
                     const std::pair<size_t, size_t>& shape) {
    
    size_t n = data.size();
    std::vector<double> result(n);
    
    #if USE_AVX2
    size_t simd_end = n - (n % 4);
    __m256d scalar_vec = _mm256_set1_pd(scalar);
    
    for (size_t i = 0; i < simd_end; i += 4) {
        __m256d a = _mm256_loadu_pd(&data[i]);
        __m256d c = _mm256_mul_pd(a, scalar_vec);
        _mm256_storeu_pd(&result[i], c);
    }
    
    for (size_t i = simd_end; i < n; ++i) {
        result[i] = data[i] * scalar;
    }
    
    #elif USE_NEON
    size_t simd_end = n - (n % 2);
    float64x2_t scalar_vec = vdupq_n_f64(scalar);
    
    for (size_t i = 0; i < simd_end; i += 2) {
        float64x2_t a = vld1q_f64(&data[i]);
        float64x2_t c = vmulq_f64(a, scalar_vec);
        vst1q_f64(&result[i], c);
    }
    
    for (size_t i = simd_end; i < n; ++i) {
        result[i] = data[i] * scalar;
    }
    
    #else
    size_t unroll_end = n - (n % 4);
    
    for (size_t i = 0; i < unroll_end; i += 4) {
        result[i] = data[i] * scalar;
        result[i+1] = data[i+1] * scalar;
        result[i+2] = data[i+2] * scalar;
        result[i+3] = data[i+3] * scalar;
    }
    
    for (size_t i = unroll_end; i < n; ++i) {
        result[i] = data[i] * scalar;
    }
    #endif
    
    return {result, shape};
}

// Python bindings
PYBIND11_MODULE(array_ops_cpp, m) {
    m.doc() = "High-performance array operations with SIMD (AVX2/NEON/scalar)";
    
    m.def("add", &add_simd, "SIMD-optimized addition",
          py::arg("data1"), py::arg("data2"), py::arg("shape1"), py::arg("shape2"));
    
    m.def("subtract", &subtract_simd, "SIMD-optimized subtraction",
          py::arg("data1"), py::arg("data2"), py::arg("shape1"), py::arg("shape2"));
    
    m.def("multiply", &multiply_simd, "SIMD-optimized multiplication",
          py::arg("data1"), py::arg("data2"), py::arg("shape1"), py::arg("shape2"));
    
    m.def("divide", &divide_simd, "SIMD-optimized division",
          py::arg("data1"), py::arg("data2"), py::arg("shape1"), py::arg("shape2"));
    
    m.def("multiply_scalar", &multiply_scalar_simd, "SIMD-optimized scalar multiplication",
          py::arg("data"), py::arg("scalar"), py::arg("shape"));
    
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
    
    // Platform info
    #ifdef _WIN32
    m.attr("platform") = "Windows";
    #elif defined(__APPLE__)
    m.attr("platform") = "macOS";
    #elif defined(__linux__)
    m.attr("platform") = "Linux";
    #else
    m.attr("platform") = "Unknown";
    #endif
}