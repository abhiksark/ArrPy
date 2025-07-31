# ArrPy Architecture Overview

This document provides a comprehensive overview of ArrPy's internal architecture, design decisions, and implementation details.

## 🏗️ High-Level Architecture

```mermaid
graph TB
    subgraph "User Interface Layer"
        A[User Code] --> B[ArrPy API]
        B --> C[Array Constructor]
        B --> D[Creation Functions]
        B --> E[Math Functions]
        B --> F[Statistics Functions]
    end
    
    subgraph "Core Layer"
        C --> G[HybridArray]
        D --> G
        E --> G
        F --> G
        G --> H[Backend Selection]
    end
    
    subgraph "Backend Layer"
        H --> I[C Extension Backend]
        H --> J[Pure Python Backend]
        I --> K[CArray C Implementation]
        J --> L[PythonArray Implementation]
    end
    
    subgraph "System Layer"
        K --> M[Memory Management]
        K --> N[SIMD Operations]
        K --> O[OpenMP Parallelization]
        L --> P[Python List Storage]
    end
    
    style A fill:#e1f5fe
    style G fill:#f3e5f5
    style I fill:#e8f5e8
    style J fill:#fff3e0
```

## 🔧 Core Components

### 1. HybridArray System

The heart of ArrPy is the hybrid array system that transparently selects between C and Python backends:

```mermaid
graph LR
    subgraph "Array Creation"
        A[Array Constructor] --> B{C Extension Available?}
        B -->|Yes| C[Try C Backend]
        B -->|No| D[Python Backend]
        C --> E{C Creation Success?}
        E -->|Yes| F[HybridArray with C]
        E -->|No| G[Fallback to Python]
        D --> H[HybridArray with Python]
        G --> H
    end
    
    subgraph "Operation Dispatch"
        F --> I[C Implementation]
        H --> J[Python Implementation]
        I --> K{Operation Available?}
        K -->|Yes| L[Execute C Code]
        K -->|No| M[Fallback to Python]
        J --> N[Execute Python Code]
    end
    
    style F fill:#c8e6c9
    style H fill:#ffecb3
    style L fill:#a5d6a7
    style N fill:#ffe082
```

### 2. Memory Layout

ArrPy uses different memory strategies for optimal performance:

```mermaid
graph TB
    subgraph "C Backend Memory Layout"
        A[CArrayObject Header] --> B[PyObject_HEAD]
        A --> C[double* data]
        A --> D[Py_ssize_t* shape]
        A --> E[Py_ssize_t* strides]
        A --> F[Py_ssize_t ndim]
        A --> G[Py_ssize_t size]
        A --> H[int flags]
        
        C --> I[Contiguous Memory Block]
        I --> J[Cache-Aligned Data]
        J --> K[SIMD-Friendly Layout]
    end
    
    subgraph "Python Backend Memory Layout"
        L[PythonArray Object] --> M[Python List]
        M --> N[Nested Lists for nD]
        N --> O[Python Objects]
        O --> P[Reference Counted]
    end
    
    style I fill:#e8f5e8
    style M fill:#fff3e0
```

## 🚀 Backend Selection Logic

### Automatic Backend Selection

```python
class HybridArray:
    def __init__(self, data, _c_array=None):
        if _c_array is not None:
            # Direct C array provided
            self._c_array = _c_array
            self._use_c = True
        elif HAS_C_EXTENSION and isinstance(data, list):
            try:
                # Try C backend for list input
                self._c_array = CArray(data)
                self._use_c = True
            except Exception:
                # Fallback to Python
                self._python_array = PythonArray(data)
                self._use_c = False
        else:
            # Use Python backend
            self._python_array = PythonArray(data)
            self._use_c = False
```

### Performance Decision Tree

```mermaid
graph TD
    A[Operation Request] --> B{C Extension Available?}
    B -->|No| C[Python Implementation]
    B -->|Yes| D{Array Uses C Backend?}
    D -->|No| C
    D -->|Yes| E{Operation Implemented in C?}
    E -->|No| F[Fallback to Python]
    E -->|Yes| G{Data Size > Threshold?}
    G -->|Small| H[Direct C Execution]
    G -->|Large| I[Parallel C Execution]
    
    style C fill:#ffecb3
    style F fill:#ffecb3
    style H fill:#c8e6c9
    style I fill:#a5d6a7
```

