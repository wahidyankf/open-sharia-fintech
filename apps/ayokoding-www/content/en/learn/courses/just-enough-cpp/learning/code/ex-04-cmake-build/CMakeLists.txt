# => Requires CMake 3.16 or newer for this small C++17 project.
cmake_minimum_required(VERSION 3.16)
# => Names the independently buildable example.
project(cmake_build LANGUAGES CXX)
# => Pins the conservative language baseline used throughout the primer.
set(CMAKE_CXX_STANDARD 17)
# => Creates the runnable target from its annotated source.
add_executable(cmake-build main.cpp)
