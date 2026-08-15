// => structured-bindings: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => structured-bindings: this line establishes the runnable C++ state or behavior.
#include <utility>
// => structured-bindings: this line establishes the runnable C++ state or behavior.
int main() {
// => structured-bindings: this line establishes the runnable C++ state or behavior.
  const std::pair<int, int> point{2, 3};
// => structured-bindings: this line establishes the runnable C++ state or behavior.
  const auto [x, y] = point;
// => structured-bindings: this line establishes the runnable C++ state or behavior.
  std::cout << x + y << "\n";
// => structured-bindings: this line establishes the runnable C++ state or behavior.
}
