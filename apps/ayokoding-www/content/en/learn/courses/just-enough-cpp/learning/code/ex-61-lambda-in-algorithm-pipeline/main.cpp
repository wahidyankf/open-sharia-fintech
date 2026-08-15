// => lambda-in-algorithm-pipeline: this line establishes the runnable C++ state or behavior.
#include <algorithm>
// => lambda-in-algorithm-pipeline: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => lambda-in-algorithm-pipeline: this line establishes the runnable C++ state or behavior.
#include <numeric>
// => lambda-in-algorithm-pipeline: this line establishes the runnable C++ state or behavior.
#include <vector>
// => lambda-in-algorithm-pipeline: this line establishes the runnable C++ state or behavior.
int main() {
// => lambda-in-algorithm-pipeline: this line establishes the runnable C++ state or behavior.
  const std::vector<int> input{1, 2, 3};
// => lambda-in-algorithm-pipeline: this line establishes the runnable C++ state or behavior.
  std::vector<int> doubled(input.size());
// => lambda-in-algorithm-pipeline: this line establishes the runnable C++ state or behavior.
  std::transform(input.begin(), input.end(), doubled.begin(), [](int value) { return value * 2; });
// => lambda-in-algorithm-pipeline: this line establishes the runnable C++ state or behavior.
  std::cout << std::accumulate(doubled.begin(), doubled.end(), 0) << "\n";
// => lambda-in-algorithm-pipeline: this line establishes the runnable C++ state or behavior.
}
