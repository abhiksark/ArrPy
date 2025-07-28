"""
Statistical analysis examples for ArrPy - showcasing all statistical functions
"""

from arrpy import (
    Array, array, zeros, ones, arange, linspace,
    # Basic statistical functions
    sum, mean, min, max, std, var, median, percentile,
    # Advanced statistical functions  
    prod, cumsum, cumprod, argmin, argmax
)

def basic_statistics():
    """Demonstrate basic statistical functions"""
    print("=== Basic Statistical Functions ===")
    
    # Sample data
    data = array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print(f"Sample data: {data}")
    
    # Basic measures
    total = sum(data)
    average = mean(data)
    minimum = min(data)
    maximum = max(data)
    
    print(f"Sum: {total}")
    print(f"Mean: {average}")
    print(f"Min: {minimum}")
    print(f"Max: {maximum}")
    
    # Variability measures
    std_dev = std(data)
    variance = var(data)
    
    print(f"Standard deviation: {std_dev}")
    print(f"Variance: {variance}")
    print()

def central_tendency_measures():
    """Demonstrate measures of central tendency"""
    print("=== Measures of Central Tendency ===")
    
    # Different datasets to show different behaviors
    datasets = {
        "Normal distribution-like": array([2, 3, 4, 4, 5, 5, 5, 6, 6, 7]),
        "Skewed data": array([1, 1, 2, 2, 2, 3, 8, 9, 10]),
        "Bimodal data": array([1, 1, 2, 2, 6, 7, 7, 8, 8]),
    }
    
    for name, data in datasets.items():
        print(f"{name}: {data}")
        
        mean_val = mean(data)
        median_val = median(data)
        
        print(f"  Mean: {mean_val:.2f}")
        print(f"  Median: {median_val:.2f}")
        print(f"  Difference (mean - median): {mean_val - median_val:.2f}")
        print()

def percentile_analysis():
    """Demonstrate percentile analysis"""
    print("=== Percentile Analysis ===")
    
    # Test scores dataset
    scores = array([65, 70, 75, 78, 82, 85, 88, 90, 92, 95, 98])
    print(f"Test scores: {scores}")
    
    # Common percentiles
    percentiles = [0, 25, 50, 75, 90, 95, 100]
    
    print("Percentile analysis:")
    for p in percentiles:
        value = percentile(scores, p)
        print(f"  {p:2d}th percentile: {value:.1f}")
    
    # Quartile analysis
    q1 = percentile(scores, 25)
    q2 = percentile(scores, 50)  # Median
    q3 = percentile(scores, 75)
    iqr = q3 - q1
    
    print(f"\\nQuartile Analysis:")
    print(f"  Q1 (25th percentile): {q1}")
    print(f"  Q2 (50th percentile/Median): {q2}")
    print(f"  Q3 (75th percentile): {q3}")
    print(f"  IQR (Q3 - Q1): {iqr}")
    print()

def variability_measures():
    """Demonstrate measures of variability"""
    print("=== Measures of Variability ===")
    
    # Different variability datasets
    datasets = {
        "Low variability": array([49, 50, 50, 51, 51]),
        "Medium variability": array([45, 48, 50, 52, 55]),
        "High variability": array([30, 40, 50, 60, 70]),
    }
    
    for name, data in datasets.items():
        print(f"{name}: {data}")
        
        mean_val = mean(data)
        std_val = std(data)
        var_val = var(data)
        range_val = max(data) - min(data)
        
        print(f"  Mean: {mean_val:.1f}")
        print(f"  Standard deviation: {std_val:.2f}")
        print(f"  Variance: {var_val:.2f}")
        print(f"  Range: {range_val}")
        print(f"  Coefficient of variation: {(std_val/mean_val)*100:.1f}%")
        print()

def advanced_statistics():
    """Demonstrate advanced statistical functions"""
    print("=== Advanced Statistical Functions ===")
    
    # Sample data
    data = array([2, 4, 6, 8, 10])
    print(f"Sample data: {data}")
    
    # Product of all elements
    product = prod(data)
    print(f"Product of all elements: {product}")
    
    # Cumulative statistics
    cumulative_sum = cumsum(data)
    cumulative_product = cumprod(data)
    
    print(f"Cumulative sum: {cumulative_sum}")
    print(f"Cumulative product: {cumulative_product}")
    
    # Index-based statistics
    min_index = argmin(data)
    max_index = argmax(data)
    
    print(f"Index of minimum value: {min_index}")
    print(f"Index of maximum value: {max_index}")
    print(f"Verification - min value: {data[min_index]}, max value: {data[max_index]}")
    print()

