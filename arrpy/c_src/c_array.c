#include "c_array.h"
#include <stdlib.h>
#include <stdint.h>

// Forward declarations for Python methods
static PyObject* CArray_new(PyTypeObject* type, PyObject* args, PyObject* kwds);
static int CArray_init(CArrayObject* self, PyObject* args, PyObject* kwds);
static PyObject* CArray_subscript(CArrayObject* self, PyObject* key);
static int CArray_ass_subscript(CArrayObject* self, PyObject* key, PyObject* value);

// Utility function to calculate total size from shape
Py_ssize_t CArray_CalculateSize(Py_ssize_t* shape, Py_ssize_t ndim) {
    Py_ssize_t size = 1;
    for (Py_ssize_t i = 0; i < ndim; i++) {
        size *= shape[i];
    }
    return size;
}

// Calculate strides for C-contiguous array
void CArray_CalculateStrides(Py_ssize_t* shape, Py_ssize_t* strides, Py_ssize_t ndim) {
    Py_ssize_t stride = 1;
    for (Py_ssize_t i = ndim - 1; i >= 0; i--) {
        strides[i] = stride;
        stride *= shape[i];
    }
}

// Create a new CArray object
static PyObject* CArray_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    CArrayObject* self;
    self = (CArrayObject*)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->data = NULL;
        self->shape = NULL;
        self->strides = NULL;
        self->ndim = 0;
        self->size = 0;
        self->flags = CARRAY_C_CONTIGUOUS | CARRAY_WRITEABLE | CARRAY_OWNDATA;
    }
    return (PyObject*)self;
}

// Initialize CArray from Python list
static int CArray_init(CArrayObject* self, PyObject* args, PyObject* kwds) {
    PyObject* data_obj;
    static char* kwlist[] = {"data", NULL};
    
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O", kwlist, &data_obj)) {
        return -1;
    }
    
    // For now, we'll implement a simple 1D array from a list
    if (PyList_Check(data_obj)) {
        Py_ssize_t size = PyList_Size(data_obj);
        
        // Allocate memory for data
        self->data = (double*)calloc(size, sizeof(double));
        if (self->data == NULL) {
            PyErr_NoMemory();
            return -1;
        }
        
        // Copy data from list
        for (Py_ssize_t i = 0; i < size; i++) {
            PyObject* item = PyList_GetItem(data_obj, i);
            if (!PyNumber_Check(item)) {
                PyErr_SetString(PyExc_TypeError, "Array elements must be numbers");
                free(self->data);
                self->data = NULL;
                return -1;
            }
            self->data[i] = PyFloat_AsDouble(item);
        }
        
        // Set shape and strides for 1D array
        self->ndim = 1;
        self->size = size;
        self->shape = (Py_ssize_t*)malloc(sizeof(Py_ssize_t));
        self->strides = (Py_ssize_t*)malloc(sizeof(Py_ssize_t));
        self->shape[0] = size;
        self->strides[0] = 1;
    }
    else {
        PyErr_SetString(PyExc_TypeError, "Data must be a list");
        return -1;
    }
    
    return 0;
}

// Deallocate CArray
void CArray_dealloc(CArrayObject* self) {
    if (self->flags & CARRAY_OWNDATA && self->data != NULL) {
        free(self->data);
    }
    if (self->shape != NULL) {
        free(self->shape);
    }
    if (self->strides != NULL) {
        free(self->strides);
    }
    Py_TYPE(self)->tp_free((PyObject*)self);
}

// String representation of CArray
PyObject* CArray_repr(CArrayObject* self) {
    // Simple representation for 1D arrays
    if (self->ndim == 1) {
        PyObject* list = PyList_New(self->size);
        for (Py_ssize_t i = 0; i < self->size; i++) {
            PyList_SetItem(list, i, PyFloat_FromDouble(self->data[i]));
        }
        PyObject* list_str = PyObject_Repr(list);
        PyObject* result = PyUnicode_FromFormat("CArray(%S)", list_str);
        Py_DECREF(list);
        Py_DECREF(list_str);
        return result;
    }
    return PyUnicode_FromString("CArray(...)");
}

