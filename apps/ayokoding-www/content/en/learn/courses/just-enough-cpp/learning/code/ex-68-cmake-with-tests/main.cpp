// => cmake-with-tests: this line establishes the runnable C++ state or behavior.
#include "math.hpp"
// => cmake-with-tests: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => cmake-with-tests: this line establishes the runnable C++ state or behavior.
int main() {
// => cmake-with-tests: this line establishes the runnable C++ state or behavior.
  if (add(2, 3) != 5) return 1;
// => cmake-with-tests: this line establishes the runnable C++ state or behavior.
  std::cout << "test passed\n";
// => cmake-with-tests: this line establishes the runnable C++ state or behavior.
}
