/**
 * Highly optimized C++ array operations with multiple performance improvements:
 * - Memory alignment for SIMD
 * - OpenMP parallelization
 * - Aggressive loop unrolling
 * - Prefetching
 * - Fast math approximations
 */

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <cstring>
#include <cmath>
#include <algorithm>

// OpenMP support (optional)
#ifdef _OPENMP
    #include <omp.h>
    #define USE_OPENMP 1
#else
    #define USE_OPENMP 0
    #define omp_get_max_threads() 1
#endif

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

// Constants for optimization
constexpr size_t CACHE_LINE = 64;
constexpr size_t SIMD_ALIGN = 32;  // For AVX2
constexpr size_t PARALLEL_THRESHOLD = 10000;  // Use OpenMP for arrays larger than this
constexpr size_t UNROLL_FACTOR = 4;  // Process 4x4 = 16 doubles per iteration with AVX2

// Check if pointer is aligned
inline bool is_aligned(const void* ptr, size_t alignment) {
    return (reinterpret_cast<uintptr_t>(ptr) & (alignment - 1)) == 0;
}

/**
 * Highly optimized addition with all improvements
 */
void add_optimized(uintptr_t ptr1, uintptr_t ptr2, uintptr_t ptr_result, size_t size) {
    double* __restrict__ data1 = reinterpret_cast<double*>(ptr1);
    double* __restrict__ data2 = reinterpret_cast<double*>(ptr2);
    double* __restrict__ result = reinterpret_cast<double*>(ptr_result);
    
    #if USE_AVX2
    // Check alignment
    bool aligned = is_aligned(data1, SIMD_ALIGN) && 
                  is_aligned(data2, SIMD_ALIGN) && 
                  is_aligned(result, SIMD_ALIGN);
    
    if (size >= PARALLEL_THRESHOLD) {
        // Parallel execution for large arrays
        #if USE_OPENMP
        #pragma omp parallel for schedule(static) num_threads(omp_get_max_threads())
        #endif
        for (size_t i = 0; i < size; i += 16) {
            // Prefetch next cache lines
            _mm_prefetch(reinterpret_cast<const char*>(data1 + i + 64), _MM_HINT_T0);
            _mm_prefetch(reinterpret_cast<const char*>(data2 + i + 64), _MM_HINT_T0);
            
            if (i + 16 <= size) {
                // Process 16 doubles at once (4x unrolled AVX2)
                if (aligned) {
                    __m256d a0 = _mm256_load_pd(data1 + i);
                    __m256d a1 = _mm256_load_pd(data1 + i + 4);
                    __m256d a2 = _mm256_load_pd(data1 + i + 8);
                    __m256d a3 = _mm256_load_pd(data1 + i + 12);
                    
                    __m256d b0 = _mm256_load_pd(data2 + i);
                    __m256d b1 = _mm256_load_pd(data2 + i + 4);
                    __m256d b2 = _mm256_load_pd(data2 + i + 8);
                    __m256d b3 = _mm256_load_pd(data2 + i + 12);
                    
                    __m256d c0 = _mm256_add_pd(a0, b0);
                    __m256d c1 = _mm256_add_pd(a1, b1);
                    __m256d c2 = _mm256_add_pd(a2, b2);
                    __m256d c3 = _mm256_add_pd(a3, b3);
                    
                    _mm256_store_pd(result + i, c0);
                    _mm256_store_pd(result + i + 4, c1);
                    _mm256_store_pd(result + i + 8, c2);
                    _mm256_store_pd(result + i + 12, c3);
                } else {
                    __m256d a0 = _mm256_loadu_pd(data1 + i);
                    __m256d a1 = _mm256_loadu_pd(data1 + i + 4);
                    __m256d a2 = _mm256_loadu_pd(data1 + i + 8);
                    __m256d a3 = _mm256_loadu_pd(data1 + i + 12);
                    
                    __m256d b0 = _mm256_loadu_pd(data2 + i);
                    __m256d b1 = _mm256_loadu_pd(data2 + i + 4);
                    __m256d b2 = _mm256_loadu_pd(data2 + i + 8);
                    __m256d b3 = _mm256_loadu_pd(data2 + i + 12);
                    
                    __m256d c0 = _mm256_add_pd(a0, b0);
                    __m256d c1 = _mm256_add_pd(a1, b1);
                    __m256d c2 = _mm256_add_pd(a2, b2);
                    __m256d c3 = _mm256_add_pd(a3, b3);
                    
                    _mm256_storeu_pd(result + i, c0);
                    _mm256_storeu_pd(result + i + 4, c1);
                    _mm256_storeu_pd(result + i + 8, c2);
                    _mm256_storeu_pd(result + i + 12, c3);
                }
            } else {
                // Handle remaining elements
                for (size_t j = i; j < size; ++j) {
                    result[j] = data1[j] + data2[j];
                }
            }
        }
    } else {
        // Single-threaded for smaller arrays
        size_t i = 0;
        
        // Main unrolled SIMD loop
        for (; i + 16 <= size; i += 16) {
            // Prefetch
            _mm_prefetch(reinterpret_cast<const char*>(data1 + i + 64), _MM_HINT_T0);
            _mm_prefetch(reinterpret_cast<const char*>(data2 + i + 64), _MM_HINT_T0);
            
            if (aligned) {
                __m256d a0 = _mm256_load_pd(data1 + i);
                __m256d a1 = _mm256_load_pd(data1 + i + 4);
                __m256d a2 = _mm256_load_pd(data1 + i + 8);
                __m256d a3 = _mm256_load_pd(data1 + i + 12);
                
                __m256d b0 = _mm256_load_pd(data2 + i);
                __m256d b1 = _mm256_load_pd(data2 + i + 4);
                __m256d b2 = _mm256_load_pd(data2 + i + 8);
                __m256d b3 = _mm256_load_pd(data2 + i + 12);
                
                _mm256_store_pd(result + i, _mm256_add_pd(a0, b0));
                _mm256_store_pd(result + i + 4, _mm256_add_pd(a1, b1));
                _mm256_store_pd(result + i + 8, _mm256_add_pd(a2, b2));
                _mm256_store_pd(result + i + 12, _mm256_add_pd(a3, b3));
            } else {
                __m256d a0 = _mm256_loadu_pd(data1 + i);
                __m256d a1 = _mm256_loadu_pd(data1 + i + 4);
                __m256d a2 = _mm256_loadu_pd(data1 + i + 8);
                __m256d a3 = _mm256_loadu_pd(data1 + i + 12);
                
                __m256d b0 = _mm256_loadu_pd(data2 + i);
                __m256d b1 = _mm256_loadu_pd(data2 + i + 4);
                __m256d b2 = _mm256_loadu_pd(data2 + i + 8);
                __m256d b3 = _mm256_loadu_pd(data2 + i + 12);
                
                _mm256_storeu_pd(result + i, _mm256_add_pd(a0, b0));
                _mm256_storeu_pd(result + i + 4, _mm256_add_pd(a1, b1));
                _mm256_storeu_pd(result + i + 8, _mm256_add_pd(a2, b2));
                _mm256_storeu_pd(result + i + 12, _mm256_add_pd(a3, b3));
            }
        }
        
        // Process remaining with single SIMD
        for (; i + 4 <= size; i += 4) {
            __m256d a = aligned ? _mm256_load_pd(data1 + i) : _mm256_loadu_pd(data1 + i);
            __m256d b = aligned ? _mm256_load_pd(data2 + i) : _mm256_loadu_pd(data2 + i);
            __m256d c = _mm256_add_pd(a, b);
            if (aligned) {
                _mm256_store_pd(result + i, c);
            } else {
                _mm256_storeu_pd(result + i, c);
            }
        }
        
        // Handle remaining elements
        for (; i < size; ++i) {
            result[i] = data1[i] + data2[i];
        }
    }
    
    #elif USE_NEON
    // ARM NEON implementation with unrolling
    size_t i = 0;
    
    if (size >= PARALLEL_THRESHOLD) {
        #if USE_OPENMP
        #pragma omp parallel for schedule(static)
        #endif
        for (i = 0; i < size - 7; i += 8) {
            float64x2_t a0 = vld1q_f64(data1 + i);
            float64x2_t a1 = vld1q_f64(data1 + i + 2);
            float64x2_t a2 = vld1q_f64(data1 + i + 4);
            float64x2_t a3 = vld1q_f64(data1 + i + 6);
            
            float64x2_t b0 = vld1q_f64(data2 + i);
            float64x2_t b1 = vld1q_f64(data2 + i + 2);
            float64x2_t b2 = vld1q_f64(data2 + i + 4);
            float64x2_t b3 = vld1q_f64(data2 + i + 6);
            
            vst1q_f64(result + i, vaddq_f64(a0, b0));
            vst1q_f64(result + i + 2, vaddq_f64(a1, b1));
            vst1q_f64(result + i + 4, vaddq_f64(a2, b2));
            vst1q_f64(result + i + 6, vaddq_f64(a3, b3));
        }
    } else {
        for (; i + 8 <= size; i += 8) {
            float64x2_t a0 = vld1q_f64(data1 + i);
            float64x2_t a1 = vld1q_f64(data1 + i + 2);
            float64x2_t a2 = vld1q_f64(data1 + i + 4);
            float64x2_t a3 = vld1q_f64(data1 + i + 6);
            
            float64x2_t b0 = vld1q_f64(data2 + i);
            float64x2_t b1 = vld1q_f64(data2 + i + 2);
            float64x2_t b2 = vld1q_f64(data2 + i + 4);
            float64x2_t b3 = vld1q_f64(data2 + i + 6);
            
            vst1q_f64(result + i, vaddq_f64(a0, b0));
            vst1q_f64(result + i + 2, vaddq_f64(a1, b1));
            vst1q_f64(result + i + 4, vaddq_f64(a2, b2));
            vst1q_f64(result + i + 6, vaddq_f64(a3, b3));
        }
    }
    
    // Handle remaining
    for (; i < size; ++i) {
        result[i] = data1[i] + data2[i];
    }
    
    #else
    // Scalar fallback with OpenMP and aggressive unrolling
    if (size >= PARALLEL_THRESHOLD) {
        #if USE_OPENMP
        #pragma omp parallel for schedule(static)
        #endif
        for (size_t i = 0; i < size; ++i) {
            result[i] = data1[i] + data2[i];
        }
    } else {
        size_t i = 0;
        // 8-way unrolling
        for (; i + 8 <= size; i += 8) {
            result[i] = data1[i] + data2[i];
            result[i+1] = data1[i+1] + data2[i+1];
            result[i+2] = data1[i+2] + data2[i+2];
            result[i+3] = data1[i+3] + data2[i+3];
            result[i+4] = data1[i+4] + data2[i+4];
            result[i+5] = data1[i+5] + data2[i+5];
            result[i+6] = data1[i+6] + data2[i+6];
            result[i+7] = data1[i+7] + data2[i+7];
        }
        for (; i < size; ++i) {
            result[i] = data1[i] + data2[i];
        }
    }
    #endif
}

