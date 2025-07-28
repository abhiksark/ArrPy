"""
Comparison and logical operations examples for ArrPy - showcasing element-wise comparisons and logical operations
"""

from arrpy import Array, array, zeros, ones, arange, linspace

def basic_comparison_operations():
    """Demonstrate basic element-wise comparison operations"""
    print("=== Basic Comparison Operations ===")
    
    # Create test arrays
    arr1 = array([1, 2, 3, 4, 5])
    arr2 = array([1, 1, 4, 4, 3])
    
    print(f"Array 1: {arr1}")
    print(f"Array 2: {arr2}")
    
    # Element-wise comparisons
    equal = arr1 == arr2
    not_equal = arr1 != arr2
    greater = arr1 > arr2
    less = arr1 < arr2
    greater_equal = arr1 >= arr2
    less_equal = arr1 <= arr2
    
    print(f"\\nElement-wise comparisons:")
    print(f"arr1 == arr2: {equal}")
    print(f"arr1 != arr2: {not_equal}")
    print(f"arr1 > arr2:  {greater}")
    print(f"arr1 < arr2:  {less}")
    print(f"arr1 >= arr2: {greater_equal}")
    print(f"arr1 <= arr2: {less_equal}")
    print()

def scalar_comparisons():
    """Demonstrate comparisons with scalar values"""
    print("=== Scalar Comparisons ===")
    
    # Create test array
    data = array([1, 5, 3, 8, 2, 7, 4, 6])
    threshold = 5
    
    print(f"Data: {data}")
    print(f"Threshold: {threshold}")
    
    # Compare with scalar
    above_threshold = data > threshold
    at_or_below = data <= threshold
    exactly_equal = data == threshold
    
    print(f"\\nComparisons with scalar {threshold}:")
    print(f"data > {threshold}:  {above_threshold}")
    print(f"data <= {threshold}: {at_or_below}")
    print(f"data == {threshold}: {exactly_equal}")
    
    # Find indices where condition is true (manual approach)
    print(f"\\nIndices where data > {threshold}:")
    indices = []
    for i, val in enumerate(data._data):
        if val > threshold:
            indices.append(i)
    print(f"Indices: {indices}")
    print(f"Values: {[data[i] for i in indices]}")
    print()

def logical_operations():
    """Demonstrate logical operations between arrays"""
    print("=== Logical Operations ===")
    
    # Create boolean arrays
    bool1 = array([True, True, False, False])
    bool2 = array([True, False, True, False])
    
    print(f"Boolean array 1: {bool1}")
    print(f"Boolean array 2: {bool2}")
    
    # Logical operations
    logical_and = bool1.logical_and(bool2)
    logical_or = bool1.logical_or(bool2)
    logical_not1 = bool1.logical_not()
    logical_not2 = bool2.logical_not()
    
    print(f"\\nLogical operations:")
    print(f"bool1 AND bool2: {logical_and}")
    print(f"bool1 OR bool2:  {logical_or}")
    print(f"NOT bool1:       {logical_not1}")
    print(f"NOT bool2:       {logical_not2}")
    
    # Truth table verification
    print(f"\\nTruth table verification:")
    print(f"T AND T = {True and True} ✓ {logical_and[0]}")
    print(f"T AND F = {True and False} ✓ {logical_and[1]}")
    print(f"F AND T = {False and True} ✓ {logical_and[2]}")
    print(f"F AND F = {False and False} ✓ {logical_and[3]}")
    print()

def numeric_logical_operations():
    """Demonstrate logical operations with numeric arrays"""
    print("=== Logical Operations with Numeric Arrays ===")
    
    # In logical context, 0 is False, non-zero is True
    num1 = array([1, 0, 2, 0])
    num2 = array([3, 0, 0, 4])
    
    print(f"Numeric array 1: {num1}")
    print(f"Numeric array 2: {num2}")
    print("(In logical context: 0 = False, non-zero = True)")
    
    # Logical operations interpret numbers as boolean
    and_result = num1.logical_and(num2)
    or_result = num1.logical_or(num2)
    not_result1 = num1.logical_not()
    
    print(f"\\nLogical operations on numeric arrays:")
    print(f"num1 AND num2: {and_result}")
    print(f"num1 OR num2:  {or_result}")
    print(f"NOT num1:      {not_result1}")
    
    # Manual verification
    print(f"\\nManual verification:")
    for i in range(len(num1._data)):
        n1, n2 = num1[i], num2[i]
        expected_and = bool(n1) and bool(n2)
        expected_or = bool(n1) or bool(n2)
        print(f"  {n1} AND {n2} = {expected_and} ✓ {and_result[i]}")
        print(f"  {n1} OR {n2} = {expected_or} ✓ {or_result[i]}")
    print()

