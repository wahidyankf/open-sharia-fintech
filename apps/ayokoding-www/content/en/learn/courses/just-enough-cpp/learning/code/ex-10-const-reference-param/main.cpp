// => const-reference-param: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => const-reference-param: this line establishes the runnable C++ state or behavior.
#include <string>
// => const-reference-param: this line establishes the runnable C++ state or behavior.
std::size_t length_of(const std::string& text) {
// => const-reference-param: this line establishes the runnable C++ state or behavior.
  return text.size();
// => const-reference-param: this line establishes the runnable C++ state or behavior.
}
// => const-reference-param: this line establishes the runnable C++ state or behavior.
int main() {
// => const-reference-param: this line establishes the runnable C++ state or behavior.
  const std::string name = "Ada";
// => const-reference-param: this line establishes the runnable C++ state or behavior.
  std::cout << length_of(name) << "\n";
// => const-reference-param: this line establishes the runnable C++ state or behavior.
}
