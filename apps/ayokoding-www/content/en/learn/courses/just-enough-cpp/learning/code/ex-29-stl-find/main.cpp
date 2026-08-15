// => stl-find: this line establishes the runnable C++ state or behavior.
#include <algorithm>
// => stl-find: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => stl-find: this line establishes the runnable C++ state or behavior.
#include <vector>
// => stl-find: this line establishes the runnable C++ state or behavior.
int main() {
// => stl-find: this line establishes the runnable C++ state or behavior.
  std::vector<int> values{3, 1, 2};
// => stl-find: this line establishes the runnable C++ state or behavior.
  const auto hit = std::find(values.begin(), values.end(), 1);
// => stl-find: this line establishes the runnable C++ state or behavior.
  std::cout << (hit != values.end()) << "\n";
// => stl-find: this line establishes the runnable C++ state or behavior.
}
