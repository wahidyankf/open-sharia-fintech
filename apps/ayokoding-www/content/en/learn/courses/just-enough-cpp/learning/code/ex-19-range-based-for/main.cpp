// => range-based-for: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => range-based-for: this line establishes the runnable C++ state or behavior.
#include <vector>
// => range-based-for: this line establishes the runnable C++ state or behavior.
int main() {
// => range-based-for: this line establishes the runnable C++ state or behavior.
  std::vector<int> values{1, 2, 3};
// => range-based-for: this line establishes the runnable C++ state or behavior.
  for (const auto& value : values) {
// => range-based-for: this line establishes the runnable C++ state or behavior.
    std::cout << value;
// => range-based-for: this line establishes the runnable C++ state or behavior.
  }
// => range-based-for: this line establishes the runnable C++ state or behavior.
  std::cout << "\n";
// => range-based-for: this line establishes the runnable C++ state or behavior.
}
