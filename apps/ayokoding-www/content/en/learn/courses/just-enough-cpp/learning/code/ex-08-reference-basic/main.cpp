// => reference-basic: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => reference-basic: this line establishes the runnable C++ state or behavior.
int main() {
// => reference-basic: this line establishes the runnable C++ state or behavior.
  int original = 7;
// => reference-basic: this line establishes the runnable C++ state or behavior.
  int& alias = original;
// => reference-basic: this line establishes the runnable C++ state or behavior.
  alias = 9;
// => reference-basic: this line establishes the runnable C++ state or behavior.
  std::cout << original << "\n";
// => reference-basic: this line establishes the runnable C++ state or behavior.
}
