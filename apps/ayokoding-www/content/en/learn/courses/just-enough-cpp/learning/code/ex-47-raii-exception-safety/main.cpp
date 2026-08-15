// => raii-exception-safety: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => raii-exception-safety: this line establishes the runnable C++ state or behavior.
#include <stdexcept>
// => raii-exception-safety: this line establishes the runnable C++ state or behavior.
struct Guard {
// => raii-exception-safety: this line establishes the runnable C++ state or behavior.
  ~Guard() { std::cout << "released\n"; }
// => raii-exception-safety: this line establishes the runnable C++ state or behavior.
};
// => raii-exception-safety: this line establishes the runnable C++ state or behavior.
int main() {
// => raii-exception-safety: this line establishes the runnable C++ state or behavior.
  try {
// => raii-exception-safety: this line establishes the runnable C++ state or behavior.
    Guard guard;
// => raii-exception-safety: this line establishes the runnable C++ state or behavior.
    throw std::runtime_error("stop");
// => raii-exception-safety: this line establishes the runnable C++ state or behavior.
  } catch (const std::runtime_error&) {
// => raii-exception-safety: this line establishes the runnable C++ state or behavior.
    std::cout << "caught\n";
// => raii-exception-safety: this line establishes the runnable C++ state or behavior.
  }
// => raii-exception-safety: this line establishes the runnable C++ state or behavior.
}
