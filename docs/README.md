# ArrPy Documentation

Welcome to the ArrPy documentation! This directory contains comprehensive documentation for the ArrPy numerical computing library.

## 📁 Documentation Structure

```
docs/
├── README.md              # This file
├── index.md              # Documentation home page
├── INSTALLATION.md       # Detailed installation guide
├── CHANGELOG.md          # Version history and release notes
│
├── api/                  # API Reference Documentation
│   ├── array.md         # Array class reference
│   ├── creation.md      # Array creation functions
│   ├── math.md          # Mathematical functions
│   ├── statistics.md    # Statistical functions
│   └── manipulation.md  # Array manipulation functions
│
└── guides/              # User Guides and Tutorials
    ├── quickstart.md   # 5-minute quick start guide
    ├── USER_GUIDE.md   # Comprehensive user guide
    └── architecture.md # Internal architecture overview
```

## 🚀 Quick Links

### Getting Started
- [Installation Guide](INSTALLATION.md) - How to install ArrPy on your system
- [Quick Start](guides/quickstart.md) - Get up and running in 5 minutes
- [User Guide](guides/USER_GUIDE.md) - Comprehensive guide to using ArrPy

### Reference Documentation
- [API Reference](api/) - Complete API documentation
- [Changelog](CHANGELOG.md) - What's new in each version

### Performance
- [Performance Report](../PERFORMANCE_REPORT.md) - Detailed benchmarks
- [NumPy Comparison](../NUMPY_COMPARISON_REPORT.md) - ArrPy vs NumPy
- [C Extension Guide](../C_EXTENSION_GUIDE.md) - Understanding the C backend

## 📚 Documentation Overview

### For New Users
1. Start with the [Installation Guide](INSTALLATION.md)
2. Follow the [Quick Start Tutorial](guides/quickstart.md)
3. Read the [User Guide](guides/USER_GUIDE.md)

### For Developers
1. Read the [Architecture Overview](guides/architecture.md)
2. Check the [API Reference](api/)
3. Review the [Contributing Guide](../CONTRIBUTING.md)

### For Contributors
1. Follow the [Contributing Guidelines](../CONTRIBUTING.md)
2. Check the [Development Setup](INSTALLATION.md#development-installation)
3. Read the [Code Style Guide](../CONTRIBUTING.md#code-style)

## 🔍 Finding Information

### By Topic

**Array Basics**
- Creating arrays: [Creation Functions](api/creation.md)
- Array properties: [Array Class](api/array.md)
- Basic operations: [User Guide](guides/USER_GUIDE.md#array-operations)

**Mathematical Operations**
- Element-wise math: [Math Functions](api/math.md)
- Linear algebra: [Array.dot()](api/array.md#dotother)
- Statistics: [Statistical Functions](api/statistics.md)

**Performance**
- C extensions: [Installation](INSTALLATION.md#c-extensions-installation)
- Benchmarks: [Performance Report](../PERFORMANCE_REPORT.md)

### By Use Case

**Scientific Computing**
- Functions: [Mathematical Functions](api/math.md)

**Data Analysis**
- Statistics: [Statistical Functions](api/statistics.md)
- Aggregations: [User Guide](guides/USER_GUIDE.md#statistical-functions)

**Education**
- Learning NumPy concepts: [User Guide](guides/USER_GUIDE.md)

## 📖 Reading Order

### Beginner Path
1. [Installation](INSTALLATION.md)
2. [Quick Start](guides/quickstart.md)
3. [User Guide](guides/USER_GUIDE.md)

### Advanced Path
1. [C Extension Guide](../C_EXTENSION_GUIDE.md)
2. [API Reference](api/)

## 🛠️ Building Documentation

To build HTML documentation (requires Sphinx):

```bash
# Install documentation dependencies
pip install sphinx sphinx-rtd-theme

# Build HTML docs
cd docs
make html

# View in browser
open _build/html/index.html
```

## 📝 Documentation Standards

When contributing documentation:

1. **Use Clear Language**: Write for clarity, not complexity
2. **Include Examples**: Every feature should have an example
3. **Stay Consistent**: Follow existing formatting patterns
4. **Test Code**: Ensure all code examples work
5. **Update Index**: Add new pages to relevant indexes

## 🤝 Contributing to Docs

We welcome documentation improvements! Please:

1. Check existing [issues](https://github.com/yourusername/ArrPy/issues) for documentation needs
2. Follow the [Contributing Guide](../CONTRIBUTING.md)
3. Test all code examples
4. Update the changelog for significant changes

## 📄 License

The documentation is licensed under the same [MIT License](../LICENSE) as ArrPy.

---

*Last updated: January 31, 2024*