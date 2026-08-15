// => unique-ptr: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => unique-ptr: this line establishes the runnable C++ state or behavior.
#include <memory>
// => unique-ptr: this line establishes the runnable C++ state or behavior.
int main() {
// => unique-ptr: this line establishes the runnable C++ state or behavior.
  auto value = std::make_unique<int>(7);
// => unique-ptr: this line establishes the runnable C++ state or behavior.
  std::cout << *value << "\n";
// => unique-ptr: this line establishes the runnable C++ state or behavior.
}
