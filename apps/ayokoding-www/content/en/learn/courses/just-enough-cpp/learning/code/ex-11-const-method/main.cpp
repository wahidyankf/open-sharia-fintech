// => const-method: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => const-method: this line establishes the runnable C++ state or behavior.
class Counter {
// => const-method: this line establishes the runnable C++ state or behavior.
 public:
// => const-method: this line establishes the runnable C++ state or behavior.
  int value() const { return value_; }
// => const-method: this line establishes the runnable C++ state or behavior.
 private:
// => const-method: this line establishes the runnable C++ state or behavior.
  int value_ = 4;
// => const-method: this line establishes the runnable C++ state or behavior.
};
// => const-method: this line establishes the runnable C++ state or behavior.
int main() {
// => const-method: this line establishes the runnable C++ state or behavior.
  const Counter counter;
// => const-method: this line establishes the runnable C++ state or behavior.
  std::cout << counter.value() << "\n";
// => const-method: this line establishes the runnable C++ state or behavior.
}
