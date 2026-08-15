// => std-vector-basic: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => std-vector-basic: this line establishes the runnable C++ state or behavior.
#include <vector>
// => std-vector-basic: this line establishes the runnable C++ state or behavior.
int main() {
// => std-vector-basic: this line establishes the runnable C++ state or behavior.
  std::vector<int> values{1, 2};
// => std-vector-basic: this line establishes the runnable C++ state or behavior.
  values.push_back(3);
// => std-vector-basic: this line establishes the runnable C++ state or behavior.
  std::cout << values.at(2) << "\n";
// => std-vector-basic: this line establishes the runnable C++ state or behavior.
}
