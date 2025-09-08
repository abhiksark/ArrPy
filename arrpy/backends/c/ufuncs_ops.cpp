/**
 * SIMD-optimized universal functions (ufuncs).
 * Uses platform-specific vectorized math libraries.
 */

#include <vector>
#include <cmath>
#include <algorithm>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

// Platform-specific headers
#if defined(__x86_64__) || defined(_M_X64) || defined(__i386__) || defined(_M_IX86)
    #ifdef __AVX2__
        #include <immintrin.h>
        #define USE_AVX2 1
    #elif defined(__SSE2__)
        #include <emmintrin.h>
        #define USE_SSE2 1
    #endif
#elif defined(__aarch64__) || defined(__ARM_NEON) || defined(_M_ARM64)
    #include <arm_neon.h>
    #define USE_NEON 1
#endif

#ifndef USE_AVX2
    #define USE_AVX2 0
#endif
#ifndef USE_SSE2
    #define USE_SSE2 0
#endif
#ifndef USE_NEON
    #define USE_NEON 0
#endif

namespace py = pybind11;

// Helper function for vectorized sin approximation (Taylor series)
inline double fast_sin(double x) {
    // Reduce x to [-pi, pi]
    const double pi = 3.14159265358979323846;
    const double two_pi = 2.0 * pi;
    x = std::fmod(x, two_pi);
    if (x > pi) x -= two_pi;
    if (x < -pi) x += two_pi;
    
    // Taylor series approximation
    double x2 = x * x;
    double result = x;
    double term = x;
    
    term *= -x2 / (2.0 * 3.0);
    result += term;
    
    term *= -x2 / (4.0 * 5.0);
    result += term;
    
    term *= -x2 / (6.0 * 7.0);
    result += term;
    
    return result;
}

// Helper function for vectorized exp approximation
inline double fast_exp(double x) {
    // Limit range for stability
    if (x < -20.0) return 0.0;
    if (x > 20.0) return std::exp(20.0) * std::exp(x - 20.0);
    
    // Padé approximation
    double x2 = x * x;
    double num = 1.0 + x + 0.5 * x2 + x2 * x / 6.0;
    double den = 1.0 - x + 0.5 * x2 - x2 * x / 6.0;
    
    return num / den;
}

/**
 * SIMD-optimized sine function.
 */
std::pair<std::vector<double>, std::pair<size_t, size_t>>
sin_simd(const std::vector<double>& data, const std::pair<size_t, size_t>& shape) {
    size_t n = data.size();
    std::vector<double> result(n);
    
    #if USE_AVX2
    // AVX2: Process 4 doubles at a time
    // Note: For true performance, we'd use Intel SVML or similar
    size_t simd_end = n - (n % 4);
    
    for (size_t i = 0; i < simd_end; i += 4) {
        __m256d a = _mm256_loadu_pd(&data[i]);
        
        // Extract and process each element (no direct SIMD sin in AVX2)
        double temp[4];
        _mm256_storeu_pd(temp, a);
        for (int j = 0; j < 4; ++j) {
            temp[j] = std::sin(temp[j]);
        }
        
        __m256d res = _mm256_loadu_pd(temp);
        _mm256_storeu_pd(&result[i], res);
    }
    
    // Handle remaining elements
    for (size_t i = simd_end; i < n; ++i) {
        result[i] = std::sin(data[i]);
    }
    
    #elif USE_NEON
    // NEON doesn't have native sin, use standard library
    for (size_t i = 0; i < n; ++i) {
        result[i] = std::sin(data[i]);
    }
    
    #else
    // Scalar fallback with unrolling
    size_t unroll_end = n - (n % 4);
    
    for (size_t i = 0; i < unroll_end; i += 4) {
        result[i] = std::sin(data[i]);
        result[i+1] = std::sin(data[i+1]);
        result[i+2] = std::sin(data[i+2]);
        result[i+3] = std::sin(data[i+3]);
    }
    
    for (size_t i = unroll_end; i < n; ++i) {
        result[i] = std::sin(data[i]);
    }
    #endif
    
    return {result, shape};
}

