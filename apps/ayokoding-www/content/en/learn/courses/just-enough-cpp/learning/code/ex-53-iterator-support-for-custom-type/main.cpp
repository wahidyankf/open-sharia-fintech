// => iterator-support-for-custom-type: this line establishes the runnable C++ state or behavior.
#include <array>
// => iterator-support-for-custom-type: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => iterator-support-for-custom-type: this line establishes the runnable C++ state or behavior.
class Pair {
// => iterator-support-for-custom-type: this line establishes the runnable C++ state or behavior.
 public:
// => iterator-support-for-custom-type: this line establishes the runnable C++ state or behavior.
  auto begin() const { return values_.begin(); }
// => iterator-support-for-custom-type: this line establishes the runnable C++ state or behavior.
  auto end() const { return values_.end(); }
// => iterator-support-for-custom-type: this line establishes the runnable C++ state or behavior.
 private:
// => iterator-support-for-custom-type: this line establishes the runnable C++ state or behavior.
  std::array<int, 2> values_{4, 5};
// => iterator-support-for-custom-type: this line establishes the runnable C++ state or behavior.
};
// => iterator-support-for-custom-type: this line establishes the runnable C++ state or behavior.
int main() {
// => iterator-support-for-custom-type: this line establishes the runnable C++ state or behavior.
  for (int value : Pair{}) std::cout << value;
// => iterator-support-for-custom-type: this line establishes the runnable C++ state or behavior.
  std::cout << "\n";
// => iterator-support-for-custom-type: this line establishes the runnable C++ state or behavior.
}
