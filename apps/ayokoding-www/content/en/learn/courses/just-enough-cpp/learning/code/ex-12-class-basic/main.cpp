// => class-basic: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => class-basic: this line establishes the runnable C++ state or behavior.
class Greeting {
// => class-basic: this line establishes the runnable C++ state or behavior.
 public:
// => class-basic: this line establishes the runnable C++ state or behavior.
  void print() const { std::cout << "hello\n"; }
// => class-basic: this line establishes the runnable C++ state or behavior.
};
// => class-basic: this line establishes the runnable C++ state or behavior.
int main() {
// => class-basic: this line establishes the runnable C++ state or behavior.
  Greeting greeting;
// => class-basic: this line establishes the runnable C++ state or behavior.
  greeting.print();
// => class-basic: this line establishes the runnable C++ state or behavior.
}
