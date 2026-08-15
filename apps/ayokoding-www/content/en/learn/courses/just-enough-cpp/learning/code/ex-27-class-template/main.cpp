// => class-template: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => class-template: this line establishes the runnable C++ state or behavior.
template <typename T>
// => class-template: this line establishes the runnable C++ state or behavior.
class Box {
// => class-template: this line establishes the runnable C++ state or behavior.
 public:
// => class-template: this line establishes the runnable C++ state or behavior.
  explicit Box(T value) : value_(value) {}
// => class-template: this line establishes the runnable C++ state or behavior.
  T value() const { return value_; }
// => class-template: this line establishes the runnable C++ state or behavior.
 private:
// => class-template: this line establishes the runnable C++ state or behavior.
  T value_;
// => class-template: this line establishes the runnable C++ state or behavior.
};
// => class-template: this line establishes the runnable C++ state or behavior.
int main() {
// => class-template: this line establishes the runnable C++ state or behavior.
  std::cout << Box<int>(7).value() << " " << Box<char>('x').value() << "\n";
// => class-template: this line establishes the runnable C++ state or behavior.
}
