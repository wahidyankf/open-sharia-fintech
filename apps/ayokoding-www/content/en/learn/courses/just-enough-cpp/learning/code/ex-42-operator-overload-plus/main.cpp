// => operator-overload-plus: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => operator-overload-plus: this line establishes the runnable C++ state or behavior.
struct Meters {
// => operator-overload-plus: this line establishes the runnable C++ state or behavior.
  int value;
// => operator-overload-plus: this line establishes the runnable C++ state or behavior.
};
// => operator-overload-plus: this line establishes the runnable C++ state or behavior.
Meters operator+(Meters left, Meters right) {
// => operator-overload-plus: this line establishes the runnable C++ state or behavior.
  return {left.value + right.value};
// => operator-overload-plus: this line establishes the runnable C++ state or behavior.
}
// => operator-overload-plus: this line establishes the runnable C++ state or behavior.
int main() {
// => operator-overload-plus: this line establishes the runnable C++ state or behavior.
  std::cout << (Meters{2} + Meters{3}).value << "\n";
// => operator-overload-plus: this line establishes the runnable C++ state or behavior.
}