/**
 * Optimized multiplication
 */
void multiply_optimized(uintptr_t ptr1, uintptr_t ptr2, uintptr_t ptr_result, size_t size) {
    double* __restrict__ data1 = reinterpret_cast<double*>(ptr1);
    double* __restrict__ data2 = reinterpret_cast<double*>(ptr2);
    double* __restrict__ result = reinterpret_cast<double*>(ptr_result);
    
    #if USE_AVX2
    bool aligned = is_aligned(data1, SIMD_ALIGN) && 
                  is_aligned(data2, SIMD_ALIGN) && 
                  is_aligned(result, SIMD_ALIGN);
    
    if (size >= PARALLEL_THRESHOLD) {
        #if USE_OPENMP
        #pragma omp parallel for schedule(static)
        #endif
        for (size_t i = 0; i < size; i += 16) {
            _mm_prefetch(reinterpret_cast<const char*>(data1 + i + 64), _MM_HINT_T0);
            _mm_prefetch(reinterpret_cast<const char*>(data2 + i + 64), _MM_HINT_T0);
            
            if (i + 16 <= size) {
                if (aligned) {
                    __m256d a0 = _mm256_load_pd(data1 + i);
                    __m256d a1 = _mm256_load_pd(data1 + i + 4);
                    __m256d a2 = _mm256_load_pd(data1 + i + 8);
                    __m256d a3 = _mm256_load_pd(data1 + i + 12);
                    
                    __m256d b0 = _mm256_load_pd(data2 + i);
                    __m256d b1 = _mm256_load_pd(data2 + i + 4);
                    __m256d b2 = _mm256_load_pd(data2 + i + 8);
                    __m256d b3 = _mm256_load_pd(data2 + i + 12);
                    
                    _mm256_store_pd(result + i, _mm256_mul_pd(a0, b0));
                    _mm256_store_pd(result + i + 4, _mm256_mul_pd(a1, b1));
                    _mm256_store_pd(result + i + 8, _mm256_mul_pd(a2, b2));
                    _mm256_store_pd(result + i + 12, _mm256_mul_pd(a3, b3));
                } else {
                    __m256d a0 = _mm256_loadu_pd(data1 + i);
                    __m256d a1 = _mm256_loadu_pd(data1 + i + 4);
                    __m256d a2 = _mm256_loadu_pd(data1 + i + 8);
                    __m256d a3 = _mm256_loadu_pd(data1 + i + 12);
                    
                    __m256d b0 = _mm256_loadu_pd(data2 + i);
                    __m256d b1 = _mm256_loadu_pd(data2 + i + 4);
                    __m256d b2 = _mm256_loadu_pd(data2 + i + 8);
                    __m256d b3 = _mm256_loadu_pd(data2 + i + 12);
                    
                    _mm256_storeu_pd(result + i, _mm256_mul_pd(a0, b0));
                    _mm256_storeu_pd(result + i + 4, _mm256_mul_pd(a1, b1));
                    _mm256_storeu_pd(result + i + 8, _mm256_mul_pd(a2, b2));
                    _mm256_storeu_pd(result + i + 12, _mm256_mul_pd(a3, b3));
                }
            } else {
                for (size_t j = i; j < size; ++j) {
                    result[j] = data1[j] * data2[j];
                }
            }
        }
    } else {
        size_t i = 0;
        for (; i + 16 <= size; i += 16) {
            _mm_prefetch(reinterpret_cast<const char*>(data1 + i + 64), _MM_HINT_T0);
            _mm_prefetch(reinterpret_cast<const char*>(data2 + i + 64), _MM_HINT_T0);
            
            if (aligned) {
                __m256d a0 = _mm256_load_pd(data1 + i);
                __m256d a1 = _mm256_load_pd(data1 + i + 4);
                __m256d a2 = _mm256_load_pd(data1 + i + 8);
                __m256d a3 = _mm256_load_pd(data1 + i + 12);
                
                __m256d b0 = _mm256_load_pd(data2 + i);
                __m256d b1 = _mm256_load_pd(data2 + i + 4);
                __m256d b2 = _mm256_load_pd(data2 + i + 8);
                __m256d b3 = _mm256_load_pd(data2 + i + 12);
                
                _mm256_store_pd(result + i, _mm256_mul_pd(a0, b0));
                _mm256_store_pd(result + i + 4, _mm256_mul_pd(a1, b1));
                _mm256_store_pd(result + i + 8, _mm256_mul_pd(a2, b2));
                _mm256_store_pd(result + i + 12, _mm256_mul_pd(a3, b3));
            } else {
                __m256d a0 = _mm256_loadu_pd(data1 + i);
                __m256d a1 = _mm256_loadu_pd(data1 + i + 4);
                __m256d a2 = _mm256_loadu_pd(data1 + i + 8);
                __m256d a3 = _mm256_loadu_pd(data1 + i + 12);
                
                __m256d b0 = _mm256_loadu_pd(data2 + i);
                __m256d b1 = _mm256_loadu_pd(data2 + i + 4);
                __m256d b2 = _mm256_loadu_pd(data2 + i + 8);
                __m256d b3 = _mm256_loadu_pd(data2 + i + 12);
                
                _mm256_storeu_pd(result + i, _mm256_mul_pd(a0, b0));
                _mm256_storeu_pd(result + i + 4, _mm256_mul_pd(a1, b1));
                _mm256_storeu_pd(result + i + 8, _mm256_mul_pd(a2, b2));
                _mm256_storeu_pd(result + i + 12, _mm256_mul_pd(a3, b3));
            }
        }
        
        for (; i + 4 <= size; i += 4) {
            __m256d a = aligned ? _mm256_load_pd(data1 + i) : _mm256_loadu_pd(data1 + i);
            __m256d b = aligned ? _mm256_load_pd(data2 + i) : _mm256_loadu_pd(data2 + i);
            __m256d c = _mm256_mul_pd(a, b);
            if (aligned) {
                _mm256_store_pd(result + i, c);
            } else {
                _mm256_storeu_pd(result + i, c);
            }
        }
        
        for (; i < size; ++i) {
            result[i] = data1[i] * data2[i];
        }
    }
    
    #else
    // Scalar with OpenMP
    if (size >= PARALLEL_THRESHOLD) {
        #if USE_OPENMP
        #pragma omp parallel for schedule(static)
        #endif
        for (size_t i = 0; i < size; ++i) {
            result[i] = data1[i] * data2[i];
        }
    } else {
        size_t i = 0;
        for (; i + 8 <= size; i += 8) {
            result[i] = data1[i] * data2[i];
            result[i+1] = data1[i+1] * data2[i+1];
            result[i+2] = data1[i+2] * data2[i+2];
            result[i+3] = data1[i+3] * data2[i+3];
            result[i+4] = data1[i+4] * data2[i+4];
            result[i+5] = data1[i+5] * data2[i+5];
            result[i+6] = data1[i+6] * data2[i+6];
            result[i+7] = data1[i+7] * data2[i+7];
        }
        for (; i < size; ++i) {
            result[i] = data1[i] * data2[i];
        }
    }
    #endif
}

