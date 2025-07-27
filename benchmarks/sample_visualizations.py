"""
Sample visualization demonstrations for ArrPy benchmarks
Shows colored terminal output, ASCII charts, and report generation
"""

import os
import time
from colors import *
from ascii_charts import ASCIICharts

def demo_colored_benchmark_output():
    """Demonstrate colorized benchmark output"""
    print(ascii_logo())
    print()
    
    # Simulate benchmark run with colors
    print(header("🚀 ARRPY BENCHMARK DEMONSTRATION", char="═", color=Colors.BRIGHT_CYAN))
    print()
    
    # Simulate running benchmarks
    operations = [
        ("Array Creation (1000 elements)", 0.000123, 0.000045, 2.7),
        ("Element-wise Addition", 0.000567, 0.000123, 4.6),
        ("Matrix Multiplication (50x50)", 0.015234, 0.000987, 15.4),
        ("Aggregation (Sum)", 0.000789, 0.000156, 5.1),
        ("Mathematical Functions (sin)", 0.002345, 0.000234, 10.0),
        ("Array Comparison", 0.000456, 0.000234, 1.9),
    ]
    
    print(subheader("Running Performance Tests", color=Colors.BRIGHT_BLUE))
    print()
    
    for i, (name, arrpy_time, numpy_time, speedup) in enumerate(operations):
        print(f"{info('Running')} {name}... ", end="", flush=True)
        
        # Simulate progress
        for j in range(5):
            print(f"\r{info('Running')} {name}... {progress_bar(j+1, 5)}", end="", flush=True)
            time.sleep(0.1)
        
        print(f"\r{benchmark_result_line(name, arrpy_time, numpy_time, speedup)}")
        time.sleep(0.1)
    
    print()
    print(success("✅ All benchmarks completed successfully!"))
    print()

def demo_ascii_charts():
    """Demonstrate ASCII chart capabilities"""
    charts = ASCIICharts()
    
    print(header("📊 ASCII CHART DEMONSTRATIONS", char="═", color=Colors.BRIGHT_GREEN))
    print()
    
    # Performance comparison chart
    performance_data = {
        "Array Creation": 2.3,
        "Arithmetic": 3.8,
        "Matrix Ops": 12.7,
        "Aggregations": 4.2,
        "Math Functions": 7.9
    }
    
    print(charts.horizontal_bar_chart(performance_data, "NumPy Speedup by Category"))
    print()
    
    # Performance matrix
    matrix_data = [
        [1.5, 2.8, 5.2],
        [2.1, 4.3, 8.7],
        [6.8, 15.2, 31.4]
    ]
    
    print(charts.performance_grid(
        matrix_data, 
        ["Small Arrays", "Medium Arrays", "Large Arrays"],
        ["Creation", "Arithmetic", "Advanced"],
        "Performance Matrix: Size vs Operation"
    ))
    print()

def demo_status_messages():
    """Demonstrate various status message types"""
    print(header("💬 STATUS MESSAGE DEMONSTRATIONS", char="═", color=Colors.BRIGHT_YELLOW))
    print()
    
    print(success("Benchmark suite initialized successfully"))
    print(info("Loading test data and preparing arrays..."))
    print(warning("Performance may vary based on system specifications"))
    print(error("Failed to load optional visualization dependencies"))
    print()
    
    print(f"Performance Summary:")
    print(f"  • Average speedup: {format_speedup(5.7)}")
    print(f"  • Best case: {format_speedup(1.2)}")
    print(f"  • Worst case: {format_speedup(25.8)}")
    print()
    
    print(f"Timing Examples:")
    print(f"  • Very fast: {format_time(123e-9)}")
    print(f"  • Fast: {format_time(567e-6)}")
    print(f"  • Medium: {format_time(234e-3)}")
    print(f"  • Slow: {format_time(1.23)}")
    print()

def demo_progress_and_tables():
    """Demonstrate progress bars and table formatting"""
    print(header("📈 PROGRESS & TABLE DEMONSTRATIONS", char="═", color=Colors.BRIGHT_MAGENTA))
    print()
    
    # Progress bar demo
    print(f"{highlight('Progress Bar Examples:', Colors.BRIGHT_CYAN)}")
    print(f"Starting:  {progress_bar(1, 10)}")
    print(f"Progress:  {progress_bar(3, 10)}")
    print(f"Halfway:   {progress_bar(5, 10)}")
    print(f"Almost:    {progress_bar(8, 10)}")
    print(f"Complete:  {progress_bar(10, 10)}")
    print()
    
    # Table formatting demo
    print(f"{highlight('Table Formatting Example:', Colors.BRIGHT_CYAN)}")
    columns = ["Operation", "ArrPy Time", "NumPy Time", "Speedup"]
    widths = [25, 12, 12, 10]
    colors = [Colors.BRIGHT_CYAN, Colors.BLUE, Colors.MAGENTA, Colors.BRIGHT_YELLOW]
    
    # Header
    print(table_row(columns, widths, colors))
    print("─" * sum(widths))
    
    # Data rows
    sample_data = [
        ["Array Creation", "123.5 μs", "45.2 μs", "2.7x"],
        ["Matrix Multiply", "15.2 ms", "987 μs", "15.4x"],
        ["Aggregation", "789 μs", "156 μs", "5.1x"]
    ]
    
    for row in sample_data:
        print(table_row(row, widths))
    print()

def create_comprehensive_demo():
    """Create a comprehensive demonstration of all visual features"""
    print(f"{colorize('🎨 ARRPY BENCHMARK VISUALIZATION SHOWCASE 🎨', Colors.BRIGHT_WHITE, style=[Colors.BOLD, Colors.UNDERLINE])}")
    print()
    
    # Demo sections
    sections = [
        ("Colored Benchmark Output", demo_colored_benchmark_output),
        ("ASCII Charts", demo_ascii_charts),
        ("Status Messages", demo_status_messages),
        ("Progress & Tables", demo_progress_and_tables)
    ]
    
    for i, (section_name, demo_func) in enumerate(sections):
        print(f"\n{colorize(f'═══ Section {i+1}/4: {section_name} ═══', Colors.BRIGHT_WHITE, style=Colors.BOLD)}")
        print()
        demo_func()
        
        if i < len(sections) - 1:
            print(f"\n{dim('Press Enter to continue to next section...')}")
            input()
    
    # Final summary
    print(header("🎉 DEMONSTRATION COMPLETE", char="═", color=Colors.BRIGHT_GREEN))
    print()
    print(f"{success('✅ All visualization features demonstrated successfully!')}")
    print()
    print(f"{highlight('Available Features:', Colors.BRIGHT_CYAN)}")
    print(f"  🎨 {colorize('Colorized terminal output with ANSI colors', Colors.BRIGHT_YELLOW)}")
    print(f"  📊 {colorize('ASCII-based charts and graphs', Colors.BRIGHT_BLUE)}")
    print(f"  📋 {colorize('Formatted tables and progress bars', Colors.BRIGHT_MAGENTA)}")
    print(f"  📄 {colorize('HTML report generation', Colors.BRIGHT_GREEN)}")
    print(f"  🎯 {colorize('Performance analysis and insights', Colors.BRIGHT_RED)}")
    print()
    print(f"{info('Use these tools to create beautiful, informative benchmark reports!')}")

if __name__ == "__main__":
    create_comprehensive_demo()