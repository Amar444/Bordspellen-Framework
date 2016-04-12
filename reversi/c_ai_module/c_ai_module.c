#include <Python.h>
#include <numpy/arrayobject.h>
#include "ai_core.h"
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

static PyObject* best_move(PyObject *self, PyObject *args)
{
    int player; /* define an int containing the value of player (1 or 2) */
    int **board; /* define an int pointer to the location of board ( an 8x8 2d int array) */
    PyObject *temp_board; /*define a pointer to store the board tuple in*/

    /* Parse the tuple that gets passed by python into the module*/
    if (!PyArg_ParseTuple(args,"Oi", &temp_board, &player ))
    {
        return NULL;
    }
    /*parse the numpy array */
    /*temp_board = PyArray_FROM_OTF(temp_board, NPY_INT, NPY_ARRAY_IN_ARRAY);*/
    int typenum = NPY_DOUBLE;
    PyArray_Descr *descr;
    descr = PyArray_DescrFromType(typenum);
    npy_intp dims[7]; /*8 possible values counted from 0*/
    if (PyArray_AsCArray(&temp_board, (void**)&board, dims, 2, descr) < 0){
        PyErr_SetString(PyExc_TypeError, "error converting to c array");
        return NULL;
    }

    int row = 0, col = 0;

    return Py_BuildValue("ii", row, col);
}

static char c_ai_module_docs[] =
    "c_ai_module : Used for calculating optimal Reversi moves\n Returns a Tuple with the format (row,col)\n";

static PyMethodDef c_ai_module_funcs[] = {
    {"best_move", (PyCFunction)best_move, METH_VARARGS, c_ai_module_docs},
    {NULL} /*NULL is used to signal that the mehtod defenition has ended*/
};

static struct PyModuleDef c_ai_moduleModule =
{
    PyModuleDef_HEAD_INIT,
    "c_ai_module",
    c_ai_module_docs,
    -1,
    c_ai_module_funcs
};

PyMODINIT_FUNC PyInit_c_ai_module(void)
{
    import_array();
    return PyModule_Create(&c_ai_moduleModule);
}