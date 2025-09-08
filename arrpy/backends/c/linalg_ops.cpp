/**
 * High-performance linear algebra operations.
 * Cross-platform support with cache-efficient algorithms.
 * OpenMP parallelization for multi-core execution.
 */

#include <vector>
#include <algorithm>
#include <cstring>
#include <cmath>
#include <cstdlib>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#ifdef _OPENMP
#include <omp.h>
#endif

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

// Cache line size (64 bytes = 8 doubles)
constexpr size_t CACHE_LINE = 64;
constexpr size_t BLOCK_SIZE = 64;

/**
 * Cache-efficient blocked matrix multiplication.
 * Works on all platforms with optional SIMD acceleration.
 */
std::pair<std::vector<double>, std::pair<size_t, size_t>> 
matmul_blocked(const std::vector<double>& data1, 
               const std::vector<double>& data2,
               const std::pair<size_t, size_t>& shape1,
               const std::pair<size_t, size_t>& shape2) {
    
    size_t m = shape1.first;
    size_t n = shape1.second;
    size_t p = shape2.second;
    
    std::vector<double> result(m * p, 0.0);
    
    // Blocked matrix multiplication for cache efficiency
    // Use OpenMP to parallelize outer loop
    #pragma omp parallel for schedule(dynamic, 1) if(m * p > 10000)
    for (size_t ii = 0; ii < m; ii += BLOCK_SIZE) {
        for (size_t jj = 0; jj < p; jj += BLOCK_SIZE) {
            for (size_t kk = 0; kk < n; kk += BLOCK_SIZE) {
                // Process block
                size_t i_end = std::min(ii + BLOCK_SIZE, m);
                size_t j_end = std::min(jj + BLOCK_SIZE, p);
                size_t k_end = std::min(kk + BLOCK_SIZE, n);
                
                for (size_t i = ii; i < i_end; ++i) {
                    for (size_t j = jj; j < j_end; ++j) {
                        double sum = result[i * p + j];
                        
                        #if USE_AVX2
                        // AVX2 for inner loop when possible
                        size_t k = kk;
                        size_t simd_end = k_end - ((k_end - kk) % 4);
                        
                        if (simd_end > kk + 4) {
                            __m256d sum_vec = _mm256_setzero_pd();
                            
                            for (; k < simd_end; k += 4) {
                                __m256d a = _mm256_loadu_pd(&data1[i * n + k]);
                                __m256d b = _mm256_set_pd(
                                    data2[(k+3) * p + j],
                                    data2[(k+2) * p + j],
                                    data2[(k+1) * p + j],
                                    data2[k * p + j]
                                );
                                sum_vec = _mm256_fmadd_pd(a, b, sum_vec);
                            }
                            
                            // Horizontal sum
                            double temp[4];
                            _mm256_storeu_pd(temp, sum_vec);
                            sum += temp[0] + temp[1] + temp[2] + temp[3];
                        }
                        
                        // Handle remaining elements
                        for (; k < k_end; ++k) {
                            sum += data1[i * n + k] * data2[k * p + j];
                        }
                        
                        #elif USE_NEON
                        // NEON for ARM processors
                        size_t k = kk;
                        size_t simd_end = k_end - ((k_end - kk) % 2);
                        
                        if (simd_end > kk + 2) {
                            float64x2_t sum_vec = vdupq_n_f64(0.0);
                            
                            for (; k < simd_end; k += 2) {
                                float64x2_t a = vld1q_f64(&data1[i * n + k]);
                                float64x2_t b = {data2[k * p + j], data2[(k+1) * p + j]};
                                sum_vec = vmlaq_f64(sum_vec, a, b);
                            }
                            
                            // Horizontal sum
                            sum += vgetq_lane_f64(sum_vec, 0) + vgetq_lane_f64(sum_vec, 1);
                        }
                        
                        // Handle remaining elements
                        for (; k < k_end; ++k) {
                            sum += data1[i * n + k] * data2[k * p + j];
                        }
                        
                        #else
                        // Scalar fallback with unrolling
                        size_t k = kk;
                        size_t unroll_end = k_end - ((k_end - kk) % 4);
                        
                        for (; k < unroll_end; k += 4) {
                            sum += data1[i * n + k] * data2[k * p + j];
                            sum += data1[i * n + k + 1] * data2[(k + 1) * p + j];
                            sum += data1[i * n + k + 2] * data2[(k + 2) * p + j];
                            sum += data1[i * n + k + 3] * data2[(k + 3) * p + j];
                        }
                        
                        for (; k < k_end; ++k) {
                            sum += data1[i * n + k] * data2[k * p + j];
                        }
                        #endif
                        
                        result[i * p + j] = sum;
                    }
                }
            }
        }
    }
    
    return {result, {m, p}};
}

/**
 * Optimized dot product with platform-specific SIMD.
 */
