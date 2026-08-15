// => const-correct-api: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => const-correct-api: this line establishes the runnable C++ state or behavior.
class Meter {
// => const-correct-api: this line establishes the runnable C++ state or behavior.
 public:
// => const-correct-api: this line establishes the runnable C++ state or behavior.
  void add(int amount) { value_ += amount; }
// => const-correct-api: this line establishes the runnable C++ state or behavior.
  int value() const { return value_; }
// => const-correct-api: this line establishes the runnable C++ state or behavior.
 private:
// => const-correct-api: this line establishes the runnable C++ state or behavior.
  int value_ = 0;
// => const-correct-api: this line establishes the runnable C++ state or behavior.
};
// => const-correct-api: this line establishes the runnable C++ state or behavior.
int main() {
// => const-correct-api: this line establishes the runnable C++ state or behavior.
  Meter meter; meter.add(3); const Meter& view = meter;
// => const-correct-api: this line establishes the runnable C++ state or behavior.
  std::cout << view.value() << "\n";
// => const-correct-api: this line establishes the runnable C++ state or behavior.
}