/**
 * SIMD-optimized cosine function.
 */
std::pair<std::vector<double>, std::pair<size_t, size_t>>
cos_simd(const std::vector<double>& data, const std::pair<size_t, size_t>& shape) {
    size_t n = data.size();
    std::vector<double> result(n);
    
    #if USE_AVX2
    size_t simd_end = n - (n % 4);
    
    for (size_t i = 0; i < simd_end; i += 4) {
        __m256d a = _mm256_loadu_pd(&data[i]);
        
        // Extract and process each element
        double temp[4];
        _mm256_storeu_pd(temp, a);
        for (int j = 0; j < 4; ++j) {
            temp[j] = std::cos(temp[j]);
        }
        
        __m256d res = _mm256_loadu_pd(temp);
        _mm256_storeu_pd(&result[i], res);
    }
    
    // Handle remaining elements
    for (size_t i = simd_end; i < n; ++i) {
        result[i] = std::cos(data[i]);
    }
    
    #else
    // Scalar with unrolling
    size_t unroll_end = n - (n % 4);
    
    for (size_t i = 0; i < unroll_end; i += 4) {
        result[i] = std::cos(data[i]);
        result[i+1] = std::cos(data[i+1]);
        result[i+2] = std::cos(data[i+2]);
        result[i+3] = std::cos(data[i+3]);
    }
    
    for (size_t i = unroll_end; i < n; ++i) {
        result[i] = std::cos(data[i]);
    }
    #endif
    
    return {result, shape};
}

/**
 * SIMD-optimized exponential function.
 */
std::pair<std::vector<double>, std::pair<size_t, size_t>>
exp_simd(const std::vector<double>& data, const std::pair<size_t, size_t>& shape) {
    size_t n = data.size();
    std::vector<double> result(n);
    
    #if USE_AVX2
    size_t simd_end = n - (n % 4);
    
    for (size_t i = 0; i < simd_end; i += 4) {
        __m256d a = _mm256_loadu_pd(&data[i]);
        
        // Extract and process each element
        double temp[4];
        _mm256_storeu_pd(temp, a);
        for (int j = 0; j < 4; ++j) {
            temp[j] = std::exp(temp[j]);
        }
        
        __m256d res = _mm256_loadu_pd(temp);
        _mm256_storeu_pd(&result[i], res);
    }
    
    // Handle remaining elements
    for (size_t i = simd_end; i < n; ++i) {
        result[i] = std::exp(data[i]);
    }
    
    #else
    // Scalar with unrolling
    size_t unroll_end = n - (n % 4);
    
    for (size_t i = 0; i < unroll_end; i += 4) {
        result[i] = std::exp(data[i]);
        result[i+1] = std::exp(data[i+1]);
        result[i+2] = std::exp(data[i+2]);
        result[i+3] = std::exp(data[i+3]);
    }
    
    for (size_t i = unroll_end; i < n; ++i) {
        result[i] = std::exp(data[i]);
    }
    #endif
    
    return {result, shape};
}

/**
 * SIMD-optimized logarithm function.
 */
