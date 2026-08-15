// => templated-container-full: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => templated-container-full: this line establishes the runnable C++ state or behavior.
#include <optional>
// => templated-container-full: this line establishes the runnable C++ state or behavior.
#include <string>
// => templated-container-full: this line establishes the runnable C++ state or behavior.
#include <utility>
// => templated-container-full: this line establishes the runnable C++ state or behavior.
#include <vector>
// => templated-container-full: this line establishes the runnable C++ state or behavior.
template <typename T> class Stack {
// => templated-container-full: this line establishes the runnable C++ state or behavior.
 public:
// => templated-container-full: this line establishes the runnable C++ state or behavior.
  void push(T value) { values_.push_back(std::move(value)); }
// => templated-container-full: this line establishes the runnable C++ state or behavior.
  std::optional<T> pop() { if (values_.empty()) return std::nullopt; T value = std::move(values_.back()); values_.pop_back(); return value; }
// => templated-container-full: this line establishes the runnable C++ state or behavior.
 private:
// => templated-container-full: this line establishes the runnable C++ state or behavior.
  std::vector<T> values_;
// => templated-container-full: this line establishes the runnable C++ state or behavior.
};
// => templated-container-full: this line establishes the runnable C++ state or behavior.
int main() {
// => templated-container-full: this line establishes the runnable C++ state or behavior.
  Stack<std::string> stack; stack.push("top");
// => templated-container-full: this line establishes the runnable C++ state or behavior.
  std::cout << stack.pop().value_or("empty") << "\n";
// => templated-container-full: this line establishes the runnable C++ state or behavior.
}
