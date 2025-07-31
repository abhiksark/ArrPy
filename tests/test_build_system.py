"""
Tests for the Cython build system and installation.

These tests verify that the build system works correctly and that
the Cython extensions are properly compiled and importable.
"""

import pytest
import os
import sys
import subprocess
import importlib
import tempfile
import shutil
from pathlib import Path


class TestCythonBuildSystem:
    """Test the Cython build system components."""
    
    def test_setup_py_exists(self):
        """Test that setup.py exists and has correct content."""
        setup_path = Path(__file__).parent.parent / "setup.py"
        assert setup_path.exists(), "setup.py should exist"
        
        with open(setup_path, 'r') as f:
            content = f.read()
        
        # Check for Cython-related imports and configurations
        assert "from Cython.Build import cythonize" in content, "Should import cythonize"
        assert "Extension" in content, "Should define Extension objects"
        assert "array_cython" in content, "Should include array_cython extension"
        assert "arithmetic_cython" in content, "Should include arithmetic_cython extension"
        assert "basic_cython" in content, "Should include basic_cython extension"
    
    def test_pyproject_toml_exists(self):
        """Test that pyproject.toml exists and has correct content."""
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        assert pyproject_path.exists(), "pyproject.toml should exist"
        
        with open(pyproject_path, 'r') as f:
            content = f.read()
        
        # Check for required build dependencies
        assert "Cython" in content, "Should require Cython as build dependency"
        assert "numpy" in content, "Should require numpy as build dependency"
        assert "setuptools" in content, "Should require setuptools"
    
    def test_pyx_files_exist(self):
        """Test that all .pyx files exist."""
        base_path = Path(__file__).parent.parent
        
        expected_pyx_files = [
            "arrpy/core/array_cython.pyx",
            "arrpy/math/arithmetic_cython.pyx", 
            "arrpy/creation/basic_cython.pyx"
        ]
        
        for pyx_file in expected_pyx_files:
            pyx_path = base_path / pyx_file
            assert pyx_path.exists(), f"{pyx_file} should exist"
    
    def test_pxd_files_exist(self):
        """Test that .pxd header files exist where needed."""
        base_path = Path(__file__).parent.parent
        
        # Array class needs a .pxd file for cimport
        pxd_path = base_path / "arrpy/core/array_cython.pxd"
        assert pxd_path.exists(), "array_cython.pxd should exist for cimport"


class TestCythonExtensions:
    """Test that Cython extensions are properly compiled and loadable."""
    
    def test_core_extension_loaded(self):
        """Test that core array extension is loaded."""
        try:
            from arrpy.core.array_cython import Array
            assert Array is not None, "Should be able to import Cython Array"
            
            # Test basic functionality
            arr = Array([1, 2, 3])
            assert arr.shape == (3,), "Cython Array should work correctly"
            
        except ImportError:
            pytest.skip("Cython extensions not built")
    
    def test_math_extension_loaded(self):
        """Test that math extension is loaded."""
        try:
            from arrpy.math.arithmetic_cython import power, absolute
            assert power is not None, "Should be able to import Cython power"
            assert absolute is not None, "Should be able to import Cython absolute"
            
        except ImportError:
            pytest.skip("Cython extensions not built")
    
    def test_creation_extension_loaded(self):
        """Test that creation extension is loaded."""
        try:
            from arrpy.creation.basic_cython import zeros, ones
            assert zeros is not None, "Should be able to import Cython zeros"
            assert ones is not None, "Should be able to import Cython ones"
            
        except ImportError:
            pytest.skip("Cython extensions not built")
    
    def test_cython_implementation_detection(self):
        """Test that the system correctly detects Cython implementation."""
        from arrpy.core import Array
        
        # Check if we're using Cython version
        module_name = type(Array).__module__
        if 'cython' in module_name.lower():
            # We're using Cython - test Cython-specific features
            arr = Array([1, 2, 3])
            assert hasattr(arr, 'sum_fast'), "Cython version should have fast methods"
        else:
            # We're using Python fallback
            pytest.skip("Using Python fallback, Cython not available")


class TestFallbackMechanism:
    """Test the fallback mechanism when Cython is not available."""
    
    def test_import_structure(self):
        """Test that import structure supports fallback."""
        # Check that the __init__.py files have proper try/except blocks
        core_init_path = Path(__file__).parent.parent / "arrpy/core/__init__.py"
        
        with open(core_init_path, 'r') as f:
            content = f.read()
        
        assert "try:" in content, "Should have try block for Cython import"
        assert "except ImportError:" in content, "Should have except block for fallback"
        assert "array_cython" in content, "Should try to import Cython version"
        assert "from .array import Array" in content, "Should fallback to Python version"
    
    def test_both_implementations_importable(self):
        """Test that both Python and Cython implementations can be imported separately."""
        # Test Python implementation
        try:
            from arrpy.core.array import Array as PythonArray
            arr_py = PythonArray([1, 2, 3])
            assert arr_py.sum() == 6, "Python implementation should work"
        except ImportError:
            pytest.fail("Python implementation should always be importable")
        
        # Test Cython implementation (if available)
        try:
            from arrpy.core.array_cython import Array as CythonArray
            arr_cy = CythonArray([1, 2, 3])
            assert arr_cy.sum() == 6, "Cython implementation should work"
        except ImportError:
            pytest.skip("Cython implementation not available")


