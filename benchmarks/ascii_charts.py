"""
ASCII-based visualization utilities for ArrPy benchmarks
Creates beautiful text-based charts that work without external dependencies
"""

import math
from colors import *

class ASCIICharts:
    """Create beautiful ASCII charts for benchmark visualization"""
    
    def __init__(self):
        self.width = 80
        self.height = 20
    
    def horizontal_bar_chart(self, data, title="Performance Comparison", max_width=60):
        """Create a horizontal bar chart using ASCII characters"""
        output = []
        
        # Add title
        output.append(header(title, char="═", color=Colors.BRIGHT_CYAN))
        output.append("")
        
        # Find max value for scaling
        max_val = max(data.values()) if data else 1
        
        for label, value in data.items():
            # Calculate bar length
            bar_length = int((value / max_val) * max_width)
            
            # Choose color based on value
            if value > max_val * 0.8:
                bar_color = Colors.BRIGHT_RED
                bar_char = "█"
            elif value > max_val * 0.5:
                bar_color = Colors.BRIGHT_YELLOW
                bar_char = "▓"
            else:
                bar_color = Colors.BRIGHT_GREEN
                bar_char = "░"
            
            # Create the bar
            bar = colorize(bar_char * bar_length, bar_color)
            
            # Format the line
            line = f"{label:<25} │{bar:<{max_width+20}} {format_speedup(value)}"
            output.append(line)
        
        return "\n".join(output)
    
    def performance_grid(self, matrix_data, row_labels, col_labels, title="Performance Matrix"):
        """Create a grid showing performance data"""
        output = []
        
        # Add title
        output.append(header(title, char="═", color=Colors.BRIGHT_MAGENTA))
        output.append("")
        
        # Header row
        header_row = "Operation" + " " * 15
        for col in col_labels:
            header_row += f"{col:>12}"
        output.append(colorize(header_row, Colors.BRIGHT_CYAN, style=Colors.BOLD))
        output.append("─" * len(header_row))
        
        # Data rows
        for i, row_label in enumerate(row_labels):
            row = f"{row_label:<25}"
            for j, col_label in enumerate(col_labels):
                if i < len(matrix_data) and j < len(matrix_data[i]):
                    value = matrix_data[i][j]
                    formatted_val = format_speedup(value)
                    row += f"{formatted_val:>12}"
                else:
                    row += f"{'N/A':>12}"
            output.append(row)
        
        return "\n".join(output)
    
    def ascii_line_chart(self, data_series, title="Performance Trend", height=15):
        """Create an ASCII line chart"""
        output = []
        
        # Add title
        output.append(header(title, char="═", color=Colors.BRIGHT_BLUE))
        output.append("")
        
        if not data_series:
            return "\n".join(output + ["No data available"])
        
        # Prepare data
        max_val = max(max(series['values']) for series in data_series.values())
        min_val = min(min(series['values']) for series in data_series.values())
        
        if max_val == min_val:
            max_val += 1
        
        # Create the chart
        chart_lines = [""] * height
        
        for y in range(height):
            line = ""
            threshold = min_val + (max_val - min_val) * (height - y - 1) / (height - 1)
            
            for x in range(len(list(data_series.values())[0]['values'])):
                char = " "
                for series_name, series_data in data_series.items():
                    if x < len(series_data['values']):
                        value = series_data['values'][x]
                        if abs(value - threshold) < (max_val - min_val) / height:
                            char = series_data.get('char', '*')
                            char = colorize(char, series_data.get('color', Colors.BRIGHT_WHITE))
                            break
                line += char
            
            # Add y-axis labels
            y_label = f"{threshold:6.2f} │"
            chart_lines[y] = colorize(y_label, Colors.DIM) + line
        
        output.extend(chart_lines)
        
        # Add x-axis
        x_axis = " " * 8 + "└" + "─" * len(list(data_series.values())[0]['values'])
        output.append(colorize(x_axis, Colors.DIM))
        
        # Add legend
        output.append("")
        output.append(colorize("Legend:", Colors.BRIGHT_WHITE, style=Colors.BOLD))
        for series_name, series_data in data_series.items():
            char = series_data.get('char', '*')
            color = series_data.get('color', Colors.BRIGHT_WHITE)
            output.append(f"  {colorize(char, color)} {series_name}")
        
        return "\n".join(output)
    
    def speedup_histogram(self, speedup_data, title="Speedup Distribution"):
        """Create a histogram showing speedup distribution"""
        output = []
        
        # Add title
        output.append(header(title, char="═", color=Colors.BRIGHT_YELLOW))
        output.append("")
        
        # Create bins
        bins = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, float('inf')]
        bin_labels = ['0.1-0.5x', '0.5-1.0x', '1.0-2.0x', '2.0-5.0x', '5.0-10x', '10x+']
        bin_counts = [0] * len(bin_labels)
        
        # Count values in bins
        for value in speedup_data:
            for i, bin_max in enumerate(bins[1:]):
                if value <= bin_max:
                    bin_counts[i] += 1
                    break
        
        # Find max count for scaling
        max_count = max(bin_counts) if bin_counts else 1
        
        # Create histogram
        for i, (label, count) in enumerate(zip(bin_labels, bin_counts)):
            bar_length = int((count / max_count) * 40) if max_count > 0 else 0
            
            # Choose color based on speedup range
            if i < 2:  # Competitive (ArrPy faster or close)
                color = Colors.BRIGHT_GREEN
                char = "█"
            elif i < 4:  # Moderate speedup
                color = Colors.BRIGHT_YELLOW
                char = "▓"
            else:  # High speedup (NumPy much faster)
                color = Colors.BRIGHT_RED
                char = "░"
            
            bar = colorize(char * bar_length, color)
            line = f"{label:<10} │{bar:<50} {count:>3} tests"
            output.append(line)
        
        return "\n".join(output)

