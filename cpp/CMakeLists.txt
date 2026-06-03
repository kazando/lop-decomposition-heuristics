cmake_minimum_required(VERSION 3.14)
project(hao_orlin_cpp)

find_package(pybind11 REQUIRED)

# Ubuntu / Macでの簡易リンク
include_directories(/usr/include)
link_libraries(lemon)

pybind11_add_module(hao_orlin_cpp hao_orlin_bind.cpp)
target_link_libraries(hao_orlin_cpp PRIVATE lemon)