// => destructor-trace: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => destructor-trace: this line establishes the runnable C++ state or behavior.
class Trace {
// => destructor-trace: this line establishes the runnable C++ state or behavior.
 public:
// => destructor-trace: this line establishes the runnable C++ state or behavior.
  ~Trace() { std::cout << "destroyed\n"; }
// => destructor-trace: this line establishes the runnable C++ state or behavior.
};
// => destructor-trace: this line establishes the runnable C++ state or behavior.
int main() {
// => destructor-trace: this line establishes the runnable C++ state or behavior.
  { Trace trace; std::cout << "inside\n"; }
// => destructor-trace: this line establishes the runnable C++ state or behavior.
  std::cout << "after\n";
// => destructor-trace: this line establishes the runnable C++ state or behavior.
}
