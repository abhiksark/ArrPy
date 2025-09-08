# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: nonecheck=False

"""
Memory pool manager for Cython operations.
Reduces allocation overhead by reusing memory blocks.
"""

import cython
from libc.stdlib cimport malloc, free, realloc
from libc.string cimport memset
from cpython.mem cimport PyMem_Malloc, PyMem_Free
from threading import Lock

# Memory pool configuration
DEF POOL_SIZE = 32  # Number of blocks in pool
DEF MIN_BLOCK_SIZE = 1024  # Minimum block size (8KB for 1024 doubles)
DEF MAX_BLOCK_SIZE = 1048576  # Maximum block size (8MB for 1M doubles)

cdef class MemoryBlock:
    """A single memory block in the pool."""
    
    def __cinit__(self, size_t size):
        self.size = size
        self.data = <double*>malloc(size * sizeof(double))
        if not self.data:
            raise MemoryError(f"Failed to allocate {size * sizeof(double)} bytes")
        self.in_use = False
    
    def __dealloc__(self):
        if self.data:
            free(self.data)
            self.data = NULL
    
    cdef bint can_fit(self, size_t requested_size):
        """Check if this block can fit the requested size."""
        return not self.in_use and self.size >= requested_size
    
    cdef double* acquire(self, size_t requested_size):
        """Acquire this block for use."""
        if self.can_fit(requested_size):
            self.in_use = True
            return self.data
        return NULL
    
    cdef void release(self):
        """Release this block back to the pool."""
        self.in_use = False
        # Optionally clear memory for security
        # memset(self.data, 0, self.size * sizeof(double))

cdef class MemoryPool:
    """Thread-safe memory pool for Cython operations."""
    
    def __cinit__(self):
        self.blocks = []
        self.lock = Lock()
        self.total_allocated = 0
        self.total_in_use = 0
        self.allocations = 0
        self.pool_hits = 0
        self.pool_misses = 0
        
        # Pre-allocate some common sizes
        common_sizes = [1024, 4096, 16384, 65536]
        for size in common_sizes:
            for _ in range(2):  # 2 blocks of each size
                block = MemoryBlock(size)
                self.blocks.append(block)
                self.total_allocated += size * sizeof(double)
    
    cdef double* get_memory(self, size_t size):
        """Get a memory block of at least the specified size."""
        cdef MemoryBlock block
        cdef double* ptr = NULL
        cdef size_t block_size
        
        with self.lock:
            self.allocations += 1
            
            # First, try to find a suitable block in the pool
            for block in self.blocks:
                ptr = block.acquire(size)
                if ptr:
                    self.pool_hits += 1
                    self.total_in_use += block.size * sizeof(double)
                    return ptr
            
            # No suitable block found, allocate a new one
            self.pool_misses += 1
            
            # Determine block size (round up to power of 2)
            block_size = MIN_BLOCK_SIZE
            while block_size < size and block_size < MAX_BLOCK_SIZE:
                block_size *= 2
            
            if block_size < size:
                block_size = size  # For very large arrays
            
            # Create new block and add to pool if within limits
            if len(self.blocks) < POOL_SIZE:
                block = MemoryBlock(block_size)
                self.blocks.append(block)
                self.total_allocated += block_size * sizeof(double)
                ptr = block.acquire(size)
                self.total_in_use += block.size * sizeof(double)
                return ptr
            else:
                # Pool is full, do direct allocation (not pooled)
                return <double*>malloc(size * sizeof(double))
    
    cdef void return_memory(self, double* ptr):
        """Return a memory block to the pool."""
        cdef MemoryBlock block
        
        if not ptr:
            return
        
        with self.lock:
            # Find the block that owns this pointer
            for block in self.blocks:
                if block.data == ptr:
                    self.total_in_use -= block.size * sizeof(double)
                    block.release()
                    return
            
            # Not a pooled block, free directly
            free(ptr)
    
    def get_stats(self):
        """Get pool statistics."""
        cdef MemoryBlock block
        cdef int in_use_blocks = 0
        
        with self.lock:
            for block in self.blocks:
                if block.in_use:
                    in_use_blocks += 1
            return {
                'total_blocks': len(self.blocks),
                'blocks_in_use': in_use_blocks,
                'total_allocated_mb': self.total_allocated / (1024 * 1024),
                'total_in_use_mb': self.total_in_use / (1024 * 1024),
                'allocations': self.allocations,
                'pool_hits': self.pool_hits,
                'pool_misses': self.pool_misses,
                'hit_rate': self.pool_hits / max(1, self.allocations)
            }
    
    def clear(self):
        """Clear all unused blocks from the pool."""
        cdef MemoryBlock block
        with self.lock:
            # Keep only blocks that are in use
            new_blocks = []
            for block in self.blocks:
                if block.in_use:
                    new_blocks.append(block)
                else:
                    self.total_allocated -= block.size * sizeof(double)
            self.blocks = new_blocks

# Global memory pool instance
cdef MemoryPool _global_pool = None

cpdef MemoryPool get_global_pool():
    """Get the global memory pool instance."""
    global _global_pool
    if _global_pool is None:
        _global_pool = MemoryPool()
    return _global_pool

@cython.boundscheck(False)
@cython.wraparound(False)
cdef class PooledArray:
    """Array wrapper that uses pooled memory."""
    
    def __cinit__(self, size_t size):
        self.size = size
        self.pool = get_global_pool()
        self.data = self.pool.get_memory(size)
        if not self.data:
            raise MemoryError(f"Failed to allocate {size} doubles from pool")
    
    def __dealloc__(self):
        if self.data:
            self.pool.return_memory(self.data)
            self.data = NULL
    
    cdef double get(self, size_t index):
        """Get value at index."""
        if index >= self.size:
            raise IndexError(f"Index {index} out of bounds for size {self.size}")
        return self.data[index]
    
    cdef void set(self, size_t index, double value):
        """Set value at index."""
        if index >= self.size:
            raise IndexError(f"Index {index} out of bounds for size {self.size}")
        self.data[index] = value
    
    def to_list(self):
        """Convert to Python list."""
        result = []
        for i in range(self.size):
            result.append(self.data[i])
        return result

# Optimized operations using pooled memory
@cython.boundscheck(False)
@cython.wraparound(False)
def pooled_add(list data1, list data2, tuple shape1, tuple shape2):
    """Addition using pooled memory."""
    cdef int i
    cdef int n = len(data1)
    cdef PooledArray result = PooledArray(n)
    
    # Perform addition
    for i in range(n):
        result.data[i] = float(data1[i]) + float(data2[i])
    
    # Convert to list (data stays in pool until next allocation)
    return result.to_list(), shape1

@cython.boundscheck(False)
@cython.wraparound(False)
def pooled_multiply(list data1, list data2, tuple shape1, tuple shape2):
    """Multiplication using pooled memory."""
    cdef int i
    cdef int n = len(data1)
    cdef PooledArray result = PooledArray(n)
    
    # Perform multiplication
    for i in range(n):
        result.data[i] = float(data1[i]) * float(data2[i])
    
    return result.to_list(), shape1

# Memory pool management functions
def reset_pool():
    """Reset the global memory pool."""
    global _global_pool
    if _global_pool is not None:
        _global_pool.clear()

def get_pool_stats():
    """Get statistics from the global memory pool."""
    pool = get_global_pool()
    return pool.get_stats()