/**
 * Optimized subtraction (similar pattern to addition)
 */
void subtract_optimized(uintptr_t ptr1, uintptr_t ptr2, uintptr_t ptr_result, size_t size) {
    double* __restrict__ data1 = reinterpret_cast<double*>(ptr1);
    double* __restrict__ data2 = reinterpret_cast<double*>(ptr2);
    double* __restrict__ result = reinterpret_cast<double*>(ptr_result);
    
    #if USE_AVX2
    bool aligned = is_aligned(data1, SIMD_ALIGN) && 
                  is_aligned(data2, SIMD_ALIGN) && 
                  is_aligned(result, SIMD_ALIGN);
    
    if (size >= PARALLEL_THRESHOLD) {
        #if USE_OPENMP
        #pragma omp parallel for schedule(static)
        #endif
        for (size_t i = 0; i < size; i += 16) {
            if (i + 16 <= size) {
                if (aligned) {
                    __m256d a0 = _mm256_load_pd(data1 + i);
                    __m256d a1 = _mm256_load_pd(data1 + i + 4);
                    __m256d a2 = _mm256_load_pd(data1 + i + 8);
                    __m256d a3 = _mm256_load_pd(data1 + i + 12);
                    
                    __m256d b0 = _mm256_load_pd(data2 + i);
                    __m256d b1 = _mm256_load_pd(data2 + i + 4);
                    __m256d b2 = _mm256_load_pd(data2 + i + 8);
                    __m256d b3 = _mm256_load_pd(data2 + i + 12);
                    
                    _mm256_store_pd(result + i, _mm256_sub_pd(a0, b0));
                    _mm256_store_pd(result + i + 4, _mm256_sub_pd(a1, b1));
                    _mm256_store_pd(result + i + 8, _mm256_sub_pd(a2, b2));
                    _mm256_store_pd(result + i + 12, _mm256_sub_pd(a3, b3));
                } else {
                    __m256d a0 = _mm256_loadu_pd(data1 + i);
                    __m256d a1 = _mm256_loadu_pd(data1 + i + 4);
                    __m256d a2 = _mm256_loadu_pd(data1 + i + 8);
                    __m256d a3 = _mm256_loadu_pd(data1 + i + 12);
                    
                    __m256d b0 = _mm256_loadu_pd(data2 + i);
                    __m256d b1 = _mm256_loadu_pd(data2 + i + 4);
                    __m256d b2 = _mm256_loadu_pd(data2 + i + 8);
                    __m256d b3 = _mm256_loadu_pd(data2 + i + 12);
                    
                    _mm256_storeu_pd(result + i, _mm256_sub_pd(a0, b0));
                    _mm256_storeu_pd(result + i + 4, _mm256_sub_pd(a1, b1));
                    _mm256_storeu_pd(result + i + 8, _mm256_sub_pd(a2, b2));
                    _mm256_storeu_pd(result + i + 12, _mm256_sub_pd(a3, b3));
                }
            } else {
                for (size_t j = i; j < size; ++j) {
                    result[j] = data1[j] - data2[j];
                }
            }
        }
    } else {
        size_t i = 0;
        for (; i + 16 <= size; i += 16) {
            if (aligned) {
                __m256d a0 = _mm256_load_pd(data1 + i);
                __m256d a1 = _mm256_load_pd(data1 + i + 4);
                __m256d a2 = _mm256_load_pd(data1 + i + 8);
                __m256d a3 = _mm256_load_pd(data1 + i + 12);
                
                __m256d b0 = _mm256_load_pd(data2 + i);
                __m256d b1 = _mm256_load_pd(data2 + i + 4);
                __m256d b2 = _mm256_load_pd(data2 + i + 8);
                __m256d b3 = _mm256_load_pd(data2 + i + 12);
                
                _mm256_store_pd(result + i, _mm256_sub_pd(a0, b0));
                _mm256_store_pd(result + i + 4, _mm256_sub_pd(a1, b1));
                _mm256_store_pd(result + i + 8, _mm256_sub_pd(a2, b2));
                _mm256_store_pd(result + i + 12, _mm256_sub_pd(a3, b3));
            } else {
                __m256d a0 = _mm256_loadu_pd(data1 + i);
                __m256d a1 = _mm256_loadu_pd(data1 + i + 4);
                __m256d a2 = _mm256_loadu_pd(data1 + i + 8);
                __m256d a3 = _mm256_loadu_pd(data1 + i + 12);
                
                __m256d b0 = _mm256_loadu_pd(data2 + i);
                __m256d b1 = _mm256_loadu_pd(data2 + i + 4);
                __m256d b2 = _mm256_loadu_pd(data2 + i + 8);
                __m256d b3 = _mm256_loadu_pd(data2 + i + 12);
                
                _mm256_storeu_pd(result + i, _mm256_sub_pd(a0, b0));
                _mm256_storeu_pd(result + i + 4, _mm256_sub_pd(a1, b1));
                _mm256_storeu_pd(result + i + 8, _mm256_sub_pd(a2, b2));
                _mm256_storeu_pd(result + i + 12, _mm256_sub_pd(a3, b3));
            }
        }
        
        for (; i < size; ++i) {
            result[i] = data1[i] - data2[i];
        }
    }
    #else
    if (size >= PARALLEL_THRESHOLD) {
        #if USE_OPENMP
        #pragma omp parallel for schedule(static)
        #endif
        for (size_t i = 0; i < size; ++i) {
            result[i] = data1[i] - data2[i];
        }
    } else {
        for (size_t i = 0; i < size; ++i) {
            result[i] = data1[i] - data2[i];
        }
    }
    #endif
}