def combined_comparison_logical():
    """Demonstrate combining comparison and logical operations"""
    print("=== Combined Comparison and Logical Operations ===")
    
    # Create test data
    scores = array([85, 72, 95, 68, 88, 76, 92, 81])
    print(f"Test scores: {scores}")
    
    # Define criteria
    passing_grade = 70
    excellent_grade = 90
    
    # Individual conditions
    passing = scores >= passing_grade
    excellent = scores >= excellent_grade
    failing = scores < passing_grade
    
    print(f"\\nIndividual conditions:")
    print(f"Passing (≥{passing_grade}):   {passing}")
    print(f"Excellent (≥{excellent_grade}): {excellent}")
    print(f"Failing (<{passing_grade}):    {failing}")
    
    # Combined conditions using logical operations
    good_not_excellent = passing.logical_and(excellent.logical_not())
    pass_or_excellent = passing.logical_or(excellent)
    
    print(f"\\nCombined conditions:")
    print(f"Good but not excellent: {good_not_excellent}")
    print(f"Passing or excellent:   {pass_or_excellent}")
    
    # Count results (manual counting)
    passing_count = sum([1 for x in passing._data if x])
    excellent_count = sum([1 for x in excellent._data if x])
    failing_count = sum([1 for x in failing._data if x])
    
    print(f"\\nSummary counts:")
    print(f"Passing students: {passing_count}")
    print(f"Excellent students: {excellent_count}")
    print(f"Failing students: {failing_count}")
    print()

def filtering_and_selection():
    """Demonstrate using comparisons for data filtering"""
    print("=== Data Filtering and Selection ===")
    
    # Create sample dataset
    temperatures = array([22, 18, 25, 30, 16, 28, 32, 19, 24, 27])
    cities = ["NYC", "LAX", "MIA", "PHX", "SEA", "ATL", "LAS", "BOS", "CHI", "DFW"]
    
    print(f"Temperatures: {temperatures}")
    print(f"Cities: {cities}")
    
    # Define conditions
    hot_threshold = 25
    cold_threshold = 20
    
    # Create condition masks
    hot_weather = temperatures > hot_threshold
    cold_weather = temperatures < cold_threshold
    mild_weather = (temperatures >= cold_threshold).logical_and(temperatures <= hot_threshold)
    
    print(f"\\nWeather conditions:")
    print(f"Hot (>{hot_threshold}°C):     {hot_weather}")
    print(f"Cold (<{cold_threshold}°C):   {cold_weather}")
    print(f"Mild ({cold_threshold}-{hot_threshold}°C): {mild_weather}")
    
    # Extract filtered data (manual filtering)
    print(f"\\nFiltered results:")
    hot_cities = [cities[i] for i, is_hot in enumerate(hot_weather._data) if is_hot]
    hot_temps = [temperatures[i] for i, is_hot in enumerate(hot_weather._data) if is_hot]
    
    cold_cities = [cities[i] for i, is_cold in enumerate(cold_weather._data) if is_cold]
    cold_temps = [temperatures[i] for i, is_cold in enumerate(cold_weather._data) if is_cold]
    
    print(f"Hot cities: {hot_cities} with temps {hot_temps}")
    print(f"Cold cities: {cold_cities} with temps {cold_temps}")
    print()

def range_and_boundary_checks():
    """Demonstrate range and boundary checking"""
    print("=== Range and Boundary Checks ===")
    
    # Create test data
    values = array([0.5, 1.2, -0.3, 2.1, 0.8, 1.5, -0.1, 1.9])
    print(f"Values: {values}")
    
    # Define ranges
    lower_bound = 0.0
    upper_bound = 2.0
    
    # Boundary checks
    within_bounds = (values >= lower_bound).logical_and(values <= upper_bound)
    below_lower = values < lower_bound
    above_upper = values > upper_bound
    at_boundaries = (values == lower_bound).logical_or(values == upper_bound)
    
    print(f"\\nBoundary analysis (range [{lower_bound}, {upper_bound}]):")
    print(f"Within bounds:  {within_bounds}")
    print(f"Below lower:    {below_lower}")
    print(f"Above upper:    {above_upper}")
    print(f"At boundaries:  {at_boundaries}")
    
    # Count violations
    below_count = sum([1 for x in below_lower._data if x])
    above_count = sum([1 for x in above_upper._data if x])
    valid_count = sum([1 for x in within_bounds._data if x])
    
    print(f"\\nSummary:")
    print(f"Valid values: {valid_count}")
    print(f"Below range: {below_count}")
    print(f"Above range: {above_count}")
    print()

def matrix_comparison_operations():
    """Demonstrate comparison operations on 2D arrays"""
    print("=== Matrix Comparison Operations ===")
    
    # Create test matrices
    matrix1 = array([[1, 2, 3], [4, 5, 6]])
    matrix2 = array([[2, 2, 2], [4, 3, 7]])
    
    print(f"Matrix 1:")
    print(f"{matrix1}")
    print(f"Matrix 2:")
    print(f"{matrix2}")
    
    # Element-wise comparisons
    equal_elements = matrix1 == matrix2
    greater_elements = matrix1 > matrix2
    
    print(f"\\nElement-wise equal:")
    print(f"{equal_elements}")
    print(f"\\nMatrix1 > Matrix2:")
    print(f"{greater_elements}")
    
    # Compare with scalar
    threshold = 4
    above_threshold = matrix1 > threshold
    
    print(f"\\nElements > {threshold}:")
    print(f"{above_threshold}")
    
    # Summary statistics on boolean results
    total_elements = len(matrix1._data)
    equal_count = sum([1 for x in equal_elements._data if x])
    greater_count = sum([1 for x in greater_elements._data if x])
    above_thresh_count = sum([1 for x in above_threshold._data if x])
    
    print(f"\\nSummary ({total_elements} total elements):")
    print(f"Equal elements: {equal_count}")
    print(f"Matrix1 > Matrix2: {greater_count}")
    print(f"Above threshold: {above_thresh_count}")
    print()

