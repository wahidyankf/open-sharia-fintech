// => iterator-explicit: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => iterator-explicit: this line establishes the runnable C++ state or behavior.
#include <vector>
// => iterator-explicit: this line establishes the runnable C++ state or behavior.
int main() {
// => iterator-explicit: this line establishes the runnable C++ state or behavior.
  const std::vector<int> values{4, 5};
// => iterator-explicit: this line establishes the runnable C++ state or behavior.
  for (auto it = values.begin(); it != values.end(); ++it) {
// => iterator-explicit: this line establishes the runnable C++ state or behavior.
    std::cout << *it;
// => iterator-explicit: this line establishes the runnable C++ state or behavior.
  }
// => iterator-explicit: this line establishes the runnable C++ state or behavior.
  std::cout << "\n";
// => iterator-explicit: this line establishes the runnable C++ state or behavior.
}