## 🔄 Data Flow Architecture

### Array Operations Pipeline

```mermaid
sequenceDiagram
    participant U as User Code
    participant H as HybridArray
    participant C as C Backend
    participant P as Python Backend
    
    U->>H: arr1 + arr2
    H->>H: Check backends
    alt Both arrays use C backend
        H->>C: c_add(arr1._c_array, arr2._c_array)
        C->>C: SIMD vectorized addition
        C->>H: Return CArray result
        H->>H: Wrap in HybridArray
    else Mixed or Python backends
        H->>P: python_add(arr1, arr2)
        P->>P: Element-wise Python addition
        P->>H: Return PythonArray result
        H->>H: Wrap in HybridArray
    end
    H->>U: Return result
```

### Memory Management Flow

```mermaid
graph LR
    subgraph "C Backend Memory"
        A[malloc] --> B[Aligned Allocation]
        B --> C[Data Storage]
        C --> D[Reference Counting]
        D --> E[Automatic Cleanup]
        E --> F[free]
    end
    
    subgraph "Python Backend Memory"
        G[Python GC] --> H[Object Creation]
        H --> I[List Storage]
        I --> J[Reference Management]
        J --> K[Garbage Collection]
    end
    
    subgraph "Hybrid Management"
        L[HybridArray] --> M{Backend Type}
        M -->|C| A
        M -->|Python| G
    end
    
    style C fill:#e8f5e8
    style I fill:#fff3e0
```

## 🏗️ Module Structure

### Directory Layout

```
arrpy/
├── __init__.py              # Main module exports
├── core/                    # Core functionality
│   ├── __init__.py         # Core exports
│   ├── array.py            # PythonArray implementation
│   ├── hybrid_array.py     # HybridArray wrapper
│   └── c_backend.py        # C extension interface
├── creation/               # Array creation functions
│   ├── __init__.py
│   └── basic.py           # zeros, ones, arange, etc.
├── math/                  # Mathematical functions
│   ├── __init__.py
│   ├── basic.py          # +, -, *, /
│   ├── trigonometric.py  # sin, cos, tan
│   ├── exponential.py    # exp, log, sqrt
│   └── rounding.py       # floor, ceil, round
├── statistics/           # Statistical functions
│   ├── __init__.py
│   ├── aggregation.py   # sum, mean, min, max
│   ├── variance.py      # std, var
│   └── advanced.py      # percentile, median
├── manipulation/        # Array manipulation
│   ├── __init__.py
│   ├── shape.py        # reshape, transpose
│   └── joining.py      # concatenate, stack
└── c_src/              # C extension source
    ├── c_array.h       # C array structure
    ├── c_array.c       # Core C implementation
    ├── c_math.c        # Mathematical operations
    ├── c_stats.c       # Statistical operations
    └── module.c        # Python module interface
```

### Import Resolution

```mermaid
graph TB
    A[import arrpy] --> B[arrpy/__init__.py]
    B --> C[Import Core Components]
    C --> D[core.Array]
    C --> E[creation functions]
    C --> F[math functions]
    C --> G[statistics functions]
    
    D --> H{C Extension Check}
    H -->|Available| I[Enable HybridArray]
    H -->|Not Available| J[Pure Python Mode]
    
    subgraph "C Extension Loading"
        I --> K[Load c_array module]
        K --> L[Initialize C backend]
        L --> M[Set HAS_C_EXTENSION = True]
    end
    
    subgraph "Pure Python Mode"
        J --> N[Set HAS_C_EXTENSION = False]
        N --> O[Use PythonArray only]
    end
    
    style I fill:#c8e6c9
    style J fill:#ffecb3
```

## ⚡ Performance Optimizations

### C Extension Optimizations

