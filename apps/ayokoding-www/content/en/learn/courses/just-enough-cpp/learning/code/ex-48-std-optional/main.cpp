// => std-optional: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => std-optional: this line establishes the runnable C++ state or behavior.
#include <optional>
// => std-optional: this line establishes the runnable C++ state or behavior.
std::optional<int> parse(bool valid) {
// => std-optional: this line establishes the runnable C++ state or behavior.
  return valid ? std::optional<int>{42} : std::nullopt;
// => std-optional: this line establishes the runnable C++ state or behavior.
}
// => std-optional: this line establishes the runnable C++ state or behavior.
int main() {
// => std-optional: this line establishes the runnable C++ state or behavior.
  std::cout << parse(false).value_or(-1) << "\n";
// => std-optional: this line establishes the runnable C++ state or behavior.
}
