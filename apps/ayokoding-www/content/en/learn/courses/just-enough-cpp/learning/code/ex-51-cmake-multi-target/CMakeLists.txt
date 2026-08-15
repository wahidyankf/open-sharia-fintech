# => Requires the CMake baseline for this C++17 example.
cmake_minimum_required(VERSION 3.16)
# => Names the multi-target project.
project(cmake_multi_target LANGUAGES CXX)
# => Pins the language level used by the source.
set(CMAKE_CXX_STANDARD 17)
# => Builds reusable code as its own target.
add_library(message message.cpp)
# => Builds the program that consumes the library.
add_executable(cmake-multi-target main.cpp)
# => Resolves message() by linking the executable to its library.
target_link_libraries(cmake-multi-target PRIVATE message)