```mermaid
graph TB
    subgraph "Compilation Optimizations"
        A[GCC Optimization Flags] --> B[-O3 Full Optimization]
        A --> C[-march=native CPU Specific]
        A --> D[-ffast-math Math Optimizations]
        A --> E[-fopenmp OpenMP Support]
    end
    
    subgraph "Runtime Optimizations"
        F[Memory Layout] --> G[Contiguous Arrays]
        F --> H[Cache-Aligned Data]
        F --> I[SIMD Vectorization]
        
        J[Parallel Processing] --> K[OpenMP Threads]
        J --> L[Vectorized Operations]
        J --> M[Batch Processing]
    end
    
    subgraph "Algorithm Optimizations"
        N[Operation Fusion] --> O[Combined Operations]
        N --> P[Reduced Memory Access]
        N --> Q[Loop Unrolling]
    end
    
    style G fill:#e8f5e8
    style I fill:#e8f5e8
    style K fill:#e8f5e8
```

### Memory Optimization Strategies

```mermaid
graph LR
    subgraph "Memory Efficiency"
        A[Stack Allocation] --> B[Small Arrays]
        C[Heap Allocation] --> D[Large Arrays]
        E[Memory Pools] --> F[Frequent Allocations]
        G[Reference Counting] --> H[Automatic Cleanup]
    end
    
    subgraph "Cache Optimization"
        I[Data Locality] --> J[Sequential Access]
        I --> K[Block Processing]
        I --> L[Prefetching]
    end
    
    subgraph "Memory Layout"
        M[Row-Major Order] --> N[C-Style Indexing]
        O[Stride Calculation] --> P[Multi-dimensional Access]
        Q[Alignment] --> R[SIMD Requirements]
    end
    
    style J fill:#e8f5e8
    style N fill:#e8f5e8
    style R fill:#e8f5e8
```

## 🔧 Extension Architecture

### C Extension Structure

```c
// Core C array structure
typedef struct {
    PyObject_HEAD
    double* data;           // Contiguous data storage
    Py_ssize_t* shape;      // Dimension sizes
    Py_ssize_t* strides;    // Memory strides
    Py_ssize_t ndim;        // Number of dimensions
    Py_ssize_t size;        // Total elements
    int flags;              // Array properties
} CArrayObject;
```

### Python-C Interface

```mermaid
graph TB
    subgraph "Python Layer"
        A[Python Function Call] --> B[Argument Parsing]
        B --> C[Type Checking]
        C --> D[C Function Call]
    end
    
    subgraph "C Layer"
        D --> E[Parameter Validation]
        E --> F[Memory Access]
        F --> G[Vectorized Computation]
        G --> H[Result Creation]
    end
    
    subgraph "Return Path"
        H --> I[Python Object Creation]
        I --> J[Reference Management]
        J --> K[Return to Python]
    end
    
    style G fill:#e8f5e8
```

## 🔄 Error Handling Strategy

### Multi-Level Error Handling

```mermaid
graph TD
    A[Operation Request] --> B[Input Validation]
    B --> C{Valid Input?}
    C -->|No| D[Raise TypeError/ValueError]
    C -->|Yes| E[Backend Selection]
    
    E --> F{C Backend Available?}
    F -->|Yes| G[Try C Operation]
    F -->|No| H[Python Operation]
    
    G --> I{C Operation Success?}
    I -->|Yes| J[Return Result]
    I -->|No| K[Log Error & Fallback]
    K --> H
    
    H --> L{Python Success?}
    L -->|Yes| J
    L -->|No| M[Raise Exception]
    
    style D fill:#ffcdd2
    style M fill:#ffcdd2
    style J fill:#c8e6c9
```

### Exception Hierarchy

```python
ArrPyError (Base Exception)
├── ShapeError (Shape incompatibility)
├── DimensionError (Dimension mismatch)
├── IndexError (Invalid indexing)
├── BackendError (C extension issues)
└── ComputationError (Mathematical errors)
```

## 📊 Testing Architecture

### Test Organization

**Test Structure:**
```
tests/
├── test_core/          # Core functionality tests
├── test_creation/      # Array creation tests
├── test_math/          # Mathematical operation tests
├── test_statistics/    # Statistical function tests
├── test_manipulation/  # Array manipulation tests
└── test_performance/   # Performance benchmark tests
```

**Test Types:**
- **Unit Tests** → Individual Functions
- **Integration Tests** → Component Interaction  
- **Performance Tests** → Benchmark Validation
- **Compatibility Tests** → Backend Consistency

**Test Execution Pipeline:**
```
pytest Runner → Automatic Discovery → Parallel Execution → Coverage Reporting
```

## 🚀 Build System

### Compilation Pipeline

