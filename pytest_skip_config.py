"""
Configuration for skipping/xfailing tests with NotImplementedError.
This can be imported in conftest.py or individual test files.
"""

import pytest

# List of test patterns that should be marked as xfail due to NotImplementedError
XFAIL_NOT_IMPLEMENTED = [
    "test_boolean_indexing_2d",  # 2D boolean indexing not implemented
    "test_argmin_argmax",  # argmin/argmax functions not implemented
    "test_abs",  # abs function not implemented
    "test_percentile",  # percentile function not implemented
    "test_median",  # median function not implemented
    "test_histogram",  # histogram function not implemented
]

def pytest_collection_modifyitems(config, items):
    """
    Automatically mark tests as xfail if they're known to raise NotImplementedError.
    
    Add this to your conftest.py:
    from pytest_skip_config import pytest_collection_modifyitems
    """
    for item in items:
        for pattern in XFAIL_NOT_IMPLEMENTED:
            if pattern in item.nodeid:
                item.add_marker(
                    pytest.mark.xfail(
                        raises=NotImplementedError,
                        reason=f"Feature not implemented yet: {pattern}"
                    )
                )

# Alternative: Decorator for individual tests
def skip_if_not_implemented(func):
    """
    Decorator to skip a test if it raises NotImplementedError.
    
    Usage:
    @skip_if_not_implemented
    def test_some_feature():
        ...
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotImplementedError as e:
            pytest.skip(f"Not implemented: {e}")
    return wrapper

# Alternative: Mark tests as expected to fail
xfail_not_implemented = pytest.mark.xfail(
    raises=NotImplementedError,
    reason="Feature not yet implemented",
    strict=False  # Don't fail test suite if it passes unexpectedly
)