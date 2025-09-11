import pytest

# Method 1: Skip a test entirely
@pytest.mark.skip(reason="Not implemented yet")
def test_not_implemented_feature():
    raise NotImplementedError("This feature is not ready")

# Method 2: Skip conditionally
@pytest.mark.skipif(True, reason="Backend doesn't support this")
def test_conditional_skip():
    raise NotImplementedError("Backend missing")

# Method 3: Expected failure (xfail)
@pytest.mark.xfail(raises=NotImplementedError, reason="Known limitation")
def test_expected_failure():
    raise NotImplementedError("This is expected to fail")

# Method 4: Skip inside the test
def test_skip_inside():
    try:
        # Try the operation
        raise NotImplementedError("Feature missing")
    except NotImplementedError:
        pytest.skip("Feature not implemented yet")

# Method 5: xfail with strict=False (won't fail the test suite)
@pytest.mark.xfail(strict=False, reason="Work in progress")
def test_work_in_progress():
    raise NotImplementedError("WIP")
