# => Requires a modern but widely available CMake release.
cmake_minimum_required(VERSION 3.16)
# => Defines the capstone C++ project.
project(just_enough_cpp_capstone LANGUAGES CXX)
# => Pins all targets to C++17.
set(CMAKE_CXX_STANDARD 17)
# => Enables portable warning flags for every capstone target.
add_library(capstone-warnings INTERFACE)
target_compile_options(capstone-warnings INTERFACE -Wall -Wextra -Wpedantic)
# => Enables AddressSanitizer and UndefinedBehaviorSanitizer when requested.
option(ENABLE_SANITIZERS "Enable address and undefined behavior sanitizers" OFF)
if(ENABLE_SANITIZERS AND CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")
  target_compile_options(capstone-warnings INTERFACE -fsanitize=address,undefined -fno-omit-frame-pointer)
  target_link_options(capstone-warnings INTERFACE -fsanitize=address,undefined)
endif()
add_library(task task.cpp)
target_link_libraries(task PRIVATE capstone-warnings)
# => Builds the CLI program.
add_executable(task-cli main.cpp)
# => Links CLI ownership to the library target.
target_link_libraries(task-cli PRIVATE task)
# => Builds the automated capstone check.
add_executable(task-test task_test.cpp)
# => Links the test to production behavior.
target_link_libraries(task-test PRIVATE task)
target_link_libraries(task-cli PRIVATE capstone-warnings)
target_link_libraries(task-test PRIVATE capstone-warnings)
# => Registers the test with CTest.
enable_testing()
add_test(NAME task-test COMMAND task-test)
