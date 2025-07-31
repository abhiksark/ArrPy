"""
Color utilities for beautiful terminal output in ArrPy benchmarks.
Provides ANSI color codes, formatting utilities, and the iconic ArrPy banner.
"""

import os
import sys

class Colors:
    """ANSI color codes for terminal output"""
    # Basic colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
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
    """Check if terminal supports color output"""
    # Check if we're in a terminal that supports colors
    if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
        # Check environment variables
        term = os.environ.get('TERM', '')
        colorterm = os.environ.get('COLORTERM', '')
        
        # Most modern terminals support colors
        if 'color' in term.lower() or colorterm or term in ['xterm', 'xterm-256color', 'screen']:
            return True
        
        # Windows Command Prompt and PowerShell
        if os.name == 'nt':
            return True
    
    return False

def colorize(text, color=Colors.WHITE, bg_color="", style=""):
    """Apply color and style to text if terminal supports it"""
    if not supports_color():
        return text
    
    return f"{style}{bg_color}{color}{text}{Colors.RESET}"

def header(text, char="=", color=Colors.BRIGHT_BLUE):
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
    return colorize(f"ℹ {text}", Colors.BRIGHT_CYAN)

def highlight(text, color=Colors.BRIGHT_WHITE):
    """Highlight text with background"""
    return colorize(f" {text} ", color, bg_color=Colors.BG_BLUE, style=Colors.BOLD)

def dim(text):
    """Make text dimmer"""
    return colorize(text, Colors.BRIGHT_BLACK, style=Colors.DIM)

def bold(text, color=Colors.WHITE):
    """Make text bold"""
    return colorize(text, color, style=Colors.BOLD)

def underline(text, color=Colors.WHITE):
    """Underline text"""
    return colorize(text, color, style=Colors.UNDERLINE)

def progress_bar(percentage, width=50, color=Colors.BRIGHT_GREEN):
    """Create a colored progress bar"""
    filled = int(width * percentage / 100)
    empty = width - filled
    bar = "█" * filled + "░" * empty
    return f"[{colorize(bar, color)}] {percentage:.1f}%"

def table_row(*columns, widths=None, colors=None):
    """Create a formatted table row with colors"""
    if widths is None:
        widths = [20] * len(columns)
    if colors is None:
        colors = [Colors.WHITE] * len(columns)
    
    formatted_columns = []
    for i, (col, width, color) in enumerate(zip(columns, widths, colors)):
        formatted_columns.append(colorize(f"{str(col):<{width}}", color))
    
    return " │ ".join(formatted_columns)

def logo_banner():
    """Create the iconic ArrPy logo banner"""
    logo = f"""
{colorize("    ╔═══════════════════════════════════════╗", Colors.BRIGHT_CYAN)}
{colorize("    ║", Colors.BRIGHT_CYAN)}  {colorize("█████╗ ██████╗ ██████╗ ██████╗ ██╗   ██╗", Colors.BRIGHT_YELLOW, style=Colors.BOLD)}  {colorize("║", Colors.BRIGHT_CYAN)}
{colorize("    ║", Colors.BRIGHT_CYAN)}  {colorize("██╔══██╗██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝", Colors.BRIGHT_YELLOW, style=Colors.BOLD)}  {colorize("║", Colors.BRIGHT_CYAN)}
{colorize("    ║", Colors.BRIGHT_CYAN)}  {colorize("███████║██████╔╝██████╔╝██████╔╝ ╚████╔╝", Colors.BRIGHT_YELLOW, style=Colors.BOLD)}   {colorize("║", Colors.BRIGHT_CYAN)}
{colorize("    ║", Colors.BRIGHT_CYAN)}  {colorize("██╔══██║██╔══██╗██╔══██╗██╔═══╝   ╚██╔╝", Colors.BRIGHT_YELLOW, style=Colors.BOLD)}    {colorize("║", Colors.BRIGHT_CYAN)}
{colorize("    ║", Colors.BRIGHT_CYAN)}  {colorize("██║  ██║██║  ██║██║  ██║██║        ██║", Colors.BRIGHT_YELLOW, style=Colors.BOLD)}     {colorize("║", Colors.BRIGHT_CYAN)}
{colorize("    ║", Colors.BRIGHT_CYAN)}  {colorize("╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝", Colors.BRIGHT_YELLOW, style=Colors.BOLD)}     {colorize("║", Colors.BRIGHT_CYAN)}
{colorize("    ║", Colors.BRIGHT_CYAN)}                                           {colorize("║", Colors.BRIGHT_CYAN)}
{colorize("    ║", Colors.BRIGHT_CYAN)}         {colorize("Cython-Optimized NumPy Alternative", Colors.BRIGHT_WHITE, style=Colors.BOLD)}         {colorize("║", Colors.BRIGHT_CYAN)}
{colorize("    ║", Colors.BRIGHT_CYAN)}              {colorize("Version 0.2.1 - Multicore Performance Benchmarks", Colors.BRIGHT_GREEN)}              {colorize("║", Colors.BRIGHT_CYAN)}
{colorize("    ╚═══════════════════════════════════════╝", Colors.BRIGHT_CYAN)}
"""
    return logo

