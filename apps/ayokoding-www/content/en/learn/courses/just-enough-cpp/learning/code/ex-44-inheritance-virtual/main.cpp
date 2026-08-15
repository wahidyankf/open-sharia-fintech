// => inheritance-virtual: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => inheritance-virtual: this line establishes the runnable C++ state or behavior.
struct Animal {
// => inheritance-virtual: this line establishes the runnable C++ state or behavior.
  virtual ~Animal() = default;
// => inheritance-virtual: this line establishes the runnable C++ state or behavior.
  virtual const char* speak() const { return "?"; }
// => inheritance-virtual: this line establishes the runnable C++ state or behavior.
};
// => inheritance-virtual: this line establishes the runnable C++ state or behavior.
struct Cat : Animal {
// => inheritance-virtual: this line establishes the runnable C++ state or behavior.
  const char* speak() const override { return "meow"; }
// => inheritance-virtual: this line establishes the runnable C++ state or behavior.
};
// => inheritance-virtual: this line establishes the runnable C++ state or behavior.
int main() {
// => inheritance-virtual: this line establishes the runnable C++ state or behavior.
  Cat cat; Animal& animal = cat;
// => inheritance-virtual: this line establishes the runnable C++ state or behavior.
  std::cout << animal.speak() << "\n";
// => inheritance-virtual: this line establishes the runnable C++ state or behavior.
}
