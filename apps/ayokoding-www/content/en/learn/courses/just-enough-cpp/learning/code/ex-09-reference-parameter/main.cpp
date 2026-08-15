// => reference-parameter: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => reference-parameter: this line establishes the runnable C++ state or behavior.
void increment(int& value) {
// => reference-parameter: this line establishes the runnable C++ state or behavior.
  ++value;
// => reference-parameter: this line establishes the runnable C++ state or behavior.
}
// => reference-parameter: this line establishes the runnable C++ state or behavior.
int main() {
// => reference-parameter: this line establishes the runnable C++ state or behavior.
  int count = 1;
// => reference-parameter: this line establishes the runnable C++ state or behavior.
  increment(count);
// => reference-parameter: this line establishes the runnable C++ state or behavior.
  std::cout << count << "\n";
// => reference-parameter: this line establishes the runnable C++ state or behavior.
}
