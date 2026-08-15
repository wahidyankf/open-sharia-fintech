// => std-variant: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => std-variant: this line establishes the runnable C++ state or behavior.
#include <string>
// => std-variant: this line establishes the runnable C++ state or behavior.
#include <variant>
// => std-variant: this line establishes the runnable C++ state or behavior.
int main() {
// => std-variant: this line establishes the runnable C++ state or behavior.
  std::variant<int, std::string> value = "ready";
// => std-variant: this line establishes the runnable C++ state or behavior.
  std::visit([](const auto& item) { std::cout << item << "\n"; }, value);
// => std-variant: this line establishes the runnable C++ state or behavior.
}