// Get item from array
static PyObject* CArray_subscript(CArrayObject* self, PyObject* key) {
    if (PyLong_Check(key)) {
        Py_ssize_t index = PyLong_AsSsize_t(key);
        
        // Handle negative indexing
        if (index < 0) {
            index += self->shape[0];
        }
        
        // Bounds checking
        if (index < 0 || index >= self->shape[0]) {
            PyErr_SetString(PyExc_IndexError, "Index out of bounds");
            return NULL;
        }
        
        return PyFloat_FromDouble(self->data[index]);
    }
    else {
        PyErr_SetString(PyExc_TypeError, "Indices must be integers");
        return NULL;
    }
}

// Set item in array
static int CArray_ass_subscript(CArrayObject* self, PyObject* key, PyObject* value) {
    if (!(self->flags & CARRAY_WRITEABLE)) {
        PyErr_SetString(PyExc_ValueError, "Array is not writeable");
        return -1;
    }
    
    if (PyLong_Check(key)) {
        Py_ssize_t index = PyLong_AsSsize_t(key);
        
        // Handle negative indexing
        if (index < 0) {
            index += self->shape[0];
        }
        
        // Bounds checking
        if (index < 0 || index >= self->shape[0]) {
            PyErr_SetString(PyExc_IndexError, "Index out of bounds");
            return -1;
        }
        
        if (!PyNumber_Check(value)) {
            PyErr_SetString(PyExc_TypeError, "Value must be a number");
            return -1;
        }
        
        self->data[index] = PyFloat_AsDouble(value);
        return 0;
    }
    else {
        PyErr_SetString(PyExc_TypeError, "Indices must be integers");
        return -1;
    }
}

// Create array filled with zeros
CArrayObject* CArray_Zeros(Py_ssize_t* shape, Py_ssize_t ndim) {
    CArrayObject* array = (CArrayObject*)CArray_new(&CArrayType, NULL, NULL);
    if (array == NULL) return NULL;
    
    array->ndim = ndim;
    array->shape = (Py_ssize_t*)malloc(ndim * sizeof(Py_ssize_t));
    array->strides = (Py_ssize_t*)malloc(ndim * sizeof(Py_ssize_t));
    
    if (array->shape == NULL || array->strides == NULL) {
        Py_DECREF(array);
        PyErr_NoMemory();
        return NULL;
    }
    
    memcpy(array->shape, shape, ndim * sizeof(Py_ssize_t));
    array->size = CArray_CalculateSize(shape, ndim);
    CArray_CalculateStrides(array->shape, array->strides, ndim);
    
    // Allocate and zero-initialize data
    array->data = (double*)calloc(array->size, sizeof(double));
    if (array->data == NULL) {
        Py_DECREF(array);
        PyErr_NoMemory();
        return NULL;
    }
    
    array->flags = CARRAY_C_CONTIGUOUS | CARRAY_WRITEABLE | CARRAY_OWNDATA;
    return array;
}

// Create array filled with ones
CArrayObject* CArray_Ones(Py_ssize_t* shape, Py_ssize_t ndim) {
    CArrayObject* array = CArray_Zeros(shape, ndim);
    if (array == NULL) return NULL;
    
    // Fill with ones
    for (Py_ssize_t i = 0; i < array->size; i++) {
        array->data[i] = 1.0;
    }
    
    return array;
}

// Element-wise addition
CArrayObject* CArray_Add(CArrayObject* self, PyObject* other) {
    // Handle scalar addition
    if (PyNumber_Check(other)) {
        double scalar = PyFloat_AsDouble(other);
        CArrayObject* result = CArray_Zeros(self->shape, self->ndim);
        if (result == NULL) return NULL;
        
        // Vectorized addition
        for (Py_ssize_t i = 0; i < self->size; i++) {
            result->data[i] = self->data[i] + scalar;
        }
        
        return result;
    }
    // Handle array addition
    else if (CArray_Check(other)) {
        CArrayObject* other_array = (CArrayObject*)other;
        
        // Check shape compatibility
        if (self->ndim != other_array->ndim || self->size != other_array->size) {
            PyErr_SetString(PyExc_ValueError, "Shape mismatch");
            return NULL;
        }
        
        CArrayObject* result = CArray_Zeros(self->shape, self->ndim);
        if (result == NULL) return NULL;
        
        // Vectorized addition
        for (Py_ssize_t i = 0; i < self->size; i++) {
            result->data[i] = self->data[i] + other_array->data[i];
        }
        
        return result;
    }
    else {
        PyErr_SetString(PyExc_TypeError, "Unsupported operand type for +");
        return NULL;
    }
}

