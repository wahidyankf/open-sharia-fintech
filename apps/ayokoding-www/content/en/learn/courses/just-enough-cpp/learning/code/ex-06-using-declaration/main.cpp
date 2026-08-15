// => using-declaration: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => using-declaration: this line establishes the runnable C++ state or behavior.
namespace status {
// => using-declaration: this line establishes the runnable C++ state or behavior.
int code() { return 200; }
// => using-declaration: this line establishes the runnable C++ state or behavior.
}
// => using-declaration: this line establishes the runnable C++ state or behavior.
using status::code;
// => using-declaration: this line establishes the runnable C++ state or behavior.
int main() {
// => using-declaration: this line establishes the runnable C++ state or behavior.
  std::cout << code() << "\n";
// => using-declaration: this line establishes the runnable C++ state or behavior.
}
