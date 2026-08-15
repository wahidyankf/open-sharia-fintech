// => vector-of-strings: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => vector-of-strings: this line establishes the runnable C++ state or behavior.
#include <string>
// => vector-of-strings: this line establishes the runnable C++ state or behavior.
#include <vector>
// => vector-of-strings: this line establishes the runnable C++ state or behavior.
int main() {
// => vector-of-strings: this line establishes the runnable C++ state or behavior.
  std::vector<std::string> names{"Ada", "Lin"};
// => vector-of-strings: this line establishes the runnable C++ state or behavior.
  for (const auto& name : names) {
// => vector-of-strings: this line establishes the runnable C++ state or behavior.
    std::cout << name << " ";
// => vector-of-strings: this line establishes the runnable C++ state or behavior.
  }
// => vector-of-strings: this line establishes the runnable C++ state or behavior.
  std::cout << "\n";
// => vector-of-strings: this line establishes the runnable C++ state or behavior.
}