def distribution_analysis():
    """Analyze data distributions"""
    print("=== Distribution Analysis ===")
    
    # Create different distribution shapes
    uniform_data = arange(1, 11)  # 1 to 10
    normal_like = array([1, 2, 3, 4, 5, 5, 5, 6, 7, 8, 9])
    skewed_data = array([1, 1, 1, 2, 2, 3, 4, 5, 8, 9, 10])
    
    distributions = {
        "Uniform": uniform_data,
        "Normal-like": normal_like, 
        "Right-skewed": skewed_data
    }
    
    for name, data in distributions.items():
        print(f"{name} distribution: {data}")
        
        mean_val = mean(data)
        median_val = median(data)
        std_val = std(data)
        
        # Calculate skewness indicator (simplified)
        skewness = (mean_val - median_val) / std_val if std_val > 0 else 0
        
        print(f"  Mean: {mean_val:.2f}")
        print(f"  Median: {median_val:.2f}")
        print(f"  Std Dev: {std_val:.2f}")
        print(f"  Skewness indicator: {skewness:.2f}")
        print()

def time_series_analysis():
    """Demonstrate time series statistical analysis"""
    print("=== Time Series Statistical Analysis ===")
    
    # Simulated monthly sales data
    sales = array([100, 110, 105, 120, 115, 130, 125, 140, 135, 150, 145, 160])
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    print("Monthly sales data:")
    for month, sale in zip(months, sales._data):
        print(f"  {month}: {sale}")
    
    # Time series statistics
    total_sales = sum(sales)
    avg_monthly = mean(sales)
    growth_data = array([sales._data[i+1] - sales._data[i] for i in range(len(sales._data)-1)])
    avg_growth = mean(growth_data)
    
    print(f"\\nTime series analysis:")
    print(f"  Total annual sales: {total_sales}")
    print(f"  Average monthly sales: {avg_monthly:.1f}")
    print(f"  Average monthly growth: {avg_growth:.1f}")
    
    # Seasonal analysis (simplified)
    q1_sales = array(sales._data[0:3])   # Jan-Mar
    q2_sales = array(sales._data[3:6])   # Apr-Jun
    q3_sales = array(sales._data[6:9])   # Jul-Sep
    q4_sales = array(sales._data[9:12])  # Oct-Dec
    
    print(f"\\nQuarterly averages:")
    print(f"  Q1 average: {mean(q1_sales):.1f}")
    print(f"  Q2 average: {mean(q2_sales):.1f}")
    print(f"  Q3 average: {mean(q3_sales):.1f}")
    print(f"  Q4 average: {mean(q4_sales):.1f}")
    print()

def comparative_statistics():
    """Compare statistics between different groups"""
    print("=== Comparative Statistics ===")
    
    # Two groups for comparison
    group_a = array([23, 25, 28, 30, 32, 35, 38])
    group_b = array([20, 22, 26, 28, 31, 33, 40])
    
    print(f"Group A: {group_a}")
    print(f"Group B: {group_b}")
    
    # Compare all statistics
    stats_comparison = {
        "Mean": (mean(group_a), mean(group_b)),
        "Median": (median(group_a), median(group_b)),
        "Std Dev": (std(group_a), std(group_b)),
        "Min": (min(group_a), min(group_b)),
        "Max": (max(group_a), max(group_b)),
        "Range": (max(group_a) - min(group_a), max(group_b) - min(group_b))
    }
    
    print("\\nComparative Statistics:")
    print(f"{'Statistic':<10} {'Group A':<8} {'Group B':<8} {'Difference':<10}")
    print("-" * 38)
    
    for stat_name, (val_a, val_b) in stats_comparison.items():
        diff = val_a - val_b
        print(f"{stat_name:<10} {val_a:<8.2f} {val_b:<8.2f} {diff:<10.2f}")
    print()

