// => c-interop: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => c-interop: this line establishes the runnable C++ state or behavior.
extern "C" int c_add(int left, int right);
// => c-interop: this line establishes the runnable C++ state or behavior.
int main() {
// => c-interop: this line establishes the runnable C++ state or behavior.
  std::cout << c_add(2, 3) << "\n";
// => c-interop: this line establishes the runnable C++ state or behavior.
}
