// => stl-transform: this line establishes the runnable C++ state or behavior.
#include <algorithm>
// => stl-transform: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => stl-transform: this line establishes the runnable C++ state or behavior.
#include <vector>
// => stl-transform: this line establishes the runnable C++ state or behavior.
int main() {
// => stl-transform: this line establishes the runnable C++ state or behavior.
  std::vector<int> input{1, 2, 3};
// => stl-transform: this line establishes the runnable C++ state or behavior.
  std::vector<int> output(input.size());
// => stl-transform: this line establishes the runnable C++ state or behavior.
  std::transform(input.begin(), input.end(), output.begin(), [](int n) { return n * n; });
// => stl-transform: this line establishes the runnable C++ state or behavior.
  std::cout << output[2] << "\n";
// => stl-transform: this line establishes the runnable C++ state or behavior.
}