/**
 * Optimized division with reciprocal approximation for speed
 */
void divide_optimized(uintptr_t ptr1, uintptr_t ptr2, uintptr_t ptr_result, size_t size, bool fast_mode = false) {
    double* __restrict__ data1 = reinterpret_cast<double*>(ptr1);
    double* __restrict__ data2 = reinterpret_cast<double*>(ptr2);
    double* __restrict__ result = reinterpret_cast<double*>(ptr_result);
    
    #if USE_AVX2
    if (fast_mode) {
        // Use reciprocal approximation for faster but slightly less accurate results
        if (size >= PARALLEL_THRESHOLD) {
            #if USE_OPENMP
        #pragma omp parallel for schedule(static)
        #endif
            for (size_t i = 0; i < size; i += 4) {
                if (i + 4 <= size) {
                    __m256d b = _mm256_loadu_pd(data2 + i);
                    __m256d a = _mm256_loadu_pd(data1 + i);
                    
                    // Fast reciprocal approximation
                    // Note: _mm256_rcp14_pd is AVX512, use division for AVX2
                    __m256d one = _mm256_set1_pd(1.0);
                    __m256d recip = _mm256_div_pd(one, b);
                    
                    // One Newton-Raphson iteration for better accuracy
                    __m256d two = _mm256_set1_pd(2.0);
                    recip = _mm256_mul_pd(recip, _mm256_fnmadd_pd(b, recip, two));
                    
                    __m256d c = _mm256_mul_pd(a, recip);
                    _mm256_storeu_pd(result + i, c);
                } else {
                    for (size_t j = i; j < size; ++j) {
                        result[j] = data1[j] / data2[j];
                    }
                }
            }
        } else {
            size_t i = 0;
            for (; i + 4 <= size; i += 4) {
                __m256d b = _mm256_loadu_pd(data2 + i);
                __m256d a = _mm256_loadu_pd(data1 + i);
                __m256d one = _mm256_set1_pd(1.0);
                __m256d recip = _mm256_div_pd(one, b);
                __m256d two = _mm256_set1_pd(2.0);
                recip = _mm256_mul_pd(recip, _mm256_fnmadd_pd(b, recip, two));
                __m256d c = _mm256_mul_pd(a, recip);
                _mm256_storeu_pd(result + i, c);
            }
            for (; i < size; ++i) {
                result[i] = data1[i] / data2[i];
            }
        }
    } else {
        // Standard division
        if (size >= PARALLEL_THRESHOLD) {
            #if USE_OPENMP
        #pragma omp parallel for schedule(static)
        #endif
            for (size_t i = 0; i < size; i += 16) {
                if (i + 16 <= size) {
                    __m256d a0 = _mm256_loadu_pd(data1 + i);
                    __m256d a1 = _mm256_loadu_pd(data1 + i + 4);
                    __m256d a2 = _mm256_loadu_pd(data1 + i + 8);
                    __m256d a3 = _mm256_loadu_pd(data1 + i + 12);
                    
                    __m256d b0 = _mm256_loadu_pd(data2 + i);
                    __m256d b1 = _mm256_loadu_pd(data2 + i + 4);
                    __m256d b2 = _mm256_loadu_pd(data2 + i + 8);
                    __m256d b3 = _mm256_loadu_pd(data2 + i + 12);
                    
                    _mm256_storeu_pd(result + i, _mm256_div_pd(a0, b0));
                    _mm256_storeu_pd(result + i + 4, _mm256_div_pd(a1, b1));
                    _mm256_storeu_pd(result + i + 8, _mm256_div_pd(a2, b2));
                    _mm256_storeu_pd(result + i + 12, _mm256_div_pd(a3, b3));
                } else {
                    for (size_t j = i; j < size; ++j) {
                        result[j] = data1[j] / data2[j];
                    }
                }
            }
        } else {
            size_t i = 0;
            for (; i + 4 <= size; i += 4) {
                __m256d a = _mm256_loadu_pd(data1 + i);
                __m256d b = _mm256_loadu_pd(data2 + i);
                __m256d c = _mm256_div_pd(a, b);
                _mm256_storeu_pd(result + i, c);
            }
            for (; i < size; ++i) {
                result[i] = data1[i] / data2[i];
            }
        }
    }
    #else
    if (size >= PARALLEL_THRESHOLD) {
        #if USE_OPENMP
        #pragma omp parallel for schedule(static)
        #endif
        for (size_t i = 0; i < size; ++i) {
            result[i] = data1[i] / data2[i];
        }
    } else {
        for (size_t i = 0; i < size; ++i) {
            result[i] = data1[i] / data2[i];
        }
    }
    #endif
}

