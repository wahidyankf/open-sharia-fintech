// => sanitizer-clean-suite: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => sanitizer-clean-suite: this line establishes the runnable C++ state or behavior.
#include <memory>
// => sanitizer-clean-suite: this line establishes the runnable C++ state or behavior.
int main() {
// => sanitizer-clean-suite: this line establishes the runnable C++ state or behavior.
  auto value = std::make_unique<int>(4);
// => sanitizer-clean-suite: this line establishes the runnable C++ state or behavior.
  std::cout << *value << "\n";
// => sanitizer-clean-suite: this line establishes the runnable C++ state or behavior.
}