// Sum of all elements
double CArray_Sum(CArrayObject* self) {
    double sum = 0.0;
    for (Py_ssize_t i = 0; i < self->size; i++) {
        sum += self->data[i];
    }
    return sum;
}

// Mean of all elements
double CArray_Mean(CArrayObject* self) {
    if (self->size == 0) {
        PyErr_SetString(PyExc_ValueError, "Cannot calculate mean of empty array");
        return -1.0;
    }
    return CArray_Sum(self) / (double)self->size;
}

// Python method wrappers
static PyObject* CArray_sum_method(CArrayObject* self) {
    return PyFloat_FromDouble(CArray_Sum(self));
}

static PyObject* CArray_mean_method(CArrayObject* self) {
    double mean = CArray_Mean(self);
    if (mean == -1.0 && PyErr_Occurred()) {
        return NULL;
    }
    return PyFloat_FromDouble(mean);
}

static PyObject* CArray_add_method(CArrayObject* self, PyObject* other) {
    CArrayObject* result = CArray_Add(self, other);
    if (result == NULL) return NULL;
    return (PyObject*)result;
}

// Get shape property
static PyObject* CArray_get_shape(CArrayObject* self, void* closure) {
    PyObject* shape_tuple = PyTuple_New(self->ndim);
    for (Py_ssize_t i = 0; i < self->ndim; i++) {
        PyTuple_SetItem(shape_tuple, i, PyLong_FromSsize_t(self->shape[i]));
    }
    return shape_tuple;
}

// Get size property
static PyObject* CArray_get_size(CArrayObject* self, void* closure) {
    return PyLong_FromSsize_t(self->size);
}

// Get ndim property
static PyObject* CArray_get_ndim(CArrayObject* self, void* closure) {
    return PyLong_FromSsize_t(self->ndim);
}

// Method definitions
static PyMethodDef CArray_methods[] = {
    {"sum", (PyCFunction)CArray_sum_method, METH_NOARGS, "Sum of array elements"},
    {"mean", (PyCFunction)CArray_mean_method, METH_NOARGS, "Mean of array elements"},
    {NULL}  // Sentinel
};

// Property definitions
static PyGetSetDef CArray_getsetters[] = {
    {"shape", (getter)CArray_get_shape, NULL, "Array shape", NULL},
    {"size", (getter)CArray_get_size, NULL, "Number of elements", NULL},
    {"ndim", (getter)CArray_get_ndim, NULL, "Number of dimensions", NULL},
    {NULL}  // Sentinel
};

// Number protocol for arithmetic operations
static PyObject* CArray_nb_add(PyObject* self, PyObject* other) {
    return (PyObject*)CArray_Add((CArrayObject*)self, other);
}

static PyNumberMethods CArray_as_number = {
    .nb_add = CArray_nb_add,
};

// Mapping protocol for subscripting
static PyMappingMethods CArray_as_mapping = {
    .mp_length = NULL,
    .mp_subscript = (binaryfunc)CArray_subscript,
    .mp_ass_subscript = (objobjargproc)CArray_ass_subscript,
};

// Type object definition
PyTypeObject CArrayType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "arrpy.c_src.CArray",
    .tp_doc = "C-accelerated array object",
    .tp_basicsize = sizeof(CArrayObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = CArray_new,
    .tp_init = (initproc)CArray_init,
    .tp_dealloc = (destructor)CArray_dealloc,
    .tp_repr = (reprfunc)CArray_repr,
    .tp_as_number = &CArray_as_number,
    .tp_as_mapping = &CArray_as_mapping,
    .tp_methods = CArray_methods,
    .tp_getset = CArray_getsetters,
};

