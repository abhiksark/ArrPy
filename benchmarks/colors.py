"""
Color utilities for enhanced benchmark output
"""

import sys
import os

class Colors:
    """ANSI color codes for terminal output"""
    # Basic colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    # Additional whites
    BRIGHT_WHITE = '\033[97m'
    
    # Bright colors
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    
    # Background colors
    BG_RED = '\033[101m'
    BG_GREEN = '\033[102m'
    BG_YELLOW = '\033[103m'
    BG_BLUE = '\033[104m'
    BG_MAGENTA = '\033[105m'
    BG_CYAN = '\033[106m'
    
    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    STRIKETHROUGH = '\033[9m'
    
    # Reset
    RESET = '\033[0m'
    END = '\033[0m'

def supports_color():
    """Check if the terminal supports color output"""
    return (
        hasattr(sys.stdout, "isatty") and sys.stdout.isatty() and
        os.environ.get("TERM") != "dumb" and
        os.environ.get("NO_COLOR") is None
    )

def colorize(text, color=None, bg_color=None, style=None):
    """Apply colors and styles to text"""
    if not supports_color():
        return text
    
    codes = []
    if color:
        codes.append(color)
    if bg_color:
        codes.append(bg_color)
    if style:
        if isinstance(style, list):
            codes.extend(style)
        else:
            codes.append(style)
    
    if codes:
        return f"{''.join(codes)}{text}{Colors.RESET}"
    return text

def header(text, char="=", color=Colors.BRIGHT_CYAN):
    """Create a colored header"""
    width = max(len(text) + 4, 80)
    border = char * width
    header_text = f"{text:^{width}}"
    
    return f"\n{colorize(border, color, style=Colors.BOLD)}\n{colorize(header_text, color, style=Colors.BOLD)}\n{colorize(border, color, style=Colors.BOLD)}"

def subheader(text, char="-", color=Colors.BRIGHT_BLUE):
    """Create a colored subheader"""
    width = max(len(text) + 4, 60)
    border = char * width
    header_text = f"{text:^{width}}"
    
    return f"\n{colorize(border, color)}\n{colorize(header_text, color, style=Colors.BOLD)}\n{colorize(border, color)}"

def success(text):
    """Style text as success message"""
    return colorize(f"✓ {text}", Colors.BRIGHT_GREEN, style=Colors.BOLD)

def warning(text):
    """Style text as warning message"""
    return colorize(f"⚠ {text}", Colors.BRIGHT_YELLOW, style=Colors.BOLD)

def error(text):
    """Style text as error message"""
    return colorize(f"✗ {text}", Colors.BRIGHT_RED, style=Colors.BOLD)

def info(text):
    """Style text as info message"""
    return colorize(f"ℹ {text}", Colors.BRIGHT_BLUE)

def highlight(text, color=Colors.BRIGHT_YELLOW):
    """Highlight important text"""
    return colorize(text, color, style=Colors.BOLD)

def dim(text):
    """Dim less important text"""
    return colorize(text, style=Colors.DIM)

def format_speedup(speedup, threshold_good=2.0, threshold_bad=0.5):
    """Format speedup ratio with appropriate colors"""
    if speedup >= threshold_good:
        return colorize(f"{speedup:.2f}x", Colors.BRIGHT_GREEN, style=Colors.BOLD)
    elif speedup <= threshold_bad:
        return colorize(f"{speedup:.2f}x", Colors.BRIGHT_RED, style=Colors.BOLD)
    else:
        return colorize(f"{speedup:.2f}x", Colors.BRIGHT_YELLOW)

def format_time(time_seconds):
    """Format time with appropriate units and colors"""
    if time_seconds < 1e-6:
        return colorize(f"{time_seconds*1e9:.2f}ns", Colors.BRIGHT_GREEN)
    elif time_seconds < 1e-3:
        return colorize(f"{time_seconds*1e6:.2f}µs", Colors.GREEN)
    elif time_seconds < 1:
        return colorize(f"{time_seconds*1e3:.2f}ms", Colors.YELLOW)
    else:
        return colorize(f"{time_seconds:.2f}s", Colors.RED)

def progress_bar(current, total, width=50, fill_char="█", empty_char="░"):
    """Create a colored progress bar"""
    if total == 0:
        percentage = 100
    else:
        percentage = (current / total) * 100
    
    filled_width = int(width * current / total) if total > 0 else width
    empty_width = width - filled_width
    
    # Color based on progress
    if percentage < 30:
        color = Colors.RED
    elif percentage < 70:
        color = Colors.YELLOW
    else:
        color = Colors.GREEN
    
    bar = colorize(fill_char * filled_width, color) + colorize(empty_char * empty_width, Colors.DIM)
    return f"[{bar}] {percentage:5.1f}%"

