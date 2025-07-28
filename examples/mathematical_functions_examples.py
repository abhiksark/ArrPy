"""
Mathematical functions examples for ArrPy - showcasing all mathematical operations
"""

import math
from arrpy import (
    Array, array, zeros, ones, linspace,
    # Trigonometric functions
    sin, cos, tan, arcsin, arccos, arctan,
    # Logarithmic functions
    exp, log, log10, log2, sqrt,
    # Arithmetic functions
    power, absolute, sign, floor_divide, mod,
    # Rounding functions
    floor, ceil, round, trunc
)

def trigonometric_functions():
    """Demonstrate trigonometric functions"""
    print("=== Trigonometric Functions ===")
    
    # Create angle arrays
    angles_rad = linspace(0, 2 * math.pi, 8)
    angles_deg_values = [0, 30, 45, 60, 90, 180, 270, 360]
    angles_deg = array([math.radians(d) for d in angles_deg_values])
    
    print("Angles (radians):", angles_rad)
    print("Angles (degrees converted):", [f"{math.degrees(a):.0f}°" for a in angles_deg._data])
    print()
    
    # Basic trigonometric functions
    print("Basic trigonometric functions:")
    sin_values = sin(angles_deg)
    cos_values = cos(angles_deg) 
    tan_values = tan(angles_deg)
    
    print(f"sin(angles): {sin_values}")
    print(f"cos(angles): {cos_values}")
    print(f"tan(angles): {tan_values}")
    print()
    
    # Show method vs function call patterns
    print("Method vs Function call patterns:")
    arr = array([0, math.pi/2, math.pi])
    
    # Using methods
    sin_method = arr.sin()
    cos_method = arr.cos()
    
    # Using functions
    sin_function = sin(arr)
    cos_function = cos(arr)
    
    print(f"arr.sin() (method): {sin_method}")
    print(f"sin(arr) (function): {sin_function}")
    print(f"Results identical: {all(abs(a - b) < 1e-10 for a, b in zip(sin_method._data, sin_function._data))}")
    print()

def inverse_trigonometric_functions():
    """Demonstrate inverse trigonometric functions"""
    print("=== Inverse Trigonometric Functions ===")
    
    # Values for inverse functions (domain [-1, 1] for arcsin/arccos)
    values = array([-1, -0.5, 0, 0.5, 1])
    print(f"Input values: {values}")
    
    # Inverse trigonometric functions
    arcsin_values = arcsin(values)
    arccos_values = arccos(values)
    
    print(f"arcsin(values): {arcsin_values}")
    print(f"arccos(values): {arccos_values}")
    
    # arctan can handle any values
    tan_values = array([-2, -1, 0, 1, 2])
    arctan_values = arctan(tan_values)
    print(f"arctan({tan_values}): {arctan_values}")
    
    # Verify inverse relationships
    print("\\nVerifying inverse relationships:")
    test_angles = array([0, math.pi/6, math.pi/4, math.pi/3])
    sin_then_arcsin = arcsin(sin(test_angles))
    print(f"arcsin(sin(angles)): {sin_then_arcsin}")
    print(f"Original angles: {test_angles}")
    print()

def logarithmic_and_exponential():
    """Demonstrate logarithmic and exponential functions"""
    print("=== Logarithmic and Exponential Functions ===")
    
    # Exponential function
    x_values = array([0, 1, 2, 3, -1, -2])
    exp_values = exp(x_values)
    print(f"exp({x_values}): {exp_values}")
    
    # Natural logarithm
    positive_values = array([1, math.e, math.e**2, 10, 100])
    log_values = log(positive_values)
    print(f"log({positive_values}): {log_values}")
    
    # Base-10 logarithm
    log10_values = log10(positive_values)
    print(f"log10({positive_values}): {log10_values}")
    
    # Base-2 logarithm
    powers_of_2 = array([1, 2, 4, 8, 16, 32])
    log2_values = log2(powers_of_2)
    print(f"log2({powers_of_2}): {log2_values}")
    
    # Square root
    sqrt_input = array([0, 1, 4, 9, 16, 25])
    sqrt_values = sqrt(sqrt_input)
    print(f"sqrt({sqrt_input}): {sqrt_values}")
    
    # Verify relationships
    print("\\nVerifying exp/log relationships:")
    test_vals = array([1, 2, 3])
    exp_log = exp(log(test_vals))
    print(f"exp(log(x)): {exp_log}")
    print(f"Original x: {test_vals}")
    print()

def arithmetic_functions():
    """Demonstrate arithmetic functions"""
    print("=== Arithmetic Functions ===")
    
    # Power function
    base = array([2, 3, 4, 5])
    exponent = array([2, 3, 2, 4])
    power_values = power(base, exponent)
    print(f"power({base}, {exponent}): {power_values}")
    
    # Power with scalar exponent
    power_scalar = power(base, 2)
    print(f"power({base}, 2): {power_scalar}")
    
    # Absolute value
    mixed_values = array([-5, -2.5, 0, 2.5, 5])
    abs_values = absolute(mixed_values)
    print(f"absolute({mixed_values}): {abs_values}")
    
    # Sign function
    sign_values = sign(mixed_values)
    print(f"sign({mixed_values}): {sign_values}")
    
    # Floor division
    dividends = array([7, 8, 9, 10])
    divisors = array([3, 3, 4, 3])
    floor_div_values = floor_divide(dividends, divisors)
    print(f"floor_divide({dividends}, {divisors}): {floor_div_values}")
    
    # Modulo operation
    mod_values = mod(dividends, divisors)
    print(f"mod({dividends}, {divisors}): {mod_values}")
    print()

