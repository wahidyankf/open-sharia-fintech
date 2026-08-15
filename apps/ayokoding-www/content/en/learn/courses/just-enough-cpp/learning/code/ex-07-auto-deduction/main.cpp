// => auto-deduction: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => auto-deduction: this line establishes the runnable C++ state or behavior.
#include <type_traits>
// => auto-deduction: this line establishes the runnable C++ state or behavior.
int main() {
// => auto-deduction: this line establishes the runnable C++ state or behavior.
  auto count = 3;
// => auto-deduction: this line establishes the runnable C++ state or behavior.
  static_assert(std::is_same_v<decltype(count), int>);
// => auto-deduction: this line establishes the runnable C++ state or behavior.
  std::cout << count << "\n";
// => auto-deduction: this line establishes the runnable C++ state or behavior.
}
