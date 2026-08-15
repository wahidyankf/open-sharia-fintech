// => constructor: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => constructor: this line establishes the runnable C++ state or behavior.
#include <string>
// => constructor: this line establishes the runnable C++ state or behavior.
#include <utility>
// => constructor: this line establishes the runnable C++ state or behavior.
class User {
// => constructor: this line establishes the runnable C++ state or behavior.
 public:
// => constructor: this line establishes the runnable C++ state or behavior.
  explicit User(std::string name) : name_(std::move(name)) {}
// => constructor: this line establishes the runnable C++ state or behavior.
  const std::string& name() const { return name_; }
// => constructor: this line establishes the runnable C++ state or behavior.
 private:
// => constructor: this line establishes the runnable C++ state or behavior.
  std::string name_;
// => constructor: this line establishes the runnable C++ state or behavior.
};
// => constructor: this line establishes the runnable C++ state or behavior.
int main() {
// => constructor: this line establishes the runnable C++ state or behavior.
  User user("Ada");
// => constructor: this line establishes the runnable C++ state or behavior.
  std::cout << user.name() << "\n";
// => constructor: this line establishes the runnable C++ state or behavior.
}
