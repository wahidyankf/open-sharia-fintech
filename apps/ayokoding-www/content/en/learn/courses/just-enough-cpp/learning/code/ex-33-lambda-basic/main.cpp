// => lambda-basic: this line establishes the runnable C++ state or behavior.
#include <algorithm>
// => lambda-basic: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => lambda-basic: this line establishes the runnable C++ state or behavior.
#include <vector>
// => lambda-basic: this line establishes the runnable C++ state or behavior.
int main() {
// => lambda-basic: this line establishes the runnable C++ state or behavior.
  std::vector<int> values{1, 3, 2};
// => lambda-basic: this line establishes the runnable C++ state or behavior.
  std::sort(values.begin(), values.end(), [](int a, int b) { return a > b; });
// => lambda-basic: this line establishes the runnable C++ state or behavior.
  std::cout << values[0] << "\n";
// => lambda-basic: this line establishes the runnable C++ state or behavior.
}
