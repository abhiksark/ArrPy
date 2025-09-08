/**
 * High-performance reduction operations using SIMD.
 * Cross-platform support for ARM (NEON) and x86/x64 (AVX2/SSE2).
 */

#include <vector>
#include <algorithm>
#include <limits>
#include <cmath>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

// Platform-specific SIMD headers
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

/**
 * SIMD-optimized sum reduction.
 */
double sum_simd(const std::vector<double>& data) {
    size_t n = data.size();
    double result = 0.0;
    
    #if USE_AVX2
    // AVX2: Process 4 doubles at a time
    size_t simd_end = n - (n % 8);
    __m256d sum1 = _mm256_setzero_pd();
    __m256d sum2 = _mm256_setzero_pd();
    
    // Unrolled loop for better ILP
    for (size_t i = 0; i < simd_end; i += 8) {
        __m256d a1 = _mm256_loadu_pd(&data[i]);
        __m256d a2 = _mm256_loadu_pd(&data[i + 4]);
        sum1 = _mm256_add_pd(sum1, a1);
        sum2 = _mm256_add_pd(sum2, a2);
    }
    
    // Combine sums
    sum1 = _mm256_add_pd(sum1, sum2);
    
    // Horizontal sum
    double temp[4];
    _mm256_storeu_pd(temp, sum1);
    result = temp[0] + temp[1] + temp[2] + temp[3];
    
    // Handle remaining elements
    for (size_t i = simd_end; i < n; ++i) {
        result += data[i];
    }
    
    #elif USE_NEON
    // NEON: Process 2 doubles at a time
    size_t simd_end = n - (n % 4);
    float64x2_t sum1 = vdupq_n_f64(0.0);
    float64x2_t sum2 = vdupq_n_f64(0.0);
    
    for (size_t i = 0; i < simd_end; i += 4) {
        float64x2_t a1 = vld1q_f64(&data[i]);
        float64x2_t a2 = vld1q_f64(&data[i + 2]);
        sum1 = vaddq_f64(sum1, a1);
        sum2 = vaddq_f64(sum2, a2);
    }
    
    // Combine and horizontal sum
    sum1 = vaddq_f64(sum1, sum2);
    result = vgetq_lane_f64(sum1, 0) + vgetq_lane_f64(sum1, 1);
    
    // Handle remaining elements
    for (size_t i = simd_end; i < n; ++i) {
        result += data[i];
    }
    
    #else
    // Scalar fallback with unrolling
    size_t unroll_end = n - (n % 4);
    
    for (size_t i = 0; i < unroll_end; i += 4) {
        result += data[i] + data[i+1] + data[i+2] + data[i+3];
    }
    
    for (size_t i = unroll_end; i < n; ++i) {
        result += data[i];
    }
    #endif
    
    return result;
}

/**
 * SIMD-optimized mean calculation.
 */
double mean_simd(const std::vector<double>& data) {
    if (data.empty()) return 0.0;
    return sum_simd(data) / data.size();
}

/**
 * SIMD-optimized minimum finding.
 */
double min_simd(const std::vector<double>& data) {
    if (data.empty()) return std::numeric_limits<double>::quiet_NaN();
    
    size_t n = data.size();
    double result = data[0];
    
    #if USE_AVX2
    size_t simd_end = n - (n % 4);
    __m256d min_vec = _mm256_set1_pd(data[0]);
    
    for (size_t i = 0; i < simd_end; i += 4) {
        __m256d a = _mm256_loadu_pd(&data[i]);
        min_vec = _mm256_min_pd(min_vec, a);
    }
    
    // Extract minimum from vector
    double temp[4];
    _mm256_storeu_pd(temp, min_vec);
    result = std::min({temp[0], temp[1], temp[2], temp[3]});
    
    // Handle remaining elements
    for (size_t i = simd_end; i < n; ++i) {
        result = std::min(result, data[i]);
    }
    
    #elif USE_NEON
    size_t simd_end = n - (n % 2);
    float64x2_t min_vec = vdupq_n_f64(data[0]);
    
    for (size_t i = 0; i < simd_end; i += 2) {
        float64x2_t a = vld1q_f64(&data[i]);
        min_vec = vminq_f64(min_vec, a);
    }
    
    // Extract minimum from vector
    result = std::min(vgetq_lane_f64(min_vec, 0), vgetq_lane_f64(min_vec, 1));
    
    // Handle remaining elements
    for (size_t i = simd_end; i < n; ++i) {
        result = std::min(result, data[i]);
    }
    
    #else
    // Scalar with unrolling
    size_t unroll_end = n - (n % 4);
    
    for (size_t i = 1; i < unroll_end; i += 4) {
        result = std::min(result, data[i]);
        result = std::min(result, data[i+1]);
        result = std::min(result, data[i+2]);
        result = std::min(result, data[i+3]);
    }
    
    for (size_t i = unroll_end; i < n; ++i) {
        result = std::min(result, data[i]);
    }
    #endif
    
    return result;
}

/**
 * SIMD-optimized maximum finding.
 */
