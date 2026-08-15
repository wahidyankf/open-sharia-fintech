// => raii-vs-manual-new: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => raii-vs-manual-new: this line establishes the runnable C++ state or behavior.
#include <memory>
// => raii-vs-manual-new: this line establishes the runnable C++ state or behavior.
int main() {
// => raii-vs-manual-new: this line establishes the runnable C++ state or behavior.
  auto safer = std::make_unique<int>(9);
// => raii-vs-manual-new: this line establishes the runnable C++ state or behavior.
  std::cout << *safer << "\n";
// => raii-vs-manual-new: this line establishes the runnable C++ state or behavior.
}
