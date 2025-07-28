"""
Data analysis examples using arrpy for basic statistical operations
"""

from arrpy import Array, array, min, max, std, var, median, percentile, concatenate

def statistical_analysis():
    """Demonstrate basic statistical analysis"""
    print("=== Statistical Analysis ===")
    
    # Sample data: test scores for different subjects
    math_scores = Array([85, 92, 78, 96, 88, 75, 89, 93, 81, 87])
    science_scores = Array([88, 85, 82, 91, 90, 79, 86, 94, 83, 89])
    english_scores = Array([82, 89, 85, 88, 91, 77, 84, 90, 86, 92])
    
    print(f"Math scores: {math_scores}")
    print(f"Science scores: {science_scores}")
    print(f"English scores: {english_scores}")
    print()
    
    # Calculate means
    math_mean = math_scores.mean()
    science_mean = science_scores.mean()
    english_mean = english_scores.mean()
    
    print(f"Average Math score: {math_mean:.2f}")
    print(f"Average Science score: {science_mean:.2f}")
    print(f"Average English score: {english_mean:.2f}")
    print()
    
    # Calculate totals
    print(f"Total Math points: {math_scores.sum()}")
    print(f"Total Science points: {science_scores.sum()}")
    print(f"Total English points: {english_scores.sum()}")
    print()

def grade_matrix_analysis():
    """Analyze grades using matrix operations"""
    print("=== Grade Matrix Analysis ===")
    
    # Students × Subjects matrix (5 students, 4 subjects)
    grades = Array([
        [85, 88, 82, 90],  # Student 1: Math, Science, English, History
        [92, 85, 89, 87],  # Student 2
        [78, 82, 85, 83],  # Student 3
        [96, 91, 88, 94],  # Student 4
        [88, 90, 91, 86]   # Student 5
    ])
    
    print("Grades matrix (Students × Subjects):")
    print("Subjects: Math, Science, English, History")
    print(f"{grades}")
    print()
    
    # Subject averages (average across all students)
    print("Subject averages:")
    for subject in range(4):
        subject_column = Array([grades[student, subject] for student in range(5)])
        avg = subject_column.mean()
        subjects = ["Math", "Science", "English", "History"]
        print(f"{subjects[subject]}: {avg:.2f}")
    print()
    
    # Student averages (average across all subjects)
    print("Student averages:")
    for student in range(5):
        student_row = Array([grades[student, subject] for subject in range(4)])
        avg = student_row.mean()
        print(f"Student {student + 1}: {avg:.2f}")
    print()
    
    # Overall class average
    total_sum = grades.sum()
    total_entries = 5 * 4  # 5 students × 4 subjects
    overall_avg = total_sum / total_entries
    print(f"Overall class average: {overall_avg:.2f}")
    print()

def sales_data_analysis():
    """Analyze sales data using arrays"""
    print("=== Sales Data Analysis ===")
    
    # Monthly sales data for different products (in thousands)
    # Rows: Products, Columns: Months (Jan-Jun)
    sales_data = Array([
        [120, 135, 142, 158, 165, 172],  # Product A
        [98, 105, 112, 118, 125, 130],   # Product B
        [87, 92, 88, 95, 102, 108],      # Product C
        [156, 148, 162, 169, 175, 182]   # Product D
    ])
    
    print("Sales data (Products × Months, in thousands):")
    print("Months: Jan, Feb, Mar, Apr, May, Jun")
    print(f"{sales_data}")
    print()
    
    # Monthly totals (sum across all products)
    print("Monthly total sales:")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    for month in range(6):
        month_column = Array([sales_data[product, month] for product in range(4)])
        total = month_column.sum()
        print(f"{months[month]}: {total}k")
    print()
    
    # Product totals (sum across all months)
    print("Product total sales (6 months):")
    products = ["Product A", "Product B", "Product C", "Product D"]
    for product in range(4):
        product_row = Array([sales_data[product, month] for month in range(6)])
        total = product_row.sum()
        avg = product_row.mean()
        print(f"{products[product]}: {total}k total, {avg:.1f}k average per month")
    print()

def financial_calculations():
    """Demonstrate financial calculations"""
    print("=== Financial Calculations ===")
    
    # Investment portfolio (shares × price per share)
    shares = Array([100, 50, 200, 75])  # Number of shares
    prices = Array([25.50, 48.75, 12.25, 33.80])  # Price per share
    
    print(f"Shares owned: {shares}")
    print(f"Price per share: {prices}")
    
    # Calculate portfolio value using element-wise multiplication
    portfolio_values = shares * prices
    print(f"Value per holding: {portfolio_values}")
    
    total_value = portfolio_values.sum()
    print(f"Total portfolio value: ${total_value:.2f}")
    print()
    
    # Calculate percentage allocation
    print("Portfolio allocation:")
    companies = ["TechCorp", "BioMed", "RetailCo", "EnergyInc"]
    for i in range(4):
        percentage = (portfolio_values[i] / total_value) * 100
        print(f"{companies[i]}: {percentage:.1f}%")
    print()

