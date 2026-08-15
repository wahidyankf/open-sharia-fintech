// => template-multiple-types: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => template-multiple-types: this line establishes the runnable C++ state or behavior.
template <typename Left, typename Right>
// => template-multiple-types: this line establishes the runnable C++ state or behavior.
auto add(Left left, Right right) {
// => template-multiple-types: this line establishes the runnable C++ state or behavior.
  return left + right;
// => template-multiple-types: this line establishes the runnable C++ state or behavior.
}
// => template-multiple-types: this line establishes the runnable C++ state or behavior.
int main() {
// => template-multiple-types: this line establishes the runnable C++ state or behavior.
  std::cout << add(2, 0.5) << "\n";
// => template-multiple-types: this line establishes the runnable C++ state or behavior.
}