```mermaid
graph LR
    subgraph "Source Files"
        A[*.c files] --> B[Preprocessor]
        C[*.h files] --> B
        D[setup_c_ext.py] --> E[Build Configuration]
    end
    
    subgraph "Compilation"
        B --> F[GCC Compiler]
        E --> F
        F --> G[Object Files]
        G --> H[Linker]
        H --> I[Shared Library]
    end
    
    subgraph "Installation"
        I --> J[Module Installation]
        J --> K[Import Testing]
        K --> L[Ready for Use]
    end
    
    style I fill:#e8f5e8
    style L fill:#c8e6c9
```

## 🔍 Debugging and Profiling

### Debug Information Flow

```mermaid
graph TB
    subgraph "Debug Modes"
        A[Development Mode] --> B[Verbose Logging]
        A --> C[Assertion Checks]
        A --> D[Memory Debugging]
    end
    
    subgraph "Profiling Tools"
        E[Python Profiler] --> F[Function Timing]
        G[C Profiler] --> H[Low-level Analysis]
        I[Memory Profiler] --> J[Allocation Tracking]
    end
    
    subgraph "Performance Monitoring"
        K[Backend Selection Stats] --> L[Usage Patterns]
        M[Operation Timing] --> N[Bottleneck Detection]
        O[Memory Usage] --> P[Optimization Targets]
    end
    
    style B fill:#e3f2fd
    style F fill:#e8f5e8
    style L fill:#fff3e0
```

## 🔧 Configuration System

### Runtime Configuration

```python
# Configuration priorities (highest to lowest)
1. Function parameters
2. Environment variables
3. Configuration files
4. Default values

# Environment variables
ARRPY_USE_C_BACKEND=1     # Force C backend
ARRPY_DEBUG=1             # Enable debug mode
ARRPY_SIMD_THRESHOLD=1000 # SIMD activation threshold
ARRPY_THREADS=4           # OpenMP thread count
```

### Feature Detection

```mermaid
graph TD
    A[Module Import] --> B[Feature Detection]
    B --> C{C Extension Available?}
    C -->|Yes| D[Check CPU Features]
    C -->|No| E[Python-Only Mode]
    
    D --> F{SIMD Support?}
    F -->|Yes| G[Enable Vectorization]
    F -->|No| H[Scalar Operations]
    
    D --> I{OpenMP Available?}
    I -->|Yes| J[Enable Parallelization]
    I -->|No| K[Single-threaded]
    
    style G fill:#c8e6c9
    style J fill:#c8e6c9
    style E fill:#ffecb3
```

## 📈 Scalability Considerations

### Performance Scaling

```mermaid
graph TB
    A[Small Arrays less than 1KB] --> B[Python Backend Competitive]
    C[Medium Arrays 1KB to 1MB] --> D[C Backend Advantage]
    E[Large Arrays greater than 1MB] --> F[Parallel C Backend]
    
    G[Element-wise Operations] --> H[Vectorization Benefits]
    I[Reduction Operations] --> J[Parallel Reductions]
    K[Matrix Operations] --> L[Blocked Algorithms]
    
    style D fill:#e8f5e8
    style F fill:#c8e6c9
    style H fill:#e8f5e8
```

## 🔮 Future Architecture Plans

### Extensibility Points

1. **Plugin System**: Dynamic backend registration
2. **GPU Support**: CUDA/OpenCL backends
3. **Distributed Computing**: Multi-node arrays
4. **Memory Mapping**: Large dataset support
5. **Custom Data Types**: Beyond double precision

### Architecture Evolution

```mermaid
graph TB
    A[Current: Hybrid C/Python] --> B[Future: Plugin Architecture]
    B --> C[Multiple Backend Support]
    C --> D[Dynamic Backend Selection]
    D --> E[Automatic Optimization]
    
    subgraph "Planned Backends"
        F[CUDA Backend]
        G[OpenCL Backend]
        H[ARM NEON Backend]
        I[WebAssembly Backend]
    end
    
    C --> F
    C --> G
    C --> H
    C --> I
    
    style B fill:#e1f5fe
    style E fill:#e8f5e8
```

This architecture overview provides a comprehensive understanding of ArrPy's design, implementation, and future direction. The modular architecture ensures maintainability, extensibility, and optimal performance across different use cases.