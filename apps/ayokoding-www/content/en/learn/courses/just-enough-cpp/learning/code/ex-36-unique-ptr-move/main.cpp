// => unique-ptr-move: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => unique-ptr-move: this line establishes the runnable C++ state or behavior.
#include <memory>
// => unique-ptr-move: this line establishes the runnable C++ state or behavior.
#include <utility>
// => unique-ptr-move: this line establishes the runnable C++ state or behavior.
int main() {
// => unique-ptr-move: this line establishes the runnable C++ state or behavior.
  auto source = std::make_unique<int>(7);
// => unique-ptr-move: this line establishes the runnable C++ state or behavior.
  auto destination = std::move(source);
// => unique-ptr-move: this line establishes the runnable C++ state or behavior.
  std::cout << (source == nullptr) << ":" << *destination << "\n";
// => unique-ptr-move: this line establishes the runnable C++ state or behavior.
}
