// => namespace-basic: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => namespace-basic: this line establishes the runnable C++ state or behavior.
namespace status {
// => namespace-basic: this line establishes the runnable C++ state or behavior.
int code() { return 200; }
// => namespace-basic: this line establishes the runnable C++ state or behavior.
}
// => namespace-basic: this line establishes the runnable C++ state or behavior.
int main() {
// => namespace-basic: this line establishes the runnable C++ state or behavior.
  std::cout << status::code() << "\n";
// => namespace-basic: this line establishes the runnable C++ state or behavior.
}
