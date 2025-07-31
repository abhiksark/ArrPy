#include "c_array.h"
#include <immintrin.h>  // For SIMD intrinsics
#include <omp.h>        // For OpenMP parallelization

// SIMD-optimized element-wise operations

// Vectorized addition using AVX2
void simd_add_scalar(double* result, const double* data, double scalar, Py_ssize_t size) {
    Py_ssize_t i = 0;
    
    #ifdef __AVX2__
    __m256d scalar_vec = _mm256_set1_pd(scalar);
    
    // Process 4 doubles at a time with AVX2
    for (; i + 3 < size; i += 4) {
        __m256d data_vec = _mm256_loadu_pd(&data[i]);
        __m256d result_vec = _mm256_add_pd(data_vec, scalar_vec);
        _mm256_storeu_pd(&result[i], result_vec);
    }
    #endif
    
    // Handle remaining elements
    for (; i < size; i++) {
        result[i] = data[i] + scalar;
    }
}

// Vectorized multiplication using AVX2
void simd_multiply_scalar(double* result, const double* data, double scalar, Py_ssize_t size) {
    Py_ssize_t i = 0;
    
    #ifdef __AVX2__
    __m256d scalar_vec = _mm256_set1_pd(scalar);
    
    // Process 4 doubles at a time with AVX2
    for (; i + 3 < size; i += 4) {
        __m256d data_vec = _mm256_loadu_pd(&data[i]);
        __m256d result_vec = _mm256_mul_pd(data_vec, scalar_vec);
        _mm256_storeu_pd(&result[i], result_vec);
    }
    #endif
    
    // Handle remaining elements
    for (; i < size; i++) {
        result[i] = data[i] * scalar;
    }
}

// Parallel reduction for sum using OpenMP
double parallel_sum(const double* data, Py_ssize_t size) {
    double sum = 0.0;
    
    #pragma omp parallel for reduction(+:sum)
    for (Py_ssize_t i = 0; i < size; i++) {
        sum += data[i];
    }
    
    return sum;
}

// Parallel reduction for max using OpenMP
double parallel_max(const double* data, Py_ssize_t size) {
    if (size == 0) return 0.0;
    
    double max_val = data[0];
    
    #pragma omp parallel for reduction(max:max_val)
    for (Py_ssize_t i = 1; i < size; i++) {
        if (data[i] > max_val) {
            max_val = data[i];
        }
    }
    
    return max_val;
}

// Parallel reduction for min using OpenMP
double parallel_min(const double* data, Py_ssize_t size) {
    if (size == 0) return 0.0;
    
    double min_val = data[0];
    
    #pragma omp parallel for reduction(min:min_val)
    for (Py_ssize_t i = 1; i < size; i++) {
        if (data[i] < min_val) {
            min_val = data[i];
        }
    }
    
    return min_val;
}

// Cache-friendly matrix multiplication
void optimized_matmul(double* result, const double* a, const double* b,
                     Py_ssize_t m, Py_ssize_t n, Py_ssize_t k) {
    // Use blocking for cache efficiency
    const Py_ssize_t BLOCK_SIZE = 64;
    
    // Initialize result to zero
    #pragma omp parallel for
    for (Py_ssize_t i = 0; i < m * n; i++) {
        result[i] = 0.0;
    }
    
    // Blocked matrix multiplication with OpenMP
    #pragma omp parallel for collapse(2)
    for (Py_ssize_t i0 = 0; i0 < m; i0 += BLOCK_SIZE) {
        for (Py_ssize_t j0 = 0; j0 < n; j0 += BLOCK_SIZE) {
            for (Py_ssize_t k0 = 0; k0 < k; k0 += BLOCK_SIZE) {
                // Mini block multiplication
                Py_ssize_t i_max = (i0 + BLOCK_SIZE < m) ? i0 + BLOCK_SIZE : m;
                Py_ssize_t j_max = (j0 + BLOCK_SIZE < n) ? j0 + BLOCK_SIZE : n;
                Py_ssize_t k_max = (k0 + BLOCK_SIZE < k) ? k0 + BLOCK_SIZE : k;
                
                for (Py_ssize_t i = i0; i < i_max; i++) {
                    for (Py_ssize_t j = j0; j < j_max; j++) {
                        double sum = 0.0;
                        for (Py_ssize_t l = k0; l < k_max; l++) {
                            sum += a[i * k + l] * b[l * n + j];
                        }
                        result[i * n + j] += sum;
                    }
                }
            }
        }
    }
}

// Fast array creation with memset
void fast_zeros(double* data, Py_ssize_t size) {
    memset(data, 0, size * sizeof(double));
}

void fast_ones(double* data, Py_ssize_t size) {
    #pragma omp parallel for
    for (Py_ssize_t i = 0; i < size; i++) {
        data[i] = 1.0;
    }
}

void fast_full(double* data, Py_ssize_t size, double value) {
    #pragma omp parallel for
    for (Py_ssize_t i = 0; i < size; i++) {
        data[i] = value;
    }
}

// Optimized arange implementation
void fast_arange(double* data, double start, double stop, double step) {
    Py_ssize_t size = (Py_ssize_t)((stop - start) / step);
    
    #pragma omp parallel for
    for (Py_ssize_t i = 0; i < size; i++) {
        data[i] = start + i * step;
    }
}

// Element-wise mathematical operations with SIMD
void simd_sqrt(double* result, const double* data, Py_ssize_t size) {
    Py_ssize_t i = 0;
    
    #ifdef __AVX2__
    // Process 4 doubles at a time with AVX2
    for (; i + 3 < size; i += 4) {
        __m256d data_vec = _mm256_loadu_pd(&data[i]);
        __m256d result_vec = _mm256_sqrt_pd(data_vec);
        _mm256_storeu_pd(&result[i], result_vec);
    }
    #endif
    
    // Handle remaining elements
    for (; i < size; i++) {
        result[i] = sqrt(data[i]);
    }
}

// Optimized standard deviation calculation
double optimized_std(const double* data, Py_ssize_t size, int ddof) {
    if (size <= ddof) return 0.0;
    
    // Calculate mean in parallel
    double mean = parallel_sum(data, size) / (double)size;
    
    // Calculate variance in parallel
    double variance = 0.0;
    #pragma omp parallel for reduction(+:variance)
    for (Py_ssize_t i = 0; i < size; i++) {
        double diff = data[i] - mean;
        variance += diff * diff;
    }
    
    variance /= (double)(size - ddof);
    return sqrt(variance);
}