def create_comprehensive_ascii_report(benchmark_results=None):
    """Create a comprehensive ASCII-based benchmark report"""
    charts = ASCIICharts()
    
    print(ascii_logo())
    print()
    
    # Sample data for demonstration
    category_performance = {
        "Array Creation": 2.5,
        "Arithmetic Ops": 1.8,
        "Matrix Operations": 15.2,
        "Aggregations": 3.4,
        "Math Functions": 8.7,
        "Comparisons": 2.1,
        "Logical Ops": 1.9,
        "Concatenation": 4.3
    }
    
    # Performance by category
    print(charts.horizontal_bar_chart(
        category_performance, 
        "📊 NumPy Speedup by Operation Category"
    ))
    print()
    
    # Performance matrix
    matrix_data = [
        [1.2, 2.1, 4.5],  # Array Creation
        [1.5, 2.8, 6.2],  # Arithmetic
        [5.2, 12.1, 25.8], # Matrix Ops
        [2.1, 3.4, 7.8],  # Aggregations
        [3.2, 6.7, 12.3]  # Math Functions
    ]
    
    row_labels = ["Array Creation", "Arithmetic", "Matrix Ops", "Aggregations", "Math Functions"]
    col_labels = ["Small", "Medium", "Large"]
    
    print(charts.performance_grid(
        matrix_data, row_labels, col_labels,
        "🎯 Performance Matrix: NumPy Speedup by Operation & Size"
    ))
    print()
    
    # Scaling trends
    sizes = list(range(10))
    data_series = {
        "ArrPy": {
            "values": [i * 0.1 + 0.5 for i in sizes],
            "char": "●",
            "color": Colors.BRIGHT_RED
        },
        "NumPy": {
            "values": [i * 0.05 + 0.1 for i in sizes],
            "char": "■",
            "color": Colors.BRIGHT_GREEN
        }
    }
    
    print(charts.ascii_line_chart(
        data_series,
        "📈 Performance Scaling Trend (Time vs Array Size)"
    ))
    print()
    
    # Speedup distribution
    sample_speedups = [0.8, 1.2, 1.5, 2.1, 2.8, 3.4, 4.2, 5.8, 8.9, 12.3, 15.7, 25.2] * 3
    
    print(charts.speedup_histogram(
        sample_speedups,
        "📈 Speedup Distribution Across All Tests"
    ))
    print()
    
    # Summary insights
    print(header("🎯 KEY PERFORMANCE INSIGHTS", char="═", color=Colors.BRIGHT_MAGENTA))
    print()
    print(f"  {success('✓ Array creation competitive for small arrays')}")
    print(f"  {warning('⚠ Matrix operations show largest performance gaps')}")
    print(f"  {info('ℹ Mathematical functions benefit from NumPy optimization')}")
    print(f"  {success('✓ ArrPy provides identical functionality in pure Python')}")
    print(f"  {highlight('🎯 Choose ArrPy for learning, NumPy for production', Colors.BRIGHT_CYAN)}")
    print()
    
    # Performance recommendations
    print(header("🚀 PERFORMANCE RECOMMENDATIONS", char="─", color=Colors.BRIGHT_GREEN))
    print()
    print(f"  🐍 {colorize('Use ArrPy when:', Colors.BRIGHT_YELLOW, style=Colors.BOLD)}")
    print(f"     • Learning array programming concepts")
    print(f"     • Prototyping with small datasets")
    print(f"     • NumPy is not available in environment")
    print(f"     • Understanding algorithm implementations")
    print()
    print(f"  🚀 {colorize('Use NumPy when:', Colors.BRIGHT_GREEN, style=Colors.BOLD)}")
    print(f"     • Performance is critical")
    print(f"     • Working with large arrays")
    print(f"     • Production applications")
    print(f"     • Advanced mathematical operations needed")
    print()
    
    print(f"{colorize('🎉 Benchmark visualization completed! 🎉', Colors.BRIGHT_CYAN, style=Colors.BOLD)}")

if __name__ == "__main__":
    create_comprehensive_ascii_report()