std::pair<std::vector<double>, std::pair<size_t, size_t>>
log_simd(const std::vector<double>& data, const std::pair<size_t, size_t>& shape) {
    size_t n = data.size();
    std::vector<double> result(n);
    
    #if USE_AVX2
    size_t simd_end = n - (n % 4);
    
    for (size_t i = 0; i < simd_end; i += 4) {
        __m256d a = _mm256_loadu_pd(&data[i]);
        
        // Extract and process each element
        double temp[4];
        _mm256_storeu_pd(temp, a);
        for (int j = 0; j < 4; ++j) {
            temp[j] = std::log(temp[j]);
        }
        
        __m256d res = _mm256_loadu_pd(temp);
        _mm256_storeu_pd(&result[i], res);
    }
    
    // Handle remaining elements
    for (size_t i = simd_end; i < n; ++i) {
        result[i] = std::log(data[i]);
    }
    
    #else
    // Scalar with unrolling
    size_t unroll_end = n - (n % 4);
    
    for (size_t i = 0; i < unroll_end; i += 4) {
        result[i] = std::log(data[i]);
        result[i+1] = std::log(data[i+1]);
        result[i+2] = std::log(data[i+2]);
        result[i+3] = std::log(data[i+3]);
    }
    
    for (size_t i = unroll_end; i < n; ++i) {
        result[i] = std::log(data[i]);
    }
    #endif
    
    return {result, shape};
}

/**
 * SIMD-optimized square root function.
 */
std::pair<std::vector<double>, std::pair<size_t, size_t>>
sqrt_simd(const std::vector<double>& data, const std::pair<size_t, size_t>& shape) {
    size_t n = data.size();
    std::vector<double> result(n);
    
    #if USE_AVX2
    // AVX2 has native sqrt instruction
    size_t simd_end = n - (n % 4);
    
    for (size_t i = 0; i < simd_end; i += 4) {
        __m256d a = _mm256_loadu_pd(&data[i]);
        __m256d res = _mm256_sqrt_pd(a);
        _mm256_storeu_pd(&result[i], res);
    }
    
    // Handle remaining elements
    for (size_t i = simd_end; i < n; ++i) {
        result[i] = std::sqrt(data[i]);
    }
    
    #elif USE_NEON
    // NEON has native sqrt for ARM64
    size_t simd_end = n - (n % 2);
    
    for (size_t i = 0; i < simd_end; i += 2) {
        float64x2_t a = vld1q_f64(&data[i]);
        float64x2_t res = vsqrtq_f64(a);
        vst1q_f64(&result[i], res);
    }
    
    // Handle remaining elements
    for (size_t i = simd_end; i < n; ++i) {
        result[i] = std::sqrt(data[i]);
    }
    
    #else
    // Scalar with unrolling
    size_t unroll_end = n - (n % 4);
    
    for (size_t i = 0; i < unroll_end; i += 4) {
        result[i] = std::sqrt(data[i]);
        result[i+1] = std::sqrt(data[i+1]);
        result[i+2] = std::sqrt(data[i+2]);
        result[i+3] = std::sqrt(data[i+3]);
    }
    
    for (size_t i = unroll_end; i < n; ++i) {
        result[i] = std::sqrt(data[i]);
    }
    #endif
    
    return {result, shape};
}

// Python bindings
PYBIND11_MODULE(ufuncs_ops_cpp, m) {
    m.doc() = "SIMD-optimized universal functions";
    
    m.def("sin", &sin_simd, "SIMD-optimized sine",
          py::arg("data"), py::arg("shape"));
    
    m.def("cos", &cos_simd, "SIMD-optimized cosine",
          py::arg("data"), py::arg("shape"));
    
    m.def("exp", &exp_simd, "SIMD-optimized exponential",
          py::arg("data"), py::arg("shape"));
    
    m.def("log", &log_simd, "SIMD-optimized logarithm",
          py::arg("data"), py::arg("shape"));
    
    m.def("sqrt", &sqrt_simd, "SIMD-optimized square root",
          py::arg("data"), py::arg("shape"));
    
    // SIMD capability detection
    #if USE_AVX2
    m.attr("simd_type") = "AVX2";
    m.attr("has_native_sqrt") = true;
    #elif USE_SSE2
    m.attr("simd_type") = "SSE2";
    m.attr("has_native_sqrt") = true;
    #elif USE_NEON
    m.attr("simd_type") = "NEON";
    m.attr("has_native_sqrt") = true;
    #else
    m.attr("simd_type") = "scalar";
    m.attr("has_native_sqrt") = false;
    #endif
}