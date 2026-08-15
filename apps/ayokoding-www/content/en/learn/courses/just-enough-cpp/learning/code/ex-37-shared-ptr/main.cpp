// => shared-ptr: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => shared-ptr: this line establishes the runnable C++ state or behavior.
#include <memory>
// => shared-ptr: this line establishes the runnable C++ state or behavior.
int main() {
// => shared-ptr: this line establishes the runnable C++ state or behavior.
  auto first = std::make_shared<int>(7);
// => shared-ptr: this line establishes the runnable C++ state or behavior.
  auto second = first;
// => shared-ptr: this line establishes the runnable C++ state or behavior.
  std::cout << second.use_count() << ":" << *first << "\n";
// => shared-ptr: this line establishes the runnable C++ state or behavior.
}
