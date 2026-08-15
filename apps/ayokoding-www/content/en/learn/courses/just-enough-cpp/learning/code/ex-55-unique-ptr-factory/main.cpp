// => unique-ptr-factory: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => unique-ptr-factory: this line establishes the runnable C++ state or behavior.
#include <memory>
// => unique-ptr-factory: this line establishes the runnable C++ state or behavior.
std::unique_ptr<int> make_score() {
// => unique-ptr-factory: this line establishes the runnable C++ state or behavior.
  return std::make_unique<int>(99);
// => unique-ptr-factory: this line establishes the runnable C++ state or behavior.
}
// => unique-ptr-factory: this line establishes the runnable C++ state or behavior.
int main() {
// => unique-ptr-factory: this line establishes the runnable C++ state or behavior.
  auto score = make_score();
// => unique-ptr-factory: this line establishes the runnable C++ state or behavior.
  std::cout << *score << "\n";
// => unique-ptr-factory: this line establishes the runnable C++ state or behavior.
}
