// => lambda-capture: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => lambda-capture: this line establishes the runnable C++ state or behavior.
int main() {
// => lambda-capture: this line establishes the runnable C++ state or behavior.
  int changed = 1;
// => lambda-capture: this line establishes the runnable C++ state or behavior.
int copied = 2;
// => lambda-capture: this line establishes the runnable C++ state or behavior.
  auto update = [copied, &changed] { ++changed; return copied + changed; };
// => lambda-capture: this line establishes the runnable C++ state or behavior.
  std::cout << update() << ":" << changed << "\n";
// => lambda-capture: this line establishes the runnable C++ state or behavior.
}