def table_row(columns, widths, colors=None, separators="|"):
    """Format a table row with colors"""
    if colors is None:
        colors = [None] * len(columns)
    
    formatted_cols = []
    for i, (col, width) in enumerate(zip(columns, widths)):
        col_str = str(col)
        if len(col_str) > width:
            col_str = col_str[:width-3] + "..."
        
        color = colors[i] if i < len(colors) else None
        formatted_col = colorize(f"{col_str:<{width}}", color)
        formatted_cols.append(formatted_col)
    
    return f" {separators} ".join(formatted_cols)

def benchmark_result_line(test_name, arrpy_time, numpy_time, speedup):
    """Format a benchmark result line with colors"""
    name_color = Colors.BRIGHT_CYAN
    arrpy_color = Colors.BLUE
    numpy_color = Colors.MAGENTA
    
    formatted_name = colorize(f"{test_name:<40}", name_color)
    formatted_arrpy = format_time(arrpy_time)
    formatted_numpy = format_time(numpy_time)
    formatted_speedup = format_speedup(speedup)
    
    # Add visual indicator for performance
    if speedup > 2.0:
        indicator = colorize("🟢", Colors.GREEN)
    elif speedup > 1.0:
        indicator = colorize("🟡", Colors.YELLOW) 
    else:
        indicator = colorize("🔴", Colors.RED)
    
    return f"{formatted_name} │ arrpy: {formatted_arrpy:>12} │ numpy: {formatted_numpy:>12} │ speedup: {formatted_speedup:>10} {indicator}"

def category_summary(category_name, avg_speedup, test_count):
    """Format category summary with colors"""
    category_color = Colors.BRIGHT_MAGENTA
    
    # Performance rating
    if avg_speedup >= 2.0:
        rating = colorize("EXCELLENT", Colors.BRIGHT_GREEN, style=Colors.BOLD)
        emoji = "🚀"
    elif avg_speedup >= 1.0:
        rating = colorize("GOOD", Colors.BRIGHT_YELLOW, style=Colors.BOLD)
        emoji = "⚡"
    else:
        rating = colorize("NEEDS WORK", Colors.BRIGHT_RED, style=Colors.BOLD)
        emoji = "🐌"
    
    return f"{emoji} {colorize(category_name, category_color, style=Colors.BOLD)}: Avg {format_speedup(avg_speedup)} across {test_count} tests - {rating}"

def ascii_logo():
    """Create ASCII art logo for ArrPy"""
    logo = f"""
{colorize("    ╔═══════════════════════════════════════╗", Colors.BRIGHT_CYAN)}
{colorize("    ║", Colors.BRIGHT_CYAN)}  {colorize("█████╗ ██████╗ ██████╗ ██████╗ ██╗   ██╗", Colors.BRIGHT_YELLOW, style=Colors.BOLD)}  {colorize("║", Colors.BRIGHT_CYAN)}
{colorize("    ║", Colors.BRIGHT_CYAN)}  {colorize("██╔══██╗██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝", Colors.BRIGHT_YELLOW, style=Colors.BOLD)}  {colorize("║", Colors.BRIGHT_CYAN)}
{colorize("    ║", Colors.BRIGHT_CYAN)}  {colorize("███████║██████╔╝██████╔╝██████╔╝ ╚████╔╝", Colors.BRIGHT_YELLOW, style=Colors.BOLD)}   {colorize("║", Colors.BRIGHT_CYAN)}
{colorize("    ║", Colors.BRIGHT_CYAN)}  {colorize("██╔══██║██╔══██╗██╔══██╗██╔═══╝   ╚██╔╝", Colors.BRIGHT_YELLOW, style=Colors.BOLD)}    {colorize("║", Colors.BRIGHT_CYAN)}
{colorize("    ║", Colors.BRIGHT_CYAN)}  {colorize("██║  ██║██║  ██║██║  ██║██║        ██║", Colors.BRIGHT_YELLOW, style=Colors.BOLD)}     {colorize("║", Colors.BRIGHT_CYAN)}
{colorize("    ║", Colors.BRIGHT_CYAN)}  {colorize("╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝", Colors.BRIGHT_YELLOW, style=Colors.BOLD)}     {colorize("║", Colors.BRIGHT_CYAN)}
{colorize("    ║", Colors.BRIGHT_CYAN)}                                           {colorize("║", Colors.BRIGHT_CYAN)}
{colorize("    ║", Colors.BRIGHT_CYAN)}         {colorize("Pure Python NumPy Alternative", Colors.BRIGHT_WHITE, style=Colors.BOLD)}         {colorize("║", Colors.BRIGHT_CYAN)}
{colorize("    ║", Colors.BRIGHT_CYAN)}              {colorize("Performance Benchmarks", Colors.BRIGHT_GREEN)}              {colorize("║", Colors.BRIGHT_CYAN)}
{colorize("    ╚═══════════════════════════════════════╝", Colors.BRIGHT_CYAN)}
"""
    return logo