def performance_indicator(speedup, operation_name="", width=30):
    """Create a visual performance indicator"""
    if speedup >= 5:
        color = Colors.BRIGHT_RED
        emoji = "🔴"
        status = "Much slower"
    elif speedup >= 2:
        color = Colors.BRIGHT_YELLOW
        emoji = "🟡"
        status = "Slower"
    elif speedup >= 0.8:
        color = Colors.BRIGHT_GREEN
        emoji = "🟢"
        status = "Competitive"
    else:
        color = Colors.BRIGHT_CYAN
        emoji = "🚀"
        status = "Faster"
    
    # Create visual bar
    bar_length = min(int(speedup * 5), width)
    bar = "█" * bar_length
    
    return f"{colorize(f'{operation_name:<25}', Colors.WHITE)} │{colorize(bar, color):<{width}} {speedup:.2f}x {emoji}"

def benchmark_summary_table(results):
    """Create a beautiful summary table of benchmark results"""
    if not results:
        return "No results to display"
    
    output = []
    output.append(colorize("\n" + "="*80, Colors.BRIGHT_BLUE, style=Colors.BOLD))
    output.append(colorize("                     📊 PERFORMANCE SUMMARY", Colors.BRIGHT_WHITE, style=Colors.BOLD))
    output.append(colorize("="*80, Colors.BRIGHT_BLUE, style=Colors.BOLD))
    
    for category, tests in results.items():
        output.append(f"\n{colorize(f'{category}:', Colors.BRIGHT_MAGENTA, style=Colors.BOLD)}")
        
        for test_name, speedup in tests.items():
            indicator = performance_indicator(speedup, test_name)
            output.append(f"  {indicator}")
    
    return "\n".join(output)

def format_time(seconds):
    """Format time in appropriate units with color"""
    if seconds < 1e-6:
        return colorize(f"{seconds*1e9:.1f}ns", Colors.BRIGHT_GREEN)
    elif seconds < 1e-3:
        return colorize(f"{seconds*1e6:.1f}μs", Colors.BRIGHT_CYAN)
    elif seconds < 1:
        return colorize(f"{seconds*1e3:.1f}ms", Colors.BRIGHT_YELLOW)
    else:
        return colorize(f"{seconds:.2f}s", Colors.BRIGHT_RED)

def format_speedup(speedup):
    """Format speedup with appropriate color"""
    if speedup > 1:
        return colorize(f"{speedup:.2f}x faster", Colors.BRIGHT_GREEN, style=Colors.BOLD)
    elif speedup < 1:
        return colorize(f"{1/speedup:.2f}x slower", Colors.BRIGHT_RED, style=Colors.BOLD)
    else:
        return colorize("Same speed", Colors.BRIGHT_BLUE)

def separator(char="─", width=80, color=Colors.BRIGHT_BLACK):
    """Create a separator line"""
    return colorize(char * width, color)

def benchmark_result_line(name, arrpy_time, numpy_time, speedup_ratio):
    """Format a benchmark result line with colors"""
    # Format times
    arrpy_str = format_time(arrpy_time)
    numpy_str = format_time(numpy_time)
    
    # Determine speedup color and emoji
    if speedup_ratio > 1:
        speedup_str = colorize(f"{speedup_ratio:.2f}x slower", Colors.BRIGHT_RED)
        emoji = "🔴"
    elif speedup_ratio < 0.8:
        speedup_str = colorize(f"{1/speedup_ratio:.2f}x faster", Colors.BRIGHT_GREEN)
        emoji = "🚀"
    else:
        speedup_str = colorize(f"{1/speedup_ratio:.2f}x", Colors.BRIGHT_YELLOW)
        emoji = "🟡"
    
    return f"  {colorize(name, Colors.BRIGHT_WHITE):<40} │ arrpy: {arrpy_str} │ numpy: {numpy_str} │ {speedup_str} {emoji}"

# Quick color functions for common use
def red(text): return colorize(text, Colors.BRIGHT_RED)
def green(text): return colorize(text, Colors.BRIGHT_GREEN)
def yellow(text): return colorize(text, Colors.BRIGHT_YELLOW)
def blue(text): return colorize(text, Colors.BRIGHT_BLUE)
def magenta(text): return colorize(text, Colors.BRIGHT_MAGENTA)
def cyan(text): return colorize(text, Colors.BRIGHT_CYAN)
def white(text): return colorize(text, Colors.BRIGHT_WHITE)

# Test function to verify colors work
def test_colors():
    """Test all color functions"""
    print(logo_banner())
    print(header("Color Test", color=Colors.BRIGHT_MAGENTA))
    print(success("Success message"))
    print(warning("Warning message"))
    print(error("Error message"))
    print(info("Info message"))
    print(highlight("Highlighted text"))
    print(progress_bar(75))
    print(performance_indicator(2.5, "Array Creation"))
    print(format_time(0.000123))
    print(format_speedup(3.4))
    print(separator())

if __name__ == "__main__":
    test_colors()