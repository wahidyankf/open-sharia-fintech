// => exception-hierarchy: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => exception-hierarchy: this line establishes the runnable C++ state or behavior.
#include <stdexcept>
// => exception-hierarchy: this line establishes the runnable C++ state or behavior.
struct InputError : std::runtime_error {
// => exception-hierarchy: this line establishes the runnable C++ state or behavior.
  using std::runtime_error::runtime_error;
// => exception-hierarchy: this line establishes the runnable C++ state or behavior.
};
// => exception-hierarchy: this line establishes the runnable C++ state or behavior.
int main() {
// => exception-hierarchy: this line establishes the runnable C++ state or behavior.
  try { throw InputError("missing"); }
// => exception-hierarchy: this line establishes the runnable C++ state or behavior.
  catch (const std::runtime_error& error) { std::cout << error.what() << "\n"; }
// => exception-hierarchy: this line establishes the runnable C++ state or behavior.
}