double max_simd(const std::vector<double>& data) {
    if (data.empty()) return std::numeric_limits<double>::quiet_NaN();
    
    size_t n = data.size();
    double result = data[0];
    
    #if USE_AVX2
    size_t simd_end = n - (n % 4);
    __m256d max_vec = _mm256_set1_pd(data[0]);
    
    for (size_t i = 0; i < simd_end; i += 4) {
        __m256d a = _mm256_loadu_pd(&data[i]);
        max_vec = _mm256_max_pd(max_vec, a);
    }
    
    // Extract maximum from vector
    double temp[4];
    _mm256_storeu_pd(temp, max_vec);
    result = std::max({temp[0], temp[1], temp[2], temp[3]});
    
    // Handle remaining elements
    for (size_t i = simd_end; i < n; ++i) {
        result = std::max(result, data[i]);
    }
    
    #elif USE_NEON
    size_t simd_end = n - (n % 2);
    float64x2_t max_vec = vdupq_n_f64(data[0]);
    
    for (size_t i = 0; i < simd_end; i += 2) {
        float64x2_t a = vld1q_f64(&data[i]);
        max_vec = vmaxq_f64(max_vec, a);
    }
    
    // Extract maximum from vector
    result = std::max(vgetq_lane_f64(max_vec, 0), vgetq_lane_f64(max_vec, 1));
    
    // Handle remaining elements
    for (size_t i = simd_end; i < n; ++i) {
        result = std::max(result, data[i]);
    }
    
    #else
    // Scalar with unrolling
    size_t unroll_end = n - (n % 4);
    
    for (size_t i = 1; i < unroll_end; i += 4) {
        result = std::max(result, data[i]);
        result = std::max(result, data[i+1]);
        result = std::max(result, data[i+2]);
        result = std::max(result, data[i+3]);
    }
    
    for (size_t i = unroll_end; i < n; ++i) {
        result = std::max(result, data[i]);
    }
    #endif
    
    return result;
}

/**
 * SIMD-optimized standard deviation.
 */
double std_simd(const std::vector<double>& data) {
    if (data.size() <= 1) return 0.0;
    
    double m = mean_simd(data);
    size_t n = data.size();
    double variance = 0.0;
    
    #if USE_AVX2
    size_t simd_end = n - (n % 4);
    __m256d mean_vec = _mm256_set1_pd(m);
    __m256d sum_sq = _mm256_setzero_pd();
    
    for (size_t i = 0; i < simd_end; i += 4) {
        __m256d a = _mm256_loadu_pd(&data[i]);
        __m256d diff = _mm256_sub_pd(a, mean_vec);
        __m256d sq = _mm256_mul_pd(diff, diff);
        sum_sq = _mm256_add_pd(sum_sq, sq);
    }
    
    // Extract sum of squares
    double temp[4];
    _mm256_storeu_pd(temp, sum_sq);
    variance = temp[0] + temp[1] + temp[2] + temp[3];
    
    // Handle remaining elements
    for (size_t i = simd_end; i < n; ++i) {
        double diff = data[i] - m;
        variance += diff * diff;
    }
    
    #elif USE_NEON
    size_t simd_end = n - (n % 2);
    float64x2_t mean_vec = vdupq_n_f64(m);
    float64x2_t sum_sq = vdupq_n_f64(0.0);
    
    for (size_t i = 0; i < simd_end; i += 2) {
        float64x2_t a = vld1q_f64(&data[i]);
        float64x2_t diff = vsubq_f64(a, mean_vec);
        float64x2_t sq = vmulq_f64(diff, diff);
        sum_sq = vaddq_f64(sum_sq, sq);
    }
    
    // Extract sum of squares
    variance = vgetq_lane_f64(sum_sq, 0) + vgetq_lane_f64(sum_sq, 1);
    
    // Handle remaining elements
    for (size_t i = simd_end; i < n; ++i) {
        double diff = data[i] - m;
        variance += diff * diff;
    }
    
    #else
    // Scalar fallback
    for (size_t i = 0; i < n; ++i) {
        double diff = data[i] - m;
        variance += diff * diff;
    }
    #endif
    
    return std::sqrt(variance / (n - 1));
}

// Python bindings
PYBIND11_MODULE(reduction_ops_cpp, m) {
    m.doc() = "SIMD-optimized reduction operations";
    
    m.def("sum", &sum_simd, "SIMD-optimized sum",
          py::arg("data"));
    
    m.def("mean", &mean_simd, "SIMD-optimized mean",
          py::arg("data"));
    
    m.def("min", &min_simd, "SIMD-optimized minimum",
          py::arg("data"));
    
    m.def("max", &max_simd, "SIMD-optimized maximum",
          py::arg("data"));
    
    m.def("std", &std_simd, "SIMD-optimized standard deviation",
          py::arg("data"));
    
    // SIMD capability detection
    #if USE_AVX2
    m.attr("simd_type") = "AVX2";
    #elif USE_SSE2
    m.attr("simd_type") = "SSE2";
    #elif USE_NEON
    m.attr("simd_type") = "NEON";
    #else
    m.attr("simd_type") = "scalar";
    #endif
}