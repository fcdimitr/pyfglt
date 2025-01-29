#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

#include <iostream>

#include "fglt.hpp"

namespace py = pybind11;

py::array_t<double, py::array::c_style> count(const py::object &sparse_mat) {

    // 1) Extract needed attributes from the CSC matrix:
    //    - indices -> row indices
    //    - indptr  -> column pointer offsets
    //    - shape   -> (num_rows, num_cols)
    py::array_t<mwIndex> indices = sparse_mat.attr("indices").cast<py::array_t<mwIndex>>();
    py::array_t<mwIndex> indptr  = sparse_mat.attr("indptr").cast<py::array_t<mwIndex>>();

    // shape is a 2-tuple (nrows, ncols)
    auto shape_py  = sparse_mat.attr("shape");
    auto shape_vec = shape_py.cast<std::pair<mwSize, mwSize>>();
    mwSize nrows = shape_vec.first;
    mwSize ncols = shape_vec.second;

    // For CSC: 
    //   - 'indices' has length = number_of_nonzeros = m
    //   - 'indptr' has length = (ncols + 1)
    //   - 'indices' are the row indices
    //   - 'indptr' gives you the column start
    mwSize m  = indices.size(); // number of nonzeros
    mwSize n  = ncols;          // number of columns

    // 2) Prepare Nx16 arrays for f and fn. We'll store them
    //    in continuous buffers but also keep "double**" pointers
    //    for each column.
    const mwSize NUM_FREQS = 16;

    // Host buffers for all data
    std::vector<double> f_buffer(n * NUM_FREQS, 0.0);
    std::vector<double> fn_buffer(n * NUM_FREQS, 0.0);

    // Pointers for each column
    std::vector<double*> f_ptrs(NUM_FREQS, nullptr);
    std::vector<double*> fn_ptrs(NUM_FREQS, nullptr);
    for (mwSize col = 0; col < NUM_FREQS; ++col) {
        f_ptrs[col]  = &f_buffer[col * n];
        fn_ptrs[col] = &fn_buffer[col * n];
    }

    mwIndex *ii = const_cast<mwIndex*>(indices.data());
    mwIndex *jStart = const_cast<mwIndex*>(indptr.data());

    // 3) Call the C function
    int status = compute(f_ptrs.data(),
                         fn_ptrs.data(),
                         ii,
                         jStart,
                         n, // number of columns
                         m, // number of nonzeros
                         1  // number of parallel workers (only single-threaded)
                        );
    if (status != 0) {
        throw std::runtime_error("compute(...) returned non-zero status: " + std::to_string(status));
    }

    // 4) Wrap the results back into NumPy arrays of shape (n, 16).
    //    We copy data into new NumPy arrays to avoid lifetime issues 
    //    (f_buffer is a local variable).
    

    // create empty NumPy arrays
    py::array_t<double> f_py({static_cast<py::ssize_t>(NUM_FREQS), static_cast<py::ssize_t>(n)});
    py::array_t<double> fn_py({static_cast<py::ssize_t>(NUM_FREQS), static_cast<py::ssize_t>(n)});

    // copy the data
    std::memcpy(f_py.mutable_data(),  f_buffer.data(),  n * NUM_FREQS * sizeof(double));
    std::memcpy(fn_py.mutable_data(), fn_buffer.data(), n * NUM_FREQS * sizeof(double));

    // 5) Return a tuple (f, fn)
    return py::make_tuple(f_py, fn_py);
}

PYBIND11_MODULE(_fglt_c, m) {
		m.def("count", &count);
}