// => template-specialization: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => template-specialization: this line establishes the runnable C++ state or behavior.
template <typename T> struct Label {
// => template-specialization: this line establishes the runnable C++ state or behavior.
  static const char* value() { return "other"; }
// => template-specialization: this line establishes the runnable C++ state or behavior.
};
// => template-specialization: this line establishes the runnable C++ state or behavior.
template <> struct Label<int> {
// => template-specialization: this line establishes the runnable C++ state or behavior.
  static const char* value() { return "int"; }
// => template-specialization: this line establishes the runnable C++ state or behavior.
};
// => template-specialization: this line establishes the runnable C++ state or behavior.
int main() {
// => template-specialization: this line establishes the runnable C++ state or behavior.
  std::cout << Label<int>::value() << ":" << Label<char>::value() << "\n";
// => template-specialization: this line establishes the runnable C++ state or behavior.
}
