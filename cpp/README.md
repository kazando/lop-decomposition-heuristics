# C++ Extension for Global Minimum Cut Computation

This directory contains a C++ implementation used by the minimum cut constructive heuristic.

The implementation is based on the Hao--Orlin minimum cut algorithm provided by the LEMON graph library and is exposed to Python through a pybind11 binding.

## Files

* `hao_orlin_cpp.cpp` : pybind11 wrapper and Python interface.
* `CMakeLists.txt` : build configuration.

## Requirements

* C++17 compatible compiler
* LEMON graph library
* pybind11
* CMake

## Build

```bash
cmake .
make
```

The resulting shared library can then be imported from Python by the minimum cut heuristic implementation in `src/`.
