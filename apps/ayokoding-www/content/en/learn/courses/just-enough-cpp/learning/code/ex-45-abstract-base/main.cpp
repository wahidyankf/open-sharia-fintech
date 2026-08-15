// => abstract-base: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => abstract-base: this line establishes the runnable C++ state or behavior.
struct Writer {
// => abstract-base: this line establishes the runnable C++ state or behavior.
  virtual ~Writer() = default;
// => abstract-base: this line establishes the runnable C++ state or behavior.
  virtual void write() const = 0;
// => abstract-base: this line establishes the runnable C++ state or behavior.
};
// => abstract-base: this line establishes the runnable C++ state or behavior.
struct ConsoleWriter : Writer {
// => abstract-base: this line establishes the runnable C++ state or behavior.
  void write() const override { std::cout << "written\n"; }
// => abstract-base: this line establishes the runnable C++ state or behavior.
};
// => abstract-base: this line establishes the runnable C++ state or behavior.
int main() {
// => abstract-base: this line establishes the runnable C++ state or behavior.
  ConsoleWriter concrete; const Writer& writer = concrete;
// => abstract-base: this line establishes the runnable C++ state or behavior.
  writer.write();
// => abstract-base: this line establishes the runnable C++ state or behavior.
}
