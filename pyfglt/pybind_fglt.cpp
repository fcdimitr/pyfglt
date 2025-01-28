#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

#include "fglt.hpp"

namespace py = pybind11;

py::array_t<double, py::array::c_style> count(int n, int d) {

    py::array_t<double, py::array::c_style> y({n,d});

    
    return y;
}

PYBIND11_MODULE(_fglt_c, m) {
		m.def("count", &count);
}