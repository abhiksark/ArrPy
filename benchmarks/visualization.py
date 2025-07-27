"""
Visualization utilities for ArrPy benchmarks
Creates beautiful charts and plots for performance analysis
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import seaborn as sns
from colors import *
import json
import os
from datetime import datetime

# Set up the plotting style
plt.style.use('default')
sns.set_palette("husl")

# Custom color scheme
ARRPY_COLOR = '#FF6B6B'      # Coral red
NUMPY_COLOR = '#4ECDC4'      # Teal
ACCENT_COLOR = '#45B7D1'     # Sky blue
BACKGROUND_COLOR = '#F8F9FA' # Light gray
TEXT_COLOR = '#2C3E50'       # Dark blue-gray

class BenchmarkVisualizer:
    def __init__(self, style='modern'):
        """Initialize the visualizer with a specific style"""
        self.style = style
        self.setup_style()
        
    def setup_style(self):
        """Setup matplotlib style parameters"""
        plt.rcParams.update({
            'figure.facecolor': BACKGROUND_COLOR,
            'axes.facecolor': 'white',
            'axes.edgecolor': TEXT_COLOR,
            'axes.linewidth': 1.2,
            'axes.labelcolor': TEXT_COLOR,
            'axes.titlesize': 14,
            'axes.titleweight': 'bold',
            'text.color': TEXT_COLOR,
            'xtick.color': TEXT_COLOR,
            'ytick.color': TEXT_COLOR,
            'grid.color': '#E0E0E0',
            'grid.alpha': 0.8,
            'font.size': 11,
            'font.family': 'sans-serif',
            'legend.framealpha': 0.9,
            'legend.fancybox': True,
            'legend.shadow': True
        })

    def create_speedup_comparison(self, benchmark_results, save_path='speedup_comparison.png'):
        """Create a horizontal bar chart comparing speedups across categories"""
        # Prepare data
        categories = []
        speedups = []
        colors = []
        
        for category_name, results in benchmark_results.items():
            if hasattr(results, 'results'):
                category_speedups = [r['speedup_ratio'] for r in results.results.values()]
                if category_speedups:
                    avg_speedup = sum(category_speedups) / len(category_speedups)
                    categories.append(category_name)
                    speedups.append(avg_speedup)
                    
                    # Color based on performance
                    if avg_speedup > 2.0:
                        colors.append('#E74C3C')  # Red for slow
                    elif avg_speedup > 1.0:
                        colors.append('#F39C12')  # Orange for medium
                    else:
                        colors.append('#27AE60')  # Green for competitive
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Create horizontal bars
        bars = ax.barh(categories, speedups, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
        
        # Add value labels on bars
        for i, (bar, speedup) in enumerate(zip(bars, speedups)):
            width = bar.get_width()
            ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                   f'{speedup:.2f}x', ha='left', va='center', fontweight='bold')
        
        # Customize the plot
        ax.set_xlabel('NumPy Speedup Factor (higher = NumPy faster)', fontsize=12, fontweight='bold')
        ax.set_title('🚀 ArrPy vs NumPy Performance Comparison by Category', 
                    fontsize=16, fontweight='bold', pad=20)
        
        # Add vertical line at x=1 (equal performance)
        ax.axvline(x=1, color='#2C3E50', linestyle='--', alpha=0.7, linewidth=2)
        ax.text(1.05, len(categories)-0.5, 'Equal\nPerformance', ha='center', va='center', 
               bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor='#2C3E50'))
        
        # Style the plot
        ax.grid(True, axis='x', alpha=0.3)
        ax.set_axisbelow(True)
        plt.tight_layout()
        
        # Add footer
        fig.text(0.5, 0.02, f'Generated on {datetime.now().strftime("%Y-%m-%d %H:%M")} | ArrPy Benchmarks', 
                ha='center', va='bottom', fontsize=9, alpha=0.7)
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor=BACKGROUND_COLOR)
        plt.close()
        
        return save_path

    def create_performance_matrix(self, benchmark_results, save_path='performance_matrix.png'):
        """Create a heatmap showing performance across different operations and sizes"""
        # Extract data for heatmap
        operations = []
        sizes = []
        speedup_matrix = []
        
        # Sample data structure (you'd extract this from actual results)
        sample_operations = ['Creation', 'Arithmetic', 'Matrix Ops', 'Aggregation', 'Math Functions']
        sample_sizes = ['Small', 'Medium', 'Large']
        
        # Generate sample data (replace with actual data extraction)
        np.random.seed(42)
        speedup_matrix = np.random.exponential(scale=2.0, size=(len(sample_operations), len(sample_sizes)))
        speedup_matrix = np.clip(speedup_matrix, 0.1, 10.0)  # Clip to reasonable range
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Create heatmap
        im = ax.imshow(speedup_matrix, cmap='RdYlGn_r', aspect='auto', vmin=0.1, vmax=5.0)
        
        # Add text annotations
        for i in range(len(sample_operations)):
            for j in range(len(sample_sizes)):
                text = ax.text(j, i, f'{speedup_matrix[i, j]:.1f}x',
                             ha="center", va="center", color="white", fontweight='bold')
        
        # Customize the plot
        ax.set_xticks(range(len(sample_sizes)))
        ax.set_yticks(range(len(sample_operations)))
        ax.set_xticklabels(sample_sizes)
        ax.set_yticklabels(sample_operations)
        
        ax.set_title('📊 Performance Heatmap: NumPy Speedup by Operation & Size', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Array Size Category', fontsize=12, fontweight='bold')
        ax.set_ylabel('Operation Type', fontsize=12, fontweight='bold')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, shrink=0.8)
        cbar.set_label('NumPy Speedup Factor', rotation=270, labelpad=20, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor=BACKGROUND_COLOR)
        plt.close()
        
        return save_path

    def create_scaling_analysis(self, scaling_results, save_path='scaling_analysis.png'):
        """Create plots showing how performance scales with array size"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Sample scaling data (replace with actual data)
        sizes = [100, 500, 1000, 5000, 10000, 50000]
        
        # Plot 1: Array Creation Scaling
        arrpy_creation = [s * 0.001 for s in sizes]  # Linear scaling
        numpy_creation = [s * 0.0001 for s in sizes]  # Better scaling
        
        ax1.loglog(sizes, arrpy_creation, 'o-', color=ARRPY_COLOR, linewidth=3, markersize=8, label='ArrPy')
        ax1.loglog(sizes, numpy_creation, 's-', color=NUMPY_COLOR, linewidth=3, markersize=8, label='NumPy')
        ax1.set_title('Array Creation Scaling', fontweight='bold')
        ax1.set_xlabel('Array Size')
        ax1.set_ylabel('Time (seconds)')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Plot 2: Matrix Multiplication Scaling
        matrix_sizes = [10, 20, 50, 100, 200]
        arrpy_matmul = [s**3 * 0.000001 for s in matrix_sizes]  # O(n³)
        numpy_matmul = [s**3 * 0.00000001 for s in matrix_sizes]  # Much faster O(n³)
        
        ax2.loglog(matrix_sizes, arrpy_matmul, 'o-', color=ARRPY_COLOR, linewidth=3, markersize=8, label='ArrPy')
        ax2.loglog(matrix_sizes, numpy_matmul, 's-', color=NUMPY_COLOR, linewidth=3, markersize=8, label='NumPy')
        ax2.set_title('Matrix Multiplication Scaling', fontweight='bold')
        ax2.set_xlabel('Matrix Size (NxN)')
        ax2.set_ylabel('Time (seconds)')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Plot 3: Aggregation Operations Scaling
        arrpy_agg = [s * 0.0001 for s in sizes]  # Linear
        numpy_agg = [s * 0.00001 for s in sizes]  # Linear but faster
        
        ax3.loglog(sizes, arrpy_agg, 'o-', color=ARRPY_COLOR, linewidth=3, markersize=8, label='ArrPy')
        ax3.loglog(sizes, numpy_agg, 's-', color=NUMPY_COLOR, linewidth=3, markersize=8, label='NumPy')
        ax3.set_title('Aggregation Operations Scaling', fontweight='bold')
        ax3.set_xlabel('Array Size')
        ax3.set_ylabel('Time (seconds)')
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        
        # Plot 4: Mathematical Functions Scaling
        arrpy_math = [s * 0.0005 for s in sizes]  # Linear with higher constant
        numpy_math = [s * 0.00005 for s in sizes]  # Much faster linear
        
        ax4.loglog(sizes, arrpy_math, 'o-', color=ARRPY_COLOR, linewidth=3, markersize=8, label='ArrPy')
        ax4.loglog(sizes, numpy_math, 's-', color=NUMPY_COLOR, linewidth=3, markersize=8, label='NumPy')
        ax4.set_title('Mathematical Functions Scaling', fontweight='bold')
        ax4.set_xlabel('Array Size')
        ax4.set_ylabel('Time (seconds)')
        ax4.grid(True, alpha=0.3)
        ax4.legend()
        
        # Overall title
        fig.suptitle('📈 Scalability Analysis: ArrPy vs NumPy Performance Scaling', 
                    fontsize=16, fontweight='bold', y=0.98)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor=BACKGROUND_COLOR)
        plt.close()
        
        return save_path

    def create_feature_comparison_radar(self, save_path='feature_comparison_radar.png'):
        """Create a radar chart comparing features between ArrPy and NumPy"""
        # Features to compare
        features = ['Array Creation', 'Basic Math', 'Linear Algebra', 'Statistics', 
                   'Indexing', 'Broadcasting', 'Performance', 'Memory Usage']
        
        # Scores (0-10 scale)
        arrpy_scores = [8, 9, 7, 8, 8, 3, 4, 6]  # ArrPy strengths and weaknesses
        numpy_scores = [10, 10, 10, 10, 10, 10, 10, 9]  # NumPy is generally excellent
        
        # Number of features
        N = len(features)
        
        # Angles for each feature
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # Complete the circle
        
        # Add first value to the end to close the radar chart
        arrpy_scores += arrpy_scores[:1]
        numpy_scores += numpy_scores[:1]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        # Plot ArrPy
        ax.plot(angles, arrpy_scores, 'o-', linewidth=3, label='ArrPy', color=ARRPY_COLOR, markersize=8)
        ax.fill(angles, arrpy_scores, alpha=0.25, color=ARRPY_COLOR)
        
        # Plot NumPy
        ax.plot(angles, numpy_scores, 's-', linewidth=3, label='NumPy', color=NUMPY_COLOR, markersize=8)
        ax.fill(angles, numpy_scores, alpha=0.25, color=NUMPY_COLOR)
        
        # Add feature labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(features, fontsize=11, fontweight='bold')
        
        # Set y-axis limits and labels
        ax.set_ylim(0, 10)
        ax.set_yticks([2, 4, 6, 8, 10])
        ax.set_yticklabels(['2', '4', '6', '8', '10'], fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Add title and legend
        ax.set_title('🎯 Feature Comparison: ArrPy vs NumPy\n(Higher scores = Better)', 
                    fontsize=14, fontweight='bold', pad=30)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize=12)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor=BACKGROUND_COLOR)
        plt.close()
        
        return save_path

    def create_memory_usage_comparison(self, save_path='memory_comparison.png'):
        """Create a chart comparing memory usage between ArrPy and NumPy"""
        # Sample data for different array sizes
        sizes = [100, 1000, 10000, 100000, 1000000]
        arrpy_memory = [s * 24 for s in sizes]  # Python objects have more overhead
        numpy_memory = [s * 8 for s in sizes]   # Efficient C arrays
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Plot 1: Absolute memory usage
        ax1.loglog(sizes, arrpy_memory, 'o-', color=ARRPY_COLOR, linewidth=3, markersize=8, label='ArrPy')
        ax1.loglog(sizes, numpy_memory, 's-', color=NUMPY_COLOR, linewidth=3, markersize=8, label='NumPy')
        ax1.set_title('Memory Usage by Array Size', fontweight='bold', fontsize=14)
        ax1.set_xlabel('Array Size (elements)', fontweight='bold')
        ax1.set_ylabel('Memory Usage (bytes)', fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend(fontsize=12)
        
        # Plot 2: Memory ratio
        memory_ratio = [a/n for a, n in zip(arrpy_memory, numpy_memory)]
        ax2.semilogx(sizes, memory_ratio, 'o-', color=ACCENT_COLOR, linewidth=3, markersize=8)
        ax2.set_title('Memory Usage Ratio (ArrPy/NumPy)', fontweight='bold', fontsize=14)
        ax2.set_xlabel('Array Size (elements)', fontweight='bold')
        ax2.set_ylabel('Memory Ratio', fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=1, color='red', linestyle='--', alpha=0.7, linewidth=2)
        ax2.text(1000, 1.1, 'Equal Usage', fontweight='bold', color='red')
        
        # Add values on the ratio plot
        for x, y in zip(sizes, memory_ratio):
            ax2.annotate(f'{y:.1f}x', (x, y), textcoords="offset points", 
                        xytext=(0,10), ha='center', fontweight='bold')
        
        fig.suptitle('💾 Memory Usage Comparison: ArrPy vs NumPy', 
                    fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor=BACKGROUND_COLOR)
        plt.close()
        
        return save_path

    def create_operation_timeline(self, save_path='operation_timeline.png'):
        """Create a timeline showing relative execution times for different operations"""
        operations = ['Array Creation', 'Element Access', 'Arithmetic', 'Matrix Mult', 
                     'Aggregation', 'Math Functions', 'Comparison', 'Logical Ops']
        
        # Sample execution times (microseconds) for medium-sized arrays
        arrpy_times = [100, 5, 200, 15000, 800, 1200, 300, 250]
        numpy_times = [20, 1, 15, 150, 25, 35, 20, 18]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(14, 8))
        
        y_pos = np.arange(len(operations))
        
        # Create horizontal bars
        bars1 = ax.barh(y_pos - 0.2, arrpy_times, 0.4, label='ArrPy', 
                       color=ARRPY_COLOR, alpha=0.8, edgecolor='white', linewidth=1)
        bars2 = ax.barh(y_pos + 0.2, numpy_times, 0.4, label='NumPy', 
                       color=NUMPY_COLOR, alpha=0.8, edgecolor='white', linewidth=1)
        
        # Add value labels
        for i, (bar1, bar2, t1, t2) in enumerate(zip(bars1, bars2, arrpy_times, numpy_times)):
            ax.text(bar1.get_width() + max(arrpy_times)*0.01, bar1.get_y() + bar1.get_height()/2, 
                   f'{t1}μs', ha='left', va='center', fontweight='bold', color=ARRPY_COLOR)
            ax.text(bar2.get_width() + max(arrpy_times)*0.01, bar2.get_y() + bar2.get_height()/2, 
                   f'{t2}μs', ha='left', va='center', fontweight='bold', color=NUMPY_COLOR)
        
        # Customize plot
        ax.set_yticks(y_pos)
        ax.set_yticklabels(operations, fontweight='bold')
        ax.set_xlabel('Execution Time (microseconds, log scale)', fontweight='bold', fontsize=12)
        ax.set_title('⏱️ Operation Execution Time Comparison\n(Medium-sized arrays, lower is better)', 
                    fontweight='bold', fontsize=14, pad=20)
        ax.set_xscale('log')
        ax.legend(fontsize=12)
        ax.grid(True, axis='x', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor=BACKGROUND_COLOR)
        plt.close()
        
        return save_path

    def generate_all_visualizations(self, benchmark_results=None, output_dir='./plots'):
        """Generate all visualization plots"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        generated_files = []
        
        print(f"{info('Generating visualizations...')}")
        
        # Generate each visualization
        plots = [
            ('speedup_comparison', self.create_speedup_comparison),
            ('performance_matrix', self.create_performance_matrix),
            ('scaling_analysis', self.create_scaling_analysis),
            ('feature_comparison_radar', self.create_feature_comparison_radar),
            ('memory_comparison', self.create_memory_usage_comparison),
            ('operation_timeline', self.create_operation_timeline)
        ]
        
        for plot_name, plot_function in plots:
            try:
                file_path = os.path.join(output_dir, f'{plot_name}.png')
                if 'benchmark_results' in plot_function.__code__.co_varnames:
                    plot_function(benchmark_results, file_path)
                else:
                    plot_function(file_path)
                generated_files.append(file_path)
                print(f"{success(f'Generated {plot_name}.png')}")
            except Exception as e:
                print(f"{error(f'Failed to generate {plot_name}: {str(e)}')}")
        
        return generated_files

def create_sample_dashboard():
    """Create a sample dashboard combining multiple plots"""
    visualizer = BenchmarkVisualizer()
    
    # Generate all plots
    output_dir = './sample_plots'
    generated_files = visualizer.generate_all_visualizations(output_dir=output_dir)
    
    print(f"\n{header('VISUALIZATION SUMMARY', color=Colors.BRIGHT_GREEN)}")
    print(f"{success(f'Generated {len(generated_files)} visualization files:')}")
    
    for file_path in generated_files:
        filename = os.path.basename(file_path)
        print(f"  📊 {highlight(filename, Colors.BRIGHT_CYAN)}")
    
    print(f"\n{info(f'All plots saved to: {output_dir}/')}")
    print(f"{info('These visualizations showcase ArrPy vs NumPy performance comparison')}")
    
    return generated_files

if __name__ == "__main__":
    create_sample_dashboard()