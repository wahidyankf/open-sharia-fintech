// => sanitizer-run: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => sanitizer-run: this line establishes the runnable C++ state or behavior.
#include <vector>
// => sanitizer-run: this line establishes the runnable C++ state or behavior.
int main() {
// => sanitizer-run: this line establishes the runnable C++ state or behavior.
  const std::vector<int> values{1, 2, 3};
// => sanitizer-run: this line establishes the runnable C++ state or behavior.
  std::cout << values.at(2) << "\n";
// => sanitizer-run: this line establishes the runnable C++ state or behavior.
}
