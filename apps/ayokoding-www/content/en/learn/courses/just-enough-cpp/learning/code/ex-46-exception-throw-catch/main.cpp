// => exception-throw-catch: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => exception-throw-catch: this line establishes the runnable C++ state or behavior.
#include <stdexcept>
// => exception-throw-catch: this line establishes the runnable C++ state or behavior.
int main() {
// => exception-throw-catch: this line establishes the runnable C++ state or behavior.
  try {
// => exception-throw-catch: this line establishes the runnable C++ state or behavior.
    throw std::runtime_error("bad input");
// => exception-throw-catch: this line establishes the runnable C++ state or behavior.
  } catch (const std::runtime_error& error) {
// => exception-throw-catch: this line establishes the runnable C++ state or behavior.
    std::cout << error.what() << "\n";
// => exception-throw-catch: this line establishes the runnable C++ state or behavior.
  }
// => exception-throw-catch: this line establishes the runnable C++ state or behavior.
}
