// => stl-sort: this line establishes the runnable C++ state or behavior.
#include <algorithm>
// => stl-sort: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => stl-sort: this line establishes the runnable C++ state or behavior.
#include <vector>
// => stl-sort: this line establishes the runnable C++ state or behavior.
int main() {
// => stl-sort: this line establishes the runnable C++ state or behavior.
  std::vector<int> values{3, 1, 2};
// => stl-sort: this line establishes the runnable C++ state or behavior.
  std::sort(values.begin(), values.end());
// => stl-sort: this line establishes the runnable C++ state or behavior.
  std::cout << values[0] << values[1] << values[2] << "\n";
// => stl-sort: this line establishes the runnable C++ state or behavior.
}
