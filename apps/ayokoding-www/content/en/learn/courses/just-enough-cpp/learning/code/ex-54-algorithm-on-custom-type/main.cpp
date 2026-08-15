// => algorithm-on-custom-type: this line establishes the runnable C++ state or behavior.
#include <algorithm>
// => algorithm-on-custom-type: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => algorithm-on-custom-type: this line establishes the runnable C++ state or behavior.
#include <vector>
// => algorithm-on-custom-type: this line establishes the runnable C++ state or behavior.
struct Task { int priority; };
// => algorithm-on-custom-type: this line establishes the runnable C++ state or behavior.
int main() {
// => algorithm-on-custom-type: this line establishes the runnable C++ state or behavior.
  std::vector<Task> tasks{{2}, {1}};
// => algorithm-on-custom-type: this line establishes the runnable C++ state or behavior.
  std::sort(tasks.begin(), tasks.end(), [](const Task& left, const Task& right) { return left.priority < right.priority; });
// => algorithm-on-custom-type: this line establishes the runnable C++ state or behavior.
  std::cout << tasks.front().priority << "\n";
// => algorithm-on-custom-type: this line establishes the runnable C++ state or behavior.
}
