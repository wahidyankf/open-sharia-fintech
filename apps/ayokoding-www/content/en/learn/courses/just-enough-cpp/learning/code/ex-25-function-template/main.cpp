// => function-template: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => function-template: this line establishes the runnable C++ state or behavior.
template <typename T>
// => function-template: this line establishes the runnable C++ state or behavior.
T larger(T left, T right) {
// => function-template: this line establishes the runnable C++ state or behavior.
  return left > right ? left : right;
// => function-template: this line establishes the runnable C++ state or behavior.
}
// => function-template: this line establishes the runnable C++ state or behavior.
int main() {
// => function-template: this line establishes the runnable C++ state or behavior.
  std::cout << larger(2, 5) << " " << larger(1.5, 1.2) << "\n";
// => function-template: this line establishes the runnable C++ state or behavior.
}
