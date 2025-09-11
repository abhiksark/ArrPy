"""
Tests for the data type system.
"""

import pytest
import arrpy as ap


class TestDType:
    """Test data type functionality."""
    
    def test_dtype_creation(self):
        """Test creating data types."""
        assert ap.int32.name == 'int32'
        assert ap.int32.size == 4
        assert ap.int64.name == 'int64'
        assert ap.int64.size == 8
        assert ap.float32.name == 'float32'
        assert ap.float32.size == 4
        assert ap.float64.name == 'float64'
        assert ap.float64.size == 8
    
    def test_dtype_inference(self):
        """Test inferring data type from data."""
        # Test integer inference
        # dtype = ap.infer_dtype([1, 2, 3])
        # assert dtype == ap.int64
        
        # Test float inference
        # dtype = ap.infer_dtype([1.0, 2.0, 3.0])
        # assert dtype == ap.float64
        
        # Test mixed inference (should promote to float)
        # dtype = ap.infer_dtype([1, 2.0, 3])
        # assert dtype == ap.float64
        pass  # TODO: Implement when infer_dtype is functional
    
    def test_dtype_conversion(self):
        """Test converting between data types."""
        # arr = ap.array([1, 2, 3], dtype=ap.int32)
        # assert arr.dtype == ap.int32
        
        # converted = arr.astype(ap.float64)
        # assert converted.dtype == ap.float64
        pass  # TODO: Implement when dtype conversion is functional
    
    def test_dtype_promotion(self):
        """Test automatic type promotion in operations."""
        # int_arr = ap.array([1, 2, 3], dtype=ap.int32)
        # float_arr = ap.array([1.5, 2.5, 3.5], dtype=ap.float32)
        
        # result = int_arr + float_arr
        # assert result.dtype == ap.float32
        pass  # TODO: Implement when operations are functional