def growth_analysis():
    """Analyze growth trends"""
    print("=== Growth Analysis ===")
    
    # Quarterly revenue data (in millions)
    q1_revenue = Array([50, 45, 52, 48])  # 4 business units
    q2_revenue = Array([55, 48, 58, 52])
    q3_revenue = Array([62, 52, 61, 57])
    q4_revenue = Array([68, 55, 65, 61])
    
    print(f"Q1 Revenue: {q1_revenue}")
    print(f"Q2 Revenue: {q2_revenue}")
    print(f"Q3 Revenue: {q3_revenue}")
    print(f"Q4 Revenue: {q4_revenue}")
    print()
    
    # Calculate quarterly growth
    q1_to_q2_growth = ((q2_revenue - q1_revenue) / q1_revenue) * 100
    q2_to_q3_growth = ((q3_revenue - q2_revenue) / q2_revenue) * 100
    q3_to_q4_growth = ((q4_revenue - q3_revenue) / q3_revenue) * 100
    
    print("Quarterly growth rates (%):")
    units = ["Unit A", "Unit B", "Unit C", "Unit D"]
    for i in range(4):
        print(f"{units[i]}:")
        print(f"  Q1→Q2: {q1_to_q2_growth[i]:.1f}%")
        print(f"  Q2→Q3: {q2_to_q3_growth[i]:.1f}%")
        print(f"  Q3→Q4: {q3_to_q4_growth[i]:.1f}%")
    print()
    
    # Year-over-year growth
    year_growth = ((q4_revenue - q1_revenue) / q1_revenue) * 100
    print("Year-over-year growth:")
    for i in range(4):
        print(f"{units[i]}: {year_growth[i]:.1f}%")
    print()

def advanced_statistical_analysis():
    """Demonstrate advanced statistical functions"""
    print("=== Advanced Statistical Analysis ===")
    
    # Customer satisfaction scores
    satisfaction_scores = array([4.2, 3.8, 4.5, 3.2, 4.8, 3.9, 4.1, 4.3, 3.7, 4.6])
    print(f"Satisfaction scores: {satisfaction_scores}")
    
    # Calculate comprehensive statistics
    mean_score = satisfaction_scores.mean()
    min_score = min(satisfaction_scores)
    max_score = max(satisfaction_scores)
    std_score = std(satisfaction_scores)
    var_score = var(satisfaction_scores)
    median_score = median(satisfaction_scores)
    
    print(f"Mean: {mean_score:.2f}")
    print(f"Min: {min_score}")
    print(f"Max: {max_score}")
    print(f"Standard deviation: {std_score:.2f}")
    print(f"Variance: {var_score:.2f}")
    print(f"Median: {median_score:.2f}")
    
    # Percentile analysis
    p25 = percentile(satisfaction_scores, 25)
    p75 = percentile(satisfaction_scores, 75)
    iqr = p75 - p25
    
    print(f"\nPercentile analysis:")
    print(f"25th percentile: {p25:.2f}")
    print(f"75th percentile: {p75:.2f}")
    print(f"Interquartile range: {iqr:.2f}")
    print()

def time_series_concatenation():
    """Demonstrate time series data concatenation"""
    print("=== Time Series Data Concatenation ===")
    
    # Monthly data for different quarters
    q1_data = array([100, 110, 105])  # Jan, Feb, Mar
    q2_data = array([120, 115, 125])  # Apr, May, Jun
    q3_data = array([130, 135, 140])  # Jul, Aug, Sep
    q4_data = array([145, 150, 155])  # Oct, Nov, Dec
    
    print(f"Q1 data: {q1_data}")
    print(f"Q2 data: {q2_data}")
    print(f"Q3 data: {q3_data}")
    print(f"Q4 data: {q4_data}")
    
    # Concatenate into full year
    full_year = concatenate([q1_data, q2_data, q3_data, q4_data])
    print(f"Full year data: {full_year}")
    
    # Calculate year statistics
    year_mean = full_year.mean()
    year_growth = ((full_year[-1] - full_year[0]) / full_year[0]) * 100
    
    print(f"Annual average: {year_mean:.1f}")
    print(f"Year-over-year growth: {year_growth:.1f}%")
    print()

if __name__ == "__main__":
    statistical_analysis()
    grade_matrix_analysis()
    sales_data_analysis()
    financial_calculations()
    growth_analysis()
    advanced_statistical_analysis()
    time_series_concatenation()
    
    print("=== All data analysis examples completed! ===")