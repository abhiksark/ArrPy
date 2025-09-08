# cython: language_level=3
"""
Memory pool declarations for Cython modules.
"""

cdef class MemoryBlock:
    cdef:
        double* data
        size_t size
        bint in_use
    
    cdef bint can_fit(self, size_t requested_size)
    cdef double* acquire(self, size_t requested_size)
    cdef void release(self)

cdef class MemoryPool:
    cdef:
        list blocks
        object lock
        size_t total_allocated
        size_t total_in_use
        size_t allocations
        size_t pool_hits
        size_t pool_misses
    
    cdef double* get_memory(self, size_t size)
    cdef void return_memory(self, double* ptr)

cdef class PooledArray:
    cdef:
        double* data
        size_t size
        MemoryPool pool
    
    cdef double get(self, size_t index)
    cdef void set(self, size_t index, double value)

cpdef MemoryPool get_global_pool()