def complex_logical_expressions():
    """Demonstrate complex logical expressions"""
    print("=== Complex Logical Expressions ===")
    
    # Student data
    math_scores = array([85, 70, 92, 68, 88, 75, 95, 82])
    science_scores = array([78, 88, 85, 72, 90, 82, 88, 79])
    attendance = array([95, 85, 98, 70, 92, 88, 97, 85])
    
    print(f"Math scores:    {math_scores}")
    print(f"Science scores: {science_scores}")
    print(f"Attendance (%): {attendance}")
    
    # Define criteria
    math_pass = 75
    science_pass = 80
    attendance_req = 90
    
    # Individual conditions
    math_passing = math_scores >= math_pass
    science_passing = science_scores >= science_pass
    good_attendance = attendance >= attendance_req
    
    # Complex conditions
    honor_student = math_passing.logical_and(science_passing).logical_and(good_attendance)
    at_risk = math_passing.logical_not().logical_or(science_passing.logical_not())
    excellent_one_subject = (math_scores >= 90).logical_or(science_scores >= 90)
    
    print(f"\\nComplex criteria:")
    print(f"Honor student (all criteria): {honor_student}")
    print(f"At risk (failing any):        {at_risk}")
    print(f"Excellent in one subject:     {excellent_one_subject}")
    
    # Student analysis
    print(f"\\nStudent analysis:")
    for i in range(len(math_scores._data)):
        status = []
        if honor_student[i]:
            status.append("Honor")
        if at_risk[i]:
            status.append("At-Risk")
        if excellent_one_subject[i]:
            status.append("Excellent")
        
        status_str = ", ".join(status) if status else "Regular"
        print(f"  Student {i+1}: {status_str}")
    print()

def performance_optimization_tips():
    """Show performance tips for comparison and logical operations"""
    print("=== Performance Optimization Tips ===")
    
    print("1. Chain comparisons efficiently:")
    data = array([1, 5, 3, 8, 2, 7, 4, 6])
    
    # Efficient: single compound expression
    in_range = (data >= 3).logical_and(data <= 6)
    print(f"   Data: {data}")
    print(f"   In range [3,6]: {in_range}")
    
    print("\\n2. Use appropriate comparison operators:")
    print("   - Use == for exact equality")
    print("   - Use >= and <= for inclusive ranges")
    print("   - Use > and < for exclusive ranges")
    
    print("\\n3. Combine conditions logically:")
    print("   Good: condition1.logical_and(condition2)")
    print("   Avoid: Manual iteration over boolean arrays")
    
    print("\\n4. Reuse comparison results:")
    threshold = 5
    above_thresh = data > threshold
    
    # Reuse the boolean array
    count_above = sum([1 for x in above_thresh._data if x])
    indices_above = [i for i, x in enumerate(above_thresh._data) if x]
    
    print(f"   Above {threshold}: count={count_above}, indices={indices_above}")
    print()

def error_handling_comparisons():
    """Demonstrate error handling in comparison operations"""
    print("=== Error Handling in Comparisons ===")
    
    # Shape mismatch
    arr1 = array([1, 2, 3])
    arr2 = array([1, 2])
    
    print("1. Shape mismatch in comparisons:")
    try:
        result = arr1 == arr2
        print(f"   This shouldn't work: {result}")
    except Exception as e:
        print(f"   ✓ Caught expected error: {type(e).__name__}: {e}")
    
    # Type mismatch in logical operations
    print("\\n2. Type errors in logical operations:")
    bool_arr = array([True, False, True])
    
    try:
        # This should work - numbers are converted to boolean
        result = bool_arr.logical_and(array([1, 0, 1]))
        print(f"   Numbers as boolean: {result}")
    except Exception as e:
        print(f"   Error: {type(e).__name__}: {e}")
    
    try:
        # Invalid logical operation
        result = bool_arr.logical_and("not an array")
        print(f"   This shouldn't work: {result}")
    except Exception as e:
        print(f"   ✓ Caught expected error: {type(e).__name__}")
    
    print()

if __name__ == "__main__":
    basic_comparison_operations()
    scalar_comparisons()
    logical_operations()
    numeric_logical_operations()
    combined_comparison_logical()
    filtering_and_selection()
    range_and_boundary_checks()
    matrix_comparison_operations()
    complex_logical_expressions()
    performance_optimization_tips()
    error_handling_comparisons()
    
    print("=== All comparison and logical operation examples completed! ===")