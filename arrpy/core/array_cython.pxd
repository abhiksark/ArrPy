# cython: language_level=3
"""
Cython header file for Array class declarations.
"""

cdef class Array:
    cdef public tuple _shape
    cdef public list _data
    cdef public object _parent
    cdef public long _parent_offset
    
    cdef tuple _get_shape(self, data)
    cdef list _flatten(self, data)
    cdef object _get_single_element(self, tuple key)
    cdef Array _get_subarray_tuple(self, tuple key)
    cdef object _get_1d_element(self, long key)
    cdef Array _get_subarray_single(self, long key)
    cdef list _check_compatible_shape(self, other)
    cdef Array _create_result_array(self, list result_data)