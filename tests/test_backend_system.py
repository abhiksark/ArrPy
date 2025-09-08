#!/usr/bin/env python3
"""
Test script demonstrating the ArrPy backend system.
"""

import time
import arrpy


def main():
    print("=" * 70)
    print("ArrPy Backend System Demo")
    print("=" * 70)
    
    # Show backend status
    print("\n1. Backend Implementation Status:")
    print("-" * 40)
    arrpy.show_backend_status()
    
    # Create test arrays
    print("\n2. Creating test arrays...")
    a = arrpy.array([[1, 2, 3], [4, 5, 6]])
    b = arrpy.array([[7, 8, 9], [10, 11, 12]])
    
    print(f"Array a:\n{a}")
    print(f"Array b:\n{b}")
    
    # Test operations with different backends
    print("\n3. Testing operations with different backends:")
    print("-" * 40)
    
    operations = [
        ("Addition (a + b)", lambda: a + b),
        ("Subtraction (a - b)", lambda: a - b),
        ("Multiplication (a * 2)", lambda: a * 2),
        ("Sum reduction", lambda: a.sum()),
    ]
    
    for backend in [arrpy.Backend.PYTHON, arrpy.Backend.CYTHON, arrpy.Backend.C]:
        print(f"\n{backend.value.upper()} Backend:")
        arrpy.set_backend(backend)
        
        for op_name, op_func in operations:
            try:
                start = time.perf_counter()
                result = op_func()
                elapsed = time.perf_counter() - start
                print(f"  {op_name}: {result} ({elapsed*1000:.3f}ms)")
            except NotImplementedError as e:
                print(f"  {op_name}: Not implemented")
            except Exception as e:
                print(f"  {op_name}: Error - {e}")
    
    # Test backend switching for performance comparison
    print("\n4. Performance Comparison (1000x1000 matrix multiply):")
    print("-" * 40)
    
    # Create larger matrices for meaningful benchmark
    size = 100
    large_a = arrpy.ones((size, size))
    large_b = arrpy.ones((size, size))
    
    for backend in [arrpy.Backend.PYTHON, arrpy.Backend.CYTHON, arrpy.Backend.C]:
        arrpy.set_backend(backend)
        print(f"\n{backend.value.upper()} Backend:")
        
        try:
            # Warmup
            _ = large_a + large_b
            
            # Benchmark addition
            start = time.perf_counter()
            for _ in range(10):
                result = large_a + large_b
            elapsed = time.perf_counter() - start
            print(f"  Addition (10 iterations): {elapsed:.4f}s")
            
        except NotImplementedError:
            print(f"  Addition: Not implemented")
        except Exception as e:
            print(f"  Error: {e}")
    
    # Show which operations are available
    print("\n5. Backend Capabilities Check:")
    print("-" * 40)
    
    operations_to_check = ['add', 'multiply', 'matmul', 'sum', 'sin']
    
    for op in operations_to_check:
        backends = arrpy.get_available_backends_for_operation(op)
        backend_names = [b.value for b in backends]
        print(f"{op:12} available in: {', '.join(backend_names) if backend_names else 'None'}")
    
    # Reset to Python backend
    arrpy.set_backend('python')
    print("\n✓ Backend reset to Python")
    print("=" * 70)


if __name__ == "__main__":
    main()