/**
 * In-place addition for reduced memory allocation
 */
void add_inplace_optimized(uintptr_t ptr1, uintptr_t ptr2, size_t size) {
    double* __restrict__ data1 = reinterpret_cast<double*>(ptr1);
    double* __restrict__ data2 = reinterpret_cast<double*>(ptr2);
    
    #if USE_AVX2
    if (size >= PARALLEL_THRESHOLD) {
        #if USE_OPENMP
        #pragma omp parallel for schedule(static)
        #endif
        for (size_t i = 0; i < size; i += 16) {
            if (i + 16 <= size) {
                __m256d a0 = _mm256_loadu_pd(data1 + i);
                __m256d a1 = _mm256_loadu_pd(data1 + i + 4);
                __m256d a2 = _mm256_loadu_pd(data1 + i + 8);
                __m256d a3 = _mm256_loadu_pd(data1 + i + 12);
                
                __m256d b0 = _mm256_loadu_pd(data2 + i);
                __m256d b1 = _mm256_loadu_pd(data2 + i + 4);
                __m256d b2 = _mm256_loadu_pd(data2 + i + 8);
                __m256d b3 = _mm256_loadu_pd(data2 + i + 12);
                
                _mm256_storeu_pd(data1 + i, _mm256_add_pd(a0, b0));
                _mm256_storeu_pd(data1 + i + 4, _mm256_add_pd(a1, b1));
                _mm256_storeu_pd(data1 + i + 8, _mm256_add_pd(a2, b2));
                _mm256_storeu_pd(data1 + i + 12, _mm256_add_pd(a3, b3));
            } else {
                for (size_t j = i; j < size; ++j) {
                    data1[j] += data2[j];
                }
            }
        }
    } else {
        size_t i = 0;
        for (; i + 16 <= size; i += 16) {
            __m256d a0 = _mm256_loadu_pd(data1 + i);
            __m256d a1 = _mm256_loadu_pd(data1 + i + 4);
            __m256d a2 = _mm256_loadu_pd(data1 + i + 8);
            __m256d a3 = _mm256_loadu_pd(data1 + i + 12);
            
            __m256d b0 = _mm256_loadu_pd(data2 + i);
            __m256d b1 = _mm256_loadu_pd(data2 + i + 4);
            __m256d b2 = _mm256_loadu_pd(data2 + i + 8);
            __m256d b3 = _mm256_loadu_pd(data2 + i + 12);
            
            _mm256_storeu_pd(data1 + i, _mm256_add_pd(a0, b0));
            _mm256_storeu_pd(data1 + i + 4, _mm256_add_pd(a1, b1));
            _mm256_storeu_pd(data1 + i + 8, _mm256_add_pd(a2, b2));
            _mm256_storeu_pd(data1 + i + 12, _mm256_add_pd(a3, b3));
        }
        for (; i < size; ++i) {
            data1[i] += data2[i];
        }
    }
    #else
    if (size >= PARALLEL_THRESHOLD) {
        #if USE_OPENMP
        #pragma omp parallel for schedule(static)
        #endif
        for (size_t i = 0; i < size; ++i) {
            data1[i] += data2[i];
        }
    } else {
        for (size_t i = 0; i < size; ++i) {
            data1[i] += data2[i];
        }
    }
    #endif
}