std::pair<std::vector<double>, std::pair<size_t, size_t>> 
dot_simd(const std::vector<double>& data1, 
         const std::vector<double>& data2,
         const std::pair<size_t, size_t>& shape1,
         const std::pair<size_t, size_t>& shape2) {
    
    // Handle vector dot product
    if (shape1.second == 1 && shape2.second == 1) {
        size_t n = data1.size();
        double result = 0.0;
        
        #if USE_AVX2
        size_t simd_end = n - (n % 8);  // Process 8 at a time
        __m256d sum1 = _mm256_setzero_pd();
        __m256d sum2 = _mm256_setzero_pd();
        
        // Unrolled loop for better ILP
        for (size_t i = 0; i < simd_end; i += 8) {
            __m256d a1 = _mm256_loadu_pd(&data1[i]);
            __m256d b1 = _mm256_loadu_pd(&data2[i]);
            __m256d a2 = _mm256_loadu_pd(&data1[i+4]);
            __m256d b2 = _mm256_loadu_pd(&data2[i+4]);
            
            sum1 = _mm256_fmadd_pd(a1, b1, sum1);
            sum2 = _mm256_fmadd_pd(a2, b2, sum2);
        }
        
        // Combine sums
        sum1 = _mm256_add_pd(sum1, sum2);
        
        // Horizontal sum
        double temp[4];
        _mm256_storeu_pd(temp, sum1);
        result = temp[0] + temp[1] + temp[2] + temp[3];
        
        // Handle remaining elements
        for (size_t i = simd_end; i < n; ++i) {
            result += data1[i] * data2[i];
        }
        
        #elif USE_NEON
        size_t simd_end = n - (n % 4);  // Process 4 at a time
        float64x2_t sum1 = vdupq_n_f64(0.0);
        float64x2_t sum2 = vdupq_n_f64(0.0);
        
        for (size_t i = 0; i < simd_end; i += 4) {
            float64x2_t a1 = vld1q_f64(&data1[i]);
            float64x2_t b1 = vld1q_f64(&data2[i]);
            float64x2_t a2 = vld1q_f64(&data1[i+2]);
            float64x2_t b2 = vld1q_f64(&data2[i+2]);
            
            sum1 = vmlaq_f64(sum1, a1, b1);
            sum2 = vmlaq_f64(sum2, a2, b2);
        }
        
        // Combine and horizontal sum
        sum1 = vaddq_f64(sum1, sum2);
        result = vgetq_lane_f64(sum1, 0) + vgetq_lane_f64(sum1, 1);
        
        // Handle remaining elements
        for (size_t i = simd_end; i < n; ++i) {
            result += data1[i] * data2[i];
        }
        
        #else
        // Scalar fallback with unrolling
        size_t unroll_end = n - (n % 4);
        
        for (size_t i = 0; i < unroll_end; i += 4) {
            result += data1[i] * data2[i];
            result += data1[i+1] * data2[i+1];
            result += data1[i+2] * data2[i+2];
            result += data1[i+3] * data2[i+3];
        }
        
        for (size_t i = unroll_end; i < n; ++i) {
            result += data1[i] * data2[i];
        }
        #endif
        
        return {{result}, {1, 1}};
    }
    
    // Matrix multiplication case
    return matmul_blocked(data1, data2, shape1, shape2);
}

/**
 * Fast matrix transpose with cache blocking.
 */
std::pair<std::vector<double>, std::pair<size_t, size_t>> 
transpose_blocked(const std::vector<double>& data,
                  const std::pair<size_t, size_t>& shape) {
    
    size_t m = shape.first;
    size_t n = shape.second;
    std::vector<double> result(m * n);
    
    // Blocked transpose for cache efficiency
    for (size_t ii = 0; ii < m; ii += BLOCK_SIZE) {
        for (size_t jj = 0; jj < n; jj += BLOCK_SIZE) {
            size_t i_end = std::min(ii + BLOCK_SIZE, m);
            size_t j_end = std::min(jj + BLOCK_SIZE, n);
            
            for (size_t i = ii; i < i_end; ++i) {
                #if USE_AVX2
                // Vectorized copy when possible
                size_t j = jj;
                size_t simd_end = j_end - ((j_end - jj) % 4);
                
                for (; j < simd_end; j += 4) {
                    // Load 4 elements from row
                    __m256d row = _mm256_loadu_pd(&data[i * n + j]);
                    
                    // Store to 4 different columns
                    result[j * m + i] = ((double*)&row)[0];
                    result[(j+1) * m + i] = ((double*)&row)[1];
                    result[(j+2) * m + i] = ((double*)&row)[2];
                    result[(j+3) * m + i] = ((double*)&row)[3];
                }
                
                for (; j < j_end; ++j) {
                    result[j * m + i] = data[i * n + j];
                }
                
                #elif USE_NEON
                size_t j = jj;
                size_t simd_end = j_end - ((j_end - jj) % 2);
                
                for (; j < simd_end; j += 2) {
                    float64x2_t row = vld1q_f64(&data[i * n + j]);
                    result[j * m + i] = vgetq_lane_f64(row, 0);
                    result[(j+1) * m + i] = vgetq_lane_f64(row, 1);
                }
                
                for (; j < j_end; ++j) {
                    result[j * m + i] = data[i * n + j];
                }
                
                #else
                for (size_t j = jj; j < j_end; ++j) {
                    result[j * m + i] = data[i * n + j];
                }
                #endif
            }
        }
    }
    
    return {result, {n, m}};
}

// Python bindings
PYBIND11_MODULE(linalg_ops_cpp, m) {
    m.doc() = "High-performance linear algebra operations (cross-platform)";
    
    m.def("matmul", &matmul_blocked, "Cache-efficient matrix multiplication",
          py::arg("data1"), py::arg("data2"), py::arg("shape1"), py::arg("shape2"));
    
    m.def("dot", &dot_simd, "SIMD-optimized dot product",
          py::arg("data1"), py::arg("data2"), py::arg("shape1"), py::arg("shape2"));
    
    m.def("transpose", &transpose_blocked, "Cache-efficient transpose",
          py::arg("data"), py::arg("shape"));
    
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