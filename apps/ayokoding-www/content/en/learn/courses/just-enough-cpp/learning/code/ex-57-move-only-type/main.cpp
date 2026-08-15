// => move-only-type: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => move-only-type: this line establishes the runnable C++ state or behavior.
#include <memory>
// => move-only-type: this line establishes the runnable C++ state or behavior.
#include <utility>
// => move-only-type: this line establishes the runnable C++ state or behavior.
class Token {
// => move-only-type: this line establishes the runnable C++ state or behavior.
 public:
// => move-only-type: this line establishes the runnable C++ state or behavior.
  Token() : value_(std::make_unique<int>(1)) {}
// => move-only-type: this line establishes the runnable C++ state or behavior.
  Token(Token&&) noexcept = default;
// => move-only-type: this line establishes the runnable C++ state or behavior.
  Token(const Token&) = delete;
// => move-only-type: this line establishes the runnable C++ state or behavior.
  int value() const { return *value_; }
// => move-only-type: this line establishes the runnable C++ state or behavior.
 private:
// => move-only-type: this line establishes the runnable C++ state or behavior.
  std::unique_ptr<int> value_;
// => move-only-type: this line establishes the runnable C++ state or behavior.
};
// => move-only-type: this line establishes the runnable C++ state or behavior.
int main() {
// => move-only-type: this line establishes the runnable C++ state or behavior.
  Token first; Token second = std::move(first);
// => move-only-type: this line establishes the runnable C++ state or behavior.
  std::cout << second.value() << "\n";
// => move-only-type: this line establishes the runnable C++ state or behavior.
}
