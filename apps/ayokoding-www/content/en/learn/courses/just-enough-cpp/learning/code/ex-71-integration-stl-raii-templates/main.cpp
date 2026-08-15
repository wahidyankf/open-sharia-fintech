// => integration-stl-raii-templates: this line establishes the runnable C++ state or behavior.
#include <algorithm>
// => integration-stl-raii-templates: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => integration-stl-raii-templates: this line establishes the runnable C++ state or behavior.
#include <memory>
// => integration-stl-raii-templates: this line establishes the runnable C++ state or behavior.
#include <vector>
// => integration-stl-raii-templates: this line establishes the runnable C++ state or behavior.
template <typename T>
// => integration-stl-raii-templates: this line establishes the runnable C++ state or behavior.
T first(const std::vector<T>& values) {
// => integration-stl-raii-templates: this line establishes the runnable C++ state or behavior.
  return values.front();
// => integration-stl-raii-templates: this line establishes the runnable C++ state or behavior.
}
// => integration-stl-raii-templates: this line establishes the runnable C++ state or behavior.
int main() {
// => integration-stl-raii-templates: this line establishes the runnable C++ state or behavior.
  auto owned = std::make_unique<std::vector<int>>(std::initializer_list<int>{1, 2, 3});
// => integration-stl-raii-templates: this line establishes the runnable C++ state or behavior.
  std::transform(owned->begin(), owned->end(), owned->begin(), [](int n) { return n * 2; });
// => integration-stl-raii-templates: this line establishes the runnable C++ state or behavior.
  std::cout << first(*owned) << "\n";
// => integration-stl-raii-templates: this line establishes the runnable C++ state or behavior.
}
