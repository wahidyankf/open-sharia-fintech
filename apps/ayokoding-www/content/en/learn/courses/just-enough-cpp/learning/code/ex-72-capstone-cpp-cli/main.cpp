// => capstone-cpp-cli: this line establishes the runnable C++ state or behavior.
#include "task.hpp"
// => capstone-cpp-cli: this line establishes the runnable C++ state or behavior.
#include <exception>
// => capstone-cpp-cli: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => capstone-cpp-cli: this line establishes the runnable C++ state or behavior.
int main() {
// => capstone-cpp-cli: this line establishes the runnable C++ state or behavior.
  try {
// => capstone-cpp-cli: this line establishes the runnable C++ state or behavior.
    std::cout << summarize({"write", "test"}) << "\n";
// => capstone-cpp-cli: this line establishes the runnable C++ state or behavior.
  } catch (const std::exception& error) {
// => capstone-cpp-cli: this line establishes the runnable C++ state or behavior.
    std::cerr << error.what() << "\n";
// => capstone-cpp-cli: this line establishes the runnable C++ state or behavior.
    return 1;
// => capstone-cpp-cli: this line establishes the runnable C++ state or behavior.
  }
// => capstone-cpp-cli: this line establishes the runnable C++ state or behavior.
}
