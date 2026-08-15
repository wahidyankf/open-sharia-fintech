// => optional-returning-parser: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => optional-returning-parser: this line establishes the runnable C++ state or behavior.
#include <optional>
// => optional-returning-parser: this line establishes the runnable C++ state or behavior.
#include <string>
// => optional-returning-parser: this line establishes the runnable C++ state or behavior.
std::optional<int> parse_port(const std::string& text) {
// => optional-returning-parser: this line establishes the runnable C++ state or behavior.
  if (text == "80") return 80;
// => optional-returning-parser: this line establishes the runnable C++ state or behavior.
  return std::nullopt;
// => optional-returning-parser: this line establishes the runnable C++ state or behavior.
}
// => optional-returning-parser: this line establishes the runnable C++ state or behavior.
int main() {
// => optional-returning-parser: this line establishes the runnable C++ state or behavior.
  std::cout << parse_port("no").value_or(-1) << "\n";
// => optional-returning-parser: this line establishes the runnable C++ state or behavior.
}