PYBIND11_MODULE(array_ops_optimized_cpp, m) {
    m.doc() = "Highly optimized array operations with SIMD, OpenMP, and memory alignment";
    
    m.def("add_optimized", &add_optimized, 
          "Optimized addition with SIMD and parallelization",
          py::arg("ptr1"), py::arg("ptr2"), py::arg("ptr_result"), py::arg("size"));
    
    m.def("subtract_optimized", &subtract_optimized,
          "Optimized subtraction with SIMD and parallelization",
          py::arg("ptr1"), py::arg("ptr2"), py::arg("ptr_result"), py::arg("size"));
    
    m.def("multiply_optimized", &multiply_optimized,
          "Optimized multiplication with SIMD and parallelization",
          py::arg("ptr1"), py::arg("ptr2"), py::arg("ptr_result"), py::arg("size"));
    
    m.def("divide_optimized", &divide_optimized,
          "Optimized division with optional fast mode",
          py::arg("ptr1"), py::arg("ptr2"), py::arg("ptr_result"), py::arg("size"), 
          py::arg("fast_mode") = false);
    
    m.def("add_inplace_optimized", &add_inplace_optimized,
          "In-place addition to reduce memory allocation",
          py::arg("ptr1"), py::arg("ptr2"), py::arg("size"));
}