def rounding_functions():
    """Demonstrate rounding functions"""
    print("=== Rounding Functions ===")
    
    # Test values with different decimal parts
    decimal_values = array([1.2, 1.5, 1.7, 2.1, 2.5, 2.9, -1.2, -1.5, -1.7])
    print(f"Original values: {decimal_values}")
    
    # Different rounding functions
    floor_values = floor(decimal_values)
    ceil_values = ceil(decimal_values)
    round_values = round(decimal_values)
    trunc_values = trunc(decimal_values)
    
    print(f"floor():  {floor_values}")
    print(f"ceil():   {ceil_values}")
    print(f"round():  {round_values}")
    print(f"trunc():  {trunc_values}")
    
    # Demonstrate the differences
    print("\\nRounding behavior comparison:")
    test_val = 2.7
    print(f"Value: {test_val}")
    print(f"  floor({test_val}) = {math.floor(test_val)} (always down)")
    print(f"  ceil({test_val}) = {math.ceil(test_val)} (always up)")
    print(f"  round({test_val}) = {round(test_val)} (nearest integer)")
    print(f"  trunc({test_val}) = {math.trunc(test_val)} (towards zero)")
    print()

def advanced_mathematical_operations():
    """Demonstrate advanced mathematical operations"""
    print("=== Advanced Mathematical Operations ===")
    
    # Combining multiple functions
    x = linspace(0, 2*math.pi, 6)
    print(f"x values: {x}")
    
    # Complex expressions
    y1 = sin(x) + cos(x)
    print(f"sin(x) + cos(x): {y1}")
    
    y2 = sqrt(absolute(sin(x)))
    print(f"sqrt(|sin(x)|): {y2}")
    
    # Exponential of trigonometric
    y3 = exp(sin(x))
    print(f"exp(sin(x)): {y3}")
    
    # Logarithm of squares
    positive_x = array([1, 2, 3, 4, 5])
    y4 = log(power(positive_x, 2))
    print(f"log(x²) where x={positive_x}: {y4}")
    print()

def scientific_calculations():
    """Demonstrate scientific calculation examples"""
    print("=== Scientific Calculation Examples ===")
    
    # Wave functions
    print("1. Wave function calculation:")
    t = linspace(0, 1, 10)
    frequency = 2  # Hz
    amplitude = 3
    wave = amplitude * sin(2 * math.pi * frequency * t._data[0])  # Simplified for demo
    print(f"   Time points: {t}")
    print(f"   Wave amplitude at t=0: {wave}")
    
    # Exponential decay
    print("\\n2. Exponential decay:")
    time_constants = array([0.5, 1.0, 1.5, 2.0])
    decay_values = exp(-time_constants)
    print(f"   Time constants: {time_constants}")
    print(f"   Decay values: {decay_values}")
    
    # Distance calculations
    print("\\n3. Distance calculations:")
    coordinates = array([3, 4, 5])  # x, y, z
    distances_squared = power(coordinates, 2)
    total_distance = sqrt(sum(distances_squared._data))  # Manual sum for demo
    print(f"   Coordinates: {coordinates}")
    print(f"   Distance from origin: {total_distance}")
    
    # pH calculations (logarithmic scale)
    print("\\n4. pH calculations:")
    h_concentrations = array([1e-1, 1e-3, 1e-7, 1e-9, 1e-12])
    ph_values = -log10(h_concentrations)
    print(f"   H+ concentrations: {h_concentrations}")
    print(f"   pH values: {ph_values}")
    print()

def error_handling_examples():
    """Demonstrate error handling for mathematical functions"""
    print("=== Error Handling in Mathematical Functions ===")
    
    # Domain errors
    print("1. Domain errors:")
    
    # Square root of negative numbers
    try:
        negative_sqrt = sqrt(array([-1, -4]))
        print(f"   sqrt(negative): {negative_sqrt}")
    except Exception as e:
        print(f"   ✓ sqrt(negative) error: {type(e).__name__}")
    
    # Logarithm of zero or negative
    try:
        log_negative = log(array([0, -1]))
        print(f"   log(non-positive): {log_negative}")
    except Exception as e:
        print(f"   ✓ log(non-positive) error: {type(e).__name__}")
    
    # arcsin/arccos outside [-1, 1]
    try:
        arcsin_invalid = arcsin(array([2, 3]))
        print(f"   arcsin(>1): {arcsin_invalid}")
    except Exception as e:
        print(f"   ✓ arcsin(>1) error: {type(e).__name__}")
    
    print()

def performance_comparison():
    """Show performance tips for mathematical functions"""
    print("=== Performance Tips for Mathematical Functions ===")
    
    print("1. Vectorized operations are more efficient:")
    print("   Good: sin(array([0, π/2, π]))")
    print("   Avoid: [math.sin(x) for x in [0, π/2, π]]")
    print()
    
    print("2. Combine operations when possible:")
    x = array([1, 4, 9, 16])
    
    # Less efficient: multiple passes
    step1 = sqrt(x)
    step2 = log(step1)
    
    # More efficient: combined (when mathematically equivalent)
    combined = log(sqrt(x))
    
    print(f"   Input: {x}")
    print(f"   log(sqrt(x)): {combined}")
    print()
    
    print("3. Use appropriate precision:")
    small_values = array([1e-10, 1e-8, 1e-6])
    print(f"   Small values: {small_values}")
    print(f"   log(small): {log(small_values)}")
    print()

if __name__ == "__main__":
    trigonometric_functions()
    inverse_trigonometric_functions()
    logarithmic_and_exponential()
    arithmetic_functions()
    rounding_functions()
    advanced_mathematical_operations()
    scientific_calculations()
    error_handling_examples()
    performance_comparison()
    
    print("=== All mathematical function examples completed! ===")