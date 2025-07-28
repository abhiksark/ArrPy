#!/usr/bin/env python3
"""
ArrPy Benchmark Runner for ML Environment

This script automatically sets up the environment and runs benchmarks
in the conda ml environment with proper matplotlib support.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_ml_environment():
    """Check if we're running in the ml conda environment"""
    conda_env = os.environ.get('CONDA_DEFAULT_ENV', '')
    python_version = sys.version_info
    
    print("🔍 Environment Check:")
    print(f"   Python: {python_version.major}.{python_version.minor}.{python_version.micro}")
    print(f"   Conda Environment: {conda_env or 'None'}")
    
    if conda_env != 'ml':
        print("\n⚠️  Warning: Not running in 'ml' conda environment")
        print("For best results, activate the ml environment first:")
        print("   source /opt/miniconda3/bin/activate ml")
        print("   python run_benchmarks_ml.py")
        print("\nContinuing with current environment...")
    else:
        print("✅ Running in ml conda environment")
    
    return conda_env == 'ml'

def check_dependencies():
    """Check if required dependencies are available"""
    print("\n📦 Checking Dependencies:")
    
    required_packages = {
        'numpy': 'NumPy',
        'matplotlib': 'Matplotlib', 
        'arrpy': 'ArrPy'
    }
    
    missing_packages = []
    
    for package, name in required_packages.items():
        try:
            if package == 'arrpy':
                # Add current directory to path for arrpy import
                current_dir = Path(__file__).parent
                if str(current_dir) not in sys.path:
                    sys.path.insert(0, str(current_dir))
            
            module = __import__(package)
            version = getattr(module, '__version__', 'unknown')
            print(f"   ✅ {name}: {version}")
        except ImportError:
            print(f"   ❌ {name}: not found")
            missing_packages.append(name)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        return False
    
    print("✅ All dependencies found")
    return True

def run_benchmark(script_name, description):
    """Run a specific benchmark script"""
    print(f"\n🚀 Running {description}")
    print("=" * 60)
    
    script_path = Path("benchmarks") / script_name
    
    if not script_path.exists():
        print(f"❌ Script not found: {script_path}")
        return False
    
    try:
        # Change to benchmarks directory and run script
        original_cwd = os.getcwd()
        os.chdir("benchmarks")
        
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=False, text=True)
        
        os.chdir(original_cwd)
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed with return code {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        os.chdir(original_cwd)
        return False

def main():
    """Main benchmark runner"""
    print("🧮 ArrPy Benchmark Suite - ML Environment")
    print("=" * 50)
    
    # Check environment
    in_ml_env = check_ml_environment()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependency check failed. Please install missing packages.")
        sys.exit(1)
    
    # Test basic ArrPy functionality
    print("\n🧪 Testing ArrPy Basic Functionality:")
    try:
        import arrpy as ap
        test_array = ap.Array([1, 2, 3, 4, 5])
        result = test_array.sum()
        print(f"   ✅ Array sum test: {result}")
        
        # Test new functions
        zeros_array = ap.zeros(3)
        print(f"   ✅ zeros(3): {zeros_array}")
        
        math_result = ap.sqrt(ap.Array([1, 4, 9]))
        print(f"   ✅ sqrt([1,4,9]): {math_result}")
        
    except Exception as e:
        print(f"   ❌ Basic functionality test failed: {e}")
        sys.exit(1)
    
    # Available benchmarks
    benchmarks = [
        ("scalability_test_clean.py", "Clean Scalability Test (Fast)"),
        ("performance_comparison.py", "Performance Comparison"),
    ]
    
    # Check which benchmarks are available
    available_benchmarks = []
    for script, desc in benchmarks:
        if (Path("benchmarks") / script).exists():
            available_benchmarks.append((script, desc))
    
    if not available_benchmarks:
        print("❌ No benchmark scripts found in benchmarks/ directory")
        sys.exit(1)
    
    print(f"\n📊 Found {len(available_benchmarks)} benchmark(s)")
    
    # Run benchmarks
    results = {}
    for script, description in available_benchmarks:
        success = run_benchmark(script, description)
        results[description] = success
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 BENCHMARK SUMMARY")
    print("=" * 60)
    
    for description, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"   {description}: {status}")
    
    successful_benchmarks = sum(1 for success in results.values() if success)
    total_benchmarks = len(results)
    
    print(f"\nResults: {successful_benchmarks}/{total_benchmarks} benchmarks completed successfully")
    
    if in_ml_env and successful_benchmarks == total_benchmarks:
        print("\n🎉 All benchmarks completed successfully in ML environment!")
        print("📊 Check for generated plots and reports in the benchmarks/ directory")
    
    # Additional recommendations
    print("\n💡 Next Steps:")
    print("   • Check benchmarks/ directory for generated plots")
    print("   • Review performance results for optimization opportunities")
    print("   • Run tests with: python -m pytest tests/ -v")

if __name__ == "__main__":
    main()