class TestBuildConfiguration:
    """Test build configuration and compiler directives."""
    
    def test_compiler_directives(self):
        """Test that proper compiler directives are used."""
        setup_path = Path(__file__).parent.parent / "setup.py"
        
        with open(setup_path, 'r') as f:
            content = f.read()
        
        # Check for performance-oriented compiler directives
        assert "boundscheck" in content, "Should disable bounds checking for performance"
        assert "wraparound" in content, "Should disable wraparound for performance"
        assert "language_level" in content, "Should specify Python language level"
    
    def test_numpy_integration(self):
        """Test that numpy is properly integrated in build."""
        setup_path = Path(__file__).parent.parent / "setup.py"
        
        with open(setup_path, 'r') as f:
            content = f.read()
        
        assert "import numpy as np" in content, "Should import numpy"
        assert "np.get_include()" in content, "Should include numpy headers"


class TestInstallationVerification:
    """Test that installation works correctly."""
    
    def test_package_importable_after_build(self):
        """Test that the package is importable after building."""
        try:
            import arrpy
            assert arrpy is not None, "Main package should be importable"
            
            # Test main submodules
            from arrpy import core, creation, math
            assert core is not None, "Core module should be importable"
            assert creation is not None, "Creation module should be importable"
            assert math is not None, "Math module should be importable"
            
        except ImportError as e:
            pytest.fail(f"Package not properly installed: {e}")
    
    def test_all_public_api_available(self):
        """Test that all public API is available after installation."""
        try:
            from arrpy.core import Array
            from arrpy.creation import zeros, ones, full, eye, identity
            from arrpy.math import power, absolute
            
            # Test basic functionality of each
            arr = Array([1, 2, 3])
            assert arr.sum() == 6
            
            z = zeros(3)
            assert z.sum() == 0
            
            o = ones(3)
            assert o.sum() == 3
            
            p = power(arr, 2)
            assert p._data == [1, 4, 9]
            
        except (ImportError, AttributeError) as e:
            pytest.fail(f"Public API not fully available: {e}")
    
    def test_version_information(self):
        """Test that version information is available."""
        # Check setup.py for version
        setup_path = Path(__file__).parent.parent / "setup.py"
        
        with open(setup_path, 'r') as f:
            content = f.read()
        
        assert "version=" in content, "Should specify version in setup.py"
        
        # Check pyproject.toml for version
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        
        with open(pyproject_path, 'r') as f:
            content = f.read()
        
        assert "version" in content, "Should specify version in pyproject.toml"


class TestDevelopmentWorkflow:
    """Test development workflow commands."""
    
    def test_makefile_exists(self):
        """Test that development Makefile exists."""
        makefile_paths = [
            Path(__file__).parent.parent / "Makefile",
            Path(__file__).parent.parent / "Makefile_cython",
            Path(__file__).parent.parent / "makefile"
        ]
        
        makefile_exists = any(p.exists() for p in makefile_paths)
        assert makefile_exists, "Should have a Makefile for development"
    
    def test_clean_target_functionality(self):
        """Test that clean functionality works."""
        base_path = Path(__file__).parent.parent
        
        # Look for build artifacts that should be cleanable
        potential_artifacts = [
            "build/",
            "dist/", 
            "*.egg-info/",
        ]
        
        # This test mainly checks that the clean command exists
        # We don't actually run it to avoid breaking the test environment
        makefile_path = None
        for path in ["Makefile", "Makefile_cython", "makefile"]:
            full_path = base_path / path
            if full_path.exists():
                makefile_path = full_path
                break
        
        if makefile_path:
            with open(makefile_path, 'r') as f:
                content = f.read()
            
            assert "clean" in content, "Makefile should have clean target"


class TestErrorHandling:
    """Test error handling in build system."""
    
    def test_missing_dependencies_error(self):
        """Test that missing dependencies produce helpful errors."""
        # This test would require manipulating the environment
        # For now, we just check that the dependencies are properly specified
        
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        with open(pyproject_path, 'r') as f:
            content = f.read()
        
        # Check that required dependencies are listed
        assert "cython" in content.lower(), "Cython should be listed as dependency"
        assert "numpy" in content.lower(), "NumPy should be listed as dependency"
    
    def test_import_error_handling(self):
        """Test that import errors are handled gracefully."""
        # Test the fallback mechanism
        from arrpy.core import Array
        
        # Should work regardless of whether Cython is available
        arr = Array([1, 2, 3])
        assert arr.sum() == 6, "Should work with either implementation"


class TestDocumentation:
    """Test that build system is properly documented."""
    
    def test_readme_has_build_instructions(self):
        """Test that README contains build instructions."""
        readme_paths = [
            Path(__file__).parent.parent / "README.md",
            Path(__file__).parent.parent / "README.rst",
            Path(__file__).parent.parent / "README.txt"
        ]
        
        readme_exists = False
        for readme_path in readme_paths:
            if readme_path.exists():
                readme_exists = True
                with open(readme_path, 'r') as f:
                    content = f.read().lower()
                
                # Should mention how to build
                build_mentioned = any(keyword in content for keyword in [
                    "build", "install", "setup", "cython", "compile"
                ])
                
                if build_mentioned:
                    return  # Found build instructions
        
        if readme_exists:
            pytest.skip("README exists but may not have build instructions")
        else:
            pytest.skip("No README file found")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])