// => stl-accumulate: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => stl-accumulate: this line establishes the runnable C++ state or behavior.
#include <numeric>
// => stl-accumulate: this line establishes the runnable C++ state or behavior.
#include <vector>
// => stl-accumulate: this line establishes the runnable C++ state or behavior.
int main() {
// => stl-accumulate: this line establishes the runnable C++ state or behavior.
  const std::vector<int> values{1, 2, 3};
// => stl-accumulate: this line establishes the runnable C++ state or behavior.
  const int total = std::accumulate(values.begin(), values.end(), 0);
// => stl-accumulate: this line establishes the runnable C++ state or behavior.
  std::cout << total << "\n";
// => stl-accumulate: this line establishes the runnable C++ state or behavior.
}