// Module-level functions
static PyObject* py_zeros(PyObject* self, PyObject* args) {
    PyObject* shape_obj;
    if (!PyArg_ParseTuple(args, "O", &shape_obj)) {
        return NULL;
    }
    
    Py_ssize_t ndim;
    Py_ssize_t* shape;
    
    // Handle integer input for 1D array
    if (PyLong_Check(shape_obj)) {
        ndim = 1;
        shape = (Py_ssize_t*)malloc(sizeof(Py_ssize_t));
        shape[0] = PyLong_AsSsize_t(shape_obj);
    }
    // Handle tuple input for multi-dimensional array
    else if (PyTuple_Check(shape_obj)) {
        ndim = PyTuple_Size(shape_obj);
        shape = (Py_ssize_t*)malloc(ndim * sizeof(Py_ssize_t));
        for (Py_ssize_t i = 0; i < ndim; i++) {
            PyObject* dim = PyTuple_GetItem(shape_obj, i);
            if (!PyLong_Check(dim)) {
                free(shape);
                PyErr_SetString(PyExc_TypeError, "Shape dimensions must be integers");
                return NULL;
            }
            shape[i] = PyLong_AsSsize_t(dim);
        }
    }
    else {
        PyErr_SetString(PyExc_TypeError, "Shape must be an integer or tuple of integers");
        return NULL;
    }
    
    CArrayObject* array = CArray_Zeros(shape, ndim);
    free(shape);
    
    return (PyObject*)array;
}

static PyObject* py_ones(PyObject* self, PyObject* args) {
    PyObject* shape_obj;
    if (!PyArg_ParseTuple(args, "O", &shape_obj)) {
        return NULL;
    }
    
    Py_ssize_t ndim;
    Py_ssize_t* shape;
    
    // Handle integer input for 1D array
    if (PyLong_Check(shape_obj)) {
        ndim = 1;
        shape = (Py_ssize_t*)malloc(sizeof(Py_ssize_t));
        shape[0] = PyLong_AsSsize_t(shape_obj);
    }
    // Handle tuple input for multi-dimensional array
    else if (PyTuple_Check(shape_obj)) {
        ndim = PyTuple_Size(shape_obj);
        shape = (Py_ssize_t*)malloc(ndim * sizeof(Py_ssize_t));
        for (Py_ssize_t i = 0; i < ndim; i++) {
            PyObject* dim = PyTuple_GetItem(shape_obj, i);
            if (!PyLong_Check(dim)) {
                free(shape);
                PyErr_SetString(PyExc_TypeError, "Shape dimensions must be integers");
                return NULL;
            }
            shape[i] = PyLong_AsSsize_t(dim);
        }
    }
    else {
        PyErr_SetString(PyExc_TypeError, "Shape must be an integer or tuple of integers");
        return NULL;
    }
    
    CArrayObject* array = CArray_Ones(shape, ndim);
    free(shape);
    
    return (PyObject*)array;
}

// Module method definitions
static PyMethodDef module_methods[] = {
    {"zeros", py_zeros, METH_VARARGS, "Create array filled with zeros"},
    {"ones", py_ones, METH_VARARGS, "Create array filled with ones"},
    {NULL, NULL, 0, NULL}  // Sentinel
};

// Module definition
static struct PyModuleDef c_array_module = {
    PyModuleDef_HEAD_INIT,
    "c_array",
    "C-accelerated array implementation",
    -1,
    module_methods
};

// Module initialization
PyMODINIT_FUNC PyInit_c_array(void) {
    PyObject* m;
    
    if (PyType_Ready(&CArrayType) < 0) {
        return NULL;
    }
    
    m = PyModule_Create(&c_array_module);
    if (m == NULL) {
        return NULL;
    }
    
    Py_INCREF(&CArrayType);
    PyModule_AddObject(m, "CArray", (PyObject*)&CArrayType);
    
    return m;
}