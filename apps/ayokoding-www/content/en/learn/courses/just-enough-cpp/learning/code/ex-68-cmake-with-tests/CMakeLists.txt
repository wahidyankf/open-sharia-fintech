# => Requires the CMake baseline for this testable project.
cmake_minimum_required(VERSION 3.16)
# => Names the project and enables C++ compilation.
project(cmake_with_tests LANGUAGES CXX)
# => Pins the primer's C++17 baseline.
set(CMAKE_CXX_STANDARD 17)
# => Builds the production code once as a library target.
add_library(math math.cpp)
# => Builds a simple executable assertion.
add_executable(math-test main.cpp)
# => Links the test to the production library.
target_link_libraries(math-test PRIVATE math)
# => Activates CTest discovery.
enable_testing()
# => Registers the executable as a named test.
add_test(NAME math-test COMMAND math-test)
