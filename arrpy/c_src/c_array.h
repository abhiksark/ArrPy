#ifndef ARRPY_C_ARRAY_H
#define ARRPY_C_ARRAY_H

#include <Python.h>
#include <string.h>
#include <math.h>

// Define the CArray structure
typedef struct {
    PyObject_HEAD
    double* data;           // Contiguous C array for data storage
    Py_ssize_t* shape;      // Array of dimensions
    Py_ssize_t* strides;    // Array of strides for each dimension
    Py_ssize_t ndim;        // Number of dimensions
    Py_ssize_t size;        // Total number of elements
    int flags;              // Flags for array properties
} CArrayObject;

// Flags for array properties
#define CARRAY_C_CONTIGUOUS 0x01
#define CARRAY_WRITEABLE    0x02
#define CARRAY_OWNDATA      0x04

// Macro for type checking
#define CArray_Check(op) PyObject_TypeCheck(op, &CArrayType)

// Function declarations
PyObject* CArray_New(PyTypeObject* type, PyObject* args, PyObject* kwds);
void CArray_dealloc(CArrayObject* self);
PyObject* CArray_repr(CArrayObject* self);

// Element access functions
PyObject* CArray_GetItem(CArrayObject* self, PyObject* key);
int CArray_SetItem(CArrayObject* self, PyObject* key, PyObject* value);

// Array creation functions
CArrayObject* CArray_Zeros(Py_ssize_t* shape, Py_ssize_t ndim);
CArrayObject* CArray_Ones(Py_ssize_t* shape, Py_ssize_t ndim);
CArrayObject* CArray_Full(Py_ssize_t* shape, Py_ssize_t ndim, double fill_value);
CArrayObject* CArray_Arange(double start, double stop, double step);

// Arithmetic operations
CArrayObject* CArray_Add(CArrayObject* self, PyObject* other);
CArrayObject* CArray_Subtract(CArrayObject* self, PyObject* other);
CArrayObject* CArray_Multiply(CArrayObject* self, PyObject* other);
CArrayObject* CArray_Divide(CArrayObject* self, PyObject* other);

// Aggregation functions
double CArray_Sum(CArrayObject* self);
double CArray_Mean(CArrayObject* self);
double CArray_Min(CArrayObject* self);
double CArray_Max(CArrayObject* self);

// Utility functions
Py_ssize_t CArray_CalculateSize(Py_ssize_t* shape, Py_ssize_t ndim);
void CArray_CalculateStrides(Py_ssize_t* shape, Py_ssize_t* strides, Py_ssize_t ndim);
int CArray_BroadcastShapes(Py_ssize_t* shape1, Py_ssize_t ndim1, 
                          Py_ssize_t* shape2, Py_ssize_t ndim2,
                          Py_ssize_t* out_shape, Py_ssize_t* out_ndim);

// Python type object
extern PyTypeObject CArrayType;

#endif // ARRPY_C_ARRAY_H