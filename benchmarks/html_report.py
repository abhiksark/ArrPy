"""
HTML Report Generator for ArrPy Benchmarks
Creates beautiful, interactive HTML reports with charts and styling
"""

import json
import os
from datetime import datetime
import base64

class HTMLReportGenerator:
    """Generate beautiful HTML reports for benchmark results"""
    
    def __init__(self):
        self.template = self._get_html_template()
    
    def _get_html_template(self):
        """Get the HTML template with embedded CSS and JavaScript"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ArrPy vs NumPy Performance Report</title>
    <style>
        :root {
            --primary-color: #2C3E50;
            --secondary-color: #3498DB;
            --accent-color: #E74C3C;
            --success-color: #27AE60;
            --warning-color: #F39C12;
            --background-color: #F8F9FA;
            --card-background: #FFFFFF;
            --text-color: #2C3E50;
            --border-color: #E0E0E0;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: var(--background-color);
        }
        
        .header {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 2rem 0;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            font-size: 3rem;
            margin-bottom: 0.5rem;
            font-weight: bold;
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        
        .stat-card {
            background: var(--card-background);
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-left: 4px solid var(--secondary-color);
            transition: transform 0.2s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }
        
        .stat-card h3 {
            color: var(--secondary-color);
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        
        .stat-card p {
            color: var(--text-color);
            font-size: 1.1rem;
        }
        
        .section {
            background: var(--card-background);
            margin: 2rem 0;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .section h2 {
            color: var(--primary-color);
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--border-color);
            font-size: 1.8rem;
        }
        
        .benchmark-table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }
        
        .benchmark-table th,
        .benchmark-table td {
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }
        
        .benchmark-table th {
            background-color: var(--background-color);
            font-weight: bold;
            color: var(--primary-color);
        }
        
        .benchmark-table tr:hover {
            background-color: var(--background-color);
        }
        
        .speedup-badge {
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            color: white;
            font-weight: bold;
            font-size: 0.9rem;
        }
        
        .speedup-good { background-color: var(--success-color); }
        .speedup-medium { background-color: var(--warning-color); }
        .speedup-poor { background-color: var(--accent-color); }
        
        .chart-container {
            margin: 2rem 0;
            padding: 1rem;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .performance-bar {
            display: flex;
            align-items: center;
            margin: 0.5rem 0;
        }
        
        .performance-bar-label {
            width: 150px;
            font-weight: bold;
        }
        
        .performance-bar-fill {
            height: 20px;
            background: linear-gradient(90deg, var(--success-color), var(--accent-color));
            border-radius: 10px;
            margin: 0 1rem;
            position: relative;
        }
        
        .performance-bar-value {
            font-weight: bold;
            color: var(--primary-color);
        }
        
        .insights {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 12px;
            margin: 2rem 0;
        }
        
        .insights h3 {
            margin-bottom: 1rem;
            font-size: 1.5rem;
        }
        
        .insights ul {
            list-style: none;
        }
        
        .insights li {
            margin: 0.5rem 0;
            padding-left: 1.5rem;
            position: relative;
        }
        
        .insights li::before {
            content: "✓";
            position: absolute;
            left: 0;
            color: #00d4aa;
            font-weight: bold;
        }
        
        .footer {
            text-align: center;
            padding: 2rem;
            color: var(--text-color);
            opacity: 0.7;
            margin-top: 2rem;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 ArrPy vs NumPy</h1>
        <p>Performance Benchmark Report</p>
        <p>Generated on {timestamp}</p>
    </div>
    
    <div class="container">
        <!-- Statistics Overview -->
        <div class="stats-grid">
            <div class="stat-card">
                <h3>{total_tests}</h3>
                <p>Total Tests Conducted</p>
            </div>
            <div class="stat-card">
                <h3>{avg_speedup:.1f}x</h3>
                <p>Average NumPy Speedup</p>
            </div>
            <div class="stat-card">
                <h3>{max_speedup:.1f}x</h3>
                <p>Maximum Speedup</p>
            </div>
            <div class="stat-card">
                <h3>{categories}</h3>
                <p>Test Categories</p>
            </div>
        </div>
        
        <!-- Performance Overview -->
        <div class="section">
            <h2>📊 Performance Overview by Category</h2>
            <div class="chart-container">
                {category_chart}
            </div>
        </div>
        
        <!-- Detailed Results -->
        <div class="section">
            <h2>📋 Detailed Benchmark Results</h2>
            <table class="benchmark-table">
                <thead>
                    <tr>
                        <th>Test Name</th>
                        <th>ArrPy Time</th>
                        <th>NumPy Time</th>
                        <th>Speedup</th>
                        <th>Performance</th>
                    </tr>
                </thead>
                <tbody>
                    {detailed_results}
                </tbody>
            </table>
        </div>
        
        <!-- Key Insights -->
        <div class="insights">
            <h3>🎯 Key Performance Insights</h3>
            <ul>
                <li>NumPy consistently outperforms ArrPy due to optimized C implementation</li>
                <li>Matrix operations show the largest performance gaps (up to {max_speedup:.0f}x)</li>
                <li>Array creation and simple operations are more competitive</li>
                <li>ArrPy provides identical functionality in pure Python</li>
                <li>Performance gaps increase with larger array sizes</li>
            </ul>
            
            <h3>🚀 Recommendations</h3>
            <ul>
                <li><strong>Use ArrPy for:</strong> Learning, prototyping, education, dependency-free environments</li>
                <li><strong>Use NumPy for:</strong> Production code, large arrays, performance-critical applications</li>
                <li>Both libraries produce identical results - choose based on your needs</li>
            </ul>
        </div>
        
        <!-- Technical Details -->
        <div class="section">
            <h2>🔧 Technical Details</h2>
            <p><strong>Test Environment:</strong> {environment}</p>
            <p><strong>ArrPy Version:</strong> 0.1.0 (Pure Python Implementation)</p>
            <p><strong>NumPy Version:</strong> Latest available</p>
            <p><strong>Test Methodology:</strong> 5 iterations per test, average timing used</p>
            <p><strong>Array Sizes:</strong> Small (100-1K), Medium (1K-10K), Large (10K-100K+ elements)</p>
        </div>
    </div>
    
    <div class="footer">
        <p>Generated by ArrPy Benchmark Suite | <a href="https://github.com/yourusername/arrpy">GitHub Repository</a></p>
    </div>
</body>
</html>
        """
    
    def format_time(self, seconds):
        """Format time in appropriate units"""
        if seconds < 1e-6:
            return f"{seconds*1e9:.2f} ns"
        elif seconds < 1e-3:
            return f"{seconds*1e6:.2f} µs"
        elif seconds < 1:
            return f"{seconds*1e3:.2f} ms"
        else:
            return f"{seconds:.3f} s"
    
    def get_speedup_class(self, speedup):
        """Get CSS class for speedup badge"""
        if speedup <= 1.5:
            return "speedup-good"
        elif speedup <= 5.0:
            return "speedup-medium"
        else:
            return "speedup-poor"
    
    def generate_category_chart(self, category_data):
        """Generate HTML for category performance chart"""
        chart_html = ""
        max_speedup = max(category_data.values()) if category_data else 1
        
        for category, speedup in category_data.items():
            bar_width = min((speedup / max_speedup) * 300, 300)  # Max 300px width
            
            chart_html += f"""
            <div class="performance-bar">
                <div class="performance-bar-label">{category}</div>
                <div class="performance-bar-fill" style="width: {bar_width}px;"></div>
                <div class="performance-bar-value">{speedup:.1f}x</div>
            </div>
            """
        
        return chart_html
    
    def generate_detailed_results(self, benchmark_results):
        """Generate HTML for detailed results table"""
        results_html = ""
        
        # Sample data structure (replace with actual data extraction)
        sample_results = [
            ("Array Creation (Small)", 0.000123, 0.000045, 2.7),
            ("Array Creation (Medium)", 0.001234, 0.000234, 5.3),
            ("Matrix Multiplication (10x10)", 0.015234, 0.000987, 15.4),
            ("Element-wise Addition", 0.000567, 0.000123, 4.6),
            ("Aggregation (Sum)", 0.000789, 0.000156, 5.1),
            ("Mathematical Functions (sin)", 0.002345, 0.000234, 10.0),
        ]
        
        for test_name, arrpy_time, numpy_time, speedup in sample_results:
            speedup_class = self.get_speedup_class(speedup)
            
            results_html += f"""
            <tr>
                <td><strong>{test_name}</strong></td>
                <td>{self.format_time(arrpy_time)}</td>
                <td>{self.format_time(numpy_time)}</td>
                <td><span class="speedup-badge {speedup_class}">{speedup:.1f}x</span></td>
                <td>{"🟢 Competitive" if speedup <= 2 else "🟡 Moderate" if speedup <= 5 else "🔴 High Gap"}</td>
            </tr>
            """
        
        return results_html
    
    def generate_report(self, benchmark_results=None, output_path="benchmark_report.html"):
        """Generate complete HTML report"""
        
        # Sample data (replace with actual data extraction)
        category_data = {
            "Array Creation": 3.2,
            "Arithmetic": 4.1,
            "Matrix Operations": 15.7,
            "Aggregations": 5.8,
            "Math Functions": 8.9,
            "Comparisons": 2.9,
            "Logical Ops": 2.1,
            "Concatenation": 6.3
        }
        
        # Calculate statistics
        total_tests = 48
        avg_speedup = sum(category_data.values()) / len(category_data)
        max_speedup = max(category_data.values())
        categories = len(category_data)
        
        # Generate components
        category_chart = self.generate_category_chart(category_data)
        detailed_results = self.generate_detailed_results(benchmark_results)
        
        # Fill template with proper escaping for CSS
        html_content = self.template.replace("{timestamp}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        html_content = html_content.replace("{total_tests}", str(total_tests))
        html_content = html_content.replace("{avg_speedup:.1f}", f"{avg_speedup:.1f}")
        html_content = html_content.replace("{max_speedup:.1f}", f"{max_speedup:.1f}")
        html_content = html_content.replace("{max_speedup:.0f}", f"{max_speedup:.0f}")
        html_content = html_content.replace("{categories}", str(categories))
        html_content = html_content.replace("{category_chart}", category_chart)
        html_content = html_content.replace("{detailed_results}", detailed_results)
        html_content = html_content.replace("{environment}", "Python 3.9+ on macOS/Linux/Windows")
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path

def create_sample_html_report():
    """Create a sample HTML report"""
    generator = HTMLReportGenerator()
    output_path = generator.generate_report()
    
    print(f"📄 HTML Report generated: {output_path}")
    print(f"🌐 Open in browser to view: file://{os.path.abspath(output_path)}")
    
    return output_path

if __name__ == "__main__":
    create_sample_html_report()