def outlier_detection():
    """Demonstrate outlier detection using statistical methods"""
    print("=== Outlier Detection ===")
    
    # Data with outliers
    normal_data = [20, 22, 23, 25, 24, 26, 27, 25, 23, 24]
    outlier_data = normal_data + [45, 50]  # Add outliers
    data_with_outliers = array(outlier_data)
    
    print(f"Data with potential outliers: {data_with_outliers}")
    
    # Statistical measures
    mean_val = mean(data_with_outliers)
    std_val = std(data_with_outliers)
    q1 = percentile(data_with_outliers, 25)
    q3 = percentile(data_with_outliers, 75)
    iqr = q3 - q1
    
    # Z-score method (simplified)
    print(f"\\nOutlier detection using Z-score method:")
    print(f"  Mean: {mean_val:.2f}, Std Dev: {std_val:.2f}")
    print("  Values with |z-score| > 2:")
    
    for i, value in enumerate(data_with_outliers._data):
        z_score = (value - mean_val) / std_val
        if abs(z_score) > 2:
            print(f"    Index {i}: value={value}, z-score={z_score:.2f}")
    
    # IQR method
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    print(f"\\nOutlier detection using IQR method:")
    print(f"  Q1: {q1:.2f}, Q3: {q3:.2f}, IQR: {iqr:.2f}")
    print(f"  Bounds: [{lower_bound:.2f}, {upper_bound:.2f}]")
    print("  Outliers (outside bounds):")
    
    for i, value in enumerate(data_with_outliers._data):
        if value < lower_bound or value > upper_bound:
            print(f"    Index {i}: value={value}")
    print()

def data_quality_assessment():
    """Assess data quality using statistical measures"""
    print("=== Data Quality Assessment ===")
    
    # Different quality datasets
    high_quality = array([98, 99, 100, 101, 102])
    medium_quality = array([85, 90, 95, 105, 110])
    low_quality = array([50, 75, 100, 125, 200])
    
    datasets = {
        "High Quality (low variance)": high_quality,
        "Medium Quality (moderate variance)": medium_quality,
        "Low Quality (high variance)": low_quality
    }
    
    for name, data in datasets.items():
        print(f"{name}: {data}")
        
        mean_val = mean(data)
        std_val = std(data)
        cv = (std_val / mean_val) * 100  # Coefficient of variation
        range_val = max(data) - min(data)
        
        # Quality indicators
        print(f"  Mean: {mean_val:.1f}")
        print(f"  Std Dev: {std_val:.2f}")
        print(f"  Coefficient of Variation: {cv:.1f}%")
        print(f"  Range: {range_val}")
        
        # Quality assessment
        if cv < 5:
            quality = "Excellent"
        elif cv < 15:
            quality = "Good"
        elif cv < 25:
            quality = "Fair"
        else:
            quality = "Poor"
        
        print(f"  Quality Assessment: {quality}")
        print()

def statistical_summary_report():
    """Generate a comprehensive statistical summary"""
    print("=== Comprehensive Statistical Summary ===")
    
    # Sample dataset - student exam scores
    scores = array([72, 85, 78, 92, 88, 76, 95, 82, 79, 86, 91, 83, 77, 89, 94])
    print(f"Student exam scores (n={len(scores._data)}): {scores}")
    
    print("\\n📊 STATISTICAL SUMMARY REPORT")
    print("=" * 50)
    
    # Central tendency
    print("Central Tendency:")
    print(f"  Mean:   {mean(scores):.2f}")
    print(f"  Median: {median(scores):.2f}")
    
    # Variability
    print("\\nVariability:")
    print(f"  Std Dev:  {std(scores):.2f}")
    print(f"  Variance: {var(scores):.2f}")
    print(f"  Range:    {max(scores) - min(scores)}")
    
    # Distribution shape
    print("\\nDistribution:")
    print(f"  Minimum:  {min(scores)}")
    print(f"  Q1:       {percentile(scores, 25):.1f}")
    print(f"  Median:   {percentile(scores, 50):.1f}")
    print(f"  Q3:       {percentile(scores, 75):.1f}")
    print(f"  Maximum:  {max(scores)}")
    
    # Advanced metrics
    print("\\nAdvanced Metrics:")
    print(f"  Sum:      {sum(scores)}")
    print(f"  Product:  {prod(scores)}")
    print(f"  Min Index: {argmin(scores)} (value: {scores[argmin(scores)]})")
    print(f"  Max Index: {argmax(scores)} (value: {scores[argmax(scores)]})")
    
    print("\\n" + "=" * 50)
    print()

if __name__ == "__main__":
    basic_statistics()
    central_tendency_measures()
    percentile_analysis()
    variability_measures()
    advanced_statistics()
    distribution_analysis()
    time_series_analysis()
    comparative_statistics()
    outlier_detection()
    data_quality_assessment()
    statistical_summary_report()
    
    print("=== All statistical analysis examples completed! ===")