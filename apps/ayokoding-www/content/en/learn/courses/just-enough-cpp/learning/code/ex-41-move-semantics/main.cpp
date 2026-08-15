// => move-semantics: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => move-semantics: this line establishes the runnable C++ state or behavior.
#include <memory>
// => move-semantics: this line establishes the runnable C++ state or behavior.
#include <utility>
// => move-semantics: this line establishes the runnable C++ state or behavior.
class Handle {
// => move-semantics: this line establishes the runnable C++ state or behavior.
 public:
// => move-semantics: this line establishes the runnable C++ state or behavior.
  Handle() : value_(std::make_unique<int>(8)) {}
// => move-semantics: this line establishes the runnable C++ state or behavior.
  Handle(Handle&&) noexcept = default;
// => move-semantics: this line establishes the runnable C++ state or behavior.
  Handle& operator=(Handle&&) noexcept = default;
// => move-semantics: this line establishes the runnable C++ state or behavior.
  Handle(const Handle&) = delete;
// => move-semantics: this line establishes the runnable C++ state or behavior.
  int value() const { return *value_; }
// => move-semantics: this line establishes the runnable C++ state or behavior.
 private:
// => move-semantics: this line establishes the runnable C++ state or behavior.
  std::unique_ptr<int> value_;
// => move-semantics: this line establishes the runnable C++ state or behavior.
};
// => move-semantics: this line establishes the runnable C++ state or behavior.
int main() {
// => move-semantics: this line establishes the runnable C++ state or behavior.
  Handle first; Handle second = std::move(first);
// => move-semantics: this line establishes the runnable C++ state or behavior.
  std::cout << second.value() << "\n";
// => move-semantics: this line establishes the runnable C++ state or behavior.
}
